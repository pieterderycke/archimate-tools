import archimate
from argparse import ArgumentParser
import xlsxwriter
import os

parser = ArgumentParser(description="archimate-export is a tool that allows to export files in the ArchiMate Model Exchange File Format.")
parser.add_argument('archimateFile', metavar="file", help="The file in  ArchiMate Model Exchange File Format to be used as input.")
parser.add_argument("--output", "-o", help="The output file to use for the expert.", required=True)
args = parser.parse_args()

if(not os.path.isfile(args.archimateFile)):
    print('The file \"%s\" does not exist.' % args.archimateFile)
    exit(1)

model = archimate.ArchimateModel(args.archimateFile)

elements = model.readElements()
relationships = model.readRelationships()

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