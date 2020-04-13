import os
from argparse import ArgumentParser

import xlsxwriter
from rdflib import Graph, Literal, BNode, RDF, URIRef, Namespace
from rdflib.namespace import DC, FOAF

import archimate

parser = ArgumentParser(description="archimate-export is a tool that allows to export files in the ArchiMate Model Exchange File Format to a number of other file formats.")
parser.add_argument('archimateFile', metavar="file", help="The file in  ArchiMate Model Exchange File Format to be used as input.")
parser.add_argument("--output", "-o", help="The output file to use for the expert.", required=True)
parser.add_argument("--format", "-f", choices=['xlsx', 'rdf', 'turtle'], default='xlsx', help="The requested output file format.", required=False)
args = parser.parse_args()

if(not os.path.isfile(args.archimateFile)):
    print('The file \"%s\" does not exist.' % args.archimateFile)
    exit(1)

model = archimate.ArchimateModel(args.archimateFile)

elements = model.readElements()
relationships = model.readRelationships()

if(args.format == "xlxs"):
    workbook = xlsxwriter.Workbook(args.output)
    header = workbook.add_format({'bold': True})

    worksheet = workbook.add_worksheet('Export')

    worksheet.write(0, 0, "ID", header)
    worksheet.write(0, 1, "Name", header)
    worksheet.write(0, 2, "Element Type", header)
    worksheet.write(0, 3, "Layer", header)
    worksheet.write(0, 4, "Aspect", header)

    for index, element in enumerate(elements) :
        worksheet.write(index + 1, 0, element.identifier)
        worksheet.write(index + 1, 1, element.name)
        worksheet.write(index + 1, 2, element.elementType)
        worksheet.write(index + 1, 3, element.layer)
        worksheet.write(index + 1, 4, element.aspect)

    workbook.close()

    print('%s elements export to \"%s\"' % (len(elements), args.output))
elif(args.format == "rdf" or args.format == 'turtle'):
    graph = Graph()

    ARCHIMATE = Namespace('http://www.opengroup.org/xsd/archimate/3.0/')

    mapping = {}
    for element in elements:
        node = BNode()
        mapping[element.identifier] = node

        graph.add((node, RDF.type, ARCHIMATE[element.elementType]))
        graph.add((node, ARCHIMATE.identifier, Literal(element.identifier)))
        graph.add((node, ARCHIMATE.name, Literal(element.name)))

    for relationship in relationships:
        node = BNode()

        graph.add((node, RDF.type, ARCHIMATE[relationship.relationshipType]))
        graph.add((node, ARCHIMATE.source, mapping[relationship.source]))
        graph.add((node, ARCHIMATE.target, mapping[relationship.target]))

    graph.bind("archimate", ARCHIMATE)

    graphformat = {'rdf': 'xml', 'turtle': 'turtle'}

    graph.serialize(args.output, format=graphformat[args.format])

    print("Archimate model exported in RDF/XML format.")