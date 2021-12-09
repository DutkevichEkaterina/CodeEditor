import unittest

from src.main.python.editor.TagRegistry import TagRegistry


class TagRegistryTest(unittest.TestCase):
    def setUp(self):
        dict = {
            "keyword": {"color": "yellow"},
            "function.method": {"color": "blue"},
            "function": {"color": "red", "underline": 1},
        }
        self.registry = TagRegistry(dict)

    def testFindTagByName(self):
        self.assertEqual(self.registry.findTagByName("keyword"), "yellow", "Unexpected result for 'keyword'")
        self.assertEqual(self.registry.findTagByName("function"), "red", "Unexpected result for 'function'")
        self.assertEqual(self.registry.findTagByName("function.foo"), "red", "Unexpected result for 'function.foo'")
        self.assertEqual(self.registry.findTagByName("function.foo.blah"), "red", "Unexpected result for 'function.foo.blah'")
        self.assertEqual(self.registry.findTagByName("function.method"), "blue", "Unexpected result for 'function.method'")
        self.assertEqual(self.registry.findTagByName("function.method.foo"), "blue", "Unexpected result for 'function.method.foo'")
        self.assertEqual(self.registry.findTagByName("function.method.foo.blah"), "blue", "Unexpected result for 'function.method.foo.blah'")

    def testFindTagByNameNotFound(self):
        self.assertIsNone(self.registry.findTagByName(""), "Unexpected result for empty string")
        self.assertIsNone(self.registry.findTagByName("abcd"), "Unexpected result for 'abcd'")
        self.assertIsNone(self.registry.findTagByName("abcd.blah"), "Unexpected result for 'abcd.blah'")
