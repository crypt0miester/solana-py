from based58 import b58encode

from solana.keypair import Keypair
from spl.memo.constants import MEMO_PROGRAM
from spl.memo.memo_program import MemoParams, decode_memo_instruction, memo_instruction


def test_memo():
    """Test creating a memo instruction."""
    params = MemoParams(signer=Keypair().public_key, message=b58encode(b"test"), memo_program_id=MEMO_PROGRAM)
    assert decode_memo_instruction(memo_instruction(params)) == params
