import unittest
import os
import sys
from playwright.sync_api import sync_playwright
from recordwright import install as install_recorder

HEADLESS = os.environ.get("HEADLESS", "false") == "true"


class TestMVSC(unittest.TestCase):
    def test_msvc(self):
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc")

        page.get_by_placeholder("What needs to be done?").wait_for()

        recorder = install_recorder(page, output=open(os.devnull,"w")
                                    if HEADLESS else sys.stderr)

        recorder.interaction("todo", """
        - Click "What needs to be done"
        - Type "Test RecordWright"
        - Press Enter
        """)

        lis = page.get_by_test_id("todo-item")
        item = lis.first
        self.assertEqual(item.inner_text(), "Test RecordWright")

        browser.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        unittest.main()


