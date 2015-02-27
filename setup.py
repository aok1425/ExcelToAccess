from distutils.core import setup
import py2exe
import pandas
import matplotlib

setup(options={"py2exe":
               {"excludes": ["zmq.libzmq", "_gtkagg", "_tkagg"],
                "bundle_files": 1,
                "compressed": True,
                "dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe", "libzmq.pyd"]}
               },
      data_files=matplotlib.get_py2exe_datafiles(),
      console=[{'script': 'tkinter_gui.py'}],
      zipfile=None
      )