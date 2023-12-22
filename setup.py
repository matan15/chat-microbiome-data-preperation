from cx_Freeze import Executable, setup
import sys

base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("main.py", base=base, icon="./static/icons/plant.ico", target_name="Chat Microbiome Data Preperation")]

includefiles = [
    "static",
    "utils",
    ".gitignore",
    "requirements.txt"
]

packages = [
    "cx_Freeze",
    "sys",
    "tarfile",
    "tkinter",
    "os",
    "shutil",
    "threading",
    "pandas",
    "re",
    "json",
    "google",
    "requests"
]

options = {
    "build_exe": {
        "packages": packages,
        "include_files": includefiles
    }
}

setup(
    name="Chat Microbiome Data Preperation",
    version="1.0",
    options=options,
    executables=executables,
    author="Matan Naydis",
    description="This project was built in order to upload data for the Microbiome chatbot."
)