from bs4 import BeautifulSoup
import requests
import multiprocessing as mp
from selenium import webdriver
import time
import datetime        
import socket
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import chromedriver_autoinstaller as chromedriver
chromedriver.install()

class Detect_DDoS_attack :
    def __init__(self, url):
        self.url = url
        self.email = "admin"
        self.password = "password"
        self.result = {
            'name': 'DDoS Attacks', 
            'status': 'Not Detected', 
            'message': 'The website is not vulnerable to DDoS attacks', 
            'screenshot': 'images/csrf/csrf_0.png', 
            'header': ''
        }



    def scan(self) :
        browser = webdriver.Chrome()
        browser.get(self.url)

        # Nombre de requêtes maximum tolérées en un court intervalle de temps
        max_request_threshold = 1000

        # Intervalle de temps à surveiller (en secondes)
        time_window = 3

        # Initialisation du compteur de requêtes
        request_counter = 0

        print("Surveillance du serveur démarrée")

        for i in range(0, max_request_threshold + 1, 1):
            # Calling the web page
            browser.get(self.url)

            try:
                # Incrémentation du compteur de requêtes
                request_counter += 1

                # Si le nombre de requêtes est supérieur au seuil, cela peut être un signe d'attaque DDOS
                if request_counter > max_request_threshold:
                    self.result['status'] = 'Detected'
                    self.result['message'] =  "The website is vulnerable from DDoS attacks with " + str(request_counter) + " requests"
                
                # Réinitialisation du compteur de requêtes toutes les 'time_window' secondes
                # time.sleep(time_window)
                request_counter = 0
            finally:
                # Fermeture de la connexion
                print('Finished')
