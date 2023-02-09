import sys, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
scannerModulePath = os.path.join(BASE_DIR,'')
sys.path.insert(0, scannerModulePath)

import SqlScanner
from SqlScanner import SqlScanner

myScanner = SqlScanner('http://www.tobiasodion.com')
myScanner.scan_sql_injection()

print(myScanner.result)
print(myScanner.url)