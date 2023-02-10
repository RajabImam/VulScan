import requests

class Detect_HSTS():
	def __init__(self,url):
		self.url=url
		self.result = {'name': 'SSL Stripping', 'status': 'Not Detected', 'message': '', 'screenshot':'', 'header':''}

	def scan(self):
		try:
			resp=requests.get(self.url)
			headers=resp.headers

			header = ''

			print ("\n\nHeaders set are : \n" )
			for k,v in headers.items():
				header = header + k+" : "+v+"\n" 
				print(k+":"+v)

			self.result['header'] = header

			if "Strict-Transport-Security" in headers.keys():
				self.result['message'] = 'HSTS Header present. Your site is not vulnerable to SSL Stripping Attacks'
			else:
				self.result['status'] = 'Detected'
				self.result['message'] = 'Strict-Transport-Security is missing. Your site is vulnerable to SSL Stripping Attacks'

		except Exception as ex:
			print("EXception caught : " +str(ex))


