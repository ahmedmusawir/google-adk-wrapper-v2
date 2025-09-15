# config.py
import json
import os
import logging
from typing import Dict

def load_config() -> Dict[str, str]:
    """
    Loads config.json, gets the base URL for the current environment,
    and dynamically builds the agent registry.
    """
    env = os.getenv("APP_ENV", "local")
    logging.info(f"Loading configuration for environment: {env}")

    try:
        with open("config.json", "r") as f:
            config_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Could not load or parse 'config.json': {e}")
        return {}

    # Get the base URL for the current environment
    base_url = config_data.get("environments", {}).get(env, {}).get("adk_bundle_url")
    
    if not base_url:
        logging.warning(f"ADK bundle URL not found for environment '{env}'.")
        return {}

    # Dynamically build the registry using the list of agents
    agent_names = config_data.get("agents", [])
    agent_registry = {name: base_url for name in agent_names}
    
    logging.info(f"Successfully built agent registry with {len(agent_registry)} agents.")
    return agent_registry

AGENT_REGISTRY = load_config()