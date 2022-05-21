"""Unit tests for solana.system_program."""
from name_service.name_program import (
    CreateNameParams,
    DeleteNameParams,
    TransferNameParams,
    UpdateNameParams,
    create_name,
    decode_create_name,
    decode_delete_name,
    decode_transfer_name,
    decode_update_name,
    delete_name,
    transfer_name,
    update_name,
)
from name_service.utils import get_hashed_name, get_name_account
from solana.keypair import Keypair


def test_create():
    """Test creating a name account."""
    funding_account = Keypair().public_key
    params = CreateNameParams(
        funding_account=funding_account,
        hashed_name=get_hashed_name("", "some_name12348364567"),
        lamports=123,
        owner_account=funding_account,
        space=len(get_hashed_name("", "some_name12348364567")),
    )
    assert decode_create_name(create_name(params)) == params


def test_update():
    """Test updating a name account."""
    params = UpdateNameParams(
        name_account=get_name_account("some_name12348364567"),
        offset=0,
        input_data=b"123",
        name_update_signer=Keypair().public_key,
    )
    assert decode_update_name(update_name(params)) == params


def test_transfer():
    """Test transfering a name account."""
    params = TransferNameParams(
        name_account=get_name_account("some_name12348364567"),
        new_owner_account=Keypair().public_key,
        owner_account=Keypair().public_key,
    )
    assert decode_transfer_name(transfer_name(params)) == params


def test_delete():
    """Test deleting a name account."""
    owner_account = Keypair().public_key
    params = DeleteNameParams(
        name_account=get_name_account("some_name12348364567"),
        owner_account=owner_account,
        refund_account=owner_account,
    )
    assert decode_delete_name(delete_name(params)) == params
