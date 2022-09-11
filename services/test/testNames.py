from . import testdata

def getTestNames(classId,board,db):

    if classId and board:

        data = getAllSubjectNamesAndCompetitionNames(classId,board,db)

        return data
    
    return


def getAllSubjectNamesAndCompetitionNames(classId,board,db):

    query = getQueryForBoardSubjectsAndCompSubjects(classId,board)
    dataFromDb = testdata.getDataFromDb(query,db)
    response={}
    response['boards']=[]
    response['comp'] = []


    for data in dataFromDb:
        data=data._asdict()
        if data.get('board'):
            response['boards'].append(data.get('board'))
        
        elif data.get('course'):
            response['comp'].append(data.get('course'))

    print(f"response:{response}")

    return response




# def getListOfSubjectsByBoard(classId,board,db):
#     queryForSubjectsByBoardName = getQueryForSubjectsAvailableByBoard(classId,board)
#     dataFromDb = testdata.getDataFromDb(queryForSubjectsByBoardName,db)

#     subjects = [d for d, in dataFromDb]
#     print(f"Subjects from db for {board} and {classId}: {subjects}")

#     return subjects


def getQueryForBoardSubjectsAndCompSubjects(classId,board):
    query = (f'''select name,board,course from subject where class={classId} or board='{board}' or course is not null;''')
    return query

# def getQueryForSubjectsAvailableByBoard(classId,board,db):
#     query=(f'''select name from subject where class={classId} and board='{board}'; ''')
#     return query



    