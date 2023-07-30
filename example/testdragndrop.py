import unittest
import os
import sys
from playwright.sync_api import sync_playwright
from recordwright import install as install_recorder

HEADLESS = os.environ.get("HEADLESS", "true") == "true"


class TestDragDrop(unittest.TestCase):
    def test_dragndrop(self):
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto("https://bestvpn.org/html5demos/drag/")
        recorder = install_recorder(page, output=open(os.devnull,"w")
                                    if HEADLESS else sys.stderr)

        lis = page.locator("#wrapper ul li")
        li = lis.first

        self.assertTrue(li.inner_html())

        recorder.interaction("drag", """
        - Drag "Best VPN" into Frame
        """)

        lis = page.locator("#wrapper ul li")
        li = lis.first
        
        self.assertFalse(li.inner_html())

        browser.close()



if __name__ == "__main__":
    with sync_playwright() as p:
        unittest.main()


