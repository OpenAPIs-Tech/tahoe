
import json
import sqlalchemy


def getTestData(testCode,db):
    if testCode:
        query = getQuery(testCode,db)
        if query:
            dataFromDB = getDataFromDb(query,db)
            response = getResponseForTest(dataFromDB)
            
        if response:
            return response
        return
    return

def getResponseForTest(dataFromDB):
    response=[]
    
    for data in dataFromDB:
        temp={}
        data=data._asdict()
        temp['questionLatex'] = data.get('question_latex',None)
        temp['SolutionLatex'] = data.get('solution_latex',None)
        temp['optionLatex'] = data.get('option_latex',None)
        temp['answer'] = data.get('answer',None)
        temp['duration'] = data.get('duration',None)
        temp['typeOfQuestion'] = data.get('type_of_question',None)
        response.append(temp)

    return response

    return
def getDataFromDb(query,db):

    try:
        datacursor = db.session.execute(sqlalchemy.text(query))
        data=datacursor.all() 

    except Exception as e:
        print(f"error occured:{e}")
        return

    print(f"data of question details from db===>{data}")
    return data




def getQuery(testCode,db):
    try:
        datacursor =db.session.execute(sqlalchemy.text(f'''select sectioninfo,sectionmarksinfo from test where testcode='{testCode}' '''))
    except Exception as e:
        print(f"error in getting data from test table for {testCode} and error:{e}")
    
    data=datacursor.all()
    print(f"data from test table===>{data}")

    if len(data)==1:
        data=data[0]._asdict()
        sections = getSectionData(data)
        
        
        questionIds = getQuestionIdfromMarksInfoDict(sections,json.loads(data.get('sectionmarksinfo')))
        query=(f'''select q.question_latex,q.duration,q.type_of_question,q.difficulty,q.answer,q.option_latex,s.solution_latex from question q join solution s on q.id=s.question_id where q.id in {questionIds} ''')
        print(f"query is==>{query}")
        return query
    return

def getQuestionIdfromMarksInfoDict(sections,sectionMarksInDict):
    questionIds = []
    for sec in sections:
        for key in sectionMarksInDict.get(sec).keys():
            questionIds.append(int(key))
    print(f"question ids===>{tuple(questionIds)}")
    return tuple(questionIds)
def getSectionData(data):
    if data.get('sectioninfo'):
        return [s for s in data.get('sectioninfo').split(",")]
    return

