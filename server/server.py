from flask import Flask, render_template, request
from Consts import Consts
from utils import get_db_info
import os


app = Flask(__name__)

@app.route('/models/<project_unique_name>')
def deploy(project_unique_name):
        title = project_unique_name
        heading = "RESNET 18 Text NLP Analysis"
        description = "This model does this htis this htis this text classification wowowowoowow"
        usecase = "used for news, news, news, news, news"
        authors = ['Rafay Kalim', 'Young Seok-Seo', 'Jay Mohile']
        type = 1

        return render_template('text_input_template.html', title=title, heading=heading, description=description, usecase=usecase, authors=authors)

@app.route('/models/add', methods=['POST'])
def add():
        return "sa"


@app.route('/run', methods=['POST'])
def run():
        prev_url = request.referrer
        data = request.form.get('text')

        print("came from {}".format(prev_url))
        print("said {}".format(data))

        return render_template('text_input_template.html', title='d', heading='ds', description='sda', usecase='dsvfds')

if __name__=="__main__":
    app.run(debug=True)