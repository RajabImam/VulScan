from ScannerService import ScannerService

myScannerService = ScannerService('http://www.tobiasodion.com')
myScannerService.scan()

print(myScannerService.report)