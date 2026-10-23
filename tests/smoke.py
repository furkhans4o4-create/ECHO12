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
      gate(key){return gateOpen(key)}, openAudit(){openAuditPanel()}, fx(){return {rings:fxRings.length,gateA:gateMemory.get('A'),wash:rewindWash}}, teleport(x,y){player.x=x;player.y=y}, position(){return {x:player.x,y:player.y}}, held(){return [...keys]}, floor(){return [floorCache.width,floorCache.height]}, inspect(){return {time:inspectorTime,elapsed,position:{...player},record:record.length,echoes:clones.length}}, advanceInspector(seconds){advanceInspectorPlayback(seconds)}, save(){return snapshotSave()}, restore(raw){return applySave(raw)}, validate(raw){return validateSave(raw)}, grantFinalFiles(){caseSolved=new Set(CASE_FILES.map(x=>x.id));updateHUD()}, choose(){return endingChoice}, grantEvidence(ids){for(const id of ids)if(ARCHIVE.some(e=>e.id===id))archiveRead.add(id);renderCaseBoard();refreshArchiveCount()}, sync(){return {...syncedEchoOwners(),scannerOn,elapsed,clones:clones.map(c=>ghostAt(c))}}, echoIDs(){return clones.map(c=>captureFingerprint(c))}, setRoute(v){sourceVerdict=v;updateHUD()}, proof(){return {timed:timedSignatureCount(),valid:sourceProofValid(),gap:clones.at(-1)?.proofGap,relay:relayUntil.ROUTE||0}}
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
            assert page.evaluate("JSON.parse(localStorage.getItem('echo12-room-clears'))")==[0]
            assert page.locator('#campaign-segments .campaign-cell.finished').count()==1
            record=page.evaluate("JSON.parse(localStorage.getItem('echo12-best-runs'))")
            assert record['0']['echoes']==1 and record['0']['seconds']>0, record
            assert page.locator('#debrief .debrief-stat').count() >= 3
            assert page.locator('#debrief').inner_text().find('Yeni kişisel rekor')>=0
            assert page.locator('#gate-counter').inner_text() == '1 / 1 açık'
            page.locator('#room-select').click()
            assert 'EN İYİ 1 YANKI' in page.locator('[data-room="0"]').inner_text()
            assert page.locator('[data-room="0"]').get_attribute('data-cleared')=='true'
            assert 'TAMAMLANDI' in page.locator('[data-room="0"]').inner_text()
            page.keyboard.press('Escape')
            page.close()
            print("PASS 1/5 + undo, performance records and post-room debrief")
            
            # Build 030: the phase shift is a real new physical constraint.
            # A delayed echo cannot open its gate until materialization time.
            page, errors = load(browser, 6)
            page.locator('#echo-editor summary').click()
            page.evaluate("document.activeElement.blur()")
            page.evaluate("window.__echo12Test.teleport(4.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.2)")
            commit(page)
            baseline=page.evaluate("window.__echo12Test.echoIDs()")
            assert page.locator('[data-echo-index="0"] .echo-phase-controls output').get_attribute('data-phase')=='0'
            assert page.locator('[data-echo-index="0"] .echo-phase-controls button').first.is_disabled()
            assert page.evaluate("window.__echo12Test.gate('Q')")==False
            page.evaluate("window.__echo12Test.tick(.2)")
            assert page.evaluate("window.__echo12Test.gate('Q')")==True
            page.locator('[data-echo-index="0"] .echo-phase-controls button').last.click()
            assert page.locator('[data-echo-index="0"] .echo-phase-controls output').get_attribute('data-phase')=='0.5'
            assert page.evaluate("window.__echo12Test.inspect().elapsed")==0
            assert page.evaluate("window.__echo12Test.echoIDs()")==baseline
            assert page.evaluate("window.__echo12Test.gate('Q')")==False
            page.evaluate("window.__echo12Test.tick(.3)")
            assert page.evaluate("window.__echo12Test.gate('Q')")==False
            page.evaluate("window.__echo12Test.tick(.4)")
            assert page.evaluate("window.__echo12Test.gate('Q')")==True
            page.locator('#plate-forecast summary').click()
            assert page.locator('[data-plate="Q"] [data-kind="contact"]').count()>0
            starts=page.locator('[data-plate="Q"] [data-kind="contact"]').first.evaluate(
                "e=>parseFloat(e.style.left)")
            assert starts>=4,starts
            page.locator('[data-echo-index="0"] .echo-phase-controls button').first.click()
            assert page.locator('[data-echo-index="0"] .echo-phase-controls output').get_attribute('data-phase')=='0'
            assert page.locator('[data-echo-index="0"] .echo-phase-controls button').first.is_disabled()
            for i in range(6):
                page.locator('[data-echo-index="0"] .echo-phase-controls button').last.click()
            assert page.locator('[data-echo-index="0"] .echo-phase-controls output').get_attribute('data-phase')=='3'
            assert page.locator('[data-echo-index="0"] .echo-phase-controls button').last.is_disabled()
            assert page.evaluate("window.__echo12Test.gate('Q')")==False
            page.locator('[data-echo-index="0"] button:last-child').click()
            assert page.locator('#echo-restore').is_enabled()
            page.locator('#echo-restore').click()
            assert page.locator('[data-echo-index="0"] .echo-phase-controls output').get_attribute('data-phase')=='3'
            assert page.evaluate("window.__echo12Test.echoIDs()")==baseline
            page.keyboard.press('r')
            assert page.locator('#echo-editor-list .echo-editor-row').count()==0
            assert not errors,errors
            page.close()
            print('PASS Build 030: delayed materialization, real gate, phase bounds and restore')

            # The first chapter retains original movement and has phase locked.
            page, errors = load(browser, 0)
            page.locator('#echo-editor summary').click()
            page.evaluate("document.activeElement.blur()")
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            assert page.locator('[data-echo-index="0"] .echo-phase-controls').get_attribute('aria-disabled')=='true'
            assert page.locator('[data-echo-index="0"] .echo-phase-controls button').first.is_disabled()
            assert page.locator('[data-echo-index="0"] .echo-phase-controls button').last.is_disabled()
            assert not errors,errors
            page.close()
            print('PASS Build 030: introductory chapter cannot phase-shift recordings')

            # Reverse records must be timed from their actual reverse appearance:
            # moving the near-end event past 12 seconds removes its plate contact.
            page, errors = load(browser, 9)
            page.locator('#echo-editor summary').click()
            page.evaluate("document.activeElement.blur()")
            page.keyboard.press('f')
            page.evaluate("window.__echo12Test.teleport(4.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.2)")
            page.evaluate("window.__echo12Test.teleport(2.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.3)")
            commit(page)
            page.locator('#plate-forecast summary').click()
            assert page.locator('[data-plate="V"] [data-kind="contact"]').count()>0
            page.locator('[data-echo-index="0"] .echo-phase-controls button').last.click()
            assert page.locator('[data-plate="V"] [data-kind="contact"]').count()==0
            assert not errors,errors
            page.close()
            print('PASS Build 030: reverse contacts are clipped when phased beyond 12 seconds')

            # Build 027: read-only plate forecast follows immutable echo recordings.
            page, errors = load(browser, 0)
            page.locator('#plate-forecast summary').click()
            page.evaluate("document.activeElement.blur()")
            assert page.locator('#plate-forecast-list .plate-forecast-item').count()==1
            assert page.locator('[data-plate="A"]').get_attribute('data-ready')=='false'
            assert page.locator('[data-plate="A"] .plate-forecast-band').count()==0
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            assert page.locator('[data-plate="A"]').get_attribute('data-ready')=='true'
            assert '1 / 1' in page.locator('[data-plate="A"]').inner_text()
            assert page.locator('[data-plate="A"] [data-kind="contact"]').count()>0
            intervals=page.locator('[data-plate="A"] [data-kind="contact"]').evaluate_all(
                "(els)=>els.map(e=>e.getAttribute('title'))")
            page.keyboard.press('z')
            assert page.locator('[data-plate="A"]').get_attribute('data-ready')=='false'
            assert page.locator('[data-plate="A"] [data-kind="contact"]').count()==0
            page.keyboard.press('Shift+z')
            assert page.locator('[data-plate="A"]').get_attribute('data-ready')=='true'
            assert page.locator('[data-plate="A"] [data-kind="contact"]').evaluate_all(
                "(els)=>els.map(e=>e.getAttribute('title'))")==intervals
            page.keyboard.press('r')
            assert page.locator('[data-plate="A"] [data-kind="contact"]').count()==0
            assert not errors,errors
            page.close()
            print('PASS Build 027: plate timing forecast, selective undo/redo, full restart')

            # Two copies must overlap on the echo-only dual pressure plate.
            page, errors = load(browser, 6)
            page.locator('#plate-forecast summary').click()
            page.evaluate("document.activeElement.blur()")
            assert page.locator('[data-plate="R"]').get_attribute('data-ready')=='false'
            page.evaluate("window.__echo12Test.teleport(9.5,7.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            assert '1 / 2' in page.locator('[data-plate="R"]').inner_text()
            assert page.locator('[data-plate="R"] [data-kind="contact"]').count()==0
            page.evaluate("window.__echo12Test.teleport(9.5,7.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            assert '2 / 2' in page.locator('[data-plate="R"]').inner_text()
            assert page.locator('[data-plate="R"]').get_attribute('data-ready')=='true'
            assert page.locator('[data-plate="R"] [data-kind="contact"]').count()>0
            assert not errors,errors
            page.close()
            print('PASS Build 027: two-record simultaneous pressure prediction')

            # Pulse extension is displayed, and scanner dependency is explicit.
            page, errors = load(browser, 3)
            page.locator('#plate-forecast summary').click()
            page.evaluate("document.activeElement.blur()")
            page.evaluate("window.__echo12Test.teleport(4.5,2.5)")
            page.evaluate("window.__echo12Test.tick(.2)")
            page.evaluate("window.__echo12Test.teleport(2.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.2)")
            commit(page)
            assert page.locator('[data-plate="A"] [data-kind="contact"]').count()>0
            assert page.locator('[data-plate="A"] [data-kind="relay"]').count()>0
            assert not errors,errors
            page.close()
            page, errors = load(browser, 8)
            page.locator('#plate-forecast summary').click()
            page.evaluate("document.activeElement.blur()")
            page.evaluate("window.__echo12Test.teleport(4.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            assert page.locator('[data-plate="T"]').get_attribute('data-ready')=='false'
            assert 'F doğrulayıcısı kapalı' in page.locator('[data-plate="T"]').inner_text()
            page.keyboard.press('f')
            assert page.locator('[data-plate="T"]').get_attribute('data-ready')=='true'
            assert not errors,errors
            page.close()
            print('PASS Build 027: relay extension and scanner-conditioned predictions')

            # Build 029: operator mastery medals persist after real room completion.
            page, errors = load(browser, 0)
            page.locator('#challenge-panel summary').click()
            assert page.locator('#challenge-list .challenge-item').count()==3
            assert page.locator('#challenge-score').inner_text().startswith('0 / 3')
            page.evaluate("document.activeElement.blur()")
            move(page,'d',.99);move(page,'w',.49);commit(page)
            move(page,'d',3.4)
            verify(page,errors,'BAŞARILI')
            medals=page.evaluate("JSON.parse(localStorage.getItem('echo12-room-challenges'))")
            assert set(medals['0'])=={'precise','focus','speed'},medals
            assert page.locator('#debrief').inner_text().count('Yeni sınama')==3
            assert page.locator('#challenge-score').inner_text().startswith('3 / 3')
            saved=page.evaluate("window.__echo12Test.save()")
            assert set(saved['progress']['challenges']['0'])=={'precise','focus','speed'}
            page.locator('#room-select').click()
            assert 'SINAMA 3/3' in page.locator('[data-room="0"]').inner_text()
            page.keyboard.press('Escape')
            assert not errors,errors
            page.close()
            print('PASS Build 029: three earned medals, debrief, room selector and export')

            # Existing backup version 1 works without the optional challenges field.
            page, errors = load(browser, 0)
            prior=page.evaluate("window.__echo12Test.save()")
            assert prior['progress']['challenges']=={}
            legacy=page.evaluate("window.__echo12Test.save()")
            legacy['progress'].pop('challenges')
            assert page.evaluate("(raw)=>window.__echo12Test.validate(raw).challenges",legacy)=={}
            invalid=page.evaluate("window.__echo12Test.save()")
            invalid['progress']['challenges']={'0':['precise']}
            try:
                page.evaluate("(raw)=>window.__echo12Test.validate(raw)",invalid)
                raise AssertionError('Uncleared room medals should not be accepted')
            except Exception as ex:
                assert 'Operatör' in str(ex)
            invalid=page.evaluate("window.__echo12Test.save()")
            invalid['progress']['challenges']={'19':['speed']}
            try:
                page.evaluate("(raw)=>window.__echo12Test.validate(raw)",invalid)
                raise AssertionError('Out-of-range room medal was accepted')
            except Exception as ex:
                assert 'Operatör' in str(ex)
            page.evaluate("(raw)=>window.__echo12Test.restore(raw)",legacy)
            assert page.evaluate("localStorage.getItem('echo12-room-challenges')")=='{}'
            assert not errors,errors
            page.close()
            print('PASS Build 029: old save import, achievement validation and safe restore')

            # Build 026: quick retry discards only the current live path, not
            # previous recordings, their order, or a pending restore candidate.
            page, errors = load(browser, 0)
            assert page.locator('#retry').is_enabled()
            assert page.locator('#mobile-retry').is_enabled()
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            first=page.evaluate("window.__echo12Test.echoIDs()")
            assert len(first)==1
            move(page,'d',.4)
            before=page.evaluate("window.__echo12Test.inspect()")
            assert before['elapsed']>0.2 and before['record']>1
            page.keyboard.press('x')
            after=page.evaluate("window.__echo12Test.inspect()")
            assert after['elapsed']<0.15 and after['record']<=10
            assert after['echoes']==1
            assert page.evaluate("window.__echo12Test.echoIDs()")==first
            assert page.evaluate("window.__echo12Test.position()")=={'x':2.5,'y':5.5}
            move(page,'d',.3)
            page.locator('#retry').click()
            assert page.evaluate("window.__echo12Test.inspect().elapsed")<0.15
            assert page.evaluate("window.__echo12Test.echoIDs()")==first
            move(page,'d',.25)
            page.locator('#mobile-retry').evaluate('(e)=>e.click()')
            assert page.evaluate("window.__echo12Test.inspect().elapsed")<0.15
            assert page.evaluate("window.__echo12Test.echoIDs()")==first
            page.locator('#undo').click()
            page.locator('#echo-editor summary').click()
            assert page.locator('#echo-restore').is_enabled()
            page.locator('#retry').click()
            assert page.locator('#echo-restore').is_enabled(), 'Retry must not erase the last deleted recording'
            page.locator('#echo-restore').click()
            assert page.evaluate("window.__echo12Test.echoIDs()")==first
            page.keyboard.press('p')
            assert page.locator('#retry').is_disabled()
            assert page.locator('#mobile-retry').is_disabled()
            page.keyboard.press('x')
            assert page.locator('#mode').inner_text()=='DURDU'
            page.keyboard.press('p')
            assert page.locator('#retry').is_enabled()
            assert not errors,errors
            page.close()
            print('PASS Build 026: preserve echoes and undo across keyboard, desktop and touch retry; block retry while paused')

            # Build 025: remove an arbitrary echo, restore it at the original index,
            # reset live progress, and expire the restore window on a new recording.
            page, errors = load(browser, 0)
            assert page.locator('#echo-editor-count').inner_text() == '0 / 6'
            page.locator('#echo-editor summary').focus()
            page.keyboard.press('Space')
            assert page.locator('#echo-editor').get_attribute('open') is not None
            assert page.locator('#clones').inner_text()=='0 / 6'
            page.keyboard.press('Space')
            assert page.locator('#echo-editor').get_attribute('open') is None
            page.locator('#echo-editor summary').click()
            assert 'henüz' in page.locator('#echo-editor-list').inner_text()
            # Give gameplay focus back before using Space to record.
            page.evaluate("document.activeElement.blur()")
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            page.evaluate("window.__echo12Test.teleport(3.5,6.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            assert page.locator('#echo-editor-list .echo-editor-row').count()==2
            original=page.evaluate("window.__echo12Test.echoIDs()")
            page.locator('#echo-editor-list [data-echo-index="0"] button:last-child').click()
            assert page.locator('#echo-editor-list .echo-editor-row').count()==1
            assert page.locator('#echo-restore').is_enabled()
            assert page.evaluate("window.__echo12Test.inspect().elapsed")<0.5
            assert page.evaluate("window.__echo12Test.echoIDs()") == original[1:]
            page.locator('#echo-restore').click()
            assert page.locator('#echo-editor-list .echo-editor-row').count()==2
            assert page.evaluate("window.__echo12Test.echoIDs()") == original
            assert page.locator('#echo-restore').is_disabled()
            page.keyboard.press('z')
            assert page.locator('#echo-restore').is_enabled()
            page.keyboard.press('Shift+z')
            assert page.locator('#echo-editor-list .echo-editor-row').count()==2
            assert page.locator('#echo-restore').is_disabled()
            page.locator('#echo-editor-list [data-echo-index="0"] button:last-child').click()
            assert page.locator('#echo-restore').is_enabled()
            page.locator('#commit').click()
            page.evaluate("window.__echo12Test.tick(.01)")
            assert page.locator('#echo-restore').is_disabled()
            assert not errors,errors
            page.keyboard.press('r')
            assert page.locator('#echo-editor-list .echo-editor-row').count()==0
            assert page.locator('#echo-restore').is_disabled()
            assert not errors,errors
            page.close()
            print('PASS Build 025: selective delete, original-order restore, Shift+Z, recording expiry and restart')

            # Removing a proof-bearing echo must invalidate its certified gate.
            page, errors = load(browser, 12)
            move(page,'d',.493);move(page,'w',.493);commit(page)
            move(page,'d',1.73);move(page,'w',.493);move(page,'d',.247);move(page,'s',.986);commit(page)
            move(page,'d',1.976);move(page,'s',.493);move(page,'w',.986);move(page,'a',.247);commit(page)
            page.keyboard.press('f')
            assert page.evaluate("window.__echo12Test.gate('PROOF')")
            page.locator('#echo-editor summary').click()
            assert 'A→B' in page.locator('#echo-editor-list').inner_text()
            assert 'B→A' in page.locator('#echo-editor-list').inner_text()
            page.locator('#echo-editor-list [data-echo-index="1"] button:last-child').click()
            assert not page.evaluate("window.__echo12Test.gate('PROOF')")
            assert 'A→B 0/1' in page.locator('#proof-evidence').inner_text()
            page.locator('#echo-restore').click()
            assert page.evaluate("window.__echo12Test.gate('PROOF')")
            assert not errors,errors
            page.close()
            print('PASS Build 025: proven opposite-order records are revoked and reinstated correctly')

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
            assert page.locator('#sync-timeline').is_visible()
            assert page.locator('#sync-timeline-tracks .sync-timeline-row').count()==2
            assert 'İki farklı' in page.locator('#sync-timeline-result').inner_text()
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
            assert page.locator('#sync-timeline-tracks .sync-timeline-row').count()==3
            assert 'ortak zamanı yok' in page.locator('#sync-timeline-result').inner_text()
            page.evaluate("window.__echo12Test.teleport(10.5,7.5)")
            page.evaluate("window.__echo12Test.tick(.09)")
            commit(page)
            page.evaluate("window.__echo12Test.tick(.1)")
            assert page.evaluate("window.__echo12Test.gate('XSYNC')"), page.evaluate('window.__echo12Test.sync()')
            assert page.locator('#sync-timeline-tracks .sync-timeline-row').count()==4
            assert page.locator('#sync-timeline .sync-timeline-segment[data-pad="ORTAK"]').count()>=1
            assert 'aynı anda' in page.locator('#sync-timeline-result').inner_text()
            assert page.locator('#sync-timeline-result').get_attribute('data-ready')=='true'
            assert 'E3' in page.locator('#sync-right').inner_text()
            page.keyboard.press('f')
            assert not page.evaluate("window.__echo12Test.gate('XSYNC')"), 'Scanner required for authenticity'
            assert page.locator('#sync-timeline-result').get_attribute('data-ready')=='false'
            assert 'F ile' in page.locator('#sync-timeline-result').inner_text()
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
            assert saved['progress']['clearedRooms']==[]
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
            page.wait_for_function("document.querySelector('#vault-feedback').textContent.includes('Geri yüklenemedi')")
            assert page.locator('#mode').inner_text()=='KAYIT KASASI'
            # Restore a complete file, not just room progress; reject manipulated values first.
            backup=page.evaluate("window.__echo12Test.save()")
            backup['progress'].update({
                'unlocked':4,'chapterPath':'cut','sourceVerdict':'seal','finalVerdict':'review',
                'archive':['A09','A12','D01','F01_REVIEW'],'endings':['cut'],'caseSolved':['C01'],
                'bestRuns':{'0':{'echoes':2,'seconds':19.1,'hints':0}},'clearedRooms':[0,1,3],'muted':True,'camera':'overview'
            })
            assert page.evaluate("""data => {try{
                const copy=JSON.parse(JSON.stringify(data));copy.progress.bestRuns['0'].seconds=-5;
                window.__echo12Test.restore(copy);return false;
              }catch(e){return true}}""",backup)
            assert page.evaluate("localStorage.getItem('echo12-unlocked')") is None
            # An invalid completed room can never exceed the unlocked range.
            assert page.evaluate("""data=>{try{
                const x=JSON.parse(JSON.stringify(data));x.progress.clearedRooms=[0,18];
                window.__echo12Test.validate(x);return false
            }catch(e){return true}}""",backup)
            # Backwards compatibility: v1 backups without explicit completion metadata.
            legacy=page.evaluate("""data=>{
                const x=JSON.parse(JSON.stringify(data));delete x.progress.clearedRooms;
                return window.__echo12Test.validate(x).clearedRooms
            }""",backup)
            assert legacy==[0,1,2,3],legacy
            # Simulate storage quota failure partway through the commit.
            # Restoring must roll back *all* previous fields and leave in-memory game state intact.
            assert page.evaluate("""data=>{
                const before=JSON.stringify(window.__echo12Store),original=localStorage.setItem;
                let failed=false;
                localStorage.setItem=function(k,v){
                    if(k==='echo12-best-runs'&&!failed){failed=true;throw Error('storage full')}
                    return original.call(this,k,v)
                };
                try{window.__echo12Test.restore(data);return false}
                catch(e){return JSON.stringify(window.__echo12Store)===before&&
                  window.__echo12Test.save().progress.unlocked===0}
                finally{localStorage.setItem=original}
            }""",backup), 'Partial quota failures must be fully rolled back'
            page.evaluate("data=>window.__echo12Test.restore(data)",backup)
            verify(page,errors,'KAYIT')
            assert page.locator('#room').inner_text()=='05 / 19'
            assert page.locator('#case-board-count').inner_text()=='1/3'
            assert page.locator('#archive-count').inner_text()=='4/35'
            assert page.evaluate("JSON.parse(localStorage.getItem('echo12-room-clears'))")==[0,1,3]
            assert page.locator('#campaign-segments .campaign-cell.finished').count()==3
            page.locator('#room-select').click()
            assert page.locator('[data-room="2"]').get_attribute('data-cleared')=='false'
            assert page.locator('[data-room="3"]').get_attribute('data-cleared')=='true'
            page.keyboard.press('Escape')
            assert page.evaluate("localStorage.getItem('echo12-final-verdict')")=='review'
            assert page.evaluate("localStorage.getItem('echo12-muted')")=='1'
            assert page.evaluate("JSON.parse(localStorage.getItem('echo12-best-runs'))['0'].echoes")==2
            page.keyboard.press('b')
            assert page.locator('#vault-endings .vault-ending.earned').count()==1
            assert '3/19 TAMAMLANDI' in page.locator('#vault-progress').inner_text()
            assert 'Bağımsız incelemeye aktar' in page.locator('#vault-endings').inner_text()
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            assert not errors,errors
            page.close()
            print('PASS Build 019: offline backup, corrupt JSON rejection, save normalization and discovered finales')

            # Build 028: laboratory play/pause, adjustable rates and time markers
            # cannot advance the actual twelve-second gameplay clock.
            page, errors = load(browser, 0)
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            base=page.evaluate("window.__echo12Test.inspect()")
            hashes=page.evaluate("window.__echo12Test.echoIDs()")
            page.keyboard.press('i')
            verify(page,errors,'YANKI İNCELEME')
            assert page.locator('#inspector-marker-list .inspector-marker').count()>=1
            assert 'PLAKA A' in page.locator('#inspector-marker-list').inner_text()
            page.locator('#inspector-marker-list .inspector-marker').first.click()
            assert page.locator('#inspector-marker-list .inspector-marker').first.get_attribute('data-near')=='true'
            page.locator('#inspector-scrub').evaluate("e=>{e.value='0';e.dispatchEvent(new Event('input',{bubbles:true}))}")
            page.locator('#inspector-play').click()
            assert page.locator('#inspector-play').get_attribute('aria-pressed')=='true'
            page.evaluate("window.__echo12Test.advanceInspector(2)")
            state=page.evaluate("window.__echo12Test.inspect()")
            assert 1.9<=state['time']<=2.2,state
            assert state['elapsed']==base['elapsed'] and state['echoes']==base['echoes']
            assert page.evaluate("window.__echo12Test.echoIDs()")==hashes
            page.locator('#inspector-speed').select_option('2')
            page.evaluate("window.__echo12Test.advanceInspector(1)")
            assert 3.9<=page.evaluate("window.__echo12Test.inspect().time")<=4.45
            page.locator('#inspector-speed').select_option('0.5')
            page.evaluate("window.__echo12Test.advanceInspector(2)")
            assert 4.9<=page.evaluate("window.__echo12Test.inspect().time")<=5.5
            page.locator('#inspector-scrub').evaluate("e=>{e.value='11.8';e.dispatchEvent(new Event('input',{bubbles:true}))}")
            assert page.locator('#inspector-play').get_attribute('aria-pressed')=='false'
            page.locator('#inspector-play').click()
            page.evaluate("window.__echo12Test.advanceInspector(2)")
            assert page.evaluate("window.__echo12Test.inspect().time")==12
            assert page.locator('#inspector-play').get_attribute('aria-pressed')=='false'
            page.locator('#inspector-loop').click()
            assert page.locator('#inspector-loop').get_attribute('aria-pressed')=='true'
            page.locator('#inspector-play').click()
            page.evaluate("window.__echo12Test.advanceInspector(2)")
            assert .7<=page.evaluate("window.__echo12Test.inspect().time")<=1.1
            page.locator('#inspector-marker-list .inspector-marker').first.click()
            assert page.locator('#inspector-play').get_attribute('aria-pressed')=='false'
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            assert page.evaluate("window.__echo12Test.inspect().elapsed")==base['elapsed']
            assert page.evaluate("window.__echo12Test.echoIDs()")==hashes
            assert not errors,errors
            page.close()
            print('PASS Build 028: play/pause, speed, loop and event jump with frozen gameplay')

            # Ters kayıtların zaman işaretleri kaynak video saatine göre değil,
            # ters çevrilmiş oynatma saatine göre görünmeli.
            page, errors = load(browser, 9)
            page.keyboard.press('f')
            page.evaluate("window.__echo12Test.teleport(4.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.2)")
            page.evaluate("window.__echo12Test.teleport(2.5,5.5)")
            page.evaluate("window.__echo12Test.tick(.3)")
            commit(page)
            page.keyboard.press('i')
            assert page.locator('#inspector-marker-list .inspector-marker').count()>=1
            assert 'PLAKA V' in page.locator('#inspector-marker-list').inner_text()
            page.locator('#inspector-marker-list .inspector-marker').first.click()
            assert page.evaluate("window.__echo12Test.inspect().time")>11
            assert not errors,errors
            page.close()
            print('PASS Build 028: reverse playback time marker accuracy')

            # Build 021: echo inspector pauses physical simulation while allowing deterministic
            # seeking into any recorded ghost, including a selected reverse echo.
            page, errors = load(browser, 0)
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.12)")
            commit(page)
            page.evaluate("window.__echo12Test.tick(.24)")
            base=page.evaluate("window.__echo12Test.inspect()")
            assert base['echoes']==1
            page.keyboard.press('i')
            verify(page,errors,'YANKI İNCELEME')
            assert page.locator('#inspector').is_visible()
            assert page.locator('#inspector-echo option').count()==3
            assert '1 / 6 yankı' in page.locator('#inspector-count').inner_text()
            assert page.locator('#inspector-map').get_attribute('width')=='864'
            assert page.locator('#inspector-map').evaluate("(e)=>e.getContext('2d').getImageData(0,0,1,1).data[3]")==255
            page.locator('#inspector-echo').select_option('0')
            assert 'E01' in page.locator('#inspector-status').inner_text()
            page.locator('#inspector-forward').click()
            time1=page.evaluate("window.__echo12Test.inspect().time")
            assert time1>base['elapsed']
            page.locator('#inspector-scrub').evaluate("""e => {e.value='10.5';e.dispatchEvent(new Event('input',{bubbles:true}))}""")
            assert abs(page.evaluate("window.__echo12Test.inspect().time")-10.5)<.001
            assert '10,5 / 12,0 sn' in page.locator('#inspector-clock').inner_text()
            page.locator('#inspector-scrub').focus()
            page.keyboard.press('ArrowRight')
            assert page.evaluate("window.__echo12Test.inspect().time")>10.5,'Keyboard scrubber must receive arrow keys'
            page.evaluate("window.__echo12Test.tick(.7)")
            after=page.evaluate("window.__echo12Test.inspect()")
            assert {k:v for k,v in base.items() if k!='time'}=={k:v for k,v in after.items() if k!='time'},(base,after)
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            assert page.locator('#inspector').is_hidden()
            page.keyboard.press('p')
            verify(page,errors,'DURDU')
            page.keyboard.press('i')
            verify(page,errors,'YANKI İNCELEME')
            page.keyboard.press('Escape')
            verify(page,errors,'DURDU')
            page.keyboard.press('p')
            verify(page,errors,'KAYIT')
            assert not errors,errors
            page.close()

            page, errors = load(browser, 9)
            page.keyboard.press('f')
            page.evaluate("window.__echo12Test.tick(.3)")
            commit(page)
            page.keyboard.press('i')
            assert 'TERS' in page.locator('#inspector-echo option').all_inner_texts()[1]
            page.locator('#inspector-echo').select_option('0')
            assert 'TERS' in page.locator('#inspector-status').inner_text()
            assert not errors,errors
            page.close()
            print('PASS Build 021: modal pause, selectable and reversed echo paths, nonmutating 12s scrubbing and keyboard')

            # Build 022: high contrast and three-state motion modes are real persistent
            # accessibility settings. They must not change the 12-second physical timeline.
            page, errors = load(browser, 0)
            assert page.locator('.accessibility-settings').count()==1
            page.locator('.accessibility-settings summary').click()
            assert page.locator('#motion-toggle').inner_text()=='Hareket: Sistem'
            assert page.locator('#contrast-toggle').get_attribute('aria-pressed')=='false'
            page.locator('#motion-toggle').click()
            assert page.locator('#motion-toggle').inner_text()=='Hareket: Azaltılmış'
            assert page.locator('body').evaluate("(e)=>e.classList.contains('reduced-motion')")
            assert page.evaluate("localStorage.getItem('echo12-motion-setting')")=='on'
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.15)")
            assert page.evaluate("window.__echo12Test.gate('A')")
            assert page.evaluate("window.__echo12Test.fx().rings")==0,'Reduced motion must suppress rings'
            assert page.evaluate("window.__echo12Test.fx().wash")==0,'Reduced motion must suppress washes'
            active=page.evaluate("window.__echo12Test.inspect().elapsed")
            page.evaluate("window.__echo12Test.tick(.30)")
            later=page.evaluate("window.__echo12Test.inspect().elapsed")
            assert .25<later-active<.35, 'Accessibility must not alter simulation rate'
            page.locator('#contrast-toggle').click()
            assert page.locator('#contrast-toggle').get_attribute('aria-pressed')=='true'
            assert page.locator('body').evaluate("(e)=>e.classList.contains('high-contrast')")
            assert page.evaluate("localStorage.getItem('echo12-contrast-setting')")=='on'
            assert page.locator('#scene').evaluate("(e)=>getComputedStyle(e).filter")!='none'
            state=page.evaluate("window.__echo12Test.save()")
            assert state['progress']['motion']=='on' and state['progress']['contrast']=='on'
            assert page.evaluate("""data=>{const x=JSON.parse(JSON.stringify(data));x.progress.motion='blink';
                try{window.__echo12Test.validate(x);return false}catch(e){return true}}""",state)
            assert page.evaluate("""data=>{const x=JSON.parse(JSON.stringify(data));x.progress.contrast='unknown';
                try{window.__echo12Test.validate(x);return false}catch(e){return true}}""",state)
            page.locator('#motion-toggle').click()
            assert page.locator('#motion-toggle').inner_text()=='Hareket: Normal'
            assert not page.locator('body').evaluate("(e)=>e.classList.contains('reduced-motion')")
            page.locator('#motion-toggle').click()
            assert page.locator('#motion-toggle').inner_text()=='Hareket: Sistem'
            page.locator('#contrast-toggle').click()
            assert not page.locator('body').evaluate("(e)=>e.classList.contains('high-contrast')")
            page.evaluate("data=>window.__echo12Test.restore(data)",state)
            assert page.locator('body').evaluate("(e)=>e.classList.contains('high-contrast')")
            assert page.locator('body').evaluate("(e)=>e.classList.contains('reduced-motion')")
            assert page.evaluate("localStorage.getItem('echo12-motion-setting')")=='on'
            assert page.locator('#motion-toggle').get_attribute('aria-pressed')=='true'
            # Older backup files lack these optional preferences, remain supported.
            previous=page.evaluate("""data=>{const x=JSON.parse(JSON.stringify(data));
                delete x.progress.motion;delete x.progress.contrast;
                return window.__echo12Test.validate(x)}""",state)
            assert previous['motion']=='auto' and previous['contrast']=='off'
            assert not errors,errors
            page.close()
            print('PASS Build 022: contrast, reduced motion, system preference cycling and portable accessibility backup')

            # Build 023: all modal views keep keyboard Tab/Shift+Tab inside their
            # accessible dialogs, then restore focus to the caller when closed.
            page, errors=load(browser,0)
            def active_id():
                return page.evaluate("document.activeElement?.id || ''")
            page.locator('#inspector-button').click()
            verify(page,errors,'YANKI İNCELEME')
            assert active_id()=='inspector-close'
            page.keyboard.press('Shift+Tab')
            assert active_id()=='inspector-scrub'
            page.keyboard.press('Tab')
            assert active_id()=='inspector-close'
            page.keyboard.press('Escape')
            assert active_id()=='inspector-button'
            verify(page,errors,'KAYIT')

            page.locator('#save-vault-button').click()
            verify(page,errors,'KAYIT KASASI')
            assert active_id()=='vault-close'
            page.keyboard.press('Shift+Tab')
            assert active_id()=='vault-export'
            page.keyboard.press('Tab')
            assert active_id()=='vault-close'
            page.keyboard.press('Escape')
            assert active_id()=='save-vault-button'

            page.locator('#case-board-button').click()
            verify(page,errors,'DELİL PANOSU')
            assert active_id()=='case-close'
            page.keyboard.press('Tab')
            assert active_id()=='case-close'
            page.keyboard.press('Shift+Tab')
            assert active_id()=='case-close'
            page.keyboard.press('Escape')
            assert active_id()=='case-board-button'

            page.locator('#room-select').click()
            verify(page,errors,'ODA SEÇİMİ')
            assert active_id()=='room-picker-close'
            page.keyboard.press('Shift+Tab')
            assert page.evaluate("document.activeElement?.dataset.room")=='0'
            page.keyboard.press('Tab')
            assert active_id()=='room-picker-close'
            page.keyboard.press('Escape')
            assert active_id()=='room-select'

            page.locator('#logbook').click()
            verify(page,errors,'ARŞİV')
            assert active_id()=='archive-close'
            page.keyboard.press('Tab')
            assert active_id()=='archive-close'
            page.keyboard.press('Escape')
            assert active_id()=='logbook', 'Archive must return focus to origin'
            verify(page,errors,'KAYIT')
            assert not errors,errors
            page.close()

            page,errors=load(browser,5)
            page.evaluate("window.__echo12Test.teleport(14.5,2.5)")
            page.keyboard.press('e')
            verify(page,errors,'KARAR')
            assert page.evaluate("document.activeElement?.id")=='decision-cancel'
            page.keyboard.press('Shift+Tab')
            assert page.evaluate("document.activeElement?.id")=='decision-confirm'
            page.keyboard.press('Tab')
            assert page.evaluate("document.activeElement?.id")=='decision-cancel'
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            assert page.evaluate("document.activeElement?.id")=='interact'
            assert not errors,errors
            page.close()

            page,errors=load(browser,10)
            # Use the non-gameplay test hook for the audit dialog without
            # depending on map traversal, and verify its focus return.
            page.locator('#logbook').evaluate("(e)=>e.focus()")
            page.evaluate("window.__echo12Test.openAudit()")
            verify(page,errors,'KANIT')
            assert page.evaluate("document.activeElement?.id")=='audit-close'
            page.keyboard.press('Escape')
            verify(page,errors,'KAYIT')
            assert page.evaluate("document.activeElement?.id")=='logbook'
            assert not errors,errors
            page.close()
            print('PASS Build 023: focus stays within six modal dialogs and returns to opening controls')

            # Build 023: gate explanations follow live occupancy and actual proof state.
            page, errors = load(browser, 0)
            assert not page.locator('#sync-timeline').is_visible()
            panel=page.locator('#diagnostics')
            assert panel.count()==1
            panel.locator('summary').click()
            assert page.locator('#diagnostic-list .diagnostic-row').count()==1
            assert 'plakaya' in page.locator('#diagnostic-list').inner_text().lower()
            assert '1 kilitli' in page.locator('#diagnostic-count').inner_text()
            page.evaluate("window.__echo12Test.teleport(6.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.08)")
            assert page.evaluate("window.__echo12Test.gate('A')")
            assert page.locator('#diagnostic-list .diagnostic-row').first.get_attribute('data-open')=='true'
            assert '0 kilitli' in page.locator('#diagnostic-count').inner_text()
            assert not errors,errors
            page.close()

            page, errors = load(browser, 12)
            assert page.locator('#diagnostic-list .diagnostic-row').count()==3
            assert page.locator('#diagnostic-list .diagnostic-row').count()==3
            page.keyboard.press('f')
            assert page.locator('#diagnostic-list .diagnostic-row').count()==3
            assert not errors,errors
            page.close()

            page, errors = load(browser, 15)
            page.keyboard.press('f')
            assert page.locator('#diagnostic-list .diagnostic-row').count()==2
            page.evaluate("window.__echo12Test.teleport(9.5,3.5)")
            page.evaluate("window.__echo12Test.tick(.1)")
            commit(page)
            page.evaluate("window.__echo12Test.tick(.1)")
            assert page.locator('#diagnostic-list .diagnostic-row').count()==2
            assert not errors,errors
            page.close()
            print('PASS Build 023: live gate diagnostics and evidence-dependent next-step suggestions')

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
