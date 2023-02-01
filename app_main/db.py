import pymongo
import secrets
import datetime
from bson.objectid import ObjectId
from bson import json_util
import json



def parse_json(data):
    return json.loads(json_util.dumps(data))

class Mongo():
    """Mongo is a simple useable function based object"""
    
    
    def __init__(self,app):
        self.app = app
        self.collection_names=[]
        self.mongo_token = secrets.token_urlsafe(8)
        self.client = pymongo.MongoClient(app.config['MONGODB_URI'])
        self.db = self.client[app.config['MONGO_APPLICATION_DATA']]
        
    def column(self,collection_name):
        '''
        return a mongodb collection
        or create new collection
        '''
        
        self.collection_names.append(collection_name)
        self.db[collection_name]
        return self.db[collection_name]
        # raise KeyError('[Collection_Error]: collection already exist '+collection_name)
        
    def add(self, item, target):
        if type(item)==type(dict()):
            if target.count_documents({}) == 0:
                item['_KEY_'] = 1
            else:
                item['_KEY_'] = (target.find().skip(target.count_documents({})-1)[0]['_KEY_'])+1
            item['__DATE__'] = datetime.datetime.utcnow().strftime("%d %B, %Y, %H:%M:%S")
            idn = target.insert_one(parse_json(item)).inserted_id
            return {'common':idn,'bson':ObjectId(idn)}
        elif type(item)==type(list()):
            ids = []
            idsb = []
            for it in item:
                it[unique] = target.create_index(unique)
                it['__DATE__'] = datetime.datetime.utcnow().strftime("%d %B, %Y, %H:%M:%S")
                ins=target.insert_one(parse_json(it)).inserted_id
                ids.append(ins)
                idsb.append(ObjectId(ins))
            return {'common':ids,'bson':idsb}

    def get(self, id_or_query, target, __id__=False, limit=0):
        if __id__==False:
            if limit > 0:
                return target.find(id_or_query).limit(limit)
            else:
                return target.find(id_or_query)
                
        elif __id__:
            if type(id_or_query['bson'])==type(list()):
                idsr=[]
                for ids in id_or_query['bson']:
                    idsr.append(target.find_one({'_id':ids}))
                return idsr
            else:
                return target.find_one({'_id':id_or_query['bson']})
            
    def update(self, query, new, target, force=False):
        if force==False:
            target.update_one(query,new)
        elif force:
            target.update_many(query,new)
        else:
            raise AttributeError('can\'t update MONGODB_URI not analys')

    def delete(self, query, target, force=False):
        #delete_one
        if force:
            return target.delete_many(query)
        elif force==False:
            return target.delete_one(query)
        else:
            raise EnvironmentError('force must be True or False')
    
    def drop(self, target):
        target.drop()

if __name__ == '__main__':
    raise ImportError('[mongodb.configuration.Error]:can\'t use without MONGO_APPLICATION_DATA')