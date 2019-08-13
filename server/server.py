from flask import Flask, render_template, request
from Consts import Consts
from utils import get_db_info
import os
import pymysql.cursors

app = Flask(__name__)

def get_db_conn():
        uname, dbname, pword, server, port = get_db_info()
        conn = pymysql.connect(host=server, port=port, user=uname, passwd=pword, db=dbname)
        return conn

@app.route('/models/<project_unique_name>')
def deploy(project_unique_name):
    title = project_unique_name
    heading = "RESNET 18 Text NLP Analysis"
    description = "This model does this htis this htis this text classification wowowowoowow"
    usecase = "used for news, news, news, news, news"
    authors = ['Rafay Kalim', 'Young Seok-Seo', 'Jay Mohile']
    type = 1

    return render_template('text_input_template.html', title=title, heading=heading, description=description,
                           usecase=usecase, authors=authors)


@app.route('/create', methods=['GET'])
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
                "PRIMARY KEY (`task_id`));"
    insertSql = "INSERT INTO tasks(title,priority)VALUES(Learn MySQL INSERT Statement',1);"
    getSql = "SELECT * FROM tasks;"
    with conn.cursor() as cursor:
        cursor.execute(createSql)
    conn.commit()
    return {"table": "created"}


@app.route('/add', methods=['POST'])
def add():
    data = request.data
    conn = get_db_conn()
    createSql = "CREATE TABLE IF NOT EXISTS tasks (task_id INT AUTO_INCREMENT, title VARCHAR(255) " \
                "NOT NULL,start_date DATE,due_date DATE,priority TINYINT NOT NULL DEFAULT 3,description " \
                "TEXT,PRIMARY KEY (task_id));"
    insertSql = "INSERT INTO `tasks`(`title`,`priority`) VALUES(%s,%s)"
    getSql = "SELECT * FROM tasks;"
    with conn.cursor() as cursor:
        cursor.execute(insertSql, ("lmaooo", 2))

    conn.commit()
    return {"added": "true"}


@app.route('/get', methods=['GET'])
def get():
    conn = get_db_conn()
    createSql = "CREATE TABLE IF NOT EXISTS tasks (task_id INT AUTO_INCREMENTtitle VARCHAR(255) NOT NULL,start_date DATE,due_date DATE,priority TINYINT NOT NULL DEFAULT 3,description TEXT,PRIMARY KEY (task_id));"
    insertSql = "INSERT INTO tasks(title,priority)VALUES(Learn MySQL INSERT Statement',1);"
    getSql = "select * from `tasks`"
    with conn.cursor() as cursor:
        cursor.execute(getSql)
        result = cursor.fetchone()
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
