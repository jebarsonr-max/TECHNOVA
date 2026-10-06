from backend.app.execution.executor import SecureCodeExecutor

def test_secure_executor_normal_code():
    code = """
import json
res = {"answer": 42.0, "status": "SUCCESS"}
print(json.dumps(res))
"""
    res = SecureCodeExecutor.execute_code(code)
    assert res["is_success"] is True
    assert res["result_data"]["answer"] == 42.0

def test_secure_executor_reject_malicious_import():
    code = """
import os
os.system("echo hacked")
"""
    res = SecureCodeExecutor.execute_code(code)
    assert res["is_success"] is False
    assert "SECURITY_VIOLATION" in res["stderr"]
