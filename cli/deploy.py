import click
import boto3, botocore
from utils import get_s3_info, api_url
import json
import os
import requests

@click.command()
@click.option('--config_file_path', '-f', default="config.json")

def main(config_file_path):
    aws_key, aws_secret_key, bucket = get_s3_info()

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret_key
    )

    with open(config_file_path, 'r') as f:
        config = json.load(f)

    print(config)

    model_filename, model_file_extension = os.path.splitext(os.path.abspath(config['Model File Path']))
    print(model_filename)
    print(model_file_extension)
    # Upload the model and the runfile
    try:
        s3.upload_file(
            os.path.abspath(config['Model File Path']),
            bucket,
            'models/{}/model{}'.format(config['Name'], model_file_extension),
            ExtraArgs={
                "ACL": "public-read"
            }
        )

    except Exception as e:
        print("Error Uploading model : ", e)
        return e

    try:
        s3.upload_file(
            os.path.abspath(config['Run File Path']),
            bucket,
            'runfiles/{}/run.py'.format(config['Name']),
            ExtraArgs={
                "ACL": "public-read"
            }
        )

    except Exception as e:
        print("Error Uploading run file : ", e)
        return e

    click.echo("Model file {} and run file {} for {} uploaded".format(config["Model File Path"], config['Run File Path'], config["Name"]))

    # Call API for Uploading to DB
    r = requests.post(url = "{}/models/add".format(api_url), json=config)
    click.echo("Your personal webpage is available at {}".format("{}/models/{}".format(api_url, config['Name'])))
    
if __name__ == "__main__":
    main()