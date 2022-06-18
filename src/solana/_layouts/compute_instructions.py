"""Byte layouts for compute budget program instructions."""
from enum import IntEnum

from construct import Switch  # type: ignore
from construct import Int32ul, Int64ul
from construct import Struct as cStruct


class InstructionType(IntEnum):
    """Instruction types for compute budget program."""

    REQUEST_UNITS = 0
    REQUEST_HEAP_FRAME = 1
    SET_COMPUTE_UNIT_LIMIT = 2
    SET_COMPUTE_UNIT_PRICE = 3


REQUEST_UNITS = cStruct("units" / Int32ul, "additional_fee" / Int32ul)
REQUEST_HEAP_FRAME = cStruct("bytes" / Int32ul)
SET_COMPUTE_UNIT_LIMIT = cStruct("units" / Int32ul)
SET_COMPUTE_UNIT_PRICE = cStruct("micro_lamports" / Int64ul)

COMPUTE_BUDGET_INSTRUCTIONS_LAYOUT = cStruct(
    "instruction_type" / Int32ul,
    "args"
    / Switch(
        lambda this: this.instruction_type,
        {
            InstructionType.REQUEST_UNITS: REQUEST_UNITS,
            InstructionType.REQUEST_HEAP_FRAME: REQUEST_HEAP_FRAME,
            InstructionType.SET_COMPUTE_UNIT_LIMIT: SET_COMPUTE_UNIT_LIMIT,
            InstructionType.SET_COMPUTE_UNIT_PRICE: SET_COMPUTE_UNIT_PRICE,
        },
    ),
)
