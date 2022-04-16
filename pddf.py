import pandas as pd

class PdDf:
    def __init__(self):
        pass

    def build_from_mongo(self, db_coll, v):
         
        v = str(v)
        #query = {}

        #project = {}
        pipeline = [
                {
                    '$replaceRoot': {
                        'newRoot': {
                            '$mergeObjects': [
                                {
                                    '_id': '$_id'
                                }, f'$impact.baseMetricV{v}.cvssV{v}', f'$impact.baseMetricV{v}'
                            ]
                        }
                    }
                }, {
                    '$project': {
                        f'cvssV{v}': 0
                    }
                }
            ]

        
        
        return pd.DataFrame.from_dict(db_coll.pull(pipeline ))

