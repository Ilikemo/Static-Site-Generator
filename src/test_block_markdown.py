from block_markdown import *
import unittest

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_no_empty_lines(self):
        md = "This is a paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph"])

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. First item\n2. Second item"), BlockType.ORDERED_LIST)

    def test_block_to_block_type_empty(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_mixed(self):
        md = """
# Heading

This is a paragraph

```python
print('Hello')
```

> This is a quote

- Item 1
- Item 2

1. First item
2. Second item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.CODE)
        self.assertEqual(block_to_block_type(blocks[3]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks[4]), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks[5]), BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()