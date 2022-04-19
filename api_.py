
import json
import datetime as dt
#from pprint import pprint
from urllib.request import urlopen


 
class APIGet:
    def __init__(self,socket="https://services.nvd.nist.gov/rest/json/cves/1.0/" ):
        self._socket = socket
        self.url_init()
        
        self.data = []
        self.result_count = 0
    
    def get(self):
        print(self.url)
        inc = 0
        self.response = urlopen(self.url)    
        self.return_json = json.loads(self.response.read())
        
        _sIndx = self.return_json['startIndex']
        _tot = self.return_json['totalResults']

        self.data+= self.return_json['result']['CVE_Items']

        

        if len(self.data) < _tot:
            _sIndx += self._res_n
            print(f"starting at: {_sIndx} /{_tot}")
            self.url_init().time(self._t[0], self._t[1]).startIndex(_sIndx)
            if self._res_n:
                self.resultsPerPage(self._res_n)
            self.get()
            return self.data
            
        #pprint(len(self.return_json['result']['CVE_Items']))
        inc +=1
        print(f"harvested : {len(self.data)} /{_tot} ")
        return self.data
    
    def url_init(self):
        self.url = self._socket
        return self

    def _add(self, query):
        #print(query)
        if self.url == self._socket:
            self.url += '?' + query
        else:
            self.url += '&' + query
        return self

    def resultsPerPage(self, n):
        self._res_n = n
        self._resultsPerPage = f'resultsPerPage={n}'
        self._add(self._resultsPerPage)
        return self
    
    def startIndex(self,n):
        self._startIndex = f'startIndex={n}'
        self._add(self._startIndex)
        return self

    def time(self, from_, days=120):
        self._t = [from_, days]
        self.start_date = dt.datetime.strptime(self._t[0], "%y-%m-%d") if type(from_) != dt.datetime else from_
        
        self.end_date = (self.start_date + dt.timedelta(days=days))
        
        self._time =f"pubStartDate={self.start_date.isoformat() +':000'}%20UTC-00:00&pubEndDate={self.end_date.isoformat() +':000'}%20UTC-00:00"
        self._add(self._time)
        
        return self
        