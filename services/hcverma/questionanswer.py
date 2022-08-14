import sqlalchemy

def getQuestionAnswer(vol,chapter,exercise,question,db):
    # result = db.session.execute(sqlalchemy.text(f'SELECT * FROM question WHERE chapter_id = {chapter} and book_id={vol} and exercise={exercise} and question_no={question}'))
    
    try:
        result=db.session.execute(sqlalchemy.text(f'select q.question_no,q.question_latex,q.option_latex,s.solution_latex,q.class_id,q.exercise,q.difficulty,q.duration,q.type_of_question,q.blooms,q.concept,q.answer,b.name,b.volume,b.author,c.chapter_id,c.chapter_name from question q left join book b on q.book_id=b.id left join solution s on q.id=s.question_id left join chapterr c on q.chapter_id=c.chapter_id and q.book_id=c.book_id where q.book_id={vol} and q.chapter_id={chapter} and q.exercise={exercise} and q.question_no={question};'))
        print(f"result from database{result.all()}")
        
        

    except Exception as e:
        print(f"error in fetching data from db, error: {e}")
    if result.all():
        data=result.all()[0]._asdict()
        print(f"data from postgresql db==>{data}")
        if data:
            getDataInDict = processData(data)
            print(f"getdata in dict===>{getDataInDict}")
            return getDataInDict

    return 

def getDataForInputTypeQuestion(data):
    response={}
    print(f"data==>{data}")
    response['bookName'] = data.get('name',None)
    response['bookPartName'] = data.get('volume',None)
    response['authorName'] = data.get('author',None)
    response['class'] = data.get('class_id',None)
    response['chapterNumber']=data.get('chapter_id',None)
    response['chapterName']=data.get("chapter_name",None)
    response['exerciseNumber']=data.get('exercise',None)
    response['questionNumber']=data.get('question_no',None)
    response['questionDataInLatex']= data.get('question_latex',None)
    response['answerOfQuestion']=data.get('answer',None)
    response['solutionLatex'] = data.get('solution_latex',"Not Available")
    response['duration']=data.get('duration',None)
    response['NatureOfQuestion'] = data.get('blooms',None)
    response['typeOfQuestion']=data.get('type_of_question',None)
    response['conceptTagOfQuestion'] = data.get('concept',None)
    print(f"response ininput type of qn===>{response}")
    return response

def getOptionsInList(data):
    print(f"data processing for options===> {data}")
    if not data:
        return ""
    resp={}
    count=0
    for d in data.split(":|:|:"):
        resp[count]=d
        count+=1
    return resp

def getDataForOptionTypeQuestions(data):
    response={}
    optionsData = getOptionsInList(data.get('option_latex'))
    response['bookName'] = data.get('name',None)
    response['bookPartName'] = data.get('volume',None)
    response['authorName'] = data.get('author',None)
    response['class'] = data.get('class_id',None)
    response['chapterNumber']=data.get('chapter_id',None)
    response['chapterName']=data.get("chapter_name",None)
    response['exerciseNumber']=data.get('exercise',None)
    response['questionNumber']=data.get('question_no',None)
    response['questionDataInLatex']= data.get('question_latex',None)
    response['Options'] = optionsData
    response['answerOfQuestion']=[d for d in data.get('answer').split(",")]
    response['solutionLatex'] = data.get('solution_latex',"Not Available")
    response['duration']=data.get('duration',None)
    response['NatureOfQuestion'] = data.get('blooms',None)
    response['typeOfQuestion']=data.get('type_of_question',None)
    response['conceptTagOfQuestion'] = data.get('concept',None)
    print(f"response of option type qn===>{response}")
    return response


def processData(data):
    print(data.get('type_of_question'))
    if data.get('type_of_question').startswith('I'):
        print("Input type procesing")
        response = getDataForInputTypeQuestion(data)

    else:
        print("options type processing")
        response=getDataForOptionTypeQuestions(data)
    
    return response
    








