
import json
from typing import final
import sqlalchemy


def getTestData(testCode,db):
    if testCode:
        query,finalres = getQuery(testCode,db)
        if query and finalres:
            dataFromDB = getDataFromDb(query,db)
            response = getResponseForTest(dataFromDB,finalres)
            
        if response:
            return response
        return
    return
def getOptionsData(data):
    print(f"data processing for options===> {data}")
    if not data:
        return ""
    resp={}
    count=0
    for d in data.split(":|:|:"):
        resp[count]=d
        count+=1
    return resp


def getResponseForTest(dataFromDB,finalres):
    finalresponse={}
    response={}
    finalresponse['answers'] = {}
    
    for data in dataFromDB:
        temp={}
        data=data._asdict()
        temp['questionId'] = data.get('id',None)
        temp['questionLatex'] = data.get('question_latex',None)
        temp['SolutionLatex'] = data.get('solution_latex',None)
        temp['optionLatex'] = getOptionsData(data.get('option_latex')) 
        temp['answer'] = [d for d in data.get('answer').split(",")]
        temp['duration'] = data.get('duration',None)
        temp['typeOfQuestion'] = data.get('type_of_question',None)
        # response.append(temp)
        finalresponse['answers'][data.get('id')] = [d for d in data.get('answer').split(",")]
        response[data.get('id')] = temp

    for sectionName,questionMetaData in finalres.items():
        # finalresponse={}
        finalresponse[sectionName]=[]
        for qId,qMarks in questionMetaData.items():
            questionDictData= response.get(qId)
            questionDictData['questionMarks'] = qMarks
            finalresponse[sectionName].append(questionDictData)

        # finalresponse.append(tempDict)
            


    return finalresponse

    
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
        
        try:
            questionIds,finalres = getQuestionIdfromMarksInfoDict(sections,json.loads(data.get('sectionmarksinfo')))
        except Exception as e:
            print(f'errrrrr=> {e}')
        query=(f'''select q.id,q.question_latex,q.duration,q.type_of_question,q.difficulty,q.answer,q.option_latex,s.solution_latex from question q join solution s on q.id=s.question_id where q.id in {questionIds} ''')
        print(f"query is==>{query}")
        return query,finalres
    return

# def getQuestionIdfromMarksInfoDict(sections,sectionMarksInDict):
#     questionIds = []
#     for sec in sections:
#         for key in sectionMarksInDict.get(sec).keys():
#             questionIds.append(int(key))
#     print(f"question ids===>{tuple(questionIds)}")
#     return tuple(questionIds)

def getQuestionIdfromMarksInfoDict(sections,sectionMarksInDict):
    questionIds = []
    tempres={}
    for sec in sections:
        questionIdsTemp = []
        questionIdsMarksTemp = {}
        for key,val in sectionMarksInDict.get(sec).items():
            
            questionIdsTemp.append(int(key))
            questionIdsMarksTemp[int(key)] = int(val)
        tempres[sec] = questionIdsMarksTemp
        questionIds = questionIds+questionIdsTemp
    # print(f"question ids===>{tuple(questionIds)}")
    return tuple(questionIds),tempres
    # return finalres


def getSectionData(data):
    if data.get('sectioninfo'):
        return [s for s in data.get('sectioninfo').split(",")]
    return

