import pymongo 

class MongoDB:
    def __init__(self,db_name,doc_name,connectionStr="mongodb://localhost:27017/"):
        self.client = pymongo.MongoClient(connectionStr)
        self.db = self.client[db_name]
        self.collection = self.db[doc_name]

    def insert(self, data={}):
        self.collection.insert_one(data)
        #lst = [data]
        #self.collection.insert_many(lst)
        return True

    def fetch(self,data=None,show_id={"_id":0}):
        result = []
        res = self.collection.find(data,show_id)
        for item in res:
            result.append(item)      
        return result
        
    def count(self,data={}):
        count = self.collection.count_documents(data)
        return count
    
    
    def update(self,prev,nxt):
        nxt = {"$set":nxt}
        up = self.collection.update_many(prev,nxt)
        count  = up.modified_count
        if count >0:
            return True
        else:
            return False

 
    def delete(self,data={}):
        dlt = self.collection.delete_many(data)
        count = dlt.deleted_count
        if count > 0:
            return True
        else:
            return False  
   
    def close(self):
        self.client.close()

   