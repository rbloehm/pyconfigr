from pyconfigr import load_config
import os


def test_load_config_simple():
    yaml_file = """
    default:
      simple: test
      simpler: "test"
    """
    config = load_config(yaml_file)
    assert config["simple"] == "test"
    assert config["simpler"] == "test"


def test_load_config_envconfig(monkeypatch):
    monkeypatch.setenv("R_CONFIG_ACTIVE", "production")
    yaml_file = """
    default:
      trials: 5
      simple: test
    production:
      trials: 30
      foo: bar
    """
    config = load_config(yaml_file)
    assert config["simple"] == "test"
    assert config["trials"] == 30
    assert config["foo"] == "bar"


def test_load_config_env(monkeypatch):
    monkeypatch.setenv("ENABLE_DEBUG", "enabled")
    yaml_file = """
    default:
      debug: !expr Sys.getenv("ENABLE_DEBUG")
      debug2: !expr Sys.getenv('ENABLE_DEBUG')
    """
    config = load_config(yaml_file)
    assert config["debug"] == "enabled"
    assert config["debug2"] == "enabled"


def test_load_config_env_missing(monkeypatch):
    monkeypatch.delenv("ENABLE_DEBUG", raising=False)
    yaml_file = """
    default:
      debug: !expr Sys.getenv("ENABLE_DEBUG")
    """
    config = load_config(yaml_file)
    assert config["debug"] is None


def test_load_config_expr_invalid(monkeypatch):
    yaml_file = """
    default:
      debug: !expr paste0(1, 2)
    """
    config = load_config(yaml_file)
    assert config["debug"] is None
