import json
from flask import Flask, request,Response,render_template
from flask_cors import CORS, cross_origin

from services.imageurl import genimageurl



app = Flask(__name__)


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

if __name__=="__main__":
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)







