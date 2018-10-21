import yaml
import os
import re


# Handle !expr Sys.getenv calls in R configs to use environment variables
def expr_constructor(loader, node):
    value = loader.construct_scalar(node)
    pattern = re.compile("""Sys\.getenv\(['"](.*)['"]\)""")
    try:
        env_var = pattern.findall(value)[0]
        return os.environ[env_var]
    except IndexError:
        print("Config values with !expr only allowed for Sys.getenv! Parameter set to None")
        return None
    except KeyError:
        # noinspection PyUnboundLocalVariable
        print("Environment variable", env_var, "not set. Parameter set to None")
        return None


def load_config(yaml_input):
    yaml.add_constructor('!expr', expr_constructor, yaml.SafeLoader)
    yaml_load_raw = yaml.safe_load(yaml_input)
    cfg = yaml_load_raw["default"]
    cfg_active = get_active_config(yaml_load_raw)
    cfg.update(cfg_active)
    return cfg


def get_active_config(load_raw):
    try:
        return load_raw[os.environ["R_CONFIG_ACTIVE"]]
    except KeyError:
        return {}


try:
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")
    with open(config_path, "r") as yaml_file:
        config = load_config(yaml_file)
except FileNotFoundError:
    print("No config file config.yml in parent-parent directory of this module")
    config = {}
