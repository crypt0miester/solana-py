"""Tests for the Memo program."""
import pytest

from spl.memo.constants import MEMO_PROGRAM
from spl.memo.memo_program import MemoParams, memo_instruction
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.commitment import Finalized
from solana.transaction import Transaction

from .utils import assert_valid_response


@pytest.mark.integration
def test_send_memo_in_transaction(stubbed_sender: Keypair, test_http_client: Client):
    """Test sending a memo instruction to localnet."""
    raw_message = "test"
    message = bytes(raw_message, encoding="utf8")
    # Create memo params
    memo_params = MemoParams(
        stubbed_sender.public_key,
        message,
    )
    # Create memo instruction
    memo_ix = memo_instruction(memo_params)
    # Create transfer tx to add memo to transaction from stubbed sender
    transfer_tx = Transaction().add(memo_ix)
    resp = test_http_client.send_transaction(transfer_tx, stubbed_sender)
    assert_valid_response(resp)
    txn_id = resp["result"]
    test_http_client.confirm_transaction(txn_id)
    resp2 = test_http_client.get_transaction(txn_id, commitment=Finalized, encoding="jsonParsed")
    log_message = resp2["result"]["meta"]["logMessages"][2].split('"')
    assert log_message[1] == raw_message
    assert resp2["result"]["transaction"]["message"]["instructions"][0]["parsed"] == raw_message
    assert resp2["result"]["transaction"]["message"]["instructions"][0]["programId"] == str(MEMO_PROGRAM)


@pytest.mark.integration
def test_send_invalid_memo_in_transaction(stubbed_sender: Keypair, test_http_client: Client):
    """Test sending an invalid memo instruction to localnet."""
    message = "test"
    # Create memo params
    memo_params = MemoParams(
        stubbed_sender.public_key,
        message,
    )
    # Create memo instruction
    memo_ix = memo_instruction(memo_params)
    # Create transfer tx to add memo to transaction from stubbed sender
    transfer_tx = Transaction().add(memo_ix)
    with pytest.raises(TypeError):
        test_http_client.send_transaction(transfer_tx, stubbed_sender)
