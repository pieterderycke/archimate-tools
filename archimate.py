# http://www.opengroup.org/xsd/archimate/

import xml.etree.ElementTree as ET

def getArchimateLayer(archimateConcept):
    switcher = {
        # ArchiMate Strategy Layer Element Types
        "Resource" : "Strategy",
        "Capability" : "Strategy",
        "ValueStream" : "Strategy",
        "CourseOfAction" : "Strategy",

        # ArchiMate Business Layer Element Types
        "BusinessActor" : "Business",
        "BusinessRole" : "Business",
        "BusinessCollaboration" : "Business",
        "BusinessInterface" : "Business",
        "BusinessProcess" : "Business",
        "BusinessFunction" : "Business",
        "BusinessInteraction" : "Business",
        "BusinessEvent" : "Business",
        "BusinessService" : "Business",
        "BusinessObject" : "Business",
        "Contract" : "Business",
        "Representation" : "Business",
        "Product" : "Business",

        # ArchiMate Application Layer ElementTypes
        "ApplicationComponent" : "Application",
        "ApplicationCollaboration" : "Application",
        "ApplicationInterface" : "Application",
        "ApplicationFunction" : "Application",
        "ApplicationInteraction" : "Application",
        "ApplicationProcess" : "Application",
        "ApplicationEvent" : "Application",
        "ApplicationService" : "Application",
        "DataObject" : "Application",

        # ArchiMate Technology Layer ElementTypes
        "Node" : "Technology",
        "Device" : "Technology",
        "SystemSoftware" : "Technology",
        "TechnologyCollaboration" : "Technology",
        "TechnologyInterface" : "Technology",
        "Path" : "Technology",
        "CommunicationNetwork" : "Technology",
        "TechnologyFunction" : "Technology",
        "TechnologyProcess" : "Technology",
        "TechnologyInteraction" : "Technology",
        "TechnologyEvent" : "Technology",
        "TechnologyService" : "Technology",
        "Artifact" : "Technology",

        # ArchiMate Physical Layer ElementTypes
        "Equipment" : "Physical",
        "Facility" : "Physical",
        "DistributionNetwork" : "Physical",
        "Material" : "Physical",

        # ArchiMate Motivation ElementTypes
        "Stakeholder" : "Motivation",
        "Driver" : "Motivation",
        "Assessment" : "Motivation",
        "Goal" : "Motivation",
        "Outcome" : "Motivation",
        "Principle" : "Motivation",
        "Requirement" : "Motivation",
        "Constraint" : "Motivation",
        "Value" : "Motivation",
    }
    return switcher.get(archimateConcept, "Invalid Archimate Concept")

def getArchimateAspect(archimateElement):
    switcher = {
        # Strategy Layer: Structure Elements
        "Resource" : "Structure",

        # Strategy Layer: Behavior Elements
        "Capability" : "Behavior",
        "ValueStream" : "Behavior",
        "CourseOfAction" : "Behavior",
        
        # Business Layer: Active Structure Elements
        "BusinessActor" : "Active Structure",
        "BusinessRole" : "Active Structure",
        "BusinessCollaboration" : "Active Structure",
        "BusinessInterface" : "Active Structure",

        # Business Layer: Behavior Elements
        "BusinessProcess" : "Behavior",
        "BusinessFunction" : "Behavior",
        "BusinessInteraction" : "Behavior",
        "BusinessEvent" : "Behavior",
        "BusinessService" : "Behavior",

        # Business Layer: Passive Structure Elements
        "BusinessObject" : "Passive Structure",
        "Contract" : "Passive Structure",
        "Representation" : "Passive Structure",

        # Business Layer: Composite Elements
        "Product" : "Composite",

        # Application Layer: Active Structure Elements
        "ApplicationComponent" : "Active Structure",
        "ApplicationCollaboration" : "Active Structure",
        "ApplicationInterface" : "Active Structure",

        # Application Layer: Behavior Elements
        "ApplicationFunction" : "Behavior",
        "ApplicationInteraction" : "Behavior",
        "ApplicationProcess" : "Behavior",
        "ApplicationEvent" : "Behavior",
        "ApplicationService" : "Behavior",

        # Application Layer: Passive Structure Elements
        "DataObject" : "Passive Structure",

        # Technology Layer: Active Structure Elements
        "Node" : "Active Structure",
        "Device" : "Active Structure",
        "SystemSoftware" : "Active Structure",
        "TechnologyCollaboration" : "Active Structure",
        "TechnologyInterface" : "Active Structure",
        "Path" : "Active Structure",
        "CommunicationNetwork" : "Active Structure",

        # Technology Layer: Behavior Elements
        "TechnologyFunction" : "Behavior",
        "TechnologyProcess" : "Behavior",
        "TechnologyInteraction" : "Behavior",
        "TechnologyEvent" : "Behavior",
        "TechnologyService" : "Behavior",

        # Technology Layer: Passive Structure Elements
        "Artifact" : "Passive Structure",

        # Physical Layer: Active Structure Elements
        "Equipment" : "Active Structure",
        "Facility" : "Active Structure",
        "DistributionNetwork" : "Active Structure",

        # Technology Layer: Passive Structure Elements
        "Material" : "Passive Structure",
    }
    return switcher.get(archimateElement, "Invalid Archimate Element")

class Element:
    def __init__(self, identifier, name, elementType):
        self.identifier = identifier
        self.name = name
        self.elementType = elementType

    @property
    def layer(self):
        return getArchimateLayer(self.elementType)

    @property
    def aspect(self):
        return getArchimateAspect(self.elementType)

class Relationship:
    def __init__(self, identifier, source, target, relationshipType):
        self.identifier = identifier
        self.source = source
        self.target = target
        self.relationshipType = relationshipType


ns = {'archimate': 'http://www.opengroup.org/xsd/archimate/3.0/',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

class ArchimateModel:
    def __init__(self, filePath):
        tree = ET.parse(filePath)
        self._xmlRoot = tree.getroot()

    def readElements(self):
        elements = self._xmlRoot.find('archimate:elements', ns)

        items = []
        for element in elements.findall('archimate:element', ns):
            identifier = element.get("identifier")
            elementType = element.attrib['{%s}type' % ns['xsi']] # The Python XML API is more cumbersome for attributes part of namespaces
            name = element.find("archimate:name[@{http://www.w3.org/XML/1998/namespace}lang='en']", ns).text

            items.append(Element(identifier, name, elementType))

        return items
    
    def readRelationships(self):
        elements = self._xmlRoot.find('archimate:relationships', ns)

        items = []
        for element in elements.findall('archimate:relationship', ns):
            identifier = element.get("identifier")
            source = element.get("source")
            target = element.get("target")
            relationshipType = element.attrib['{%s}type' % ns['xsi']] # The Python XML API is more cumbersome for attributes part of namespaces

            items.append(Relationship(identifier, source, target, relationshipType))

        return items