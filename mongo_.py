from pprint import pprint


 

class MongoDB():
    def __init__(self, db, coll):
        #self.db = db
        self._db_coll = db[coll]
     
    def insert(self, json_list):

        self.result_dict ={'T':0,'F':0}

        for json in json_list: 
            filter_ = {'_id': json['cve']['CVE_data_meta']['ID'] }
            update = {"$set":json}
            
            result = self._db_coll.update_one(filter_,update,upsert=True)
            
            self.result_dict['T' if result.upserted_id else 'F'] += 1
        
        print(f"{self.result_dict['T']} documents added to  collection,  {self.result_dict['F']} already exist")
        
        return self

    def pull(self, pipeline):
        
        cursor = self._db_coll.aggregate(pipeline)

        #[pprint(i) for i in cursor]
        #print(list(cursor))
        

        return cursor

if __name__ == '__main__':
    from pymongo import MongoClient
    db_name = 'tenable_db'
    collection = 't1'
    client = MongoClient()[db_name]
    m = MongoDB(client, collection)
    #pprint(m._db.command('collstats',collection)['count'])
    #client['collection'].command()