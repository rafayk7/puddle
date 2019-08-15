from flask import Flask, render_template, request
from Consts import Consts
from utils import get_db_info, get_s3_info
import os
import pymysql.cursors
import json
import boto3

app = Flask(__name__)


def get_db_conn():
        uname, dbname, pword, server, port = get_db_info()
        conn = pymysql.connect(host=server, port=port, user=uname, passwd=pword, db=dbname)
        return conn
def get_s3_conn():
    aws_key, aws_secret_key, bucket = get_s3_info()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret_key
    )

    return s3, bucket

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
    getDisplayData = "SELECT * FROM `models_test` WHERE `name`=%s"
    getAuthorData = "SELECT * FROM `author_models_test` WHERE `model_name`=%s"

    colsModels = get_table_info(conn, 'models_test')
    with conn.cursor() as cursor:
            cursor.execute(getDisplayData, (project_unique_name))
            projectData = cursor.fetchone()
            cursor.execute(getAuthorData, (project_unique_name))
            authorData = cursor.fetchall()

    authorNames = []
    for author in authorData:
        authorNames.append(author[2])
    col_names = []
    for col_info in colsModels:
            col_names.append(col_info[0])

    print(projectData)
    result_json = dict(zip(col_names, projectData))
    print(result_json)


    # return {
    #     'project' : result_json,
    #     'authors' : authorNames
    # }

    return render_template('text_input_template.html', title=result_json['name'], heading=result_json['name'], description=result_json['description'],
                           usecase=result_json['use_cases'], authors=authorNames, modelfile=result_json['model_s3'], runfile=result_json['runfile_s3'])


@app.route('/models/add', methods=['POST'])
def add():
    data = request.data
    data = json.loads(data)
    conn = get_db_conn()

    insertToModels = "INSERT INTO " \
                "`models_test`(`name`,`input_type`,`use_cases`, `model_s3`, `runfile_s3`, `description` ) " \
                "VALUES(%s,%s, %s, %s, %s, %s)"
    
    authors = data['Authors'] 
    insertToAuthors = "INSERT INTO `author_models_test`(`model_name`, `author_name`) VALUES(%s, %s)"
    author_id_list = []
    with conn.cursor() as cursor:
        for author in authors:
                try:
                        cursor.execute(insertToAuthors, (data['Name'], author))
                        author_id_list.append(conn.insert_id())
                except IndexError:
                        cursor.execute(insertToAuthors, (author.split(' ')[0], 'NaN'))
                        author_id_list.append(conn.insert_id())
        
    conn.commit()
    model_filename, model_file_extension = os.path.splitext(data['Model File Path'])
    s3_model_name = 'models/{}/model{}'.format(data['Name'], model_file_extension)
    s3_runfile_name = 'runfiles/{}/run.py'.format(data['Name'])

    with conn.cursor() as cursor:
        cursor.execute(insertToModels, (data['Name'], data['Input Type'], data['Use Cases'], s3_model_name, s3_runfile_name, data['Description']))

    conn.commit()
    return {"added": "true"}

@app.route('/test', methods=['GET'])
def getAuthors():
    conn = get_db_conn()
    sql = "SELECT * FROM `models_test`;"

    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    
    return {'result': result}

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
def createModelDB():
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
def createAuthorModelDB():
    conn = get_db_conn()
    createSql = "CREATE " \
                "TABLE `author_models_test`(" \
                "`author_id` INT AUTO_INCREMENT, " \
                "`model_name` VARCHAR(255) NOT NULL, " \
                "`author_name` VARCHAR(255) NOT NULL," \
                "PRIMARY KEY (`author_id`));"
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


@app.route('/text/run', methods=['POST'])
def runText():
    conn = get_db_conn()
    prev_url = request.referrer
    data = request.form.get('text')

    try:
        proj_name = prev_url.split('/')[4]
    except:
        return render_template('error_template.html')

    getDisplayData = "SELECT * FROM `models_test` WHERE `name`=%s"

    colsModels = get_table_info(conn, 'models_test')
    with conn.cursor() as cursor:
            cursor.execute(getDisplayData, (proj_name))
            projectData = cursor.fetchone()

    col_names = []
    for col_info in colsModels:
            col_names.append(col_info[0])

    result_json = dict(zip(col_names, projectData))
    print(result_json)

    run_path_s3 = result_json['runfile_s3']
    model_path_s3 = result_json['model_s3']

    model_filename, model_file_extension = os.path.splitext(os.path.abspath(result_json['model_s3']))

    s3, bucket = get_s3_conn()
    model_saved_file = "model{}".format(model_file_extension)
    s3.download_file(bucket, model_path_s3, model_saved_file)
    s3.download_file(bucket, run_path_s3, 'run.py')

    from run import run

    result = run(data)

    print(result)
    print("run file {}. model file {}".format(run_path_s3, model_path_s3))

    return render_template('text_input_template.html', title='d', heading='ds', description='sda', usecase='dsvfds')


if __name__ == "__main__":
    app.run(debug=True)
