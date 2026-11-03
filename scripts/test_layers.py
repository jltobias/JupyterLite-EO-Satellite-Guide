"""Lifecycle/family unions, linked filtering and persistent legend browser checks."""
import argparse,csv,functools,io,json,re,threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import expect,sync_playwright
from test_browser import ROOT,QA,QuietHandler,check_workspace


def check_layers(page,base):
    catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))['satellites']
    active={s['id'] for s in catalog if s['status']=='operational'};retired={s['id'] for s in catalog if s['status']=='retired'}
    sentinel={s['id'] for s in catalog if 'sentinel' in s.get('mission_families',[])}
    landsat={s['id'] for s in catalog if 'landsat' in s.get('mission_families',[])}
    ids=lambda:set(page.locator('.sat-node:not(.filtered)').evaluate_all('(es)=>es.map(e=>e.dataset.id)'))
    page.goto(base+'/explorer/')
    expect(page.locator('#satellite-legend')).to_be_in_viewport()
    expect(page.locator('#orbit-key')).to_contain_text('Sun-synchronous (LEO)')
    expect(page.locator('#legend svg')).to_have_count(7)
    assert page.evaluate('EOLayers.families.reduce((n,g)=>n+g.count,0)')==len(catalog)
    assert ids()=={s['id'] for s in catalog}
    page.locator('#toggle-active').uncheck();assert not ids()&active
    expect(page.locator('#layers-button')).to_contain_text('1 off')
    page.locator('#toggle-active').check();page.locator('#toggle-other-status').uncheck()
    assert ids()==active|retired
    page.locator('#toggle-retired').uncheck();assert ids()==active
    expect(page.locator('#status')).to_have_value('operational')
    page.locator('#status').select_option('retired');assert ids()==retired
    expect(page.locator('#toggle-active')).not_to_be_checked();expect(page.locator('#toggle-retired')).to_be_checked()
    page.locator('#layers-button').click();expect(page.locator('#layer-panel')).to_be_visible()
    page.locator('[data-status-preset="all"]').click();page.locator('[data-family-preset="none"]').click()
    assert not ids();expect(page.locator('#no-results')).to_be_visible()
    page.locator('#layer-family-sentinel').check();page.locator('#layer-family-landsat').check()
    assert ids()==sentinel|landsat
    page.locator('[data-status-preset="operational"]').click();assert ids()==(sentinel|landsat)&active
    page.locator('#close-layers').click();expect(page.locator('#layers-button')).to_be_focused()
    page.locator('#node-sentinel-5p').hover();expect(page.locator('#row-sentinel-5p')).to_have_class(re.compile(r'.*\bis-brushed\b.*'))
    with page.expect_download() as download:page.locator('#export').click()
    rows=list(csv.DictReader(io.StringIO(Path(download.value.path()).read_text(encoding='utf-8-sig'))))
    expected={s['name'] for s in catalog if s['id'] in (sentinel|landsat)&active}
    assert {r['satellite'] for r in rows}==expected and {r['status'] for r in rows}=={'operational'}
    page.locator('#layers-button').click();page.locator('#layer-status-commissioning').check()
    assert page.locator('#toggle-other-status').evaluate('e=>e.indeterminate')
    page.locator('#close-layers').click();page.locator('#reset').click()
    assert len(ids())==len(catalog)
    page.locator('#catalog').scroll_into_view_if_needed();expect(page.locator('#satellite-legend')).to_be_in_viewport()
    assert page.locator('#satellite-legend').bounding_box()['y']>=-1
    assert page.locator('#satellite-legend').bounding_box()['y']<5
    page.locator('#color-mode').select_option('sensor');expect(page.locator('#sensor-legend-label')).to_have_text('Sensor colors + shapes')
    page.locator('#color-mode').select_option('orbit')
    page.locator('#fullscreen').click();page.wait_for_function("document.fullscreenElement?.id==='poster'")
    legend=page.locator('#satellite-legend').bounding_box();map_box=page.locator('#atlas').bounding_box();table=page.locator('#catalog').bounding_box()
    assert legend['y']+legend['height']<=min(map_box['y'],table['y'])+1
    assert legend['width']>map_box['width']+table['width']-20
    page.locator('#layers-button').click();page.locator('[data-status-preset="retired"]').click()
    assert ids()==retired
    page.screenshot(path=str(QA/'legend-layers-fullscreen.png'))
    page.keyboard.press('Escape');expect(page.locator('#layer-panel')).not_to_be_visible()
    assert page.evaluate("document.fullscreenElement?.id==='poster'")
    page.keyboard.press('Escape');page.wait_for_function('document.fullscreenElement===null')
    assert ids()==retired
    page.locator('#reset').click()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source',action='store_true');args=parser.parse_args()
    QA.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT if args.source else ROOT/'_site')))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_port}/guide'
    try:
        with sync_playwright() as p:
            b=p.chromium.launch();context=b.new_context(viewport={'width':1600,'height':1000});page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            check_layers(page,base)
            if args.source:check_workspace(page,base)
            mobile=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);mp=mobile.new_page();mp.on('pageerror',lambda e:errors.append(str(e)))
            mp.goto(base+'/explorer/');mp.locator('#layers-button').click();mp.locator('[data-status-preset="operational"]').click();mp.locator('#close-layers').click();mp.locator('#catalog').scroll_into_view_if_needed();expect(mp.locator('#satellite-legend')).to_be_in_viewport()
            assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            mp.screenshot(path=str(QA/'legend-layers-mobile.png'))
            mp.locator('#fullscreen').click();mp.wait_for_function("document.fullscreenElement?.id==='poster'")
            expect(mp.locator('#satellite-legend')).to_be_in_viewport();expect(mp.locator('#constellation')).to_be_in_viewport();expect(mp.locator('#catalog')).to_be_in_viewport()
            assert mp.locator('#constellation').bounding_box()['height']>70
            mp.locator('#layers-button').click();mp.locator('[data-family-preset="none"]').click();mp.locator('#layer-family-sentinel').check();mp.locator('#close-layers').click()
            mp.screenshot(path=str(QA/'legend-layers-mobile-fullscreen.png'));mp.locator('#exit-workspace').click();mobile.close()
            offline=b.new_context(offline=True);op=offline.new_page();requests=[];op.on('request',lambda r:requests.append(r.url));op.goto((ROOT/'downloads/eo-explorer.html').as_uri());op.locator('#toggle-other-status').uncheck();op.locator('#toggle-retired').uncheck()
            active_count=sum(s['status']=='operational' for s in json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))['satellites']);expect(op.locator('#count')).to_contain_text(f'{active_count} MATCHES')
            assert not [u for u in requests if u.startswith(('http:','https:'))];offline.close()
            assert not errors,errors
            (QA/'layers-results.json').write_text(json.dumps({'passed':True,'console_errors':errors}),encoding='utf-8')
            print('Lifecycle switches, additive family layers, status shortcut, linked row paging, CSV, sticky/full-width legend, fullscreen, mobile and offline passed.');b.close()
    finally:server.shutdown();server.server_close();thread.join(timeout=5)


if __name__=='__main__':main()
