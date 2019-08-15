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

def get_table_info(conn, table_name):
        uname, dbname, pword, server, port = get_db_info()
        getCols = "SHOW COLUMNS FROM {}".format(table_name)
        with conn.cursor() as cursor:
                cursor.execute(getCols)
                result = cursor.fetchall()
        return result


@app.route('/models/<project_unique_name>', methods=['GET'])
def deploy(project_unique_name):
    conn = get_db_conn()
    getSql = "SELECT * FROM `models_test` WHERE `name`=%s"
    cols = get_table_info(conn, 'models_test')
    with conn.cursor() as cursor:
            cursor.execute(getSql, (project_unique_name))
            result = cursor.fetchone()

    col_names = []
    for col_info in cols:
            col_names.append(col_info[0])

    result_json = dict(zip(col_names, result))

    heading = "RESNET 18"
    authors = ['Rafay Kalim', 'Maggie Vuong']

    return render_template('text_input_template.html', title=result_json['name'], heading=heading, description=result_json['description'],
                           usecase=result_json['use_cases'], authors=authors)


@app.route('/models/add', methods=['POST'])
def add():
    data = request.data
    data = json.loads(data)
    conn = get_db_conn()

    insertToModels = "INSERT INTO " \
                "`models_test_2`(`name`,`input_type`,`use_cases`, `model_s3`, `runfile_s3`, `description` ) " \
                "VALUES(%s,%s, %s, %s, %s, %s)"
    authors = data['Authors']
    
    insertToAuthors = "INSERT INTO `authors_test`(`first_name`, `last_name`) VALUES(%s, %s) ON DUPLICATE KEY `author_id` = `author_id`"
    insertToAuthorModel = "INSERT INTO `author_models`(`author_id`, `model_name`) VALUES(%s, %s)"
    author_id_list = []
    with conn.cursor() as cursor:
        for author in authors:
                try:
                        cursor.execute(insertToAuthors, (author.split(' ')[0], author.split(' ')[1]))
                        author_id_list.append(conn.insert_id())
                except IndexError:
                        cursor.execute(insertToAuthors, (author.split(' ')[0], 'NaN'))
                        author_id_list.append(conn.insert_id())
        for id in author_id_list:
                


    conn.commit()
    model_filename, model_file_extension = os.path.splitext(data['Model File Path'])
    s3_model_name = 'models/{}/model{}'.format(data['Name'], model_file_extension)
    s3_runfile_name = 'runfiles/{}/run.py'.format(data['Name'])

    with conn.cursor() as cursor:
        cursor.execute(insertSql, (data['Name'], data['Input Type'], data['Use Cases'], s3_model_name, s3_runfile_name, data['Description']))

    conn.commit()
    return {"added": "true"}

# Initialize Authors Table
@app.route('/database/authors/create', methods=['GET'])
def create():
    conn = get_db_conn()
    createSql = "CREATE " \
                "TABLE `authors_test`(" \
                "`author_id` INT AUTO_INCREMENT, " \
                "`first_name` VARCHAR(255) NOT NULL," \
                "`last_name` VARCHAR(255) NOT NULL," \
                "PRIMARY KEY (`author_id`));"
    insertSql = "INSERT INTO tasks(title,priority)VALUES(Learn MySQL INSERT Statement',1);"
    getSql = "SELECT * FROM tasks;"
    with conn.cursor() as cursor:
        cursor.execute(createSql)
    conn.commit()
    return {"table": "created"}

# Initialize Models Table
@app.route('/database/models/create', methods=['GET'])
def create():
    conn = get_db_conn()
    createSql = "CREATE " \
                "TABLE `models_test_2`(" \
                "`model_id` INT AUTO_INCREMENT, " \
                "`name` VARCHAR(255) NOT NULL," \
                "`input_type` VARCHAR(255) NOT NULL," \
                "`use_cases` TEXT," \
                "`model_s3` VARCHAR(255)," \
                "`runfile_s3` VARCHAR(255)," \
                "`description` TEXT," \
                "PRIMARY KEY (`model_id`));"

                with conn.cursor() as cursor:
        cursor.execute(createSql)
    conn.commit()
    return {"table": "created"}

# Initialize Author/Model Table
@app.route('/database/authors_models/create', methods=['GET'])
def create():
    conn = get_db_conn()
    createSql = "CREATE " \
                "TABLE `author_models`(" \
                "`author_id` INT NOT NULL, " \
                "`model_name` VARCHAR(255) NOT NULL," \
                "PRIMARY KEY (`author_id`, `model_name`));"
    with conn.cursor() as cursor:
        cursor.execute(createSql)
    conn.commit()
    return {"table": "created"}

# For testing
@app.route('/models', methods=['GET'])
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
