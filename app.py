from flask import Flask, render_template, jsonify, request
from chatbot import replyGenerator
from datetime import datetime 

app = Flask(__name__)


@app.route('/')
def index():

	return render_template('index2.html')


@app.route('/update', methods = ['POST'])
def update():

	text = request.form['text']

	modelpath = "data/chatbot v1 2021-05-28 21_06 (32,50).h5"
	reply = replyGenerator(str(text), modelpath)

	date = str(datetime.now())[8:10] + "-" + str(datetime.now())[5:7] + "-"+ str(datetime.now())[:4]
	parts = modelpath.split(' ')
	filename = parts[0] +' '+ parts[1] +' '+ date

	file = open(filename, encoding = 'utf-8', mode= 'a')
	file.write('User: ' + str(text) + '\n')
	file.write('Comp: '+ str(reply) + '\n\n')
	file.close()
	
	return jsonify({'data':reply})

if __name__=='__main__':
	app.run(debug=True, port = 5000)
	