import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"optimize": True,
                     "packages": ["ctrl",'db','mod','resources','view'],}

setup(  name = "mbackup",
        version = "0.1",
        description = "Reliable backup",
        options = {"build_exe": build_exe_options},
        executables = [Executable("mbackup",)])