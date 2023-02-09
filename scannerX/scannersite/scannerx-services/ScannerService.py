import os, sys

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
scannerModulePath = os.path.join(BASE_DIR,'scannerx-scanners')
sys.path.insert(0, scannerModulePath)

import threading
import Csrf_detector, Cj_detector, HSTS_detector, Xss_reflected_detector, Xss_stored_detector, Sql_injection_detector, DDoS_detector

from Csrf_detector import Detect_Csrf
from Cj_detector import Detect_CJ
from HSTS_detector import Detect_HSTS
from Xss_reflected_detector  import Detect_Xss_Reflected
from Xss_stored_detector  import Detect_Xss_Stored
from Sql_injection_detector  import Detect_Sql_Injection
from DDoS_detector import Detect_DDoS_attack

class ScannerService:
    def __init__(self, url):
        self.report = []
        self.url = url

    def scan(self):
        myScanner1 = Detect_Sql_Injection(self.url)
        myScanner2 = Detect_Csrf(self.url)
        myScanner3 = Detect_CJ(self.url)
        myScanner4 = Detect_HSTS(self.url)
        myScanner5 = Detect_Xss_Reflected(self.url)
        myScanner6 = Detect_Xss_Stored(self.url)
        myScanner7 = Detect_DDoS_attack(self.url)

        t1 = threading.Thread(target=myScanner1.scan())
        t2 = threading.Thread(target=myScanner2.scan())
        t3 = threading.Thread(target=myScanner3.scan())
        t4 = threading.Thread(target=myScanner4.scan())
        t5 = threading.Thread(target=myScanner5.scan())
        t6 = threading.Thread(target=myScanner6.scan())
        t7 = threading.Thread(target=myScanner7.scan())

        # Start the threads
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()

        # Wait for both threads to finish
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()

        self.report.append(myScanner1.result)
        self.report.append(myScanner2.result)
        self.report.append(myScanner3.result)
        self.report.append(myScanner4.result)
        self.report.append(myScanner5.result)
        self.report.append(myScanner6.result)
        self.report.append(myScanner7.result)