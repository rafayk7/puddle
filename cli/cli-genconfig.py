import click
import boto3, botocore
from utils import get_s3_info

@click.command()
@click.option("--name", prompt="Your Project's Name",
              help="A unique name used to identify your project. Is not changeable later.")

def hello(name):
    # Make API Call
    click.echo("{} created.".format(name))

if __name__ == '__main__':
    hello()