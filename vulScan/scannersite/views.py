import json
import sys, os
from django.shortcuts import render

scannerModulePath = os.path.join(os.path.dirname(__file__),'scannerx-scanners')
servicesModulePath = os.path.join(os.path.dirname(__file__),'scannerx-services')

sys.path.insert(0, scannerModulePath)
sys.path.insert(0, servicesModulePath)

import ScannerService
from ScannerService import ScannerService

def home(request):
    if request.method == 'POST':
        website = request.POST.get('website')
        print('hello')
        scannerService = ScannerService(website)
        scannerService.scan()
        report = scannerService.report

        return render(request, 'report.html', {'report': report})

    return render(request, 'index.html', {'title': 'index'})

def about(request):
    return render(request, 'about.html', {'title': 'about'})


def contact(request):
    return render(request, 'contact.html', {'title': 'contact'})
