import json
from os import stat
from flask import Flask, request,Response,render_template,jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import os


from sqlalchemy.sql import func
from sqlalchemy import text
import sqlalchemy

from services.imageurl import genimageurl
from services.hcverma import questionanswer

# postgresql://nrzlppgvzcreqh:9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28@ec2-34-235-198-25.compute-1.amazonaws.com:5432/dbnu9bnpvc38nj
# database="dbnu9bnpvc38nj", user="nrzlppgvzcreqh", password="9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28", host="ec2-34-235-198-25.compute-1.amazonaws.com", port="5432"
app = Flask(__name__)
url=os.environ['DATABASE_URL']
url=url.replace("postgres","postgresql")
print(url)
app.config['SQLALCHEMY_DATABASE_URI'] =url

# app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://nrzlppgvzcreqh:9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28@ec2-34-235-198-25.compute-1.amazonaws.com:5432/dbnu9bnpvc38nj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
@app.route('/',methods=['GET'])
def index():
    return "Hello world"


@app.route('/generateUrl',methods=['POST'])
@cross_origin()
def urlGenerator():
    response = genimageurl.getUrl(request)
   
    if response.get('url',""):
        return Response(json.dumps(response),status=200,mimetype="application/json")
    
    return Response(json.dumps(response),status=400,mimetype="application/json")

@app.route('/hc-verma/<int:volume>/<int:chapter>/<int:exercise>/<int:question>',methods=['GET'])
@cross_origin()
def hcVermaData(volume: int,chapter:int,exercise:int,question:int):
    statusCode=200
    msgText='Success'
    data=getQuestionAnswer(volume,chapter,exercise,question)
    if data:
        return jsonify(statusCode=statusCode,msgText=msgText,data=data)


    return jsonify(statusCode=400,msgText="We are very sorry. We are doing our best to fix this up.")

def getQuestionAnswer(vol,chapter,exercise,question):
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
if __name__=="__main__":
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)







