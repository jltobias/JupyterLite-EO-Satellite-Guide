"""Browser checks that global and named-family records are visible and linked."""
import functools,json,re,threading
from http.server import ThreadingHTTPServer
from playwright.sync_api import expect,sync_playwright
from test_browser import ROOT,QA,QuietHandler


def check_inventory(page,base):
    catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
    report=json.loads((ROOT/'data/mission-coverage.json').read_text(encoding='utf-8'))
    ids=lambda selector:set(page.locator(selector).evaluate_all('(es)=>es.map(e=>e.dataset.id)'))
    page.goto(base+'/explorer/')
    expect(page.locator('#map-mode')).to_have_value('overview')
    expect(page.locator('.sat-node:not(.filtered)')).to_have_count(len(catalog['satellites']))
    expect(page.locator('#rows tr')).to_have_count(13)
    expect(page.locator('#inventory-summary')).to_contain_text('Every match is on the map')
    page.locator('#node-sentinel-5p').hover()
    expect(page.locator('#row-sentinel-5p')).to_have_class(re.compile(r'.*\bis-brushed\b.*'))
    expect(page.locator('#inventory-tooltip')).to_be_visible()
    expect(page.locator('#inventory-tooltip')).to_contain_text('Sentinel-5P')
    page.locator('#search').fill('Sentinel-5P');assert ids('.sat-node:not(.filtered)')=={'sentinel-5p'}
    page.locator('#search').fill('Sentinel 5')
    expect(page.locator('#node-sentinel-5p')).not_to_have_class(re.compile(r'.*\bfiltered\b.*'))
    expect(page.locator('#node-metop-sg-a1')).not_to_have_class(re.compile(r'.*\bfiltered\b.*'))
    expect(page.locator('#node-meteosat-13')).to_have_class(re.compile(r'.*\bfiltered\b.*'))
    page.locator('#question').fill('NO2')
    for family in ('sentinel','landsat','noaa'):
        page.locator('#mission-family').select_option(family)
        expect(page.locator('#question')).to_have_value('')
        expect(page.locator('#search')).to_have_value('')
        assert ids('.sat-node:not(.filtered)')==set(report['families'][family]),family
    page.locator('#mission-family').select_option('sentinel')
    page.locator('#jump-mission').select_option('metop-sg-a1')
    expect(page.locator('#inspector')).to_contain_text('Sentinel-5A')
    expect(page.locator('#row-metop-sg-a1')).to_have_class(re.compile(r'.*\bis-selected\b.*'))
    expect(page.locator('#inspector')).to_contain_text('UVNS')
    page.locator('#overview').click();page.locator('#atlas-fullscreen').click()
    page.wait_for_function("document.fullscreenElement?.id==='poster'")
    page.locator('#node-sentinel-5p').hover()
    expect(page.locator('#row-sentinel-5p')).to_have_class(re.compile(r'.*\bis-brushed\b.*'))
    page.screenshot(path=str(QA/'all-sentinels-fullscreen.png'))
    page.locator('#exit-workspace').click()
    page.locator('#mission-family').select_option('landsat');page.locator('#jump-mission').select_option('landsat-6')
    expect(page.locator('#inspector')).to_contain_text('failed to achieve orbit')
    expect(page.locator('#inspector')).to_contain_text('No orbit achieved')
    page.locator('#mission-family').select_option('sentinel');page.locator('#map-mode').select_option('page')
    seen=set()
    while True:
        rows=ids('#rows tr');assert rows==ids('.sat-node:not(.filtered)')
        assert not seen&rows;seen.update(rows)
        if page.locator('#page-next').is_disabled():break
        page.locator('#page-next').click()
    assert seen==set(report['families']['sentinel'])
    page.goto(base+'/explorer/?family=sentinel&mission=sentinel-5p')
    expect(page.locator('#mission-family')).to_have_value('sentinel')
    expect(page.locator('#inspector')).to_contain_text('TROPOMI')
    expect(page.locator('#row-sentinel-5p')).to_have_class(re.compile(r'.*\bis-selected\b.*'))
    page.goto(base+'/explorer/?family=landsat');expect(page.locator('#jump-mission option[value="landsat-6"]')).to_have_count(1)


def main():
    QA.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT/'_site')))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        with sync_playwright() as p:
            b=p.chromium.launch();context=b.new_context(viewport={'width':1600,'height':1000});page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            check_inventory(page,f'http://127.0.0.1:{server.server_port}/guide')
            assert not errors,errors
            (QA/'inventory-results.json').write_text(json.dumps({'passed':True,'console_errors':errors}),encoding='utf-8')
            print('Full inventory, all family members, punctuation aliases, hosted Sentinel discovery, linked row paging, historical failures and fullscreen passed.');b.close()
    finally:server.shutdown();server.server_close();thread.join(timeout=5)


if __name__=='__main__':main()
