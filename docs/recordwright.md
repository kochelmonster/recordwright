# Why UI Tests Are So Brittle – And How a Small Library Makes UI Testing Robust and Maintainable

A Google search for "why are UI tests so brittle" reveals a bunch of problems with UI testing. In summary:

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

Traditional solutions like page objects, stable selectors, reduced test coverage, and regular maintenance help, but do not solve the core problem: UI tests must be manually updated whenever the UI changes.

---

## A Different Approach: Recordwright

The open-source library **Recordwright** takes a fundamentally different approach:

- **Record Instead of Script:**  
  Interactions are recorded directly in the browser and saved as JSON. The first run records the interaction; subsequent runs replay it automatically.
- **Effortless Updates:**  
  If the UI changes and a test fails, simply re-record the interaction—no need to update selectors or test code.
- **Minimal Test Code:**  
  Test logic remains concise, as interactions are stored as recordings.
- **Complex Interactions Supported:**  
  Even challenging actions like drag-and-drop are reliably captured and replayed.
- **Seamless Playwright Integration:**  
  Recordwright plugs directly into Playwright tests with a simple API:

```python
recorder = install_recorder(page)
recorder.interaction("my_test", "Description of the interaction")
```

If the UI changes, just re-record—no refactoring required.

Unlike Selenium, Recordwright can record all user interactions, including drag and drop operations, and it replays them with the same timing as the original recording.

---

## Example: A Simple UI Test with Recordwright

Here is a simple example of a UI test using Recordwright:

```python
# testmvc.py
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

---

## Step-by-Step: Recording and Playback

1. **Start the test:**

   ```bash
   python testmsvc.py
   ```

2. **Record the interaction:**

   Follow the instructions in the terminal:

   ```
   record interaction todo.json

           - Click "What needs to be done"
           - Type "Test RecordWright"
           - Press Enter

   stop with ctrl+shift+f11
   ```

   Click the input field in the browser, type the text, confirm with Enter, and finish recording with **ctrl+shift+f11**.

   ![Browser](https://github.com/kochelmonster/recordwright/blob/main/docs/browser.png?raw=true)

3. **Playback:**  
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

---

## How Does Recordwright Work?

- On the first test run, the interaction is recorded in the browser and saved as JSON.
- On the next run, Recordwright detects the existing recording and replays it automatically.
- If the UI changes, simply rerun the test and re-record the interaction.

---

## Troubleshooting & Tips

- **Playback errors:**  
  If playback fails (for example, because the UI has changed significantly), simply re-record the interaction.
- **Complex interactions:**  
  Drag-and-drop or multi-selections are also supported.
- **Headless mode:**  
  In headless mode, only playback is performed; no recording is started.

---

## Recordwright vs. Traditional Solutions

**Problem:**  
- UI Changes  
  - Traditional: Update selectors/test code  
  - Recordwright: Re-record the interaction

- Maintenance Overhead  
  - Traditional: High, many places affected  
  - Recordwright: Very low, just re-record

- Learning Curve  
  - Traditional: High, requires abstraction and code  
  - Recordwright: Low, intuitive recording

- Complex Interactions  
  - Traditional: Hard to script  
  - Recordwright: Easy to record

- Test Robustness  
  - Traditional: Improved, but never perfect  
  - Recordwright: High, as long as the interaction is the same

---

## Conclusion

The brittleness of UI tests is a well-known pain point, rooted in their tight coupling to the ever-changing UI structure. Traditional solutions like Page Objects and stable selectors help, but require ongoing maintenance and technical expertise.

**Recordwright** offers a pragmatic, recording-based approach: simply re-record interactions when the UI changes. This makes UI testing faster, more robust, and dramatically reduces maintenance effort.

---

## Further Resources

- [Recordwright on GitHub](https://github.com/kochelmonster/Recordwright)
- [Playwright Documentation](https://playwright.dev/python/)
