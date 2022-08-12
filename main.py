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

app.config['SQLALCHEMY_DATABASE_URI'] =os.environ['DATABASE_URL']

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
    data=questionanswer.getQuestionAnswer(volume,chapter,exercise,question,db)
    if data:
        return jsonify(statusCode=statusCode,msgText=msgText,data=data)


    return jsonify(statusCode=400,msgText="We are very sorry. We are doing our best to fix this up.")

if __name__=="__main__":
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)







