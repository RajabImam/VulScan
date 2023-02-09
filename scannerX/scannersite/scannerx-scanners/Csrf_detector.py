import os
from bs4 import BeautifulSoup
import requests
import multiprocessing as mp
from selenium import webdriver
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import chromedriver_autoinstaller as chromedriver
chromedriver.install()

#from django.conf import settings

class Detect_Csrf():
	def __init__(self,url):
		self.url=url
		self.email="admin"
		self.password="password"
		self.target_links=["vulnerabilities/csrf/"]
		self.cookies=["RequestVerificationToken","token","csrfToken","csrftoken"]
		self.hidden=["__RequestVerificationToken","token","_csrfToken","_csrftoken"]
		self.result = {'name': 'CSRF', 'status': 'Not Detected', 'message': 'CSRF Protection Header present. Your site is not vulnerable to CSRF Attacks', 'screenshot':'images/csrf/csrf_0.png', 'header':''}

	def scan(self):
		try:
			browser = webdriver.Chrome()
			browser.get(self.url)
			element_username=browser.find_element(By.NAME, "username")
			element_username.clear()
			element_username.send_keys(self.email)
			element_username.click()
			element_password=browser.find_element(By.NAME, "password")
			element_password.clear()
			element_password.send_keys(self.password)
			element_password.click()

			try:
				element_submit = WebDriverWait(browser, 2).until(
					EC.element_to_be_clickable((By.NAME, "Login"))
				)
				time. sleep(2)
				element_submit.click()
			except Exception as ee:
					print("Exception : "+str(ee))
					browser.quit()
			html = browser.page_source
			cookie={'domain':'127.0.0.1','name': 'security','value':'low','path': '/','httponly': False, 'secure': False}
			browser.add_cookie(cookie)
			all_cookies = browser.get_cookies()				
			soup = BeautifulSoup(html, "html.parser")
			anchor_tags=soup.find_all("a")
			#browser.save_screenshot('screen.png')
			#print("\n Saved Screen shot Post Login.Note the cookie values : ")
			found_form=False
			forms=[]
			count =0 
			for i,link in enumerate(anchor_tags):
				try:	
					actuall_link=link.attrs["href"]
					actuall_link=actuall_link.replace("/.","/")
					if actuall_link in self.target_links:
						nav_url=str(self.url)+str(actuall_link)
						browser.get(nav_url)
						#browser.save_screenshot("screen"+str(i)+".png")
						page_source=browser.page_source
						soup = BeautifulSoup(page_source, "html.parser")
						forms_=soup.find_all("form")
						submit_button=""
						
						all_cookies = browser.get_cookies()
						for no,form in enumerate(forms_) :
							anti_csrf=False
							inputs=form.find_all("input")
							for ip in inputs:
								if ip.attrs["type"] in ["hidden"]:
									hidden=browser.find_element(By.NAME, ip.attrs["name"])
									if hidden in self.hidden:
										for c,v in all_cookies.items():
											if c in self.cookies:
												anti_csrf=True
							if anti_csrf==False:
								self.result['status'] = 'Detected'
								self.result['message'] = 'CSRF Protection header is missing!. Your site is vulnerable to CSRF Attacks'
								forms.append({"url":nav_url,"form":str(form)})
								#static_root = settings.STATIC_ROOT
								filename = 'csrf_'+str(no)+".png"
								#print(f'{static_root}/images/csrf/{filename}')
								#browser.save_screenshot(f'{static_root}/images/csrf/{filename}')
								browser.save_screenshot(filename)
				except Exception as ex:
					print("## Exception caught : " +str(ex))
			
			if len(forms):
				print("Discovered folowing Forms without CSRF protection : ")
				for form in forms:
					print("URL : "+str(form["url"])+"\n")
					print("Form : " +str(form["form"]))
					print("\n\n\n\n")

			print("\n\nSucessfully executed and Screenshots Saved")
		except Exception as ex:
			print(str(ex))
