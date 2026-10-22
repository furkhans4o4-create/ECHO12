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
      gate(key){return gateOpen(key)}, fx(){return {rings:fxRings.length,gateA:gateMemory.get('A'),wash:rewindWash}}, teleport(x,y){player.x=x;player.y=y}, position(){return {x:player.x,y:player.y}}, held(){return [...keys]}, floor(){return [floorCache.width,floorCache.height]}, save(){return snapshotSave()}, restore(raw){return applySave(raw)}, validate(raw){return validateSave(raw)}, grantFinalFiles(){caseSolved=new Set(CASE_FILES.map(x=>x.id));updateHUD()}, choose(){return endingChoice}, grantEvidence(ids){for(const id of ids)if(ARCHIVE.some(e=>e.id===id))archiveRead.add(id);renderCaseBoard();refreshArchiveCount()}, sync(){return {...syncedEchoOwners(),scannerOn,elapsed,clones:clones.map(c=>ghostAt(c))}}, setRoute(v){sourceVerdict=v;updateHUD()}, proof(){return {timed:timedSignatureCount(),valid:sourceProofValid(),gap:clones.at(-1)?.proofGap,relay:relayUntil.ROUTE||0}}
    };
    })();'''
    assert needle in html
    html=html.replace(needle,injected)
    # Browser tests run in about:blank; simulate local storage without affecting shipped code.
    storage_stub="""<script>
    window.__echo12Store ??= {};
    Object.defineProperty(window, 'localStorage', {configurable:true,value:{
      getItem(key){return Object.hasOwn(window.__echo12Store,key)?window.__echo12Store[key]:null},
      setItem(key,value){window.__echo12Store[key]=String(value)},
      removeItem(key){delete window.__echo12Store[key]}
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
            assert page.locator('#campaign-segments .campaign-cell').count() == 19
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
            assert page.locator("#archive-count").inner_text() == "1/35"
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
            assert 'KESİNLEŞEN BULGU' in page.locator('#chapter-recap').inner_text()
            assert 'AÇIK KALAN SORU' in page.locator('#chapter-recap').inner_text()
            assert 'çekirdekte kaldı' in page.locator('#chapter-recap').inner_text()
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
            assert 'çekirdeği susturdun' in page.locator('#chapter-recap').inner_text().lower()
            assert page.locator('#archive-count').inner_text()=='2/35'
            saved=page.evaluate('JSON.stringify(window.__echo12Store)')
            html=page.evaluate('document.documentElement.outerHTML')
            html=html.replace('window.__echo12Store ??= {};','window.__echo12Store = '+saved+';')
            page.set_content(html,wait_until='load')
            page.locator('#logbook').click()
            assert '2 / 35' in page.locator('#archive-status').inner_text()
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
            assert page.locator('#archive-count').inner_text().endswith('/35')
            assert 'BÖLÜM II' in page.locator('#kicker').inner_text()
            assert 'üçüncü silueti' in page.locator('#chapter-recap').inner_text().lower()
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
            assert page.locator('#archive-count').inner_text().endswith('/35')
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
            verify(page,errors,'BAŞARILI')
            assert 'yetki başlığı' in page.locator('#dialog-text').inner_text()
            assert 'OPERATÖR 00' in page.locator('#chapter-recap').inner_text()
            assert page.locator('#archive-count').inner_text().endswith('/35')
            page.close()
            print('PASS room 11: evidence triage and chapter IV transition')

            # Build 013: a forged silhouette and a wrong-order trace cannot certify identity.
            page, errors = load(browser, 11)
            assert page.locator('#room').inner_text()=='12 / 19'
            assert 'BÖLÜM IV' in page.locator('#chapter-label').inner_text()
            assert page.locator('#frequency').is_enabled()
            assert page.locator('#proof-panel').is_visible()
            assert 'A/B: sıralı okuma anları' in page.locator('#timeline-legend').inner_text()
            assert 'F İLE DOĞRULA' in page.locator('#proof-evidence').inner_text()
            assert not page.evaluate("window.__echo12Test.gate('PROOF')")
            page.keyboard.press('f')
            page.evaluate("window.__echo12Test.tick(.3)")
            assert not page.evaluate("window.__echo12Test.gate('PROOF')"),'A rendered phantom is never signed proof'
            page.keyboard.press('r')
            move(page,'d',.493);move(page,'w',.493);commit(page)
            # First real attempt uses B before A: deliberately invalid.
            move(page,'d',1.976);move(page,'s',.493);move(page,'w',.986);move(page,'a',.247);commit(page)
            page.keyboard.press('f')
            assert not page.evaluate("window.__echo12Test.gate('PROOF')"),'B to A must not satisfy A to B'
            assert 'A→B 0/1' in page.locator('#gate-status').inner_text()
            assert 'B→A' in page.locator('#proof-records').inner_text()
            assert 'A→B 0/1' in page.locator('#proof-evidence').inner_text()
            # A different real trace goes A then B.
            move(page,'d',1.729);move(page,'w',.493);move(page,'d',.247);move(page,'s',.986);commit(page)
            assert page.evaluate("window.__echo12Test.gate('PROOF')"),'Recorded A to B unlocks proof when scanner is on'
            assert 'A→B' in page.locator('#proof-records').inner_text()
            assert page.locator('#proof-evidence').evaluate("(e)=>e.classList.contains('valid')")
            assert 'GERÇEK İMZA ONAYLANDI' in page.locator('#proof-status').inner_text()
            assert page.locator('#gate-counter').inner_text()=='1 / 2 açık' or page.locator('#gate-counter').inner_text()=='2 / 2 açık'
            move(page,'d',3.45)
            verify(page,errors,'BAŞARILI')
            assert page.locator('#archive-count').inner_text().endswith('/35')
            page.close()
            print('PASS room 12: real ordered provenance, rejected inversion and scanner verification')

            # Build 013: two independently recorded opposite directions, then a lasting choice.
            page, errors = load(browser, 12)
            assert page.locator('#room').inner_text()=='13 / 19'
            assert not page.evaluate("window.__echo12Test.gate('PROOF')")
            move(page,'d',.493);move(page,'w',.493);commit(page)
            move(page,'d',1.73);move(page,'w',.493);move(page,'d',.247);move(page,'s',.986);commit(page)
            page.keyboard.press('f')
            assert not page.evaluate("window.__echo12Test.gate('PROOF')"),'Only forward trace is insufficient in final chamber'
            assert 'A→B 1/1' in page.locator('#gate-status').inner_text()
            assert 'A→B 1/1' in page.locator('#proof-evidence').inner_text()
            assert 'B→A 0/1' in page.locator('#proof-evidence').inner_text()
            move(page,'d',1.976);move(page,'s',.493);move(page,'w',.986);move(page,'a',.247);commit(page)
            assert page.evaluate("window.__echo12Test.gate('PROOF')")
            assert page.locator('#proof-evidence').evaluate("(e)=>e.classList.contains('valid')")
            assert page.locator('#proof-records .proof-record.verified').count()==2
            assert 'B→A 1/1' in page.locator('#proof-evidence').inner_text()
            assert page.locator('#gate-counter').inner_text() in ('1 / 3 açık','2 / 3 açık')
            page.evaluate("window.__echo12Test.teleport(14.5,2.5)")
            page.keyboard.press('e')
            assert page.locator('#decision-title').inner_text()=='KANITI YAYINLA'
            page.locator('#decision-cancel').click()
            assert not page.evaluate("window.__echo12Test.gate('OUT')")
            page.keyboard.press('e')
            page.locator('#decision-confirm').click()
            assert page.evaluate("window.__echo12Test.gate('OUT')")
            page.evaluate("window.__echo12Test.teleport(16.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.03)")
            verify(page,errors,'BAŞARILI')
            assert page.evaluate("localStorage.getItem('echo12-source-verdict')")=='publish'
            assert 'BÖLÜM V' in page.locator('#start').inner_text()
            assert page.locator('#archive-count').inner_text().endswith('/35')
            page.close()
            print('PASS room 13: dual real imprints and chapter V handoff')

            # Build 015: correct order with insufficient travel time cannot be signed.
            page, errors = load(browser, 13)
            assert page.locator('#room').inner_text()=='14 / 19'
            assert 'BÖLÜM V' in page.locator('#chapter-label').inner_text()
            move(page,'d',.493);move(page,'w',.493);commit(page)
            move(page,'d',1.729);move(page,'w',.493);move(page,'d',.247);move(page,'s',.986);commit(page)
            page.keyboard.press('f')
            assert not page.evaluate("window.__echo12Test.gate('STAMP')")
            assert 'A→B' in page.locator('#proof-records').inner_text()
            assert page.evaluate('window.__echo12Test.proof().gap') < 1.6
            assert '1,6–3,6 sn' in page.locator('#proof-evidence').inner_text()
            assert not page.locator('#proof-evidence').evaluate("(e)=>e.classList.contains('valid')")
            move(page,'d',1.729);move(page,'w',.493)
            page.evaluate("window.__echo12Test.tick(.7)")
            move(page,'d',.247);move(page,'s',.986);commit(page)
            assert page.evaluate("window.__echo12Test.gate('STAMP')")
            assert page.evaluate("window.__echo12Test.proof().timed")==1
            assert page.locator('#proof-evidence').evaluate("(e)=>e.classList.contains('valid')")
            move(page,'d',3.45)
            verify(page,errors,'BAŞARILI')
            assert page.locator('#archive-count').inner_text().endswith('/35')
            assert not errors,errors
            page.close()
            print('PASS room 14: attestation gap rejects fast spoof and accepts measured movement')

            # Build 015: previous publication vs quarantine creates genuinely distinct gate rules.
            page, errors = load(browser, 14)
            page.evaluate("window.__echo12Test.setRoute('publish')")
            assert page.locator('#room').inner_text()=='15 / 19'
            assert 'Yankı 0/2' in page.locator('#gate-status').inner_text()
            assert not page.evaluate("window.__echo12Test.gate('ROUTE')")
            page.evaluate("window.__echo12Test.teleport(14.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.12)")
            commit(page)
            assert not page.evaluate("window.__echo12Test.gate('ROUTE')"), 'One echo must not open public route'
            page.evaluate("window.__echo12Test.teleport(14.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.12)")
            commit(page)
            page.evaluate("window.__echo12Test.tick(.18)")
            assert page.evaluate("window.__echo12Test.gate('ROUTE')")
            assert '2/2' in page.locator('#gate-status').inner_text() or 'Etkin' in page.locator('#gate-status').inner_text()
            page.evaluate("window.__echo12Test.teleport(16.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.03)")
            verify(page,errors,'BAŞARILI')
            assert 'İki yankı' in page.locator('#dialog-title').inner_text()
            assert 'A18_PUBLIC' in page.evaluate("localStorage.getItem('echo12-archive')")
            assert page.locator('#archive-count').inner_text().endswith('/35')
            assert page.locator('#authority-chain .authority-node').count()==4
            page.close()
            print('PASS room 15 public: synchronized two-echo route and chapter V result')

            page, errors = load(browser, 14)
            page.evaluate("window.__echo12Test.setRoute('seal')")
            assert 'Canlı temas' in page.locator('#gate-status').inner_text()
            page.evaluate("window.__echo12Test.teleport(14.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.04)")
            assert page.evaluate("window.__echo12Test.gate('ROUTE')")
            page.evaluate("window.__echo12Test.teleport(16.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.03)")
            verify(page,errors,'BAŞARILI')
            assert 'yalnızca sana' in page.locator('#dialog-title').inner_text()
            assert 'A18_SEALED' in page.evaluate("localStorage.getItem('echo12-archive')")
            assert 'güvenle' in page.locator('#chapter-recap').inner_text().lower()
            assert not errors,errors
            page.close()
            print('PASS room 15 sealed: live-only relay and protected outcome')

            # Build 016: two separate recorded witnesses, not one clone or a forged image.
            page, errors = load(browser, 15)
            assert page.locator('#room').inner_text()=='16 / 19'
            assert 'BÖLÜM VI' in page.locator('#chapter-label').inner_text()
            assert page.locator('#sync-panel').is_visible()
            assert not page.evaluate("window.__echo12Test.gate('XSYNC')")
            page.keyboard.press('f')
            assert not page.evaluate("window.__echo12Test.gate('XSYNC')"), 'Hologram cannot operate both sensors'
            page.evaluate("window.__echo12Test.teleport(9.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.09)")
            commit(page)
            assert not page.evaluate("window.__echo12Test.gate('XSYNC')"), 'One recorded clone is insufficient'
            assert 'E1' in page.locator('#sync-left').inner_text()
            page.evaluate("window.__echo12Test.teleport(9.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.09)")
            commit(page)
            assert not page.evaluate("window.__echo12Test.gate('XSYNC')"), 'Two clones on same pad are insufficient'
            page.evaluate("window.__echo12Test.teleport(10.5,7.5)")
            page.evaluate("window.__echo12Test.tick(.09)")
            commit(page)
            page.evaluate("window.__echo12Test.tick(.1)")
            assert page.evaluate("window.__echo12Test.gate('XSYNC')"), page.evaluate('window.__echo12Test.sync()')
            assert 'E3' in page.locator('#sync-right').inner_text()
            page.keyboard.press('f')
            assert not page.evaluate("window.__echo12Test.gate('XSYNC')"), 'Scanner required for authenticity'
            page.keyboard.press('f')
            page.evaluate("window.__echo12Test.teleport(15.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.04)")
            verify(page,errors,'BAŞARILI')
            assert not errors,errors
            page.close()
            print('PASS room 16: independent simultaneous ghosts, wrong pad and fake signal rejected')

            # Build 016: same evidence produces publication versus sealed testimony.
            for route in ['publish','seal']:
                page, errors = load(browser, 16)
                page.evaluate("window.__echo12Test.setRoute('"+route+"')")
                assert page.locator('#room').inner_text()=='17 / 19'
                page.keyboard.press('f')
                page.evaluate("window.__echo12Test.teleport(9.5,3.5)")
                page.evaluate("window.__echo12Test.tick(.1)")
                commit(page)
                page.evaluate("window.__echo12Test.teleport(10.5,7.5)")
                page.evaluate("window.__echo12Test.tick(.1)")
                commit(page)
                page.evaluate("window.__echo12Test.tick(.1)")
                assert page.evaluate("window.__echo12Test.gate('XSYNC')")
                assert not page.evaluate("window.__echo12Test.gate('WITNESS')")
                page.evaluate("window.__echo12Test.teleport(14.5,5.5)")
                if route=='seal':
                    page.keyboard.press('e')
                    assert not page.evaluate("window.__echo12Test.gate('WITNESS')"), 'Sealed witnesses need scanner off'
                    page.keyboard.press('f')
                page.keyboard.press('e')
                assert page.evaluate("window.__echo12Test.gate('WITNESS')"), 'Witness console must authorize'
                assert 'ONAY' in page.locator('#sync-verdict').inner_text()
                page.evaluate("window.__echo12Test.teleport(16.5,5.5)")
                page.evaluate("window.__echo12Test.tick(.04)")
                verify(page,errors,'BAŞARILI')
                assert 'SON BÖLÜM' in page.locator('#start').inner_text()
                assert ('A21_PUBLIC' if route=='publish' else 'A21_SEALED') in page.evaluate("localStorage.getItem('echo12-archive')")
                assert page.locator('#archive-count').inner_text().endswith('/35')
                assert 'KORA' in page.locator('#kicker').inner_text()
                assert 'AÇIK KALAN SORU' in page.locator('#chapter-recap').inner_text()
                assert not errors,errors
                page.close()
            print('PASS room 17: Kora witness publication and privacy-controlled sealed route')

            # Build 018: penultimate room combines an authenticated timestamp and two distinct
            # simultaneous witnesses. A single real trace cannot stand in for both.
            page, errors = load(browser, 17)
            assert page.locator('#room').inner_text() == '18 / 19'
            assert 'BÖLÜM VII' in page.locator('#chapter-label').inner_text()
            page.keyboard.press('f')
            page.evaluate("window.__echo12Test.teleport(4.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.12)")
            commit(page)
            page.evaluate("window.__echo12Test.teleport(9.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.12)")
            page.evaluate("window.__echo12Test.tick(2)")
            page.evaluate("window.__echo12Test.teleport(10.5,7.5)")
            page.evaluate("window.__echo12Test.tick(.12)")
            commit(page)
            assert page.evaluate("window.__echo12Test.gate('STAMP')")
            assert not page.evaluate("window.__echo12Test.gate('XSYNC')")
            page.evaluate("window.__echo12Test.teleport(9.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.12)")
            commit(page)
            page.evaluate("window.__echo12Test.tick(2.6)")
            assert page.evaluate("window.__echo12Test.gate('STAMP')")
            assert page.evaluate("window.__echo12Test.gate('XSYNC')"), page.evaluate("window.__echo12Test.sync()")
            page.evaluate("window.__echo12Test.teleport(16.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.04)")
            verify(page,errors,'BAŞARILI')
            assert not errors,errors
            page.close()
            print('PASS room 18: authenticated time bridge and simultaneous distinct witnesses')

            # Build 018: final choices respect the solved proof, are not substitutes for the
            # earlier publish/seal outcome, and only grant independent review after 3 deductions.
            for choice in ['revoke','preserve','review']:
                page, errors = load(browser, 18)
                assert page.locator('#room').inner_text()=='19 / 19'
                assert not page.evaluate("window.__echo12Test.gate('FINAL')")
                page.keyboard.press('f')
                page.evaluate("window.__echo12Test.teleport(4.5,3.5)")
                page.evaluate("window.__echo12Test.tick(.12)")
                commit(page)
                page.evaluate("window.__echo12Test.teleport(9.5,3.5)")
                page.evaluate("window.__echo12Test.tick(.12)")
                page.evaluate("window.__echo12Test.teleport(10.5,7.5)")
                page.evaluate("window.__echo12Test.tick(.12)")
                commit(page)
                page.evaluate("window.__echo12Test.teleport(10.5,7.5)")
                page.evaluate("window.__echo12Test.tick(.12)")
                page.evaluate("window.__echo12Test.teleport(9.5,3.5)")
                page.evaluate("window.__echo12Test.tick(.12)")
                commit(page)
                assert page.evaluate("window.__echo12Test.gate('PROOF')")
                assert not page.evaluate("window.__echo12Test.gate('FINAL')")
                page.evaluate("window.__echo12Test.teleport(14.5,5.5)")
                page.keyboard.press('e')
                assert page.locator('#decision').is_hidden(), 'Independent review requires case files'
                assert page.locator('#mode').inner_text()=='KAYIT'
                if choice=='review':
                    page.evaluate("window.__echo12Test.grantFinalFiles()")
                coord={'revoke':(14.5,2.5),'preserve':(14.5,8.5),'review':(14.5,5.5)}[choice]
                page.evaluate("window.__echo12Test.teleport(..."+str(list(coord))+")")
                page.keyboard.press('e')
                assert page.locator('#decision').is_visible()
                page.locator('#decision-confirm').click()
                assert page.evaluate("window.__echo12Test.choose()")==choice
                assert page.evaluate("window.__echo12Test.gate('FINAL')")
                page.evaluate("window.__echo12Test.teleport(16.5,5.5)")
                page.evaluate("window.__echo12Test.tick(.04)")
                verify(page,errors,'TAMAMLANDI')
                assert page.evaluate("localStorage.getItem('echo12-final-verdict')")==choice
                assert ('F01_'+{'revoke':'PURGE','preserve':'PRESERVE','review':'REVIEW'}[choice]) in page.evaluate("localStorage.getItem('echo12-archive')")
                assert page.locator('#archive-count').inner_text().endswith('/35')
                assert 'BÖLÜM VII' in page.locator('#kicker').inner_text()
                assert 'AÇIK KALAN SORU' in page.locator('#chapter-recap').inner_text()
                assert not errors,errors
                page.close()
            print('PASS room 19: three distinct endings, mandatory proof and independent case file prerequisite')

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
            assert page.locator('#room-picker-grid button').count() == 19
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
            assert page.locator('#room').inner_text()=='07 / 19'
            assert page.locator('#hint-assist').is_hidden()
            assert page.evaluate("localStorage.getItem('echo12-unlocked')")=='10'
            page.keyboard.press('h')
            assert 'EŞİK' in page.locator('#hint-step').inner_text()
            page.keyboard.press('o')
            page.locator('[data-room="0"]').click()
            verify(page,errors,'KAYIT')
            assert page.locator('#room').inner_text()=='01 / 19'
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

            # Build 011: touch-pad layout and independent multi-touch directions.
            page, errors = load(browser, 0)
            page.set_viewport_size({"width":390,"height":844})
            assert page.locator('.mobile-controls').is_visible()
            assert page.locator('.mobilepad [data-dir]').count()==4
            assert page.locator('#mobile-record').is_visible()
            assert page.locator('#mobile-interact').is_visible()
            assert page.evaluate("window.__echo12Test.floor()")==[864,528], 'Floor is cached at fixed game resolution'
            start=page.evaluate("window.__echo12Test.position()")
            page.evaluate("""() => {
              const down=(code,id)=>document.querySelector('[data-dir="'+code+'"]').dispatchEvent(
                new PointerEvent('pointerdown',{bubbles:true,pointerId:id,pointerType:'touch',isPrimary:id===11}));
              down('ArrowUp',11);down('ArrowRight',22);
            }""")
            assert page.locator('[data-dir="ArrowUp"]').get_attribute('aria-pressed')=='true'
            assert page.locator('[data-dir="ArrowRight"]').get_attribute('aria-pressed')=='true'
            page.evaluate("window.__echo12Test.tick(.30)")
            moved=page.evaluate("window.__echo12Test.position()")
            assert moved['x']>start['x']+.5 and moved['y']<start['y']-.5, (start,moved)
            page.evaluate("""() => document.querySelector('[data-dir="ArrowUp"]').dispatchEvent(
              new PointerEvent('pointerup',{bubbles:true,pointerId:11,pointerType:'touch'}))""")
            before=page.evaluate("window.__echo12Test.position()")
            page.evaluate("window.__echo12Test.tick(.20)")
            after=page.evaluate("window.__echo12Test.position()")
            assert after['x']>before['x']+.3 and abs(after['y']-before['y'])<.01, (before,after)
            page.evaluate("""() => document.querySelector('[data-dir="ArrowRight"]').dispatchEvent(
              new PointerEvent('pointercancel',{bubbles:true,pointerId:22,pointerType:'touch'}))""")
            assert page.locator('[data-dir="ArrowRight"]').get_attribute('aria-pressed')=='false'
            assert not page.evaluate("window.__echo12Test.held()"), 'Touch cancel must release direction'
            before=page.evaluate("window.__echo12Test.position()")
            page.evaluate("window.__echo12Test.tick(.15)")
            after=page.evaluate("window.__echo12Test.position()")
            assert abs(after['x']-before['x'])<.01 and abs(after['y']-before['y'])<.01
            page.locator('#mobile-record').click()
            assert page.locator('#clones').inner_text()=='1 / 6'
            page.locator('#mobile-undo').click()
            assert page.locator('#clones').inner_text()=='0 / 6'
            page.locator('#mobile-pause').click()
            verify(page,errors,'DURDU')
            page.locator('#mobile-pause').click()
            verify(page,errors,'KAYIT')
            assert not errors, errors
            page.close()
            print('PASS Build 011: responsive D-pad, concurrent touch, cancellation, central record and mobile pause')

            # Build 012: overview, optional follow-camera, minimap and stored preference.
            page, errors = load(browser, 0)
            assert page.locator('#camera-toggle').get_attribute('aria-pressed')=='false', 'Desktop defaults to overview'
            assert page.locator('#minimap-box').is_hidden()
            page.set_viewport_size({"width":390,"height":844})
            page.locator('#camera-toggle').click()
            assert page.locator('#camera-toggle').get_attribute('aria-pressed')=='true'
            assert page.locator('.stage').evaluate("(e)=>e.classList.contains('focus-camera')")
            assert page.locator('#minimap-box').is_visible()
            assert page.evaluate("localStorage.getItem('echo12-camera-mode')")=='focus'
            origin_before=page.locator('#scene').evaluate("(e)=>e.style.transformOrigin")
            move(page,'d',.35)
            origin_after=page.locator('#scene').evaluate("(e)=>e.style.transformOrigin")
            assert origin_before!=origin_after, (origin_before,origin_after)
            assert page.locator('#minimap').get_attribute('width')=='216'
            # Static 11x18 map is rendered even as the main canvas follows the character.
            px=page.locator('#minimap').evaluate("(e)=>[...e.getContext('2d').getImageData(0,0,1,1).data]")
            assert px[3]==255, px
            page.locator('#camera-toggle').click()
            assert page.locator('#camera-toggle').get_attribute('aria-pressed')=='false'
            assert page.locator('#minimap-box').is_hidden()
            assert page.evaluate("localStorage.getItem('echo12-camera-mode')")=='overview'
            assert not errors, errors
            page.close()
            print('PASS Build 012: focus camera, full-map minimap, follow origin, manual overview and preference')

            # Build 017: three independent evidence cases are locked until their actual archive sources are found.
            page, errors = load(browser, 0)
            assert page.locator('#case-board-count').inner_text()=='0/3'
            page.keyboard.press('k')
            verify(page,errors,'DELİL PANOSU')
            assert page.locator('#case-grid .case-item').count()==3
            assert page.locator('[data-case-id="C01"] .case-options button').first.is_disabled()
            frozen=page.locator('#time').inner_text()
            page.evaluate("window.__echo12Test.tick(1.2)")
            assert page.locator('#time').inner_text()==frozen, 'Case board must pause active loop'
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            assert page.locator('#case-board').is_hidden()
            page.evaluate("window.__echo12Test.grantEvidence(['A09'])")
            page.keyboard.press('k')
            assert page.locator('[data-case-id="C01"] .case-options button').first.is_disabled(), 'Both sources must be present'
            page.keyboard.press('Escape')
            page.evaluate("window.__echo12Test.grantEvidence(['A12'])")
            page.keyboard.press('k')
            assert page.locator('[data-case-id="C01"] .case-options button').first.is_enabled()
            page.locator('[data-case-id="C01"] .case-options button').first.click()
            assert page.locator('#case-board-count').inner_text()=='0/3', 'Wrong inference must not grant reward'
            assert 'Henüz doğrulanamadı' in page.locator('[data-case-id="C01"] .case-feedback').inner_text()
            page.locator('[data-case-id="C01"] .case-options button').nth(1).click()
            assert page.locator('#case-board-count').inner_text()=='1/3'
            assert 'D01' in page.evaluate("localStorage.getItem('echo12-archive')")
            assert 'C01' in page.evaluate("localStorage.getItem('echo12-case-deductions')")
            assert page.locator('[data-case-id="C01"] .case-options button').first.is_disabled()
            assert page.locator('[data-case-id="C02"] .case-options button').first.is_disabled()
            page.keyboard.press('Escape')
            page.evaluate("window.__echo12Test.grantEvidence(['A14','A17','A19','A20'])")
            page.keyboard.press('k')
            page.locator('[data-case-id="C02"] .case-options button').nth(1).click()
            page.locator('[data-case-id="C03"] .case-options button').nth(1).click()
            assert page.locator('#case-progress').inner_text().startswith('3 / 3')
            assert page.locator('#case-board-count').inner_text()=='3/3'
            assert page.locator('#archive-count').inner_text().endswith('/35')
            for name in ['D01','D02','D03']:
                assert name in page.evaluate("localStorage.getItem('echo12-archive')")
            page.keyboard.press('k')
            verify(page,errors,'KAYIT')
            assert page.locator('#case-board').is_hidden()
            page.keyboard.press('l')
            verify(page,errors,'ARŞİV')
            assert page.locator('#archive-list button').count()==35
            assert page.locator('#archive-list button').filter(has_text='ÇIKARIM 03').count()==1
            assert not errors, errors
            page.close()
            print('PASS Build 017: source-gated independent casework, wrong answer rejection, persistent files and paused modal')

            # Build 019: save vault freezes the loop and exports a versioned, offline JSON backup.
            page, errors = load(browser, 0)
            page.keyboard.press('b')
            verify(page,errors,'KAYIT KASASI')
            assert page.locator('#vault-endings .vault-ending').count()==3
            assert page.locator('#vault-endings .vault-ending.earned').count()==0
            before=page.locator('#time').inner_text()
            page.evaluate("window.__echo12Test.tick(.7)")
            assert page.locator('#time').inner_text()==before
            saved=page.evaluate("window.__echo12Test.save()")
            assert saved['format']=='ECHO12_SAVE_V1' and saved['version']==1
            assert saved['progress']['unlocked']==0
            assert page.evaluate("""() => {try{window.__echo12Test.validate({format:'evil'});return false}catch(e){return true}}""")
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            page.keyboard.press('b')
            with page.expect_download() as d:
                page.locator('#vault-export').click()
            assert d.value.suggested_filename=='ECHO12_Kayit_Yedegi.json'
            page.locator('#vault-import').set_input_files({
                "name":"broken.json","mimeType":"application/json","buffer":b'{{corrupt'
            })
            assert 'Geri yüklenemedi' in page.locator('#vault-feedback').inner_text()
            assert page.locator('#mode').inner_text()=='KAYIT KASASI'
            # Restore a complete file, not just room progress; reject manipulated values first.
            backup=page.evaluate("window.__echo12Test.save()")
            backup['progress'].update({
                'unlocked':4,'chapterPath':'cut','sourceVerdict':'seal','finalVerdict':'review',
                'archive':['A09','A12','D01','F01_REVIEW'],'endings':['cut'],'caseSolved':['C01'],
                'bestRuns':{'0':{'echoes':2,'seconds':19.1,'hints':0}},'muted':True,'camera':'overview'
            })
            assert page.evaluate("""data => {try{
                const copy=JSON.parse(JSON.stringify(data));copy.progress.bestRuns['0'].seconds=-5;
                window.__echo12Test.restore(copy);return false;
              }catch(e){return true}}""",backup)
            assert page.evaluate("localStorage.getItem('echo12-unlocked')") is None
            page.evaluate("data=>window.__echo12Test.restore(data)",backup)
            verify(page,errors,'KAYIT')
            assert page.locator('#room').inner_text()=='05 / 19'
            assert page.locator('#case-board-count').inner_text()=='1/3'
            assert page.locator('#archive-count').inner_text()=='4/35'
            assert page.evaluate("localStorage.getItem('echo12-final-verdict')")=='review'
            assert page.evaluate("localStorage.getItem('echo12-muted')")=='1'
            assert page.evaluate("JSON.parse(localStorage.getItem('echo12-best-runs'))['0'].echoes")==2
            page.keyboard.press('b')
            assert page.locator('#vault-endings .vault-ending.earned').count()==1
            assert 'Bağımsız incelemeye aktar' in page.locator('#vault-endings').inner_text()
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            assert not errors,errors
            page.close()
            print('PASS Build 019: offline backup, corrupt JSON rejection, save normalization and discovered finales')

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
