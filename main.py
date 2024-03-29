import json
from os import stat
from flask import Flask, request,Response,render_template,jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.sql import func
from sqlalchemy import text

from services.imageurl import genimageurl
from services.hcverma import questionanswer
from services.test import testdata,testNames,testListing
from services.subjects import subjectdata

# url ='postgresql://nrzlppgvzcreqh:9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28@ec2-34-235-198-25.compute-1.amazonaws.com:5432/dbnu9bnpvc38nj'

# database="dbnu9bnpvc38nj", user="nrzlppgvzcreqh", password="9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28", host="ec2-34-235-198-25.compute-1.amazonaws.com", port="5432"
app = Flask(__name__)
url=os.environ['DATABASE_URL']
url=url.replace("postgres","postgresql")
print(url)
app.config['SQLALCHEMY_DATABASE_URI'] =url

# app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://nrzlppgvzcreqh:9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28@ec2-34-235-198-25.compute-1.amazonaws.com:5432/dbnu9bnpvc38nj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# @app.route('/',methods=['GET'])
# def index():
#     return "Hello world"

@app.route('/health',methods=['GET'])
@cross_origin()
def urlGenhjderator():
    return "hello"

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
    if ((exercise==1) or (exercise==2) or (exercise==3) or (exercise==4)) and (chapter==1):
        data=questionanswer.getQuestionAnswer(volume,chapter,exercise,question,db)
        if data:
            response={}
            response['statusCode'] = statusCode
            response['msgText']=msgText
            response['data']=data
            return Response(json.dumps(response),status=200,mimetype="application/json")


    return Response(json.dumps({'statusCode':400,'msgText':"We are still developing it. Thank you for your patience"}),status=400,mimetype="application/json")

@app.route('/getTestData',methods=['POST'])
@cross_origin()
def dataForTestPlatform():
    response={}
    statusCode=200
    msgText=""
    data=None
    try:
        testCode = request.get_json().get('testCode')
        
    except:
        statusCode=400
        msgText="bad request, failed to get body from request"
        response['statusCode']=statusCode
        response['msgText']=msgText
        response['data']=data
        return Response(json.dumps(response),status=200,mimetype="application/json")

    
    data = testdata.getTestData(testCode,db)
        # return 
    if data:
        response['statusCode'],response['msgText'],response['data']=statusCode,"Success",data
        return Response(json.dumps(response),status=200,mimetype="application/json")
    response['statusCode'],response['msgText'],response['data']=400,"Failed",data
    return Response(json.dumps(response),status=400,mimetype="application/json")

@app.route('/getSubjects',methods=['POST'])
@cross_origin()
def dataOfSubjectsByClass():
    response={}
    statusCode=200
    msgText=""
    data=None
    try:
        classId = int(request.get_json().get('class'))

    except Exception as e:
        print(f"error:{e}")
        statusCode=400
        msgText="bad request, failed to get body from request"
        response['statusCode']=statusCode
        response['msgText']=msgText
        response['data']=data
        return Response(json.dumps(response),status=200,mimetype="application/json")

    data = subjectdata.getSubjects(classId,db)
    if data:
        response['statusCode'],response['msgText'],response['data']=statusCode,"Success",data
        return Response(json.dumps(response),status=200,mimetype="application/json")
    response['statusCode'],response['msgText'],response['data']=400,"Failed",data
    return Response(json.dumps(response),status=400,mimetype="application/json")


@app.route('/getTestEntity',methods=['POST'])
@cross_origin()
def TestNames():
    response={}
    statusCode=200
    msgText=""
    data=None
    try:
        reqBody = request.get_json()
        classId = int(reqBody.get('class'))
        board = reqBody.get('board')

    except Exception as e:
        print(f"error:{e}")
        statusCode=205
        msgText="bad request, failed to get body from request"
        response['statusCode']=statusCode
        response['msgText']=msgText
        response['data']=data
        return Response(json.dumps(response),status=205,mimetype="application/json")

    data = testNames.getTestNames(classId,board,db)
    if data:
        response['statusCode'],response['msgText'],response['data']=statusCode,"Success",data
        return Response(json.dumps(response),status=200,mimetype="application/json")
    response['statusCode'],response['msgText'],response['data']=200,"Failed",data
    return Response(json.dumps(response),status=200,mimetype="application/json")

@app.route('/getTestListing',methods=['POST'])
@cross_origin()
def TestLists():
    response={}
    statusCode=200
    msgText=""
    data=None
    try:
        reqBody = request.get_json()
        classId = int(reqBody.get('class'))
        board = reqBody.get('board')
        subject = reqBody.get('subject')
        course = reqBody.get('course')

    except Exception as e:
        print(f"error:{e}")
        statusCode=400
        msgText="bad request, failed to get body from request"
        response['statusCode']=statusCode
        response['msgText']=msgText
        response['data']=data
        return Response(json.dumps(response),status=205,mimetype="application/json")

    data = testListing.getAllTestInList(classId,board,subject,course,db)
    if data:
        response['statusCode'],response['msgText'],response['data']=statusCode,"Success",data
        return Response(json.dumps(response),status=200,mimetype="application/json")
    response['statusCode'],response['msgText'],response['data']=200,"Failed",data
    return Response(json.dumps(response),status=200,mimetype="application/json")

    



if __name__=="__main__":
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)







