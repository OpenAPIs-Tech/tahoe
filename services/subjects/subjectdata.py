
from services.test.testdata import getQuery
from dao import models


def getSubjects(classId,db):
    if classId:
        query = getQueryForSubjectByClass(classId)
        dataFromDB = models.getDataFromDb(query,db)
        response = getResponseForSubjects(dataFromDB)

        if response:
            return response
        
    return


def getResponseForSubjects(dataFromDB):
    resp = []
    for data, in dataFromDB:
        resp.append(data)


def getQueryForSubjectByClass(classId):
    return (f'''select name from subject where class={classId}''')