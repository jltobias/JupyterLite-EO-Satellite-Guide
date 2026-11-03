"""End-to-end checks for shared selection, evidence, offline use and generated site.

Build first with scripts/build.py --execute. Screenshots go to tmp/qa/.
Use --lite to additionally download/start Pyodide and execute the poster notebook.
"""
from __future__ import annotations

import argparse
import functools
import json
import re
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT / "tmp/qa"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):
        pass
    def translate_path(self,path):
        if path.startswith("/guide/"):
            path=path[len("/guide"):]
        return super().translate_path(path)


def check_workspace(page,base):
    """Both linked views and every mission row must fit typical desktop viewports."""
    dimensions=[]
    for width,height in [(1280,720),(1366,768),(1920,1080)]:
        page.set_viewport_size({'width':width,'height':height})
        page.goto(base+'/explorer/')
        page.get_by_role('button',name='Full screen',exact=False).click()
        page.wait_for_function("document.fullscreenElement?.id === 'poster'")
        expect(page.locator('#exit-workspace')).to_have_text('Exit full screen')
        geometry=page.evaluate('''() => {
          const pane=document.querySelector('#catalog .table-scroll'),
                map=document.getElementById('constellation').getBoundingClientRect(),
                table=pane.getBoundingClientRect(),
                last=document.querySelector('#rows tr:last-child').getBoundingClientRect();
          return {width:innerWidth,height:innerHeight,pageHeight:document.documentElement.scrollHeight,
                  tableScroll:pane.scrollHeight-pane.clientHeight,tableWidth:pane.scrollWidth-pane.clientWidth,
                  mapRight:map.right,tableLeft:table.left,lastBottom:last.bottom,tableBottom:table.bottom};
        }''')
        assert geometry['pageHeight']<=geometry['height']+1,geometry
        assert geometry['tableScroll']<=1 and geometry['tableWidth']<=1,geometry
        assert geometry['mapRight']<=geometry['tableLeft'] and geometry['lastBottom']<=geometry['tableBottom']+1,geometry
        page.locator('#row-sentinel-2c .row-select').hover()
        expect(page.locator('#node-sentinel-2c')).to_have_class(re.compile(r'.*\bis-brushed\b.*'))
        expect(page.locator('#brush-readout')).to_contain_text('Sentinel-2C')
        page.locator('#node-enmap').hover()
        expect(page.locator('#row-enmap')).to_have_class(re.compile(r'.*\bis-brushed\b.*'))
        assert page.evaluate('window.scrollY')==0
        page.locator('#row-enmap .row-select').click()
        expect(page.locator('#constellation')).to_have_attribute('viewBox','0 0 1200 650')
        page.screenshot(path=str(QA/f'workspace-{width}x{height}.png'),full_page=True)
        dimensions.append(geometry)
        page.locator('#exit-workspace').click()
        page.wait_for_function('document.fullscreenElement === null')
        expect(page.locator('body')).not_to_have_class(re.compile(r'.*\bworkspace-mode\b.*'))
        expect(page.locator('#fullscreen')).to_be_focused()
    page.set_viewport_size({'width':1366,'height':768})
    page.goto(base+'/explorer/')
    page.locator('#row-enmap [data-pin]').click()
    page.locator('#row-eo-1 [data-pin]').click()
    page.locator('#fullscreen').click()
    page.wait_for_function("document.fullscreenElement?.id === 'poster'")
    expect(page.locator('#workspace-pin-count')).to_have_text('(2)')
    page.locator('#workspace-filters').click()
    page.locator('#search').fill('EnMAP')
    expect(page.locator('#rows tr')).to_have_count(1)
    page.locator('#rows .row-select').click()
    page.locator('#workspace-details').click()
    expect(page.locator('#inspector .detail-name')).to_have_text('EnMAP')
    page.locator('#inspector .sensor summary').first.click()
    expect(page.locator('#inspector .sensor-content')).to_be_visible()
    page.locator('#workspace-details').click()
    page.locator('#workspace-compare').click()
    expect(page.locator('.comparison-table')).to_be_visible()
    page.locator('#workspace-close-comparison').click()
    expect(page.locator('#comparison')).not_to_be_visible()
    page.keyboard.press('Escape')
    page.wait_for_function('document.fullscreenElement === null')
    expect(page.locator('#search')).to_have_value('EnMAP')
    expect(page.locator('#pin-count')).to_have_text('2 pinned')
    # Iframes and browsers can deny the native API; the viewport layout still works.
    page.goto(base+'/explorer/')
    page.evaluate("Object.defineProperty(document,'fullscreenEnabled',{value:false,configurable:true})")
    page.locator('#fullscreen').click()
    expect(page.locator('#exit-workspace')).to_have_text('Exit workspace')
    assert page.evaluate('document.fullscreenElement === null')
    page.locator('#node-himawari-9').hover()
    expect(page.locator('#row-himawari-9')).to_have_class(re.compile(r'.*\bis-brushed\b.*'))
    page.keyboard.press('Escape')
    expect(page.locator('#fullscreen')).to_have_attribute('aria-pressed','false')
    # A short window may need table scrolling; brushing must reveal the row
    # without moving the constellation or the surrounding document.
    page.set_viewport_size({'width':1280,'height':480})
    page.locator('#fullscreen').click()
    page.locator('#node-himawari-9').hover()
    expect(page.locator('#row-himawari-9')).to_have_class(re.compile(r'.*\bis-brushed\b.*'))
    short=page.evaluate('''() => {
      const pane=document.querySelector('#catalog .table-scroll'),
            row=document.getElementById('row-himawari-9').getBoundingClientRect(),
            bounds=pane.getBoundingClientRect();
      return {scrollY,tableScroll:pane.scrollTop,rowBottom:row.bottom,paneBottom:bounds.bottom};
    }''')
    assert short['scrollY']==0 and short['tableScroll']>0 and short['rowBottom']<=short['paneBottom']+1,short
    page.locator('#exit-workspace').click()
    page.set_viewport_size({'width':1600,'height':1100})
    (QA/'workspace-layouts.json').write_text(json.dumps(dimensions,indent=2),encoding='utf-8')


def check_discovery(page,base):
    """Coverage, concept specificity, linked paging and reproducible handoffs."""
    import ast
    import nbformat
    page.goto(base+'/explorer/')
    count=len(json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))['satellites'])
    seen=set()
    while True:
        rows=page.locator('#rows tr').evaluate_all('(rows)=>rows.map(r=>r.dataset.id)')
        nodes=page.locator('.sat-node:not(.filtered)').evaluate_all('(nodes)=>nodes.map(n=>n.dataset.id)')
        assert set(rows)==set(nodes) and len(rows)<=13
        assert not seen.intersection(rows),'Duplicate records across pages'
        seen.update(rows)
        if page.locator('#page-next').is_disabled():break
        page.locator('#page-next').click()
    assert len(seen)==count,(len(seen),count)
    page.goto(base+'/explorer/?q=air+quality+and+NO2+measures')
    expected={'sentinel-5p','aura','intelsat-40e'}
    assert set(page.locator('#rows tr').evaluate_all('(rows)=>rows.map(r=>r.dataset.id)'))==expected
    expect(page.locator('.sat-node.research-match')).to_have_count(3)
    expect(page.locator('#node-sentinel-5p .sensor-shape > path')).to_have_count(1)
    expect(page.locator('.mission-row.research-match')).to_have_count(3)
    expect(page.locator('#research-results')).to_contain_text('not ground-level concentrations')
    expect(page.locator('#research-results .data-route')).to_have_count(3)
    page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.eoCopied=value}}})")
    page.locator('[data-copy-route="s5p-no2"]').click()
    expect(page.locator('#handoff-status')).to_contain_text('Copied')
    assert page.evaluate('window.eoCopied')=='https://stac.dataspace.copernicus.eu/v1'
    page.locator('#node-sentinel-5p').hover()
    expect(page.locator('#row-sentinel-5p')).to_have_class(re.compile(r'.*\bis-brushed\b.*'))
    page.locator('#row-intelsat-40e .row-select').click()
    expect(page.locator('#node-intelsat-40e')).to_have_class(re.compile(r'.*\bis-selected\b.*'))
    expect(page.locator('#inspector')).to_contain_text('TEMPO')
    with page.expect_download() as download:
        page.locator('#export-question').click()
    brief=json.loads(Path(download.value.path()).read_text(encoding='utf-8'))
    assert brief['concepts']==['no2'] and set(brief['platforms'])==expected
    assert brief['profile']=='eo-research-brief/1' and len(brief['routes'])==3
    with page.expect_download() as download:
        page.locator('#research-notebook').click()
    notebook=nbformat.read(download.value.path(),as_version=4);nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type=='code':ast.parse(cell.source)
    assert 'sentinel-5p-l2-no2-offl' in notebook.cells[1].source
    page.locator('#fullscreen').click()
    page.wait_for_function("document.fullscreenElement?.id==='poster'")
    page.locator('#row-sentinel-5p .row-select').hover()
    expect(page.locator('#brush-readout')).to_contain_text('SSO')
    page.locator('#workspace-research').click()
    expect(page.locator('#research')).to_be_visible()
    page.screenshot(path=str(QA/'research-fullscreen.png'),full_page=True)
    page.locator('#workspace-research').click()
    page.locator('[data-orbit="Geostationary"]').click()
    expect(page.locator('#rows tr')).to_have_count(1)
    expect(page.locator('#rows')).to_contain_text('Intelsat 40e')
    page.locator('#exit-workspace').click()
    page.locator('#reset').click()
    page.locator('#question').fill('NO20 dinosaur observations')
    expect(page.locator('#rows tr')).to_have_count(0)
    expect(page.locator('#research-results')).to_contain_text('No curated measurement pathway')
    page.locator('#question').fill('aerosol and PM2.5')
    expect(page.locator('#research-results')).to_contain_text('not PM₂.₅')
    assert page.evaluate("EOResearch.resolve(document.getElementById('question').value).concepts.map(t=>t.id)")==['aerosol']
    page.locator('#clear-research').click()
    expect(page.locator('#rows tr')).to_have_count(13)
    page.locator('#orbit').select_option('Unknown / not curated')
    expect(page.locator('#rows')).to_contain_text('Unknown / not curated')
    page.goto(base+'/book/stac-coverage.html')
    expect(page.locator('h1').last).to_contain_text('STAC coverage audit')
    page.goto(base+'/book/notebooks/07_research_to_stac.html')
    expect(page.locator('h1').last).to_contain_text('Research question')
    expect(page.frame_locator('iframe[title="Interactive EO constellation poster"]').locator('#rows tr')).to_have_count(3)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lite",action="store_true")
    args=parser.parse_args()
    QA.mkdir(parents=True,exist_ok=True)
    handler=functools.partial(QuietHandler,directory=str(ROOT / "_site"))
    server=ThreadingHTTPServer(("127.0.0.1",0),handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    base=f"http://127.0.0.1:{server.server_port}/guide"
    results=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            context=browser.new_context(viewport={"width":1600,"height":1100},device_scale_factor=1)
            page=context.new_page()
            errors=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.goto(base+"/explorer/")
            expect(page.locator("#rows tr")).to_have_count(13)
            expect(page.locator(".sat-node:not(.filtered)")).to_have_count(13)
            page.screenshot(path=str(QA / "poster-desktop.png"),full_page=True)
            page.locator("#node-landsat-8").click()
            expect(page.locator("#inspector .detail-name")).to_have_text("Landsat 8")
            expect(page.locator("#row-landsat-8")).to_have_class(re.compile(r".*\bis-selected\b.*"))
            page.locator("#inspector .sensor").nth(1).locator("summary").first.click()
            expect(page.locator("#inspector")).to_contain_text("100 m native thermal")
            page.locator("#inspector .sensor").nth(1).locator(".product summary").click()
            expect(page.locator("#inspector").get_by_role("link",name="Open data access").last).to_be_visible()
            page.locator("#row-sentinel-1c .row-select").hover()
            expect(page.locator("#node-sentinel-1c")).to_have_class(re.compile(r".*\bis-brushed\b.*"))
            page.locator("#row-sentinel-1c .row-select").click()
            expect(page.locator("#inspector .detail-name")).to_have_text("Sentinel-1C")
            page.locator("#overview").click()
            page.locator("#node-enmap").focus()
            page.keyboard.press("Enter")
            expect(page.locator("#inspector .detail-name")).to_have_text("EnMAP")
            page.keyboard.press("Escape")
            expect(page.locator("#inspector .detail-name")).to_have_count(0)
            results.append("Map/table selection, bidirectional brushing, sensor/product drill-down and keyboard selection passed.")
            page.locator("#row-landsat-8 [data-pin]").click()
            page.locator("#row-sentinel-1c [data-pin]").click()
            expect(page.locator(".comparison-table")).to_be_visible()
            expect(page.locator("#pin-count")).to_have_text("2 pinned")
            page.locator("#type").select_option("hyperspectral")
            expect(page.locator("#rows tr")).to_have_count(2)
            expect(page.locator("#pin-count")).to_have_text("2 pinned")
            expect(page.locator("#node-landsat-8")).to_have_class(re.compile(r".*\bpinned\b.*\bfiltered\b.*"))
            page.locator("#search").fill("does not exist")
            expect(page.locator("#rows tr")).to_have_count(0)
            expect(page.locator("#no-results")).to_be_visible()
            page.locator("#reset").click()
            page.locator("#property").select_option("ocean colour")
            expect(page.locator("#rows tr")).to_have_count(1)
            page.locator("#reset").click()
            page.locator("#application").select_option("philadelphia-heat")
            expect(page.locator("#rows tr")).to_have_count(2)
            with page.expect_download() as download_info:
                page.locator("#export").click()
            export_path=QA / "filtered.csv"
            download_info.value.save_as(export_path)
            csv=export_path.read_text(encoding="utf-8-sig")
            assert "Landsat 8" in csv and "source" in csv and "Sentinel-1C" not in csv
            results.append("Persistent pins, contextual comparison, filters, empty state, reset and contextual CSV export passed.")
            page.locator("#reset").click()
            page.locator("#clear-pins").click()
            page.locator("#node-landsat-8").click()
            page.locator("#inspector .pathway").first.locator("summary").click()
            expect(page.locator("#inspector")).to_contain_text("study predates Landsat 8 and 9")
            page.screenshot(path=str(QA / "poster-selected.png"),full_page=True)
            page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
            page.emulate_media(media="print")
            page.screenshot(path=str(QA / "poster-print.png"),full_page=True)
            page.emulate_media(media="screen")
            mobile=browser.new_context(viewport={"width":390,"height":844},device_scale_factor=1,is_mobile=True,has_touch=True)
            mp=mobile.new_page();mp.goto(base+"/explorer/")
            assert mp.evaluate("document.documentElement.scrollWidth <= window.innerWidth+1"),"Horizontal viewport overflow"
            mp.locator("#search").fill("EnMAP")
            expect(mp.locator("#rows tr")).to_have_count(1)
            mp.locator("#rows .row-select").click()
            expect(mp.locator("#inspector .detail-name")).to_have_text("EnMAP")
            mp.screenshot(path=str(QA / "poster-mobile.png"),full_page=True)
            mobile.close()
            results.append("Mobile interaction, viewport containment and A1 print render passed (visual review still required).")
            # A completely fresh, disconnected context opens the file without cached resources.
            offline=browser.new_context(viewport={"width":1400,"height":1000},offline=True)
            op=offline.new_page();requests=[]
            op.on("request",lambda r:requests.append(r.url))
            op.goto((ROOT / "downloads/eo-explorer.html").as_uri())
            expect(op.locator("#rows tr")).to_have_count(13)
            op.locator("#node-enmap").click()
            expect(op.locator("#inspector .detail-name")).to_have_text("EnMAP")
            op.locator("#inspector [data-pin]").click()
            op.locator("#row-eo-1 [data-pin]").click()
            expect(op.locator(".comparison-table")).to_be_visible()
            op.locator("#search").fill("Hyperion")
            expect(op.locator("#rows tr")).to_have_count(1)
            op.locator("#rows .row-select").focus();op.keyboard.press("Enter")
            expect(op.locator("#inspector .detail-name")).to_have_text("EO-1 / Hyperion")
            op.locator("#inspector .sensor summary").first.click()
            expect(op.locator("#inspector")).to_contain_text("220 channels")
            op.locator(".sources-section summary").click()
            expect(op.locator("#source-arset")).to_be_visible()
            op.locator('#fullscreen').click()
            op.wait_for_function("document.fullscreenElement?.id === 'poster'")
            expect(op.locator('#rows tr')).to_have_count(1)
            op.locator('#exit-workspace').click()
            op.wait_for_function('document.fullscreenElement === null')
            op.locator('#reset').click()
            op.locator('#question').fill('air quality and NO2 measures')
            expect(op.locator('#rows tr')).to_have_count(3)
            expect(op.locator('#research-results .data-route')).to_have_count(3)
            assert not [u for u in requests if u.startswith(("https:","http:"))],requests
            offline.close()
            results.append("Fresh offline file load, search, drill-down, comparison, citations and keyboard access passed; zero HTTP(S) asset requests.")
            # Verify deep paths under a project-site prefix, not just an origin root.
            response=context.request.get(base+"/book/intro.html");assert response.status==200
            response=context.request.get(base+"/lab/index.html");assert response.status==200
            html=context.request.get(base+"/explorer/").text()
            assert all(name+'?v=' in html for name in ('catalog.js','orbits.js','app.js'))
            lite_config=context.request.get(base+"/jupyter-lite.json").json()
            assert any(x['name']=='@jupyterlite/pyodide-kernel-extension' for x in lite_config['jupyter-config-data']['federated_extensions'])
            for name in ["01_constellation_poster.ipynb","06_knowledge_graph_and_curation.ipynb","07_research_to_stac.ipynb","data/catalog.json","data/research-topics.json","data/research-ontology.ttl","support/eo-explorer.html","eo_guide.py"]:
                response=context.request.get(base+"/files/"+name)
                assert response.status==200,(name,response.status)
            page.goto(base+"/book/poster.html")
            expect(page.frame_locator('iframe[title="Global EO interactive satellite constellation poster"]').locator("#rows tr")).to_have_count(13)
            page.screenshot(path=str(QA / "book.png"),full_page=True)
            book_frame=page.frame_locator('iframe[title="Global EO interactive satellite constellation poster"]')
            book_frame.locator('#fullscreen').click()
            page.wait_for_function("document.fullscreenElement?.tagName === 'IFRAME'")
            expect(book_frame.locator('#exit-workspace')).to_have_text('Exit full screen')
            book_frame.locator('#exit-workspace').click()
            page.wait_for_function('document.fullscreenElement === null')
            results.append("Book iframe, Lab entry point and bundled notebook/data/support paths passed.")
            check_workspace(page,base)
            results.append('Native fullscreen fits both views and all 13 rows at 1280x720, 1366x768 and 1920x1080; bidirectional brushing, panels, state preservation, Escape and window-fit fallback passed.')
            check_discovery(page,base)
            results.append('All catalog records reachable in synchronized pages; NO2 specificity, research highlights, orbit filtering, brief/notebook exports, fullscreen research controls, unknown wording and Book audit/lesson passed.')
            if args.lite:
                lab=context.new_page();lab.goto(base+"/lab/index.html?path=01_constellation_poster.ipynb")
                lab.screenshot(path=str(QA / "jupyterlite-launch.png"),full_page=True)
                lab.on('pageerror',lambda e:print('Lab error:',str(e),flush=True))
                try:
                    lab.wait_for_selector(".jp-LabShell",timeout=60000)
                except Exception:
                    lab.screenshot(path=str(QA / "jupyterlite-failure.png"),full_page=True)
                    print(lab.locator('body').inner_text()[-9000:],flush=True)
                    raise
                print('Lab shell loaded:',lab.title(),flush=True)
                try:
                    lab.get_by_role("tab",name="01_constellation_poster.ipynb").wait_for(timeout=30000)
                except Exception:
                    lab.screenshot(path=str(QA / "jupyterlite-failure.png"),full_page=True)
                    print(lab.locator('body').inner_text()[-9000:],flush=True)
                    raise
                # JupyterLab's visible Run menu invokes the real browser kernel.
                lab.get_by_role("menuitem",name="Run",exact=True).click()
                lab.get_by_role("menuitem",name="Run All Cells",exact=True).click()
                try:
                    expect(lab.locator(".jp-OutputArea-output").filter(has_text="Metadata verified:")).to_be_visible(timeout=180000)
                    expect(lab.frame_locator('iframe[title="Interactive EO constellation poster"]').locator("#rows tr")).to_have_count(13,timeout=60000)
                except Exception:
                    lab.screenshot(path=str(QA / "jupyterlite-failure.png"),full_page=True)
                    print(lab.locator('body').inner_text()[-14000:],flush=True)
                    raise
                lab.screenshot(path=str(QA / "jupyterlite-executed.png"),full_page=True)
                results.append("Real Pyodide browser kernel executed notebook 01 and rendered its interactive poster.")
                lab.goto(base+"/lab/index.html?path=07_research_to_stac.ipynb")
                lab.get_by_role('tab',name='07_research_to_stac.ipynb').wait_for(timeout=60000)
                lab.get_by_role('menuitem',name='Run',exact=True).click()
                lab.get_by_role('menuitem',name='Run All Cells',exact=True).click()
                expect(lab.locator('.jp-OutputArea-output').filter(has_text='Potential platforms:')).to_be_visible(timeout=180000)
                expect(lab.frame_locator('iframe[title="Interactive EO constellation poster"]').locator('#rows tr')).to_have_count(3,timeout=60000)
                expect(lab.locator('.jp-OutputArea-output').filter(has_text='No provider request.')).to_be_visible(timeout=60000)
                lab.screenshot(path=str(QA/'jupyterlite-research-executed.png'),full_page=True)
                results.append('Real Pyodide kernel executed notebook 07, resolved NO2, rendered three linked mission rows and preserved opt-in live metadata requests.')
            assert not errors,errors
            browser.close()
        (QA / "results.json").write_text(json.dumps({"passed":results,"console_errors":errors},indent=2),encoding="utf-8")
        print("\n".join(results))
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__=="__main__":
    main()
