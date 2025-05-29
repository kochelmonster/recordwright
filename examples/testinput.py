import unittest
import os
import sys
from playwright.sync_api import sync_playwright
from recordwright import install as install_recorder

HEADLESS = os.environ.get("HEADLESS", "false") == "true"


class TestInput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = p.chromium.launch(headless=HEADLESS)
        cls.page = cls.browser.new_page()
        cls.page.goto("https://pauljadam.com/demos/html5-input-types.html")

        inputs = cls.page.locator("input")
        inputs.first ## wait
        cls.recorder = install_recorder(cls.page, output=open(os.devnull,"w")
                                        if HEADLESS else sys.stderr)

        cls.inputs = {}
        for i in inputs.all():
            cls.inputs[i.get_attribute("type")] = i

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()

    def test_default(self):
        self.assertEqual(self.inputs[None].input_value(), "")
        self.recorder.interaction("input-default", """
        - Click the Default Field
        - Write "default" in the Default field
        """)
        self.assertEqual(self.inputs[None].input_value(), "default")

    def test_datetime(self):
        dt = self.inputs["datetime-local"]
        self.assertEqual(dt.input_value(), "")
        self.recorder.interaction("input-datetime", """
        - Click the Datetime-local Field
        - Choose 2020-11-13 10:20 with the mouse
        """)
        self.assertEqual(dt.input_value(), "2020-11-13T11:20")
      
    def test_range(self):
        tmp = self.inputs["range"]
        self.assertEqual(tmp.input_value(), "50")
        self.recorder.interaction("input-range", """
        - Click the range Field
        - Move the slider to the right end.
        """)
        self.assertEqual(tmp.input_value(), "100")


if __name__ == "__main__":
    with sync_playwright() as p:
        unittest.main()


