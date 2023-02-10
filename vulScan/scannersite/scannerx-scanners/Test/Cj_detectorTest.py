import sys, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
scannerModulePath = os.path.join(BASE_DIR,'')
sys.path.insert(0, scannerModulePath)

import Cj_detector
from Cj_detector import Detect_CJ

myScanner = Detect_CJ('http://localhost:8085/')
myScanner.scan()

print(myScanner.result)
print(myScanner.url)