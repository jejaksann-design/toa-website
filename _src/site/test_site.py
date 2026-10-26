import http.server, threading, functools, os, base64
from playwright.sync_api import sync_playwright
ROOT = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/site/toa-website'
OUT = '/tmp/claude-0/-home-claude/0e4dbd05-0425-5a72-883f-583c558b89ff/scratchpad/site/'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def log_request(self, code='-', size='-'):
        if str(code) not in ('200', '304'): print('HTTP', code, self.path)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8799), functools.partial(H, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = 'http://127.0.0.1:8799'
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 900}, accept_downloads=True)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: m.type == 'error' and errs.append('console: ' + m.text))
    # landing
    pg.goto(B + '/', wait_until='domcontentloaded')
    pg.wait_for_function("document.querySelector('#lb-per-sel option')", timeout=20000)
    print('title:', pg.title(), '| logo ok:', pg.evaluate("document.querySelector('img.toa-logo').naturalWidth>0"))
    print('ebook covers loaded:', pg.evaluate("[...document.querySelectorAll('.eb img')].filter(i=>i.complete&&i.naturalWidth>0).length"), '/ 5')
    print('prestasi:', pg.inner_text('#lb-count'))
    # syahadah download
    pg.click('.lb-pod.r1'); pg.click('#lb-certbtn')
    pg.wait_for_selector('#lb-cdl:not([hidden])', timeout=20000)
    with pg.expect_download(timeout=15000) as dl:
        pg.click('#lb-cdl')
    d = dl.value; print('syahadah download:', d.suggested_filename, '| msg:', pg.inner_text('#lb-cmsg'))
    pg.click('#lb-cclose')
    print('landing scrollWidth', pg.evaluate('document.documentElement.scrollWidth'))
    # navigate to kuis via landing link
    pg.click('#kuis a.btn')
    pg.wait_for_url('**/kuis/**', timeout=10000)
    print('kuis url:', pg.url, '| title:', pg.title())
    print('kuis logo ok:', pg.evaluate("document.querySelector('img.toa-logo').naturalWidth>0"))
    # Ayat Hari Ini loads quran.json
    pg.click('#daily-card'); pg.wait_for_selector('#d-area .opt', timeout=20000)
    print('ayat hari ini:', pg.inner_text('#d-title'), '| options', pg.locator('#d-area .opt').count())
    pg.goto(B + '/kuis/#tes', wait_until='domcontentloaded'); pg.wait_for_timeout(500)
    print('tes deep link visible:', pg.is_visible('#s-tes'))
    # result CTA links back to landing
    hrefs = pg.evaluate("[...document.querySelectorAll('a')].map(a=>a.getAttribute('href')).filter(h=>h&&h.startsWith('/'))")
    print('internal links in kuis:', sorted(set(hrefs)))
    pg.screenshot(path=OUT + 'kuis-hosted.png')
    print('kuis scrollWidth', pg.evaluate('document.documentElement.scrollWidth'))
    print('errors:', errs)
    b.close()
srv.shutdown()
