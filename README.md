# Archimate Tools
A collection of scripts that help working with files in the ArchiMate Model Exchange File Format. This is a tool and vendor agnostic file format to exchange Archimate models using XML files. More information on the ArchiMate Model Exchange File Format can be found at: https://www.opengroup.org/open-group-archimate-model-exchange-file-format. When I refer below to a model, I mean a model in the ArchiMate Model Exchange File Format.

More information on Archimate itself can be found at: https://pubs.opengroup.org/architecture/archimate3-doc/.

## archimate-export
archimate-export is a small command line application that allows to export all the Archimate elements from a model into an Excel file.

Example:
```shell
python archimate-export.py --output output.xlsx input_model.xml
```