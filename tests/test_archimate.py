import unittest   # The test framework

from archimatetools import ArchimateModel

class TestArchimateModel001(unittest.TestCase):
    def test_loadModel(self):
        model = ArchimateModel("tests/models/ATAM.xml")
        self.assertEqual(len(model.readElements()), 30)
        self.assertEqual(len(model.readRelationships()), 39)

if __name__ == '__main__':
    unittest.main()