from solana.compute_budget import (RequestUnitsParams,RequestHeapFrameParams,
                                   SetComputeUnitLimitParams,
                                   SetComputeUnitPriceParams)
from solana.compute_budget import (decode_request_units,
                                   decode_request_heap_frame,
                                   decode_set_compute_unit_limit,
                                   decode_set_compute_unit_price)
from solana.compute_budget import (request_units,
                                   request_heap_frame,
                                   set_compute_unit_limit,
                                   set_compute_unit_price)


def test_request_units():
    """Test request units instruction."""
    params = RequestUnitsParams(units=150_000, additional_fee=1_000_000_000)
    assert decode_request_units(request_units(params)) == params

def test_request_heap_frame():
    """Test request heap frame instruction."""
    params = RequestHeapFrameParams(bytes=33*1024)
    assert decode_request_heap_frame(request_heap_frame(params)) == params
    
def test_set_compute_unit_limit():
    """Test set compute unit limit instruction."""
    params = SetComputeUnitLimitParams(units=150_000)
    assert decode_set_compute_unit_limit(set_compute_unit_limit(params)) == params
    
def test_set_compute_unit_price():
    """Test set compute unit price instruction."""
    params = SetComputeUnitPriceParams(micro_lamports=1_000_000_000)
    assert decode_set_compute_unit_price(set_compute_unit_price(params)) == params