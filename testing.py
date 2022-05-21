from memo.constants import MEMO_PROGRAM
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from solana.rpc.api import Client
from based58 import b58decode
from solana.blockhash import Blockhash
import asyncio
from base64 import b64decode
from memo.memo_program import MemoParams, memo_instruction

api_endpoint = "https://api.devnet.solana.com"


async def send_memo():
    memoer_raw_priv_key = b"FVGpgVbCjUGoMVXfBz39fLsLi7EhHL2bcAdBnnDHfECgjW5wDjkr57bJ7km7h8SUQA3CxnimMKLqkSYt2YQPhzN"
    decoded = b58decode(memoer_raw_priv_key)
    memoer_priv_key = Keypair.from_secret_key(bytes(decoded))
    memoer_public_key = memoer_priv_key.public_key
    print(memoer_public_key)
    client = AsyncClient(api_endpoint)
    txn = Transaction()
    message = "testing"
    data = message.encode()
    memo_params = MemoParams(memoer_public_key, data, MEMO_PROGRAM)
    memo_ix = memo_instruction(memo_params)
    txn.add(memo_ix)
    blockhash_resp = await client.get_recent_blockhash()
    txn.recent_blockhash = Blockhash(blockhash_resp["result"]["value"]["blockhash"])
    send_txn = await client.send_transaction(txn, *[memoer_priv_key])
    txn_id = send_txn["result"]
    # print(send_txn)
    # print(txn_id)
    await asyncio.sleep(1)
    confirm_txn = await client.confirm_transaction(txn_id)
    # print(confirm_txn)
    resp = await client.get_transaction(txn_id, encoding="jsonParsed")
    print(resp["result"])
    log_message = resp["result"]["meta"]["logMessages"][2].split('"')
    print(log_message)
    print(log_message[1] == "testing")
    # print("testing" in resp['result']['meta']['logMessages'][2])
    print(resp["result"]["transaction"]["message"]["instructions"][0]["parsed"])
    print(resp["result"]["transaction"]["message"]["instructions"][0]["programId"])
    await client.close()


def get_name_data(client, account):
    """
    Look up account data, deserialize it.
    """
    response = client.get_account_info(account, encoding="jsonParsed")
    value = response["result"]["value"]
    if value is None:
        print(f"{account} not found")
        return None
    data = value["data"][0]
    data = b64decode(data)
    data = data[96:]
    return data


async def create_name_spl():
    """
    Look up account data, deserialize it.
    """
    memoer_raw_priv_key = b"FVGpgVbCjUGoMVXfBz39fLsLi7EhHL2bcAdBnnDHfECgjW5wDjkr57bJ7km7h8SUQA3CxnimMKLqkSYt2YQPhzN"
    decoded = b58decode(memoer_raw_priv_key)
    memoer_priv_key = Keypair.from_secret_key(bytes(decoded))
    memoer_public_key = memoer_priv_key.public_key
    print(memoer_public_key)
    client = AsyncClient(api_endpoint)
    txn = Transaction()
    message = "testing"
    data = message.encode()
    memo_params = MemoParams(memoer_public_key, data, MEMO_PROGRAM)
    memo_ix = memo_instruction(memo_params)
    txn.add(memo_ix)
    blockhash_resp = await client.get_recent_blockhash()
    txn.recent_blockhash = Blockhash(blockhash_resp["result"]["value"]["blockhash"])
    send_txn = await client.send_transaction(txn, *[memoer_priv_key])
    txn_id = send_txn["result"]
    print(txn_id)
    await asyncio.sleep(1)
    confirm_txn = await client.confirm_transaction(txn_id)
    print(confirm_txn)
    await client.close()


t = get_name_data(
    Client("https://api.mainnet-beta.solana.com"), PublicKey("5jh8G8S4XFUT9Qsqj7WuDpDtH5K34G47JFFiVyct6BGy")
)
print(t.decode())
# asyncio.run(send_memo())
# t = b"message"
# print(t.encode())
# print(b58decode(t))
# print(b58encode(t.encode()))
