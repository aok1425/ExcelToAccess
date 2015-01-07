# Validation Check
This program takes in Excel files from Rima (as of December 2014), and turns them into an Access file to upload to E2Boston.

## Usage
I wrote this program to be compiled into an EXE using Py2EXE. (Thus the `setup.py` file.) The EXE and its folder would be placed into a folder containing the DOR and COD Excel files, and `validation_check.exe` would search the folder above it for the Excel files. It would then output a log file and the Access file.

Instructional YouTube videos are [here](https://www.youtube.com/playlist?list=PLfx7-sTu8YindPPz65f9MC732YQJjlWJe).

## To run locally
I `cd`'ed into a sub-directory of the directory with the Excel files, and ran `python ../validation_check.py`. You need to change a line in the script so that it looks for the Access template locally

## Testing
This requires Excel files to be in the `/tests` folder. Run `nosetests` at the parent directory. Tests only cover the validations themselves, not the rest of the script.