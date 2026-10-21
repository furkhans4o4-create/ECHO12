"""ECHO/12 browser smoke tests. Install: pip install playwright && playwright install chromium."""
from pathlib import Path
import os
import shutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")

def move(page, key, seconds):
    page.evaluate('([key, seconds]) => { const game=window.__echo12Test; game.key(key,true); game.tick(seconds); game.key(key,false); }', [key,seconds])

def commit(page):
    page.keyboard.press("Space")
    page.evaluate('window.__echo12Test.tick(0.01)')

def load(browser, level):
    # Isolate each level without requiring a previous save.
    html = HTML.replace("loadLevel(getUnlocked())", f"loadLevel({level})")
    html = html.replace("levelIndex=getUnlocked();level=", f"levelIndex={level};level=")
    assert html != HTML
    needle='updateHUD();requestAnimationFrame(frame);\n})();'
    injected='''updateHUD();
    window.__echo12Test = {
      tick(seconds) { const n=Math.round(seconds/DT); for(let i=0;i<n;i++)step(DT); draw();drawTimeline();updateHUD(); },
      key(code,down) {const name = code.length === 1 ? 'Key'+code.toUpperCase() : code; if(down)keys.add(name);else keys.delete(name)},
      gate(key){return gateOpen(key)}, fx(){return {rings:fxRings.length,gateA:gateMemory.get('A'),wash:rewindWash}}, teleport(x,y){player.x=x;player.y=y}
    };
    })();'''
    assert needle in html
    html=html.replace(needle,injected)
    # Browser tests run in about:blank; simulate local storage without affecting shipped code.
    storage_stub="""<script>
    window.__echo12Store ??= {};
    Object.defineProperty(window, 'localStorage', {configurable:true,value:{
      getItem(key){return Object.hasOwn(window.__echo12Store,key)?window.__echo12Store[key]:null},
      setItem(key,value){window.__echo12Store[key]=String(value)}
    }});
    </script>"""
    html=html.replace('<script>\n(()=>{',storage_stub+'<script>\n(()=>{')
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.set_content(html, wait_until="load")
    page.click("#start")
    return page, errors

def verify(page, errors, expected):
    actual = page.locator("#mode").inner_text()
    assert actual == expected, f"Expected {expected}, got {actual}"
    assert not errors, f"Unexpected JS errors: {errors}"

def main():
    with sync_playwright() as playwright:
        exe = os.getenv("ECHO12_CHROMIUM") or shutil.which("chromium")
        kwargs = {"executable_path": exe, "args": ["--no-sandbox"]} if exe else {}
        browser = playwright.chromium.launch(headless=True, **kwargs)
        try:
            page, errors = load(browser, 0)
            assert page.locator('#signal-value').inner_text() == 'KAYIT ALINIYOR'
            assert page.locator('#scene-banner-title').inner_text() == 'SEKTÖR 01'
            page.keyboard.press('m')
            assert 'kapalı' in page.locator('#sound').inner_text()
            assert page.evaluate("localStorage.getItem('echo12-muted')") == '1'
            page.keyboard.press('m')
            assert 'açık' in page.locator('#sound').inner_text()
            assert page.evaluate("localStorage.getItem('echo12-muted')") == '0'
            print('PASS sound toggle, local setting and sector title')
            move(page, "d", .99); move(page, "w", .49); commit(page)
            assert page.locator("#clones").inner_text() == "1 / 6"
            page.keyboard.press("z")
            assert page.locator("#clones").inner_text() == "0 / 6"
            move(page, "d", .99); move(page, "w", .49); commit(page)
            move(page, "d", 3.4)
            verify(page, errors, "BAŞARILI")
            page.close()
            print("PASS 1/5 + undo")
            
            page, errors = load(browser, 1)
            move(page, "d", .247); move(page, "s", .985); commit(page)
            move(page, "d", 2.04); move(page, "s", 1.235); commit(page)
            move(page, "d", 2.5); move(page, "s", .989); move(page, "d", 1.3)
            verify(page, errors, "BAŞARILI")
            page.close()
            print("PASS 2/5")
            
            page, errors = load(browser, 2)
            move(page, "d", .247); move(page, "w", 1.234); commit(page)
            move(page, "w", .245); move(page, "d", 2.28); move(page, "s", .495); commit(page)
            move(page, "w", .247); move(page, "d", 2.7); move(page, "w", .495)
            move(page, "d", .85); move(page, "w", .246)
            verify(page, errors, "BAŞARILI")
            page.close()
            print("PASS 3/5")
            
            page, errors = load(browser, 3)
            move(page, "d", .493); move(page, "w", .738); commit(page)
            move(page, "d", 1.53); move(page, "s", .738); move(page, "d", .247); commit(page)
            move(page, "d", 1.9); move(page, "s", .247); move(page, "d", 1.6)
            verify(page, errors, "BAŞARILI")
            page.close()
            print("PASS 4/5")

            page, errors = load(browser, 4)
            move(page, "d", .493); move(page, "s", .247)
            assert not page.evaluate("window.__echo12Test.gate('C')"), "Player must not trigger echo-only switch"
            commit(page)
            page.evaluate("window.__echo12Test.tick(.80)")
            assert page.evaluate("window.__echo12Test.gate('C')"), "Recorded echo should trigger C"
            page.keyboard.press("r")
            move(page, "d", .493); move(page, "s", .247); commit(page)
            move(page, "d", 1.73)
            assert page.locator("#interact").is_enabled(), "Expected readable terminal"
            page.keyboard.press("e")
            assert page.locator("#mode").inner_text() == "ARŞİV"
            assert "PERSONEL NO. 12" in page.locator("#archive-body").inner_text()
            assert page.locator("#archive-count").inner_text() == "1/6"
            saved = page.locator("#time").inner_text()
            page.evaluate("window.__echo12Test.tick(1.5)")
            assert page.locator("#time").inner_text() == saved, "Archive must pause simulation"
            page.keyboard.press("Escape")
            assert page.locator("#mode").inner_text() == "KAYIT"
            move(page, "d", .247); move(page, "w", .493); commit(page)
            move(page, "d", 3.26)
            verify(page, errors, "BAŞARILI")
            page.close()
            print("PASS 5/6: echo-only plate, terminal and archive pause")
            # Room 6: solve two echo locks, confirm one decision, then replay the alternative.
            page, errors = load(browser, 5)
            move(page,'d',.493); move(page,'w',.493)
            assert not page.evaluate("window.__echo12Test.gate('F')"), "Live player must not activate F"
            commit(page)
            move(page,'d',1.74); move(page,'s',.493); commit(page)
            move(page,'d',2.97); move(page,'d',.12)
            assert page.evaluate("window.__echo12Test.gate('F')")
            assert page.evaluate("window.__echo12Test.gate('G')")
            assert not page.evaluate("window.__echo12Test.gate('OUT')")
            move(page,'w',.74)
            page.keyboard.press('e')
            assert page.locator('#mode').inner_text()=='KARAR'
            assert page.locator('#decision-title').inner_text()=='TANIKLARI KORU'
            snapshot=page.locator('#time').inner_text()
            page.evaluate('window.__echo12Test.tick(1)')
            assert page.locator('#time').inner_text()==snapshot
            page.locator('#decision-cancel').click()
            assert not page.evaluate("window.__echo12Test.gate('OUT')")
            page.keyboard.press('e')
            page.locator('#decision-confirm').click()
            assert page.evaluate("window.__echo12Test.gate('OUT')")
            move(page,'s',.74); move(page,'d',.48)
            verify(page,errors,'TAMAMLANDI')
            assert 'Yalnız da değilsin' in page.locator('#dialog-title').inner_text()
            assert page.evaluate("JSON.parse(localStorage.getItem('echo12-endings'))")==['keep']
            print('PASS 6/6: keep-ending and cancellation checks')

            page.locator('#replay-choice').click()
            move(page,'d',.493); move(page,'w',.493); commit(page)
            move(page,'d',1.74); move(page,'s',.493); commit(page)
            move(page,'d',2.97); move(page,'d',.12); move(page,'s',.74)
            page.keyboard.press('e')
            assert page.locator('#decision-title').inner_text()=='ÇEKİRDEĞİ SUSTUR'
            page.locator('#decision-confirm').click()
            move(page,'w',.74); move(page,'d',.48)
            verify(page,errors,'TAMAMLANDI')
            assert 'Kimse cevap vermedi' in page.locator('#dialog-title').inner_text()
            assert set(page.evaluate("JSON.parse(localStorage.getItem('echo12-endings'))"))=={'cut','keep'}
            assert page.locator('#archive-count').inner_text()=='2/6'
            saved=page.evaluate('JSON.stringify(window.__echo12Store)')
            html=page.evaluate('document.documentElement.outerHTML')
            html=html.replace('window.__echo12Store ??= {};','window.__echo12Store = '+saved+';')
            page.set_content(html,wait_until='load')
            page.locator('#logbook').click()
            assert '2 / 6' in page.locator('#archive-status').inner_text()
            verify(page,errors,'ARŞİV')
            page.close()
            print('PASS persisted endings: both results recoverable from storage')

            # Verify display and audio feedback without changing a real puzzle solution.
            page, errors = load(browser, 0)
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.10)")
            assert page.evaluate("window.__echo12Test.gate('A')")
            assert page.evaluate("window.__echo12Test.fx().rings") > 0, 'Opening gate must create a visible temporal ring'
            assert page.locator('#signal-value').inner_text() == 'GEÇİŞ AÇIK'
            page.evaluate("window.__echo12Test.tick(9.2)")
            assert page.locator('#signal-strip').evaluate("(e)=>e.classList.contains('critical')")
            assert page.locator('#signal-value').inner_text().startswith('SON ')
            assert not errors
            page.close()
            print('PASS gate VFX, live HUD and 3-second countdown alert')

        finally:
            browser.close()

if __name__ == "__main__":
    main()
