# Why UI Tests Are So Brittle – And How A Small Library Makes UI Testing Robust and Maintainable

A Google search for "why are UI tests so brittle" reveals a bunch of problems of ui-testing, in summary it is:

- **Tight Coupling to UI Structure:**  
  UI tests often rely on selectors, IDs, or visible text that change frequently as the UI evolves.
- **Frequent UI Changes:**  
  Even minor UI tweaks (renaming a button, moving elements) can break many tests.
- **Unstable Selectors:**  
  Dynamically generated or poorly chosen selectors make tests fragile.
- **High Maintenance Overhead:**  
  Every UI change can require updates to numerous test cases.
- **Flaky Tests:**  
  Tests may fail intermittently due to timing issues, animations, or asynchronous behavior.

**Traditional solutions** like page objects, stable selectors, reduced test coverage, and regular maintenance help, but do not solve the core problem: UI tests must be manually updated whenever the UI changes.

The open-source library **RecordWright** takes a fundamentally different approach:

- **Record Instead of Script:**  
  Interactions are recorded directly in the browser and saved as JSON. The first run records the interaction; subsequent runs replay it automatically.
- **Effortless Updates:**  
  If the UI changes and a test fails, simply re-record the interaction—no need to update selectors or test code.
- **Minimal Test Code:**  
  Test logic remains concise, as interactions are stored as recordings.
- **Complex Interactions Supported:**  
  Even challenging actions like drag-and-drop are reliably captured and replayed.
- **Seamless Playwright Integration:**  
  RecordWright plugs directly into Playwright tests with a simple API:

  ```python
  recorder = install_recorder(page)
  recorder.interaction("my_test", "Description of the interaction")
  ```

  If the UI changes, just re-record—no refactoring required.

Unlike Selenium, RecordWright can record all user interactions including drag and drop operations and it replays in the same timing as the recording was done.

## An Example

Here is a simple example of a UI test with RecordWright:

```python
# testmvc.py
import unittest
import os
import sys
from playwright.sync_api import sync_playwright
from RecordWright import install as install_recorder

HEADLESS = os.environ.get("HEADLESS", "false") == "true"

class TestMVSC(unittest.TestCase):
    def test_msvc(self):
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc")

        page.get_by_placeholder("What needs to be done?").wait_for()
        recorder = install_recorder(page, output=open(os.devnull, "w")
                                    if HEADLESS else sys.stderr)

        recorder.interaction("todo", """
        - Click "What needs to be done"
        - Type "Test RecordWright"
        - Press Enter
        """)

        lis = page.get_by_test_id("todo-item")
        self.assertEqual(lis.first.inner_text(), "Test RecordWright")
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        unittest.main()
```

Step-by-Step: Recording and Playback

Start the script in the terminal:

1. **Start the test:**

```bash
python testmsvc.py
```

2. **Record the interaction:**

Follow the instructions in the terminal:

```console
record interaction todo.json

        - Click "What needs to be done"
        - Type "Test RecordWright"
        - Press Enter
        
stop with ctrl+shift+f11
```

Click the input field in the browser, type the text, confirm with Enter, and finish recording with *ctrl+shift+f11*.

![Browser](https://github.com/kochelmonster/recordwright/blob/main/docs/browser.png?raw=true)

1. **Playback:**  
On the next run, the interaction is automatically replayed:

```bash
python testmsvc.py
play todo.json
done
.
----------------------------------------------------------------------
Ran 1 test in 10.817s

OK
```

The file `todo.json` contains the recording and is used during the test run.

## How Does RecordWright Work?

- On the first test run, the interaction is recorded in the browser and saved as JSON.
- On the next run, RecordWright detects the existing recording and replays it automatically.
- UI changed? Simply rerun the test and re-record the interaction.

## Troubleshooting & Tips

- **Playback errors:**  
  If playback fails (e.g., because the UI has changed significantly), simply re-record the interaction.
- **Complex interactions:**  
  Drag-and-drop or multi-selections are also supported.
- **Headless mode:**  
  In headless mode, no recording is started, only playback.

### RecordWright vs. Traditional Solutions

| Problem                | Traditional Solutions (Page Objects, Stable Selectors) | RecordWright                        |
|------------------------|--------------------------------------------------------|-------------------------------------|
| UI Changes             | Update selectors/test code                             | Re-record the interaction           |
| Maintenance Overhead   | High, many places affected                             | Very low, just re-record            |
| Learning Curve         | High, requires abstraction and code                    | Low, intuitive recording            |
| Complex Interactions   | Hard to script                                         | Easy to record                      |
| Test Robustness        | Improved, but never perfect                            | High, as long as the interaction is the same |

---

## Conclusion

The brittleness of UI tests is a well-known pain point, rooted in their tight coupling to the ever-changing UI structure. Traditional solutions like Page Objects and stable selectors help, but require ongoing maintenance and technical expertise.

**RecordWright** offers a pragmatic, recording-based approach: simply re-record interactions when the UI changes. This makes UI testing faster, more robust, and dramatically reduces maintenance effort.

## Further Resources

- [RecordWright on GitHub](https://github.com/kochelmonster/RecordWright)
- [Playwright Documentation](https://playwright.dev/python/)
