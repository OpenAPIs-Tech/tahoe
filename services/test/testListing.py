import json
from dao import models
import json


def getAllTestInList(classId,board,subject,course,db):

    data  = getAllTestsData(classId,board,subject,course,db)
    return data

def getAllTestsData(classId,board,subject,course,db):

    query  =  getQueryForAllTests(classId,board,subject,course)

    dataFromDb = models.getDataFromDb(query,db)

    TestsData = getResponseBodyForAllTestsData(dataFromDb)
    
    print(f"final response: {TestsData}")
    return TestsData


def getResponseBodyForAllTestsData(dataFromDb):
    response = []

    for data in dataFromDb:
        temp={}

        data = data._asdict()
        print(f"dataindict from db: {data}")

        for k,v in data.items():

            if k=='testcode':
                k='testCode'

            elif k=='testname':
                k='testName'
            
            elif k=='testduration':
                k='testDuration'

            elif k=='sectioninfo':
                k='sectionInfo'
                v = [d for d in v.split(',')]
            
            elif k == 'sectionmarksinfo':
                k='sectionMarksInfo'
                v = json.loads(v) if v != None else None

            elif k=='test_marks':
                k='testMarks'

            temp[k] = v
        
    
        print(f"tempdata dict:{temp}")
        response.append(temp)

    return response

def getQueryForAllTests(classId,board,subject,course):
 
    if board and course:
        query = (f'''
    select a.test_code as testCode,a.class,a.subject,a.course,a.board,b.isdisplayed,b.sectioninfo as sectionInfo,b.sectionmarksinfo as sectionMarksInfo,b.test_name as testName,b.test_marks,b.test_duration as testDuration from test_display a join test b on a.test_code = b.testcode where class={classId} and board='{board}' and subject='{subject}' and course = '{course}';
    ''')

    elif not board:
        query = (f'''
    select a.test_code as testCode,a.class,a.subject,a.course,a.board,b.isdisplayed,b.sectioninfo as sectionInfo,b.sectionmarksinfo as sectionMarksInfo,b.test_name as testName,b.test_marks,b.test_duration as testDuration from test_display a join test b on a.test_code = b.testcode where class={classId} and board is null and subject='{subject}' and course = '{course}';
    ''')

    elif not course:
        query = (f'''
    select a.test_code as testCode,a.class,a.subject,a.course,a.board,b.isdisplayed,b.sectioninfo as sectionInfo,b.sectionmarksinfo as sectionMarksInfo,b.test_name as testName,b.test_marks,b.test_duration as testDuration from test_display a join test b on a.test_code = b.testcode where class={classId} and board='{board}' and subject='{subject}' and course is null;
    ''')

    return query