import json


def load_config_variables(request):
    settings = {}

    with open("static/nfl/config/config.json", "r") as config:
        settings = json.load(config)

    return {'settings': settings}