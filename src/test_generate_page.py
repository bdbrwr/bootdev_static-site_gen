import unittest
from generate_page import *

class generate_page(unittest.TestCase):
    def test_title_no_header(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        with self.assertRaises(Exception):
            title = extract_title(md)


    def test_title_multiple_h1(self):
        md = """
# Proper Title

Paragrpah

# Another Heading 1
"""
        title = extract_title(md)
        self.assertEqual(title, "Proper Title")



if __name__ == "__main__":
    unittest.main()
