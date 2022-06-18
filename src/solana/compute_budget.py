"""Library to interface with the compute budget program."""
from __future__ import annotations

from typing import Any, NamedTuple

from solana._layouts.compute_instructions import COMPUTE_BUDGET_INSTRUCTIONS_LAYOUT, InstructionType
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction
from solana.utils.validate import validate_instruction_type

COMPUTE_BUDGET_PROGRAM_ID: PublicKey = PublicKey("ComputeBudget111111111111111111111111111111")
"""Public key that identifies the Compute Budget program."""


class RequestUnitsParams(NamedTuple):
    """Request units instruction params."""

    units: int
    """Units to request for transaction-wide compute."""
    additional_fee: int
    """Prioritization fee lamports."""


class RequestHeapFrameParams(NamedTuple):
    """Request heap frame instruction params."""

    bytes: int
    """Requested transaction-wide program heap size in bytes.
    Must be multiple of 1024. Applies to each program, including CPIs.
    """


class SetComputeUnitLimitParams(NamedTuple):
    """Set compute unit limit instruction params."""

    units: PublicKey
    """Transaction-wide compute unit limit."""


class SetComputeUnitPriceParams(NamedTuple):
    """Set compute unit price instruction params."""

    micro_lamports: int
    """Transaction compute unit price used for prioritization fees."""


def __parse_and_validate_instruction(
    instruction: TransactionInstruction,
    expected_type: InstructionType,
) -> Any:  # Returns a Construct container.
    data = COMPUTE_BUDGET_INSTRUCTIONS_LAYOUT.parse(instruction.data)
    validate_instruction_type(data, expected_type)
    return data


def decode_request_units(instruction: TransactionInstruction) -> RequestUnitsParams:
    """Decode a request units instruction and retrieve the instruction params.

    Args:
        instruction: The instruction to decode.

    Returns:
        The decoded instruction.
    """
    parsed_data = __parse_and_validate_instruction(instruction, InstructionType.REQUEST_UNITS)
    return RequestUnitsParams(
        units=parsed_data.args.units,
        additional_fee=parsed_data.args.additional_fee,
    )


def decode_request_heap_frame(instruction: TransactionInstruction) -> RequestHeapFrameParams:
    """Decode a request heap frame instruction and retrieve the instruction params.

    Args:
        instruction: The instruction to decode.

    Returns:
        The decoded instruction.
    """
    parsed_data = __parse_and_validate_instruction(instruction, InstructionType.REQUEST_HEAP_FRAME)
    return RequestHeapFrameParams(bytes=parsed_data.args.bytes)


def decode_set_compute_unit_limit(instruction: TransactionInstruction) -> SetComputeUnitLimitParams:
    """Decode a set compute unit limit instruction and retrieve the instruction params.

    Args:
        instruction: The instruction to decode.

    Returns:
        The decoded instruction.
    """
    parsed_data = __parse_and_validate_instruction(instruction, InstructionType.SET_COMPUTE_UNIT_LIMIT)
    return SetComputeUnitLimitParams(units=parsed_data.args.units)


def decode_set_compute_unit_price(instruction: TransactionInstruction) -> SetComputeUnitPriceParams:
    """Decode a set compute unit price instruction and retrieve the instruction params.

    Args:
        instruction: The instruction to decode.

    Returns:
        The decoded instruction.
    """
    parsed_data = __parse_and_validate_instruction(instruction, InstructionType.SET_COMPUTE_UNIT_PRICE)
    return SetComputeUnitPriceParams(
        micro_lamports=parsed_data.args.micro_lamports,
    )


def request_units(params: RequestUnitsParams) -> TransactionInstruction:
    """Generate an instruction that requests units.

    Example:

        >>> instruction = request_units(
        ...    RequestUnitsParams(
        ...        units=150_000,
        ...        additional_fee=1_000_000_000,
        ...    )
        ... )
        >>> type(instruction)
        <class 'solana.transaction.TransactionInstruction'>

    Returns:
        The generated instruction.
    """
    data = COMPUTE_BUDGET_INSTRUCTIONS_LAYOUT.build(
        dict(
            instruction_type=InstructionType.REQUEST_UNITS,
            args=dict(units=params.units, additional_fee=params.additional_fee),
        )
    )

    return TransactionInstruction(
        keys=[],
        program_id=COMPUTE_BUDGET_PROGRAM_ID,
        data=data,
    )


def request_heap_frame(params: RequestHeapFrameParams) -> TransactionInstruction:
    """Generate an instruction that requests heap frame.

    Example:

        >>> instruction = request_heap_frame(
        ...    RequestHeapFrameParams(
        ...        bytes=33 * 1024,
        ...    )
        ... )
        >>> type(instruction)
        <class 'solana.transaction.TransactionInstruction'>

    Returns:
        The generated instruction.
    """
    data = COMPUTE_BUDGET_INSTRUCTIONS_LAYOUT.build(
        dict(instruction_type=InstructionType.REQUEST_HEAP_FRAME, args=dict(bytes=params.bytes))
    )

    return TransactionInstruction(
        keys=[],
        program_id=COMPUTE_BUDGET_PROGRAM_ID,
        data=data,
    )


def set_compute_unit_limit(params: SetComputeUnitLimitParams) -> TransactionInstruction:
    """Generate an instruction that sets compute unit limit.

    Example:

        >>> instruction = set_compute_unit_limit(
        ...    SetComputeUnitLimitParams(
        ...        units=50_000,
        ...    )
        ... )
        >>> type(instruction)
        <class 'solana.transaction.TransactionInstruction'>

    Returns:
        The generated instruction.
    """
    data = COMPUTE_BUDGET_INSTRUCTIONS_LAYOUT.build(
        dict(instruction_type=InstructionType.SET_COMPUTE_UNIT_LIMIT, args=dict(units=params.units))
    )

    return TransactionInstruction(
        keys=[],
        program_id=COMPUTE_BUDGET_PROGRAM_ID,
        data=data,
    )


def set_compute_unit_price(params: SetComputeUnitPriceParams) -> TransactionInstruction:
    """Generate an instruction that sets compute unit price.

    Example:

        >>> instruction = set_compute_unit_price(
        ...    SetComputeUnitPriceParams(
        ...        micro_lamports=100_000,
        ...    )
        ... )
        >>> type(instruction)
        <class 'solana.transaction.TransactionInstruction'>

    Returns:
        The generated instruction.
    """
    data = COMPUTE_BUDGET_INSTRUCTIONS_LAYOUT.build(
        dict(instruction_type=InstructionType.SET_COMPUTE_UNIT_PRICE, args=dict(micro_lamports=params.micro_lamports))
    )

    return TransactionInstruction(
        keys=[],
        program_id=COMPUTE_BUDGET_PROGRAM_ID,
        data=data,
    )
