# Validation Check
This program takes in Excel files from Rima (as of February 2015), and turns them into an Access file to upload to E2Boston.

## Usage
I wrote this program to be compiled into an EXE using Py2EXE. (Thus the `setup.py` file.) Run the EXE, choose the input Excel files, and the program will output an Access file. This program fixes some common errors in the Excel files, like missing SSN or mom's first name. It also outputs a log file if any errors arise.

Instructional videos for end-users are here:
- [how to use](https://www.dropbox.com/s/fdl8e766whmfcsq/validation%20check%20-%20how%20to%20use.flv?dl=0)
- [what errors mean](https://www.dropbox.com/s/g2f8zt5egj9cg58/validation%20check%20-%20what%20errors%20mean.flv?dl=0)

## To run locally
Build program by running `python setup.py`. Or, run it via `python tkinter_gui.py`. To get the resulting Access file, you will need some sample Excel files.

## Testing
These tests might no longer work since I updated the code. What I had said before I made a GUI was:

> This requires Excel files to be in the `/tests` folder. Run `nosetests` at the parent directory. Tests only cover the validations themselves, not the rest of the script.