import json

def get_settings():
    """Parses the settings from redis-live.conf.
    """
    # TODO: Consider YAML. Human writable, machine readable.
    return json.load(open("cheapec2.conf"))

def get_dbdriver():
    config = get_settings()
    return config["dbdriver"]

def get_awskey():
    config = get_settings()
    return config["aws"]
