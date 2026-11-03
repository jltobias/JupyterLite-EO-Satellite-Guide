"""Browser contracts for orbit encodings, research/AOI geometry and metadata layers."""
from __future__ import annotations
import argparse
import functools
import json
import math
import re
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.parse import parse_qs,urlsplit
from playwright.sync_api import expect,sync_playwright
from test_browser import ROOT,QA,QuietHandler


def check_colors(page,base):
    page.goto(base+'/explorer/')
    expect(page.locator('#color-mode')).to_have_value('orbit')
    color=lambda selector:page.locator(selector).evaluate("e=>getComputedStyle(e).getPropertyValue('--encoding').trim()")
    assert color('#node-landsat-8')=='#42d9ba'
    assert color('#node-goes-19')=='#f6bf58'
    assert color('#row-landsat-8')==color('#node-landsat-8')
    expect(page.locator('#orbit-key')).to_contain_text('Highly elliptical')
    page.locator('#row-landsat-8 [data-pin]').click()
    page.locator('#color-mode').select_option('sensor')
    assert color('#node-goes-19')=='#84b7f6'
    expect(page.locator('#pin-count')).to_have_text('1 pinned')
    page.locator('#color-mode').select_option('orbit')
    page.locator('[data-orbit="Highly elliptical"]').click()
    assert page.locator('#rows tr').count()>=2
    expect(page.locator('#rows')).to_contain_text('Arktika-M1')
    assert color('#node-arcm1')=='#c396ff'
    page.locator('#orbit').select_option('all-leo')
    expect(page.locator('#node-sentinel-5p')).not_to_have_class(re.compile(r'.*\bfiltered\b.*'))
    expect(page.locator('.sat-node:not(.filtered)[data-id="goes-19"]')).to_have_count(0)
    page.locator('#reset').click()
    page.locator('#fullscreen').click()
    page.wait_for_function("document.fullscreenElement?.id==='poster'")
    page.screenshot(path=str(QA/'orbit-colors-workspace.png'),full_page=True)
    page.locator('#exit-workspace').click()


def check_lab(page,base):
    page.goto(base+'/explorer/swaths.html?q=air+quality+and+NO2+measures&bbox=-76,39,-74,41')
    expect(page.locator('#candidate-rows tr')).to_have_count(5)
    expect(page.locator('#mission')).to_have_value('sentinel-5p')
    page.locator('#lab-question').fill('heat');page.locator('#lab-question').press('Enter')
    expect(page.locator('#mission')).to_have_value('landsat-8')
    expect(page.locator('#pixel-note')).to_contain_text('100 m native thermal')
    expect(page.locator('#pixel-view')).to_contain_text('30 cells across = 3 km')
    page.locator('#lab-question').fill('air quality and NO2 measures');page.locator('#lab-question').press('Enter')
    expect(page.locator('#mission')).to_have_value('sentinel-5p')
    expect(page.locator('#study-metrics')).to_contain_text('2,600 km')
    expect(page.locator('#pixel-note')).to_contain_text('3.5')
    model=page.evaluate('''() => {
       const p=EO_GEOMETRY.presets.find(p=>p.id==='sentinel-5p'),b=[-76,39,-74,41],phase=EOGeometry.align(p,b),q=EOGeometry.point(p,0,phase),T=EOGeometry.period(p),end=EOGeometry.point(p,T,phase);
       const geo=EO_GEOMETRY.presets.find(p=>p.id==='intelsat-40e');
       return {q,period:T,latitudeMax:Math.max(...Array.from({length:360},(_,i)=>Math.abs(EOGeometry.point(p,T*i/360,phase).lat))),longitudeShift:end.lon-q.lon,geo0:EOGeometry.point(geo,0),geo1:EOGeometry.point(geo,10000),intervals:EOGeometry.opportunities(p,b,phase,6),bad:EOGeometry.validBox([10,0,-10,10])};
    }''')
    assert abs(model['q']['lon']+75)<1e-8 and abs(model['q']['lat']-40)<1e-8
    assert 100*60<model['period']<103*60 and model['latitudeMax']<=81.30001
    assert -26<model['longitudeShift']< -24 and model['geo0']==model['geo1']
    assert model['intervals'] and model['intervals'][0][0]==0 and not model['bad']
    page.locator('#align-pass').click()
    expect(page.locator('#lab-status')).to_contain_text('not a real pass prediction')
    expect(page.locator('#area-assessment')).to_contain_text('Within')
    page.locator('#play').click()
    page.wait_for_function("document.getElementById('time-label').value!=='T+00:00:00'")
    page.locator('#play').click()
    page.locator('#model-time').evaluate("e=>{e.value='3600';e.dispatchEvent(new Event('input'))}")
    expect(page.locator('#time-label')).to_have_text('T+01:00:00')
    box=lambda:[page.locator('#'+k).input_value() for k in ('west','south','east','north')]
    before=box();page.locator('[data-use="aura"]').click();assert box()==before
    expect(page.locator('#pixel-note')).to_contain_text('13 × 24')
    page.locator('[data-use="intelsat-40e"]').click()
    q0=page.locator('#model-satellite').get_attribute('transform')
    page.locator('#model-time').evaluate("e=>{e.value='10000';e.dispatchEvent(new Event('input'))}")
    assert page.locator('#model-satellite').get_attribute('transform')==q0
    expect(page.locator('#current-swath')).to_have_attribute('d','')
    expect(page.locator('#time-context')).to_contain_text('60 min')
    for key,value in zip(('west','south','east','north'),('-2','50','2','54')):page.locator('#'+key).fill(value)
    page.locator('#apply-bbox').click()
    expect(page.locator('#area-assessment')).to_contain_text('outside the spherical-Earth geometric horizon')
    expect(page.locator('#area-assessment')).to_contain_text('outside the advertised TEMPO')
    page.locator('#zoom-box').click();assert page.locator('#study-map').get_attribute('viewBox')!='0 0 1200 600'
    page.locator('#world-view').click();expect(page.locator('#study-map')).to_have_attribute('viewBox','0 0 1200 600')
    page.locator('#draw-bbox').click();page.locator('#study-map').scroll_into_view_if_needed()
    points=page.locator('#study-map').evaluate('''e=>{const m=e.getScreenCTM();return [[-85,35],[-73,44]].map(([lon,lat])=>({x:m.a*((lon+180)/360*1200)+m.e,y:m.d*((90-lat)/180*600)+m.f}))}''')
    page.mouse.move(points[0]['x'],points[0]['y']);page.mouse.down();page.mouse.move(points[1]['x'],points[1]['y'],steps=5);page.mouse.up()
    actual=list(map(float,box()));assert all(abs(a-b)<.02 for a,b in zip(actual,[-85,35,-73,44])),actual
    with page.expect_download() as download:page.locator('#save-study').click()
    brief=json.loads(Path(download.value.path()).read_text(encoding='utf-8'))
    assert brief['profile']=='eo-study-area/1' and brief['concepts']==['no2'] and brief['bbox']==actual
    page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.eoCopied=value}}})")
    page.locator('#share-study').click();page.wait_for_function('typeof window.eoCopied === "string"')
    query=parse_qs(urlsplit(page.evaluate('window.eoCopied')).query)
    assert query['mission']==['intelsat-40e'] and list(map(float,query['bbox'][0].split(',')))==actual
    page.locator('#west').fill('100');page.locator('#east').fill('-100');page.locator('#apply-bbox').click()
    expect(page.locator('#box-error')).to_contain_text('west < east')
    for key,value in zip(('west','south','east','north'),('-76','39','-74','41')):page.locator('#'+key).fill(value)
    page.locator('#apply-bbox').click();page.locator('[data-use="sentinel-5p"]').click();page.locator('#align-pass').click();page.locator('#zoom-box').click()
    assert page.locator('#model-satellite circle').bounding_box()['width']<20,'Zoom must keep the model marker small enough to see the study box'
    assert page.locator('#model-satellite text').bounding_box()['width']<180,'Zoom must preserve readable label size'
    page.screenshot(path=str(QA/'swaths-aligned-study-area.png'),full_page=True)
    for trigger,exit_button in (('#lab-map-fullscreen','#lab-fullscreen'),('#lab-fullscreen',None)):
        page.locator(trigger).click();page.wait_for_function("document.fullscreenElement===document.documentElement")
        for button in ('#lab-fullscreen','#lab-map-fullscreen'):
            expect(page.locator(button)).to_have_text('Exit full screen');expect(page.locator(button)).to_have_attribute('aria-pressed','true')
        expect(page.locator('#mission')).to_have_value('sentinel-5p');expect(page.locator('#study-map')).to_be_in_viewport()
        if exit_button:page.locator(exit_button).click()
        else:page.keyboard.press('Escape')
        page.wait_for_function('document.fullscreenElement===null');expect(page.locator(trigger)).to_be_focused()
        for button in ('#lab-fullscreen','#lab-map-fullscreen'):
            expect(page.locator(button)).to_have_text('Full screen');expect(page.locator(button)).to_have_attribute('aria-pressed','false')
    page.evaluate("Object.defineProperty(document,'fullscreenEnabled',{value:false,configurable:true})")
    page.locator('#lab-map-fullscreen').click();expect(page.locator('body')).to_have_class(re.compile(r'.*\blab-window\b.*'))
    assert page.evaluate('document.fullscreenElement===null')
    page.keyboard.press('Escape');expect(page.locator('body')).not_to_have_class(re.compile(r'.*\blab-window\b.*'));expect(page.locator('#lab-map-fullscreen')).to_be_focused()


def check_metadata(page,base):
    page.goto(base+'/explorer/swaths.html?q=NO2&mission=sentinel-5p')
    requests=[];page.on('request',lambda r:requests.append(r.url))
    payload={'type':'FeatureCollection','features':[
        {'type':'Feature','id':'fixture-no2','geometry':{'type':'Polygon','coordinates':[[[-76,39],[-74,39],[-74,41],[-76,41],[-76,39]]]},'properties':{'platform':'sentinel-5p','datetime':'2025-07-03T18:00:00Z'},'links':[{'rel':'self','href':'https://example.org/metadata/fixture-no2'}],'assets':{'data':{'href':'https://example.org/never-download.nc'}}},
        {'type':'Feature','id':'<img src=x onerror="window.bad=true">','geometry':None,'properties':{'platform':'other-platform','datetime':'2025-07-03T18:00:00Z'},'links':[]}]}
    pattern='https://stac.dataspace.copernicus.eu/v1/collections/sentinel-5p-l2-no2-offl/items?**'
    page.route(pattern,lambda route:route.fulfill(status=200,headers={'Access-Control-Allow-Origin':'*'},content_type='application/geo+json',body=json.dumps(payload)))
    page.locator('#fetch-footprints').click()
    expect(page.locator('#footprint-rows tr')).to_have_count(2)
    expect(page.locator('#archive-status')).to_contain_text('1 polygon footprint(s); 1 explicitly name')
    assert not page.evaluate('window.bad||false') and page.locator('#footprint-rows img').count()==0
    assert len(requests)==1 and '/items?' in requests[0] and 'bbox=-76%2C39%2C-74%2C41' in requests[0]
    page.locator('#footprint-rows button').first.hover()
    expect(page.locator('#observed-footprints [data-observed="0"]')).to_have_class(re.compile(r'.*\bactive\b.*'))
    with page.expect_download() as download:page.locator('#save-footprints').click()
    exported=json.loads(Path(download.value.path()).read_text(encoding='utf-8'))
    assert exported['provenance']['bbox']==[-76,39,-74,41]
    assert exported['features'][0]['properties']['selected_platform_match'] and not exported['features'][1]['properties']['selected_platform_match']
    assert all('assets' not in f for f in exported['features'])
    page.locator('#west').fill('-77');page.locator('#apply-bbox').click()
    expect(page.locator('#footprint-rows tr')).to_have_count(0)
    expect(page.locator('#save-footprints')).to_be_disabled()
    page.unroute(pattern)
    page.route(pattern,lambda route:route.fulfill(status=403,headers={'Access-Control-Allow-Origin':'*'},content_type='application/json',body='{}'))
    page.locator('#fetch-footprints').click()
    expect(page.locator('#archive-status')).to_contain_text('HTTP 403')
    expect(page.locator('#study-metrics')).to_contain_text('2,600 km')
    page.unroute(pattern)
    held=[];page.route(pattern,lambda route:held.append(route))
    page.locator('#fetch-footprints').click();page.wait_for_function("document.getElementById('fetch-footprints').disabled")
    page.locator('#mission').select_option('aura')
    expect(page.locator('#footprint-rows tr')).to_have_count(0)
    expect(page.locator('#archive-status')).to_contain_text('No provider request')
    for route in held:
        try:route.fulfill(status=200,content_type='application/json',body=json.dumps(payload))
        except Exception:pass
    expect(page.locator('#footprint-rows tr')).to_have_count(0)
    page.unroute(pattern)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--live',action='store_true');parser.add_argument('--lite',action='store_true');args=parser.parse_args()
    QA.mkdir(parents=True,exist_ok=True);server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT/'_site')));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_port}/guide'
    results=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch();context=browser.new_context(viewport={'width':1600,'height':1100});page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            check_colors(page,base);results.append('Orbit/sensor colors, matching table swatches, SSO/LEO hierarchy and HEO legend passed.')
            check_lab(page,base);results.append('Research candidates, nominal geometry invariants, animation, bbox editing/drawing, GEO reach, sampling, sharing and exports passed.')
            check_metadata(page,base);results.append('Metadata-only footprints, platform distinctions, linked highlighting, inert provider text, no asset requests, HTTP failures and stale-request cancellation passed.')
            for name in ('book/swaths.html','book/orbit-guide.html','book/notebooks/08_swaths_orbits_study_area.html','files/08_swaths_orbits_study_area.ipynb','files/support/eo-swaths.html','files/data/geometry-presets.json','data/orbit-types.json'):
                assert context.request.get(base+'/'+name).ok,name
            page.goto(base+'/book/notebooks/08_swaths_orbits_study_area.html')
            expect(page.frame_locator('iframe[title="EO study-area swaths and orbits"]').locator('#candidate-rows tr')).to_have_count(5)
            results.append('Book orbit/methods pages, executed lesson 08 and bundled Lab support/preset paths passed.')
            mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);mp=mobile.new_page();mp.goto(base+'/explorer/swaths.html?q=NO2')
            assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Mobile horizontal overflow';mp.screenshot(path=str(QA/'swaths-mobile.png'),full_page=True)
            mp.locator('#lab-map-fullscreen').click();expect(mp.locator('#study-map')).to_be_in_viewport();expect(mp.locator('#lab-map-fullscreen')).to_be_in_viewport()
            assert mp.locator('.coverage-main').bounding_box()['y']>=mp.locator('.masthead').bounding_box()['height']-1,'Full-screen header must not overlap the study view'
            mp.locator('#lab-map-fullscreen').click();expect(mp.locator('#lab-map-fullscreen')).to_have_attribute('aria-pressed','false');mobile.close()
            offline=browser.new_context(offline=True,viewport={'width':1400,'height':1000});op=offline.new_page();network=[];op.on('request',lambda r:network.append(r.url));op.goto((ROOT/'downloads/eo-swaths.html').as_uri()+'?q=NO2');expect(op.locator('#candidate-rows tr')).to_have_count(5);op.locator('#align-pass').click();expect(op.locator('#area-assessment')).to_contain_text('Within');assert not [u for u in network if u.startswith(('https:','http:'))];offline.close();results.append('Mobile containment and fresh offline study-area lab passed; no automatic network requests.')
            if args.live:
                page.goto(base+'/explorer/swaths.html?q=NO2&mission=sentinel-5p');page.locator('#fetch-footprints').click();expect(page.locator('#archive-status')).to_contain_text('No data assets requested',timeout=35000);assert page.locator('#footprint-rows tr').count()>0;page.screenshot(path=str(QA/'swaths-live-footprints.png'),full_page=True);results.append('Live normal-browser NO2 metadata footprint query passed.')
            if args.lite:
                lab=context.new_page();lab.goto(base+'/lab/index.html?path=08_swaths_orbits_study_area.ipynb');lab.get_by_role('tab',name='08_swaths_orbits_study_area.ipynb').wait_for(timeout=60000);lab.get_by_role('menuitem',name='Run',exact=True).click();lab.get_by_role('menuitem',name='Run All Cells',exact=True).click();expect(lab.locator('.jp-OutputArea-output').filter(has_text='Measurement concepts:')).to_be_visible(timeout=180000);frame=lab.frame_locator('iframe[title="EO study-area swaths and orbits"]');expect(frame.locator('#candidate-rows tr')).to_have_count(3,timeout=60000);frame.locator('#align-pass').click();expect(frame.locator('#area-assessment')).to_contain_text('Within');expect(lab.locator('.jp-OutputArea-output').filter(has_text='Saved question and area graph')).to_be_visible(timeout=60000);lab.screenshot(path=str(QA/'jupyterlite-study-area.png'),full_page=True);results.append('Real Pyodide notebook 08 executed and rendered the offline interactive research/AOI lab.')
            assert not errors,errors;browser.close()
        (QA/'swaths-results.json').write_text(json.dumps({'passed':results,'console_errors':errors},indent=2),encoding='utf-8');print('\n'.join(results))
    finally:server.shutdown();server.server_close();thread.join(timeout=5)


if __name__=='__main__':main()
