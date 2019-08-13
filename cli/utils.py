def get_s3_info():
    aws_key = ""
    aws_secret_key = ""
    bucket_name = ""

    '''
        keys.txt looks like 
            USERNAME=username
            DBNAME=dbname
            PASSWORD=password
            SERVER=server
            PORT=port 
            AWS_KEY=aws_key
            AWS_SECRET_KEY=aws_secret_key
            BUCKET_NAME=bucket_name
    '''

    with open('../server/keys.txt', 'r') as f:
        lines = f.readlines()
        lines = [x.replace('\n', '').split('=')[1] for x in lines]
        aws_key = lines[5]
        aws_secret_key = lines[6]
        bucket_name = lines[7]

        return aws_key, aws_secret_key, bucket_name

api_url = "http://localhost:5000"