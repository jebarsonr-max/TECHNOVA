from backend.app.verification.trap_detector import PS08TrapDetector

def test_missing_cost_trap():
    schema = [{
        "dataset_id": "ds-missing-cost",
        "columns": [
            {"name": "sales_amount", "type": "float"},
            {"name": "region", "type": "categorical"}
        ]
    }]
    res = PS08TrapDetector.inspect_for_traps("What is the net profit margin?", schema)
    assert res["has_trap"] is True
    assert res["trap_type"] == "MISSING_DATA"
    assert "CANNOT_DETERMINE" in res["refusal_reason"]

def test_currency_mismatch_trap():
    schema = [{
        "dataset_id": "ds-curr",
        "columns": [
            {"name": "amount_usd", "currency": "$"},
            {"name": "amount_eur", "currency": "€"}
        ]
    }]
    res = PS08TrapDetector.inspect_for_traps("What is the total combined revenue?", schema)
    assert res["has_trap"] is True
    assert res["trap_type"] == "CURRENCY_MISMATCH"
    assert "CANNOT_DETERMINE" in res["refusal_reason"]

def test_future_prediction_trap():
    schema = [{
        "dataset_id": "ds-orders",
        "columns": [{"name": "order_date", "type": "date"}]
    }]
    res = PS08TrapDetector.inspect_for_traps("What will be the total revenue next year?", schema)
    assert res["has_trap"] is True
    assert res["trap_type"] == "FUTURE_DATA_TRAP"
