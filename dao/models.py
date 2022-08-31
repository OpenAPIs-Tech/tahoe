import json
import sqlalchemy

def getDataFromDb(query,db):

    try:
        datacursor = db.session.execute(sqlalchemy.text(query))
        data=datacursor.all() 

    except Exception as e:
        print(f"error occured:{e}")
        return

    print(f"data from db===>{data}")
    return data