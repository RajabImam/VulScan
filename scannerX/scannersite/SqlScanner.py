import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin


class SqlScanner:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.session.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
        self.report = {'status': False, 'message': ''}

    # function to extract all html forms tags

    def extract_forms(self):
        res = self.session.get(self.url)
        soup = BeautifulSoup(res.content, "html.parser")
        return soup.find_all("form")

    # function to get form details

    def get_form_details(self, form):
        details = {}
        # get the form action (target url)
        try:
            action = form.attrs.get("action").lower()
        except:
            action = None
        # get the form method (POST, GET, etc.)
        method = form.attrs.get("method", "get").lower()
        # get all the input details such as type and name
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value = input_tag.attrs.get("value", "")
            inputs.append(
                {"type": input_type, "name": input_name, "value": input_value})
        # put everything to the resulting dictionary
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details

    # function for vulnerability testing

    def vulnerable(self, response):
        errors = {
            # MySQL
            "you have an error in your sql syntax;",
            "warning: mysql",
            # SQL Server
            "unclosed quotation mark after the character string",
            # Oracle
            "quoted string not properly terminated",
        }
        for error in errors:
            if error in response.content.decode().lower():
                return True
        return False

    # function to scan a url for sql injections

    def scan_sql_injection(self):
        # extract all forms from the url
        forms = self.extract_forms()
        # returning value
        js_scripts = []
        # iterate over all forms
        for form in forms:
            form_details = self.get_form_details(form)
            for c in "\"'":
                # the data body we want to submit
                data = {}
                for input_tag in form_details["inputs"]:
                    if input_tag["type"] == "hidden" or input_tag["value"]:
                        # any input form that has some value or hidden input, use it in the form body
                        try:
                            data[input_tag["name"]] = input_tag["value"] + c
                        except:
                            pass
                    elif input_tag["type"] != "submit":
                        # all others except submit, fill with a test payload
                        data[input_tag["name"]] = f"test{c}"

                # join the url with the action (form request URL)
                url = urljoin(self.url, form_details["action"])
                if form_details["method"] == "post":
                    res = self.session.post(url, data=data)
                elif form_details["method"] == "get":
                    res = self.session.get(url, params=data)

                # test for sql injection
                if self.vulnerable(res):
                    self.report['status'] = True
                    self.report['message'] = "[+] Detected {len(forms)} forms on {self.url}. [+] SQL Injection discovered on {self.url}"
                    #for key, value in data.items():
                        #print(f"[*] {key}: {value}")
                    #print("[+] Form:")
                    #print(form)
                else:
                    self.report['status'] = False
                    self.report['message'] = "No SQL Injection found"
