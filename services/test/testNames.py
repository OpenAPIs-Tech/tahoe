from . import testdata

def getTestNames(classId,board,db):

    if classId and board:

        data = getAllSubjectNamesAndCompetitionNames(classId,board,db)
        data = None if not data.get('boards') and not data.get('competitive') else data
        return data
    
    return


def getAllSubjectNamesAndCompetitionNames(classId,board,db):

    query = getQueryForBoardSubjectsAndCompSubjects(classId,board)
    dataFromDb = testdata.getDataFromDb(query,db)
    response={}
    response['boards']=[]
    response['competitive'] = []


    for data in dataFromDb:
        data=data._asdict()
        # if data.get('class')==classId:
        board,course = data.get('board'),data.get('course')
        if board and board not in response['boards']:
            response['boards'].append(board)
        
        elif course and course not in response['competitive']:
            response['competitive'].append(course)

    print(f"response:{response}")

    return response




# def getListOfSubjectsByBoard(classId,board,db):
#     queryForSubjectsByBoardName = getQueryForSubjectsAvailableByBoard(classId,board)
#     dataFromDb = testdata.getDataFromDb(queryForSubjectsByBoardName,db)

#     subjects = [d for d, in dataFromDb]
#     print(f"Subjects from db for {board} and {classId}: {subjects}")

#     return subjects


def getQueryForBoardSubjectsAndCompSubjects(classId,board):
    query = (f'''select s.name,s.class,s.board,c.exam_name from subject s join competitive_exams c on s.class=c.class where s.class={classId} and s.board='{board}';''')
    return query

# def getQueryForSubjectsAvailableByBoard(classId,board,db):
#     query=(f'''select name from subject where class={classId} and board='{board}'; ''')
#     return query



    