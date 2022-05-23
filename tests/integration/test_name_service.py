"""Tests for the Name Service Program program."""
import pytest

from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction
from spl.name_service.constants import NAME_PROGRAM_HASH_PREFIX, REQ_INITIAL_ACCOUNT_BUFFER
from spl.name_service.name_program import (  # DeleteNameParams,; TransferNameParams,; delete_name,; transfer_name,
    CreateNameParams,
    UpdateNameParams,
    create_name,
    update_name,
)
from spl.name_service.utils import get_hashed_name, get_name_account, get_name_data

from .utils import assert_valid_response


@pytest.mark.integration
def test_create_name_account(stubbed_sender: Keypair, name_service_name: str, test_http_client: Client):
    """Test creating a name service to localnet."""
    space = len(name_service_name) + REQ_INITIAL_ACCOUNT_BUFFER
    min_rent = test_http_client.get_minimum_balance_for_rent_exemption(space + 32 + 32 + 32)

    # Create create name instruction
    create_name_params = CreateNameParams(
        funding_account=stubbed_sender.public_key,
        hashed_name=get_hashed_name(NAME_PROGRAM_HASH_PREFIX, name_service_name),
        lamports=min_rent["result"],
        space=space,
        owner_account=stubbed_sender.public_key,
    )
    create_name_ix = create_name(create_name_params)

    # Create transfer tx to create a name service
    create_name_tx = Transaction().add(create_name_ix)
    resp = test_http_client.send_transaction(create_name_tx, stubbed_sender)
    assert_valid_response(resp)

    txn_id = resp["result"]
    test_http_client.confirm_transaction(txn_id)
    # _ due to data not being populated yet
    _, owner = get_name_data(test_http_client, get_name_account(name=name_service_name))
    assert owner == stubbed_sender.public_key


@pytest.mark.integration
def test_update_name_account(
    stubbed_sender: Keypair, name_service_name: str, name_service_data: str, test_http_client: Client
):
    """Test creating a name service to localnet."""
    # Create update name instruction
    update_name_params = UpdateNameParams(
        name_account=get_name_account(name=name_service_name),
        offset=REQ_INITIAL_ACCOUNT_BUFFER,
        input_data=name_service_data.encode(),
        name_update_signer=stubbed_sender.public_key,
    )
    update_name_ix = update_name(update_name_params)

    # Create transfer tx to update a name service
    update_name_tx = Transaction().add(update_name_ix)
    resp = test_http_client.send_transaction(update_name_tx, stubbed_sender)
    assert_valid_response(resp)

    txn_id = resp["result"]
    test_http_client.confirm_transaction(txn_id)
    data, owner = get_name_data(test_http_client, get_name_account(name_service_name))
    assert owner == stubbed_sender.public_key
    assert data == name_service_data
