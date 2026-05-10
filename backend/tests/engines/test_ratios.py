import pytest
from engines.ratios.profitability import calculate_roe, calculate_roce
from engines.ratios.valuation import calculate_pe, calculate_pb
from engines.ratios.growth import calculate_cagr

def test_calculate_roe():
    assert calculate_roe(10, 100) == 10.0
    assert calculate_roe(None, 100) is None
    assert calculate_roe(10, 0) is None

def test_calculate_roce():
    assert calculate_roce(15, 150) == 10.0
    assert calculate_roce(15, -10) is None

def test_calculate_pe():
    assert calculate_pe(100, 5) == 20.0
    assert calculate_pe(100, 0) is None

def test_calculate_cagr():
    assert round(calculate_cagr(100, 133.1, 3), 2) == 10.0
    assert calculate_cagr(0, 100, 3) is None
