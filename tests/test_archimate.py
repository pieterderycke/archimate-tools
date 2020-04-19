import unittest   # The test framework

from archimatetools import ArchimateModel

class TestArchimateModel001(unittest.TestCase):
    def test_loadModel(self):
        model = ArchimateModel("tests/models/ATAM.xml")
        self.assertEqual(len(model.readElements()), 30)
        self.assertEqual(len(model.readRelationships()), 39)

    def test_loadProperties(self):
        model = ArchimateModel("tests/models/model001.xml")

        element = next(filter(lambda x: x.name == "API", model.readElements()))
        self.assertEqual(element.properties["api-name"], "test-api")

if __name__ == '__main__':
    unittest.main()