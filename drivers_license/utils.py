import os
from dotenv import load_dotenv

from django.core.exceptions import ImproperlyConfigured

# Load environment variables
load_dotenv()


def get_env_variable(var_name) :
    """Get an environment variable or raise an exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


def get_bool_env(env_var) -> bool:
    """Parse 'boolean' environment variable strings."""
    return os.getenv(env_var, "False") == "True"

SECRET_KEY = get_env_variable("SECRET_KEY")

# cors_utils.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_cors_allow_all_origins():
    """
    Get the CORS_ALLOW_ALL_ORIGINS setting from environment variables.
    Returns True if the environment variable is set to 'True' (case insensitive),
    False otherwise.
    """
    return os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() == 'true'