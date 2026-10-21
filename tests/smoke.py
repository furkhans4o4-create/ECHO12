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
            # Build 010: contextual onboarding and chapter pacing are visible from start.
            assert page.locator('#chapter-label').inner_text() == 'BÖLÜM I · HAFIZA'
            assert page.locator('#campaign-segments .campaign-cell').count() == 11
            assert page.locator('#campaign-segments .campaign-cell.active').count() == 1
            assert page.locator('#gate-counter').inner_text() == '0 / 1 açık'
            assert 'WASD' in page.locator('#hint').inner_text()
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.02)")
            assert 'BOŞLUK' in page.locator('#hint').inner_text(), 'First-room tutorial advances at pressure plate'
            page.evaluate("window.__echo12Test.teleport(2.5,5.5)")
            print('PASS Build 010: dynamic first-room onboarding and chapter overview')
            move(page, "d", .99); move(page, "w", .49); commit(page)
            assert page.locator("#clones").inner_text() == "1 / 6"
            page.keyboard.press("z")
            assert page.locator("#clones").inner_text() == "0 / 6"
            move(page, "d", .99); move(page, "w", .49); commit(page)
            move(page, "d", 3.4)
            verify(page, errors, "BAŞARILI")
            record=page.evaluate("JSON.parse(localStorage.getItem('echo12-best-runs'))")
            assert record['0']['echoes']==1 and record['0']['seconds']>0, record
            assert page.locator('#debrief .debrief-stat').count() >= 3
            assert page.locator('#debrief').inner_text().find('Yeni kişisel rekor')>=0
            assert page.locator('#gate-counter').inner_text() == '1 / 1 açık'
            page.locator('#room-select').click()
            assert 'EN İYİ 1 YANKI' in page.locator('[data-room="0"]').inner_text()
            page.keyboard.press('Escape')
            page.close()
            print("PASS 1/5 + undo, performance records and post-room debrief")
            
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
            assert page.locator("#archive-count").inner_text() == "1/15"
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
            verify(page,errors,'BAŞARILI')
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
            verify(page,errors,'BAŞARILI')
            assert 'Kimse cevap vermedi' in page.locator('#dialog-title').inner_text()
            assert set(page.evaluate("JSON.parse(localStorage.getItem('echo12-endings'))"))=={'cut','keep'}
            assert page.locator('#archive-count').inner_text()=='2/15'
            saved=page.evaluate('JSON.stringify(window.__echo12Store)')
            html=page.evaluate('document.documentElement.outerHTML')
            html=html.replace('window.__echo12Store ??= {};','window.__echo12Store = '+saved+';')
            page.set_content(html,wait_until='load')
            page.locator('#logbook').click()
            assert '2 / 15' in page.locator('#archive-status').inner_text()
            verify(page,errors,'ARŞİV')
            page.close()
            print('PASS persisted endings: both results recoverable from storage')

            # Build 006: a live player never counts toward a dual-echo switch.
            page, errors = load(browser, 6)
            move(page,'d',.493); move(page,'w',.493); commit(page)
            move(page,'d',1.73); move(page,'s',.493)
            assert not page.evaluate("window.__echo12Test.gate('R')"), "One recorded echo plus live player must not satisfy 2-echo plate"
            commit(page)
            move(page,'d',1.73); move(page,'s',.493)
            assert not page.evaluate("window.__echo12Test.gate('R')"), "Two echoes must exist simultaneously"
            commit(page)
            page.evaluate("window.__echo12Test.tick(2.3)")
            assert page.evaluate("window.__echo12Test.gate('R')"), "Two synchronized echo replays must open R"
            page.keyboard.press('r')
            move(page,'d',.493);move(page,'w',.493);commit(page)
            move(page,'d',1.73);move(page,'s',.493);commit(page)
            move(page,'d',1.73);move(page,'s',.493);commit(page)
            move(page,'d',3.3)
            verify(page,errors,'BAŞARILI')
            page.close()
            print('PASS room 7: echo consensus opens synchronized gate')

            # Build 006: only live player can energize the short relay; older echoes cannot.
            page, errors = load(browser, 7)
            page.evaluate("window.__echo12Test.teleport(9.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.05)")
            assert page.evaluate("window.__echo12Test.gate('P')"),"The live player should trigger P"
            page.evaluate("window.__echo12Test.teleport(2.5,5.5)")
            page.evaluate("window.__echo12Test.tick(3)")
            assert not page.evaluate("window.__echo12Test.gate('P')"),"Live pulse must expire"
            page.keyboard.press('r')
            move(page,'d',.493);move(page,'w',.493);commit(page)
            move(page,'d',.493);move(page,'w',.493);commit(page)
            page.evaluate("window.__echo12Test.tick(1.2)")
            assert page.evaluate("window.__echo12Test.gate('S')")
            move(page,'d',1.73)
            assert page.evaluate("window.__echo12Test.gate('P')")
            move(page,'d',1.6)
            verify(page,errors,'BAŞARILI')
            assert page.locator('#archive-count').inner_text().endswith('/15')
            assert 'BÖLÜM II' in page.locator('#kicker').inner_text()
            page.close()
            print('PASS room 8: dual echo gate, live-only pulse, chapter II handoff')

            # Build 007 / Room 9: an injected phantom cannot open even the scanned plate.
            page, errors = load(browser, 8)
            assert page.locator('#frequency').is_enabled()
            assert not page.evaluate("window.__echo12Test.gate('T')")
            page.keyboard.press('f')
            assert 'AÇIK' in page.locator('#frequency').inner_text()
            page.evaluate("window.__echo12Test.tick(1.2)")
            assert not page.evaluate("window.__echo12Test.gate('T')"),'Phantom is not a recorded ghost'
            page.keyboard.press('r')
            move(page,'d',.493);move(page,'w',.493);commit(page)
            page.evaluate("window.__echo12Test.tick(1.2)")
            assert not page.evaluate("window.__echo12Test.gate('T')"),'Recording without verification cannot trigger T'
            page.keyboard.press('f')
            assert page.evaluate("window.__echo12Test.gate('T')"),'Scanning must authenticate true ghost'
            page.keyboard.press('r')
            move(page,'d',.493);move(page,'w',.493);commit(page)
            page.keyboard.press('f')
            move(page,'d',1.976);move(page,'s',.493)
            assert page.evaluate("window.__echo12Test.gate('T')")
            commit(page)
            move(page,'d',3.5)
            verify(page,errors,'BAŞARILI')
            page.close()
            print('PASS room 9: spoofed signal rejected, verified echoes unlock both gates')

            # Build 007 / Room 10: a reversed trace starts at its last position.
            page, errors = load(browser, 9)
            assert page.locator('#frequency').is_enabled()
            page.keyboard.press('f')
            assert 'TERS' in page.locator('#frequency').inner_text()
            move(page,'d',.493);move(page,'w',.493);commit(page)
            assert page.evaluate("window.__echo12Test.gate('V')"),'Reverse replay must activate V at t=0'
            assert not page.evaluate("window.__echo12Test.gate('Y')"),'Reverse replay must never count as a forward trace'
            page.keyboard.press('f')
            assert 'NORMAL' in page.locator('#frequency').inner_text()
            move(page,'d',1.976);move(page,'s',.493);commit(page)
            assert not page.evaluate("window.__echo12Test.gate('Y')"),'Normal replay must take time to reach Y'
            move(page,'d',3.5)
            verify(page,errors,'BAŞARILI')
            assert 'OPERATÖR 00' in page.locator('#dialog-text').inner_text()
            assert page.locator('#archive-count').inner_text().endswith('/15')
            page.close()
            print('PASS room 10: reverse replay, forward-only gate, chapter III handoff')

            # Build 008: 3 forensic observations are required before a gated, reasoned verdict.
            page, errors = load(browser, 10)
            assert not page.evaluate("window.__echo12Test.gate('AUDIT')")
            move(page,'d',.493); move(page,'w',.493); commit(page)
            page.evaluate("window.__echo12Test.tick(1.3)")
            assert page.evaluate("window.__echo12Test.gate('B')"), 'The first barrier needs a real recorded echo'
            page.evaluate("window.__echo12Test.teleport(9.5,2.5)")
            page.keyboard.press('e')
            assert not page.locator('#mode').inner_text() == 'KANIT', 'Scanner-off sample must not open audit'
            page.keyboard.press('f')
            page.keyboard.press('e')
            page.evaluate("window.__echo12Test.teleport(9.5,5.5)")
            page.keyboard.press('e')
            page.evaluate("window.__echo12Test.teleport(11.5,5.5)")
            page.keyboard.press('e')
            assert page.locator('#mode').inner_text() == 'KANIT'
            assert page.locator('#audit-options [data-verdict="injected"]').is_disabled(), 'All three measurements must be supplied'
            prev_time=page.locator('#time').inner_text()
            page.evaluate("window.__echo12Test.tick(2)")
            assert page.locator('#time').inner_text()==prev_time, 'The audit board pauses the clock'
            page.keyboard.press('Escape')
            page.evaluate("window.__echo12Test.teleport(9.5,8.5)")
            page.keyboard.press('e')
            page.evaluate("window.__echo12Test.teleport(11.5,5.5)")
            page.keyboard.press('e')
            assert page.locator('#audit-options [data-verdict="injected"]').is_enabled()
            facts=page.locator('#audit-evidence').inner_text()
            assert 'optik siluet' in facts and '00 doğrulanmış fiziksel temas' in facts and 'yakalama imzası yok' in facts, facts
            page.locator('#audit-options [data-verdict="real"]').click()
            assert not page.evaluate("window.__echo12Test.gate('AUDIT')")
            assert 'Yanlış:' in page.locator('#audit-feedback').inner_text()
            page.locator('#audit-options [data-verdict="injected"]').click()
            assert page.evaluate("window.__echo12Test.gate('AUDIT')")
            assert 'kimliği henüz doğrulanmadı' in page.locator('#audit-feedback').inner_text()
            page.keyboard.press('Escape')
            page.evaluate("window.__echo12Test.teleport(11.5,5.5)")
            move(page,'d',1.11)
            verify(page,errors,'TAMAMLANDI')
            assert 'yönetici yetkisi' in page.locator('#dialog-text').inner_text()
            assert page.locator('#archive-count').inner_text().endswith('/15')
            page.close()
            print('PASS room 11: evidence triage, wrong verdict, correct verdict, final gate and chapter ending')

            # Build 009: room selection pauses simulation, enforces unlocks and keeps saved progress.
            page, errors = load(browser, 0)
            assert page.locator('#hint-assist').is_hidden()
            page.keyboard.press('h')
            assert 'İPUCU 1/3' in page.locator('#hint-step').inner_text()
            page.keyboard.press('h')
            assert 'İPUCU 2/3' in page.locator('#hint-step').inner_text()
            page.keyboard.press('h')
            page.keyboard.press('h')
            assert 'İPUCU 3/3' in page.locator('#hint-step').inner_text()
            page.locator('#room-select').click()
            verify(page,errors,'ODA SEÇİMİ')
            assert page.locator('[data-room="0"]').is_enabled()
            assert page.locator('[data-room="1"]').is_disabled()
            assert page.locator('#room-picker-grid button').count() == 11
            page.evaluate("window.__echo12Test.tick(1.3)")
            frozen=page.locator('#time').inner_text()
            page.evaluate("window.__echo12Test.tick(2)")
            assert page.locator('#time').inner_text()==frozen
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            assert page.locator('#hint-assist').is_visible()
            page.locator('#help-button').focus()
            page.keyboard.press('Space')
            assert page.locator('#clones').inner_text()=='0 / 6'
            page.evaluate("localStorage.setItem('echo12-unlocked','10')")
            page.keyboard.press('o')
            assert page.locator('[data-room="10"]').is_enabled()
            page.locator('[data-room="6"]').click()
            verify(page,errors,'KAYIT')
            assert page.locator('#room').inner_text()=='07 / 11'
            assert page.locator('#hint-assist').is_hidden()
            assert page.evaluate("localStorage.getItem('echo12-unlocked')")=='10'
            page.keyboard.press('h')
            assert 'EŞİK' in page.locator('#hint-step').inner_text()
            page.keyboard.press('o')
            page.locator('[data-room="0"]').click()
            verify(page,errors,'KAYIT')
            assert page.locator('#room').inner_text()=='01 / 11'
            assert not errors, errors
            page.close()
            print('PASS Build 009: hints, room navigation, simulation pause, focus-safe Space and save integrity')

            # Build 010: labels match chapter transitions and multi-gate requirements.
            page, errors = load(browser, 6)
            assert 'BÖLÜM II' in page.locator('#chapter-label').inner_text()
            assert 'İki ayrı iz' not in page.locator('#hint').inner_text()
            assert '0/2' in page.locator('#gate-status').inner_text(), 'Dual-echo plate has a live tally'
            assert page.locator('#gate-counter').inner_text() == '0 / 2 açık'
            assert 'KARŞI SİNYAL' in page.locator('#scene-banner-detail').inner_text() or 'bekliyor' in page.locator('#scene-banner-detail').inner_text().lower()
            page.close()
            page, errors = load(browser, 10)
            assert page.locator('#chapter-label').inner_text() == 'BÖLÜM III · KANIT'
            assert '0/3' in page.locator('#gate-status').inner_text()
            page.evaluate("window.__echo12Test.teleport(9.5,5.5)")
            page.keyboard.press('f')
            page.keyboard.press('e')
            assert '1/3' in page.locator('#gate-status').inner_text()
            assert not errors
            page.close()
            print('PASS Build 010: chapter III evidence tally and chapter II synchronization feedback')

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
