"""Library to interface with system programs."""
from __future__ import annotations

from typing import Any, NamedTuple, Optional

from name_service._layouts import NAME_PROGRAM_INSTRUCTIONS_LAYOUT, InstructionType
from name_service.constants import NAME_PROGRAM_ID, REQ_INITIAL_ACCOUNT_BUFFER
from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import AccountMeta, TransactionInstruction
from solana.utils.validate import validate_instruction_keys, validate_instruction_type


# Instruction Params
class CreateNameParams(NamedTuple):
    """Create name account transaction params."""

    funding_account: PublicKey  # System Address
    hashed_name: bytes
    lamports: int
    space: int  # Storage space for arbitrary data
    owner_account: PublicKey  # Default: funding account
    class_account: PublicKey = SYS_PROGRAM_ID  # Signer
    parent_account: PublicKey = SYS_PROGRAM_ID
    parent_owner_account: PublicKey = SYS_PROGRAM_ID  # Signer, optional but needed if parent_account != default
    name_program_id: PublicKey = NAME_PROGRAM_ID


class UpdateNameParams(NamedTuple):
    """Update name account transaction params."""

    name_account: PublicKey  # Name account to modify
    offset: int
    input_data: bytes
    name_update_signer: PublicKey  # Owner account -- or class account if that's not default
    name_program_id: PublicKey = NAME_PROGRAM_ID


class TransferNameParams(NamedTuple):
    """Transfer name account transaction params."""

    name_account: PublicKey
    new_owner_account: PublicKey
    owner_account: PublicKey
    class_account: PublicKey = SYS_PROGRAM_ID
    name_program_id: PublicKey = NAME_PROGRAM_ID


class DeleteNameParams(NamedTuple):
    """Delete name account transaction params."""

    name_account: PublicKey
    owner_account: PublicKey
    refund_account: Optional[PublicKey] = None  # Default to owner
    name_program_id: PublicKey = NAME_PROGRAM_ID


def __parse_and_validate_instruction(
    instruction: TransactionInstruction,
    expected_keys: int,
    expected_type: InstructionType,
) -> Any:  # Returns a Construct container.
    """Parse and validate name service program instruction."""
    validate_instruction_keys(instruction, expected_keys)
    data = NAME_PROGRAM_INSTRUCTIONS_LAYOUT.parse(instruction.data)
    validate_instruction_type(data, expected_type)
    return data


def decode_create_name(instruction: TransactionInstruction) -> CreateNameParams:
    """Decode a create name instruction and retrieve the instruction params."""
    parsed_data = __parse_and_validate_instruction(instruction, 6, InstructionType.CREATE)
    return CreateNameParams(
        funding_account=instruction.keys[1].pubkey,
        hashed_name=parsed_data.args.hashed_name,
        owner_account=instruction.keys[3].pubkey,
        lamports=parsed_data.args.lamports,
        space=parsed_data.args.space - REQ_INITIAL_ACCOUNT_BUFFER,
        name_program_id=instruction.program_id,
    )


def decode_update_name(instruction: TransactionInstruction) -> UpdateNameParams:
    """Decode an update name instruction and retrieve the instruction params."""
    parsed_data = __parse_and_validate_instruction(instruction, 2, InstructionType.UPDATE)
    return UpdateNameParams(
        name_update_signer=instruction.keys[1].pubkey,
        name_account=instruction.keys[0].pubkey,
        offset=parsed_data.args.offset,
        input_data=parsed_data.args.input_data,
        name_program_id=instruction.program_id,
    )


def decode_transfer_name(instruction: TransactionInstruction) -> TransferNameParams:
    """Decode a transfer name instruction and retrieve the instruction params."""
    parsed_data = __parse_and_validate_instruction(instruction, 2, InstructionType.TRANSFER)
    return TransferNameParams(
        owner_account=instruction.keys[1].pubkey,
        new_owner_account=PublicKey(parsed_data.args.new_owner),
        name_account=instruction.keys[0].pubkey,
        class_account=SYS_PROGRAM_ID,
        name_program_id=instruction.program_id,
    )


def decode_delete_name(instruction: TransactionInstruction) -> DeleteNameParams:
    """Decode a delete name instruction and retrieve the instruction params."""
    return DeleteNameParams(
        owner_account=instruction.keys[1].pubkey,
        name_account=instruction.keys[0].pubkey,
        refund_account=instruction.keys[1].pubkey,
        name_program_id=instruction.program_id,
    )


def create_name(params: CreateNameParams) -> TransactionInstruction:
    """Generate an instruction that creates and funds a new name account."""
    data = NAME_PROGRAM_INSTRUCTIONS_LAYOUT.build(
        dict(
            instruction_type=InstructionType.CREATE,
            args=dict(
                hashed_name_size=len(params.hashed_name),
                hashed_name=params.hashed_name,
                lamports=params.lamports,
                space=params.space + REQ_INITIAL_ACCOUNT_BUFFER,
            ),
        )
    )
    name_record_pubkey, _ = PublicKey.find_program_address(
        [params.hashed_name, bytes(params.class_account), bytes(params.parent_account)], params.name_program_id
    )

    # Enforce specified parent owner account.
    if params.parent_account != SYS_PROGRAM_ID and params.parent_owner_account == SYS_PROGRAM_ID:
        raise ValueError("Must specify the supplied parent name account's owner account")
    keys = [
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=params.funding_account, is_signer=True, is_writable=True),
        AccountMeta(pubkey=name_record_pubkey, is_signer=False, is_writable=True),
        AccountMeta(pubkey=params.owner_account, is_signer=False, is_writable=False),
    ]
    # Class Account?
    if params.class_account != SYS_PROGRAM_ID:
        keys.append(AccountMeta(pubkey=params.class_account, is_signer=True, is_writable=False))
    else:
        keys.append(AccountMeta(pubkey=params.class_account, is_signer=False, is_writable=False))
    # Parent Account?  If so, then owner account as well.
    keys.append(AccountMeta(pubkey=params.parent_account, is_signer=False, is_writable=False))
    if params.parent_account != SYS_PROGRAM_ID:
        keys.append(AccountMeta(pubkey=params.parent_owner_account, is_signer=True, is_writable=False))
    return TransactionInstruction(
        keys=keys,
        program_id=params.name_program_id,
        data=data,
    )


def update_name(params: UpdateNameParams) -> TransactionInstruction:
    """Generate an instruction that updates a name account."""
    data = NAME_PROGRAM_INSTRUCTIONS_LAYOUT.build(
        dict(
            instruction_type=InstructionType.UPDATE,
            args=dict(offset=params.offset, size=len(params.input_data), input_data=params.input_data),
        )
    )
    keys = [
        AccountMeta(params.name_account, is_signer=False, is_writable=True),
        AccountMeta(params.name_update_signer, is_signer=True, is_writable=False),
    ]
    return TransactionInstruction(keys=keys, program_id=params.name_program_id, data=data)


def transfer_name(params: TransferNameParams) -> TransactionInstruction:
    """Generate an instruction that transfers a name account."""
    data = NAME_PROGRAM_INSTRUCTIONS_LAYOUT.build(
        dict(
            instruction_type=InstructionType.TRANSFER,
            args=dict(new_owner=bytes(params.new_owner_account)),
        )
    )
    keys = [
        AccountMeta(params.name_account, is_signer=False, is_writable=True),
        AccountMeta(params.owner_account, is_signer=True, is_writable=False),
    ]
    if params.class_account != SYS_PROGRAM_ID:
        keys.append(AccountMeta(params.class_account, is_signer=True, is_writable=False))
    return TransactionInstruction(keys=keys, program_id=params.name_program_id, data=data)


def delete_name(params: DeleteNameParams) -> TransactionInstruction:
    """Delete a name account created by SPL Name Service.

    If refund account is not specified, funds are returned to account owner.
    """
    data = NAME_PROGRAM_INSTRUCTIONS_LAYOUT.build(dict(instruction_type=InstructionType.DELETE, args={}))
    refund_account = params.refund_account or params.owner_account
    keys = [
        AccountMeta(params.name_account, is_signer=False, is_writable=True),
        AccountMeta(params.owner_account, is_signer=True, is_writable=False),
        AccountMeta(refund_account, is_signer=False, is_writable=True),
    ]
    return TransactionInstruction(keys=keys, program_id=params.name_program_id, data=data)
