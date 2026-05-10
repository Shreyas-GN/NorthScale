"""
tests/api/test_api.py

Tests for the NorthScale REST API Layer.
Verifies caching, standardized envelopes, pagination, and unified analysis.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app
from core.dependencies import get_db

client = TestClient(app)

# --- Mock Data ---

mock_stock = {
    "id": "stock-id-1",
    "ticker": "TCS",
    "company_name": "Tata Consultancy Services",
    "exchange": "NSE",
    "sectors": {"slug": "it"},
    "market_cap_category": "LARGE_CAP",
    "is_active": True
}

mock_rec_summary = {
    "recommendation": "STRONG_BUY",
    "conviction_score": 8.5,
    "confidence_level": "VERY_HIGH",
    "composite_score": 9.0,
    "growth_score": 8.0,
    "profitability_score": 9.0,
    "valuation_score": 7.0,
    "financial_health_score": 9.0,
    "ownership_score": 8.0,
    "risk_score": 0.5,
    "generated_at": "2024-01-01T10:00:00Z"
}

mock_thesis = {
    "thesis_summary": "Great stock.",
    "key_strengths": ["Growth"],
    "key_risks": ["None"],
    "valuation_perspective": "Fair",
    "overall_view": "Buy",
    "confidence_note": "High confidence",
    "is_fallback": False
}

mock_fin = {
    "snapshot_date": "2024-01-01",
    "data_source": "System",
    "freshness_score": 100
}

def override_get_db():
    mock_db = MagicMock()
    
    # Simple chain mock for Supabase client
    def mock_table(table_name):
        mock_query = MagicMock()
        mock_query.select.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.or_.return_value = mock_query
        mock_query.order.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.range.return_value = mock_query
        
        # Determine what to return based on table
        if table_name == "stocks":
            mock_query.execute.return_value.data = [mock_stock]
            mock_query.execute.return_value.count = 1
        elif table_name == "recommendations":
            mock_query.execute.return_value.data = [mock_rec_summary]
        elif table_name == "ai_theses":
            mock_query.execute.return_value.data = [mock_thesis]
        elif table_name == "stock_financial_snapshots":
            mock_query.execute.return_value.data = [mock_fin]
        else:
            mock_query.execute.return_value.data = []
            
        return mock_query
        
    mock_db.table = mock_table
    return mock_db

app.dependency_overrides[get_db] = override_get_db

# Tests

@patch('api.v1.endpoints.analysis.get_cache', return_value=None)
@patch('api.v1.endpoints.analysis.set_cache')
def test_analysis_endpoint(mock_set_cache, mock_get_cache):
    response = client.get("/api/v1/analysis/TCS")
    assert response.status_code == 200
    
    json_resp = response.json()
    assert json_resp["success"] is True
    assert "data" in json_resp
    assert "meta" in json_resp
    
    data = json_resp["data"]
    assert data["ticker"] == "TCS"
    assert data["recommendation"] == "STRONG_BUY"
    assert data["thesis_summary"] == "Great stock."
    
    assert json_resp["meta"]["cached"] is False
    assert json_resp["meta"]["data_freshness"] == 100
    mock_set_cache.assert_called_once()

@patch('api.v1.endpoints.analysis.get_cache')
def test_analysis_endpoint_cached(mock_get_cache):
    mock_get_cache.return_value = {
        "ticker": "TCS",
        "company_name": "Tata Consultancy Services",
        "sector": "it",
        "recommendation": "STRONG_BUY",
        "conviction_score": 8.5,
        "confidence_level": "VERY_HIGH",
        "thesis_summary": "Great stock (cached).",
        "bullish_factors": ["Growth"],
        "bearish_factors": [],
        "positive_signals": ["Growth"],
        "negative_signals": [],
        "risk_score": 0.5,
        "freshness_score": 100,
        "data_source": "System",
        "snapshot_date": "2024-01-01",
        "is_fallback": False
    }
    
    response = client.get("/api/v1/analysis/TCS")
    assert response.status_code == 200
    
    json_resp = response.json()
    assert json_resp["success"] is True
    assert json_resp["meta"]["cached"] is True
    assert json_resp["data"]["thesis_summary"] == "Great stock (cached)."

def test_stocks_list_endpoint():
    response = client.get("/api/v1/stocks")
    assert response.status_code == 200
    
    json_resp = response.json()
    assert json_resp["success"] is True
    assert json_resp["data"]["total"] == 1
    assert len(json_resp["data"]["items"]) == 1
    assert json_resp["data"]["items"][0]["ticker"] == "TCS"

def test_search_endpoint():
    response = client.get("/api/v1/search?q=tcs")
    assert response.status_code == 200
    
    json_resp = response.json()
    assert json_resp["success"] is True
    assert len(json_resp["data"]["results"]) == 1
    assert json_resp["data"]["results"][0]["ticker"] == "TCS"

def test_recommendation_endpoint():
    response = client.get("/api/v1/recommendations/TCS")
    assert response.status_code == 200
    
    json_resp = response.json()
    assert json_resp["success"] is True
    assert json_resp["data"]["ticker"] == "TCS"
    assert json_resp["data"]["recommendation"] == "STRONG_BUY"
    assert json_resp["data"]["composite_score"] == 9.0

# Cleanup
def teardown_module():
    app.dependency_overrides.clear()
