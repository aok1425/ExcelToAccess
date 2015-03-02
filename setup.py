from distutils.core import setup
import py2exe
import pandas
import matplotlib
import sys

sys.argv.append('py2exe')

setup(options={"py2exe":
               {"excludes": ["zmq.libzmq", "_gtkagg", "_tkagg", "scipy", "requests", "matplotlib"],
                # "bundle_files": 1,
                # "compressed": True,
                "dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe", "libzmq.pyd"],
                "optimize": 0
                }
               },
      data_files=matplotlib.get_py2exe_datafiles(),
      windows=[{'script': 'tkinter_gui.py'}],
      zipfile=None
      )