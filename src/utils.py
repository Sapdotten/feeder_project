import yaml


def get_yaml(path: str) -> dict:
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config
