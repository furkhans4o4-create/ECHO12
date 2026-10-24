"""Build 051: real-network Chromium offline PWA regression."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import os
import shutil
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

def main():
    handler=partial(QuietHandler,directory=str(ROOT))
    server=ThreadingHTTPServer(("127.0.0.1",0),handler)
    thread=Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        with sync_playwright() as p:
            exe=os.getenv("ECHO12_CHROMIUM") or shutil.which("chromium")
            kwargs={"executable_path":exe,"args":["--no-sandbox"]} if exe else {}
            browser=p.chromium.launch(headless=True,**kwargs)
            context=browser.new_context()
            errors=[]
            page=context.new_page()
            page.on("pageerror",lambda e:errors.append(str(e)))
            url=f"http://127.0.0.1:{server.server_port}/"
            try:
                page.goto(url,wait_until="load")
                assert page.locator("#mode").inner_text()=="HAZIR"
                assert page.locator('link[rel="manifest"]').get_attribute("href")=="./manifest.webmanifest"
                page.wait_for_function("navigator.serviceWorker.controller !== null",timeout=20000)
                page.wait_for_function("""async () => {
                    const cache=await caches.open('echo12-shell-build-051');
                    const entries=await cache.keys();
                    return entries.length>=4;
                }""",timeout=20000)
                assert "ÇEVRİMDIŞI HAZIR" in page.locator("#offline-state").inner_text()
                page.locator("#start").click()
                assert page.locator("#mode").inner_text()=="KAYIT"
                page.keyboard.press("Space")
                assert page.locator("#clones").inner_text()=="1 / 6"
                assert page.evaluate("localStorage.getItem('echo12-active-room-v1')") is not None
                saved=page.evaluate("localStorage.getItem('echo12-active-room-v1')")
                context.set_offline(True)
                page.reload(wait_until="load")
                assert "ÇEVRİMDIŞI" in page.locator("#offline-state").inner_text()
                assert page.locator("#room-resume").is_visible()
                assert page.locator("#mode").inner_text()=="HAZIR"
                assert page.evaluate("localStorage.getItem('echo12-active-room-v1')")==saved
                page.locator("#start").click()
                assert page.locator("#mode").inner_text()=="KAYIT"
                assert page.locator("#clones").inner_text()=="1 / 6"
                assert not errors,errors
                print("PASS Build 051: full game loads offline, committed echo and save survive reload")
                page.keyboard.press("x")
                assert page.locator("#clones").inner_text()=="1 / 6"
                context.set_offline(False)
                page.reload(wait_until="load")
                assert page.locator("#mode").inner_text()=="HAZIR"
                assert not errors,errors
                print("PASS Build 051: restored connectivity and versioned shell maintain same progress")
            finally:
                context.close()
                browser.close()
    finally:
        server.shutdown()
        server.server_close()

if __name__=="__main__":
    main()
