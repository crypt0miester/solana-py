"""Tests for the Memo program."""
import pytest

from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.commitment import Finalized
from solana.transaction import Transaction

from .utils import AIRDROP_AMOUNT, assert_valid_response
from solana.compute_budget import (RequestUnitsParams,RequestHeapFrameParams,
                                   SetComputeUnitLimitParams,
                                   SetComputeUnitPriceParams)
from solana.compute_budget import (request_units,
                                   request_heap_frame,
                                   set_compute_unit_limit,
                                   set_compute_unit_price)


@pytest.mark.integration
def test_request_units_in_transaction(stubbed_sender_compute_budget: Keypair, test_http_client: Client):
    """Test sending a memo instruction to localnet."""
    resp = test_http_client.request_airdrop(stubbed_sender_compute_budget.public_key, AIRDROP_AMOUNT)
    print(stubbed_sender_compute_budget.public_key)
    test_http_client.confirm_transaction(resp["result"], Finalized)
    # Create memo params    
    params = RequestUnitsParams(units=150_000, additional_fee=1_000_000_000)

    # Create memo instruction
    request_units_ix = request_units(params)
    # Create transfer tx to add memo to transaction from stubbed sender
    transfer_tx = Transaction().add(request_units_ix)
    resp = test_http_client.send_transaction(transfer_tx, stubbed_sender_compute_budget)
    print(resp)
    assert_valid_response(resp)


# @pytest.mark.integration
# def test_send_invalid_memo_in_memo_params(stubbed_sender: Keypair):
#     """Test creating a string message instead of bytes for the message."""
#     message = "test"
#     with pytest.raises(TypeError):
#         memo_params = MemoParams(
#             program_id=MEMO_PROGRAM_ID,
#             signer=stubbed_sender.public_key,
#             message=message,
#         )
#         memo_ix = create_memo(memo_params)
#         # The test will fail here.
#         Transaction().add(memo_ix)
