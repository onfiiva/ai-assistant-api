

def validate_generation_config(config: dict | None) -> dict:
    if not config:
        return {}

    validated = {}

    if "temperature" in config:
        validated["temperature"] = config["temperature"]

    if "top_p" in config:
        validated["top_p"] = config["top_p"]

    if "max_tokens" in config:
        validated["max_tokens"] = config["max_tokens"]

    return validated
