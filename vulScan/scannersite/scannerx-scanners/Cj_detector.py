import requests

class Detect_CJ():
	def __init__(self,url):
		self.result = {'name': 'Click Jacking', 'status': 'Not Detected', 'message': '', 'screenshot':'', 'header':''}
		self.url = url

	def scan(self):
		try:
			resp=requests.get(self.url)
			headers=resp.headers
			
			header = ''

			print ("\n\nHeaders set are : \n" )
			for k,v in headers.items():
				header = header+k+" : "+v+"\n" 
				print(k+":"+v)

			self.result['header'] = header

			if "X-Frame-Options" in headers.keys():
				self.result['message'] = 'Click Jacking Header present. Your site is not vulnerable to Click Jacking Attacks'
			else:
				self.result['status'] = 'Detected'
				self.result['message'] = 'X-Frame-Options is missing ! Your site is vulnerable to Click Jacking Attacks'
		except Exception as ex:
			print("EXception caught : " +str(ex))

