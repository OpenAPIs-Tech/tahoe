import json
from flask import Flask, render_template, request, url_for, redirect
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
from flask import Flask, request,Response,render_template
from flask_cors import CORS, cross_origin

from services.imageurl import genimageurl



app = Flask(__name__)


@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/generateUrl',methods=['POST'])
@cross_origin()
def urlGenerator():
    response = genimageurl.getUrl(request)
   
    if response.get('url',""):
        return Response(json.dumps(response),status=200,mimetype="application/json")
    
    return Response(json.dumps(response),status=400,mimetype="application/json")
# @app.route("/sendemail/", methods=['POST'])
# def sendemail():
#     if request.method == "POST":
#         name = request.form['name']
#         subject = request.form['Subject']
#         email = request.form['_replyto']
#         message = request.form['message']

#         your_name = "Emad"
#         your_email = "emadk3@gmail.com"
#         your_password = "Emmurules11"

#         # Logging in to our email account
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.ehlo()
#         server.starttls()
#         server.login(your_email, your_password)

#         # Sender's and Receiver's email address
#         sender_email = "emadk3@gmail.com"
#         receiver_email = "emadteaches@gmail.com"

#         msg = EmailMessage()
#         msg.set_content("First Name : "+str(name)+"\nEmail : "+str(email)+"\nSubject : "+str(subject)+"\nMessage : "+str(message))
#         msg['Subject'] = 'New Response on Personal Website'
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         # Send the message via our own SMTP server.
#         try:
#             # sending an email
#             server.send_message(msg)
#         except:
#             pass
#     return redirect('/')

if __name__=="__main__":
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)







