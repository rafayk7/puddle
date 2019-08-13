from flask import Flask, render_template, request
from Consts import Consts
from utils import get_db_info
import os
import pymysql.cursors
import json

app = Flask(__name__)

def get_db_conn():
        uname, dbname, pword, server, port = get_db_info()
        conn = pymysql.connect(host=server, port=port, user=uname, passwd=pword, db=dbname)
        return conn

@app.route('/models/<project_unique_name>', methods=['GET'])
def deploy(project_unique_name):
    title = project_unique_name
    heading = "RESNET 18 Text NLP Analysis"
    description = "This model does this htis this htis this text classification wowowowoowow"
    usecase = "used for news, news, news, news, news"
    authors = ['Rafay Kalim', 'Young Seok-Seo', 'Jay Mohile']
    type = 1

    return render_template('text_input_template.html', title=title, heading=heading, description=description,
                           usecase=usecase, authors=authors)
                           
@app.route('/models/add', methods=['POST'])
def add():
    data = request.data
    data = json.loads(data)
    print(data)
    conn = get_db_conn()

    insertSql = "INSERT INTO " \
                "`models_test`(`name`,`input_type`,`use_cases`, `model_s3`, `runfile_s3`, `description` ) " \
                "VALUES(%s,%s, %s, %s, %s, %s)"

    model_filename, model_file_extension = os.path.splitext(data['Model File Path'])
    s3_model_name = 'models/{}/model{}'.format(data['Name'], model_file_extension)
    s3_runfile_name = 'runfiles/{}/run.py'.format(data['Name'])

    with conn.cursor() as cursor:
        cursor.execute(insertSql, (data['Name'], data['Input Type'], data['Use Cases'], s3_model_name, s3_runfile_name, data['Description']))

    conn.commit()
    return {"added": "true"}

# Initiliaze Table
@app.route('/database/create', methods=['GET'])
def create():
    conn = get_db_conn()
    createSql = "CREATE " \
                "TABLE `models_test`(" \
                "`model_id` INT AUTO_INCREMENT, " \
                "`name` VARCHAR(255) NOT NULL," \
                "`input_type` VARCHAR(255) NOT NULL," \
                "`use_cases` TEXT," \
                "`model_s3` VARCHAR(255)," \
                "`runfile_s3` VARCHAR(255)," \
                "`description` TEXT," \
                "PRIMARY KEY (`model_id`));"
    insertSql = "INSERT INTO tasks(title,priority)VALUES(Learn MySQL INSERT Statement',1);"
    getSql = "SELECT * FROM tasks;"
    with conn.cursor() as cursor:
        cursor.execute(createSql)
    conn.commit()
    return {"table": "created"}


# For testing
@app.route('/get', methods=['GET'])
def get():
    conn = get_db_conn()
    getSql = "select * from `models_test`"
    with conn.cursor() as cursor:
        cursor.execute(getSql)
        result = cursor.fetchall()
        print(result)

    return {"RESULT": result}


@app.route('/run', methods=['POST'])
def run():
    prev_url = request.referrer
    data = request.form.get('text')

    print("came from {}".format(prev_url))
    print("said {}".format(data))

    return render_template('text_input_template.html', title='d', heading='ds', description='sda', usecase='dsvfds')


if __name__ == "__main__":
    app.run(debug=True)
