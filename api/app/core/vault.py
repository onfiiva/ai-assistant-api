import json
import os
from typing import Any
import hvac


def get_vault_secret(path: str) -> dict:
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        return {}

    client = hvac.Client(
        url=vault_addr,
        token=vault_token
    )

    if not client.is_authenticated():
        raise RuntimeError("Vault authentication failed")

    # KV v2
    secret = client.secrets.kv.v2.read_secret_version(
        path=path,
        mount_point="secret"
    )

    return secret["data"]["data"]


def get_vault_list(
    vault_data: dict[str, Any],
    key: str,
    default: list[str] | None = None
) -> list[str]:
    """
    Returns list from Vault secret stored as JSON-str.
    """
    value = vault_data.get(key)
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return default or []
    return default or []
