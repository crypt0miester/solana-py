"""Library to interface with Memo program."""
from __future__ import annotations

from typing import NamedTuple

from spl.memo.constants import MEMO_PROGRAM
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction


# Instruction Params
class MemoParams(NamedTuple):
    """Create name account transaction params."""

    signer: PublicKey
    message: bytes
    memo_program_id: PublicKey = MEMO_PROGRAM


def decode_memo_instruction(instruction: TransactionInstruction) -> MemoParams:
    """Decode a create memo instruction and retrieve the instruction params."""
    return MemoParams(
        signer=instruction.keys[0].pubkey, message=instruction.data, memo_program_id=instruction.program_id
    )


def memo_instruction(params: MemoParams) -> TransactionInstruction:
    """Generate an instruction that creates the memo."""
    keys = [
        AccountMeta(pubkey=params.signer, is_signer=True, is_writable=True),
    ]
    return TransactionInstruction(
        keys=keys,
        program_id=params.memo_program_id,
        data=params.message,
    )
