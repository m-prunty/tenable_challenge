import json

import time
import datetime as dt
from pymongo import MongoClient

from collections import Counter 

from api_ import APIGet
from mongo_ import MongoDB
from pddf import PdDf


class Run():
    def __init__(self,db_name = 'tenable_db',collection = 't1'):
        self.db_name= db_name 
        self.collection= collection 
        
        self.db = MongoClient()[db_name]
        self.db_coll = MongoDB(self.db, collection)
        
        #self.fill_mongo()

        
        
    def fill_df(self):
        self.dfV2 = PdDf().build_from_mongo(self.db_coll,2)
        self.dfV3 = PdDf().build_from_mongo(self.db_coll,3)
        return self


    def fill_mongo(self, from_ = 2014, to_ = dt.datetime.now() ):
        from_ = dt.datetime(from_,1,1,0)
        _tot = Counter({})
        api= APIGet()
        while from_ < to_:
            print("waiting 1s ...")
            time.sleep(1)

            api= APIGet()
            
            json_list = api.time(from_).resultsPerPage(2000).get()
            from_ = api.end_date 
            self.db_coll.insert(json_list)
            _tot += Counter(self.db_coll.result_dict)
            

        print(f"In total, {_tot['T']} added and {_tot['F']} already exist in {self.db_name}.{self.collection}")
        print(f"{self.db.command('collstats',self.collection)['count']} files in collection")
            
        
        return self
        
        
if __name__ == '__main__':
    r= Run()
    r = Run(collection='t2').fill_mongo(2022)
    
    #print(r.db.command('collStats'))
