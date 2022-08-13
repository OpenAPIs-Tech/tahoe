import sqlalchemy

def getQuestionAnswer(vol,chapter,exercise,question,db):
    # result = db.session.execute(sqlalchemy.text(f'SELECT * FROM question WHERE chapter_id = {chapter} and book_id={vol} and exercise={exercise} and question_no={question}'))
    result=db.session.execute(sqlalchemy.text(f'select q.question_no,q.question_latex,q.class_id,q.exercise,q.difficulty,q.duration,q.type_of_question,q.blooms,q.concept,q.answer,b.name,b.volume,b.author,c.chapter_id,c.chapter_name from question q left join book b on q.book_id=b.id left join chapterr c on q.chapter_id=c.chapter_id and q.book_id=c.book_id where q.book_id={vol} and q.chapter_id={chapter} and q.exercise={exercise} and q.question_no={question}'))
    data=result.all()[0]._asdict()
    print(f"data from postgresql db==>{data}")
    if data:
        getDataInDict = processData(data)
    return getDataInDict

def processData(data):
    response={}
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
    response['solutionLatex'] = data.get('solution',"Will be added very soon")
    response['duration']=data.get('duration',None)
    response['NatureOfQuestion'] = data.get('blooms',None)
    response['typeOfQuestion']=data.get('type_of_question',None)
    response['conceptTagOfQuestion'] = data.get('concept',None)
    return response
    








