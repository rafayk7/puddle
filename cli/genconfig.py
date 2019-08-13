import click
import json

@click.command()
@click.option('--config_path', default='config.json')
@click.option('--unique_name', prompt=True)
@click.option('--description', default="None", prompt=True)
@click.option('--use_cases', default="None", prompt=True)
@click.option('--model_file_path', default="model.pkl", prompt=True)
@click.option('--run_file__path', default="run.py", prompt=True)
@click.option('--input_type', default="text", prompt=True)

def test(config_path, unique_name,description, use_cases, model_file_path, run_file__path, input_type):
    config= {
        "Name" : unique_name,
        "Description" : description,
        "Input Type" : input_type,
        "Use Cases" : use_cases,
        "Model File Path" : model_file_path,
        "Run File Path" : run_file__path
    }

    with open(config_path, 'w+') as f:
        json.dump(config, f)

    print("Config file for {} has been created at {}".format(unique_name, config_path))

if __name__ == "__main__":
    test()