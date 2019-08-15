![alt text](puddle.png)

### What it is
Puddle is a Python package and CLI that allows Machine Learning developers and enthusiasts to quickly and easily host their models, with a beautiful UI to showcase their models, with just one command

### How to use
1. Simply install the package using Pip,
2. Create a config.json file using `puddle gen-config -m proj-name` OR create a config.json manually
3. Deploy using `puddle deploy -f config.json`
4. Your unique webpage link will be displayed, usually oururl. com/models/proj-name

### Why this exists
There are too many models floating around online unused, that can be used by everyday people if the ML engineers had an easy way to share them. This takes care of the front-end, back-end component, and provides incredibly flexibility to engineers to be able to share their models easily. Think of it like the Github of Machine Learning Models. 

## TODO
1. Make model display page prettier
2. Make landing page for project
3. Create pipeline when user attempts to use model
   1. Accept Input,
   2. Validate input,
   3. Run input through run file,
   4. Get result,
   5. Display result

# How to contribute
1. Set up an SQL database here - https://remotemysql.com/
2. Get the username, password, dbname, server and port
3. Set up an Amazon S3 account
4. Get the AWS key, AWS Secret key, bucket name that you choose
5. Clone this repo
6. Create a file server/keys.txt, with the following format
```
USERNAME=your_db_username
DBNAME=your_db_name
PASSWORD=your_db_password
SERVER=remotemysql.com
PORT=your_db_port
AWS_KEY=your_aws_key
AWS_SECRET_KEY=your_aws_secret_key
BUCKET_NAME=your_bucket_name
```
7. Run cli/gen-config.py
8. Run cli/deploy.py
9. Run server/server.py
10. See if everything works like it should by clicking on the link displayed by cli/deploy.py
11. Start coding :)

