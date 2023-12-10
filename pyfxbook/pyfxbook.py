import requests as r
import requests.packages
from typing import List, Dict
from endpoints import API_PATH
from pyfxbook.exceptions import PyfxbookApiException
from pyfxbook.models import Result
from json import JSONDecodeError
import logging

class Pyfxbook: 

    base_url = "https://www.myfxbook.com/"
    email = None
    password = None 
    session = None


    def __init__(self, email:str, password:str):
        self.email = email
        self.password = password
    

    def login(self):
        login = r.get(self.base_url + API_PATH['login'], params={'email':self.email, 'password':self.password}).json()  
        self.session = login['session']
        return login 


    def _do(self, http_method:str, endpoint:str, ep_params: Dict=None) -> List[Dict]:
        full_url = self.base_url + endpoint
        try:
            response = r.request(method=http_method, url=full_url, params=ep_params)
        except requests.exceptions.RequestException as e:
            raise PyfxbookApiException("Request Failed") from e
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            raise PyfxbookApiException("Bad JSON response") from e
        if 299 >= response.status_code >= 200:
            return Result(response.status_code, message=response.reason, data=data_out)
        raise PyfxbookApiException(f"{response.status_code}: {response.reason}")


    def get(self, endpoint:str, ep_params: Dict = None) -> Result: 
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)
    
