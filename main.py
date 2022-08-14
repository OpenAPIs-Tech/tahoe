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






@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/contact',methods=['GET'])
def contact():
    return render_template('contact.html')



@app.route('/error')
def errorpage():
    return render_template('404.html')

# Services----->START
@app.route('/Services',methods=['GET'])
def allServices():
    return render_template("service-signle.html")

@app.route('/Services/survey',methods=['GET'])
def survey():
    return render_template("survey.html")

@app.route('/Services/soil-testing',methods=['GET'])
def soilTesting():
    return render_template("soil-testing.html")

@app.route('/Services/railway-bridges',methods=['GET'])
def railwayBridges():
    return render_template("railway-bridges.html")

@app.route('/Services/buildings',methods=['GET'])
def buildings():
    return render_template("buildings.html")

@app.route('/Services/industrial-sheds',methods=['GET'])
def industrialSheds():
    return render_template("industrial-sheds.html")


#  Services------>END


# ABOUT-->start
@app.route('/About',methods=['GET'])
def aboutPage():
    return render_template("about.html")

@app.route('/About-team',methods=['GET'])
def teamPage():
    return render_template("our-team.html")


# @app.route('/Contact',methods=['GET'])
# def teamPage():
#     return render_template("contact.html")





@app.route('/')
def callback():
    return render_template('index.html')
if __name__=="__main__":
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)







