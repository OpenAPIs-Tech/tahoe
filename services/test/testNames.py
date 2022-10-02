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
    response['competitive'] = {}

    if dataFromDb:
        
        for data in dataFromDb:
            data=data._asdict()
            print(data)
            subject,course = data.get('name'),data.get('course')

            if subject and subject not in response['boards'] and not course:
                response['boards'].append(subject)
            
            elif course:

                if response['competitive'].get(course):

                    if subject not in response['competitive'][course]:
                        response['competitive'][course].append(subject)

                else:

                    response['competitive'][course] = []
                    response['competitive'][course].append(subject)

    print(f"response:{response}")

    return response




# def getListOfSubjectsByBoard(classId,board,db):
#     queryForSubjectsByBoardName = getQueryForSubjectsAvailableByBoard(classId,board)
#     dataFromDb = testdata.getDataFromDb(queryForSubjectsByBoardName,db)

#     subjects = [d for d, in dataFromDb]
#     print(f"Subjects from db for {board} and {classId}: {subjects}")

#     return subjects


def getQueryForBoardSubjectsAndCompSubjects(classId,board):
    query=(f'''select * from (select * from subject where class={classId}) as foo where board='{board}' or course is not null;''')
    # query = (f'''select s.name,s.class,s.board,c.exam_name from subject s join competitive_exams c on s.class=c.class where s.class={classId} and s.board='{board}';''')
    return query
    


# def getQueryForSubjectsAvailableByBoard(classId,board,db):
#     query=(f'''select name from subject where class={classId} and board='{board}'; ''')
#     return query



    