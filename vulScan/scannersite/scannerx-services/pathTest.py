from pathlib import Path
import os, sys

APPDIR = '/Users/tobiasodion/Documents/Semester 3/Software Security_II3524/project/SecurityProject/scannerX/scannersite/'
scannerModulePath = os.path.join(os.path.dirname(APPDIR),'scannerx-scanners')

BASE_DIR = Path(__file__).resolve().parent.parent
scannerModulePath2 = os.path.join(BASE_DIR,'scannerx-scanners')

if (scannerModulePath == scannerModulePath2):
    print(True)
else:
    print(False)
