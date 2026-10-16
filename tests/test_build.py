import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from build import md_to_html


class BuildTests(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(md_to_html("# A\n## B"), "<h1>A</h1>\n<h2>B</h2>")

    def test_html_is_escaped(self):
        self.assertNotIn("<script>", md_to_html("hello <script>alert(1)</script>"))

    def test_list(self):
        self.assertEqual(md_to_html("- a\n- b"), "<ul><li>a</li><li>b</li></ul>")

    def test_code_block_is_escaped(self):
        self.assertIn("&lt;b&gt;", md_to_html("```\n<b>\n```"))


if __name__ == "__main__":
    unittest.main()
