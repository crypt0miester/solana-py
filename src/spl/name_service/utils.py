"""Memo program utils."""
from base64 import b64decode
from hashlib import sha256
from typing import Tuple, Union

from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.system_program import SYS_PROGRAM_ID

from .constants import NAME_PROGRAM_HASH_PREFIX, NAME_PROGRAM_ID, REQ_INITIAL_ACCOUNT_BUFFER


def get_hashed_name(hash_prefix: str, name: str) -> bytes:
    """Get name-based hash used in seeding the derivation of a program address."""
    return sha256((hash_prefix + name).encode()).digest()


def get_name_account(
    name: str,
    class_account: PublicKey = SYS_PROGRAM_ID,
    parent_account: PublicKey = SYS_PROGRAM_ID,
    hash_prefix: str = NAME_PROGRAM_HASH_PREFIX,
) -> PublicKey:
    """Calculate the name account based on necessary parameters."""
    hashed_name = get_hashed_name(hash_prefix, name)
    account, _ = PublicKey.find_program_address(
        [hashed_name, bytes(class_account), bytes(parent_account)], NAME_PROGRAM_ID
    )
    return account


def get_name_data(client: Client, account: PublicKey) -> Tuple[Union[str, None], Union[PublicKey, None]]:
    """Look up account data, deserialize it."""
    response = client.get_account_info(account, encoding="jsonParsed")
    value = response["result"]["value"]
    if value is None:
        print(f"{account} not found")
        return None, None
    encoded_data = value["data"][0]
    raw_data = b64decode(encoded_data)
    name_owner_raw = raw_data[32:64]
    name_owner_public_key = PublicKey(name_owner_raw)
    data = raw_data[REQ_INITIAL_ACCOUNT_BUFFER:]
    return data.decode(), name_owner_public_key


async def async_get_name_data(
    client: AsyncClient, account: PublicKey
) -> Tuple[Union[str, None], Union[PublicKey, None]]:
    """Look up account data using async client, deserialize it."""
    response = await client.get_account_info(account, encoding="jsonParsed")
    value = response["result"]["value"]
    if value is None:
        print(f"{account} not found")
        return None, None
    encoded_data = value["data"][0]
    raw_data = b64decode(encoded_data)
    name_owner_raw = raw_data[32:64]
    name_owner_public_key = PublicKey(name_owner_raw)
    data = raw_data[REQ_INITIAL_ACCOUNT_BUFFER:]
    return data.decode(), name_owner_public_key
