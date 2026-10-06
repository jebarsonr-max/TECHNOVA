import sys
import os
import time
import tempfile
import subprocess
import json
from typing import Dict, Any
from backend.app.execution.security import SecurityValidator
from backend.app.config import settings

class SecureCodeExecutor:
    @staticmethod
    def execute_code(code: str) -> Dict[str, Any]:
        """
        Executes analytical proof code in secure sandbox environment with timeout and security controls.
        Never executes arbitrary code on host without validation.
        """
        # Step 1: Security Scan
        is_safe, sec_msg = SecurityValidator.validate_code_safety(code)
        if not is_safe:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": sec_msg,
                "execution_time_ms": 0.0,
                "result_data": None,
                "is_success": False,
                "error_type": "SECURITY_VIOLATION"
            }

        start_time = time.time()
        
        # Write code to isolated temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            # Use current Python interpreter to run runner.py with restricted scope
            runner_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "sandbox", "runner.py"))
            python_exe = sys.executable

            cmd = [python_exe, runner_script, tmp_path]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.SANDBOX_TIMEOUT_SECONDS
            )

            execution_time_ms = round((time.time() - start_time) * 1000, 2)
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()

            result_data = None
            is_success = False

            if proc.returncode == 0 and stdout:
                try:
                    parsed_output = json.loads(stdout)
                    if isinstance(parsed_output, dict) and "is_success" in parsed_output:
                        is_success = parsed_output.get("is_success", False)
                        inner_stdout = parsed_output.get("stdout", "").strip()
                        inner_stderr = parsed_output.get("stderr", "").strip()
                        if inner_stdout:
                            try:
                                result_data = json.loads(inner_stdout)
                            except Exception:
                                result_data = {"raw_output": inner_stdout}
                        stdout = inner_stdout
                        stderr = inner_stderr
                    else:
                        result_data = parsed_output
                        is_success = True
                except Exception:
                    result_data = {"raw_output": stdout}
                    is_success = True

            return {
                "exit_code": proc.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "execution_time_ms": execution_time_ms,
                "result_data": result_data,
                "is_success": is_success and proc.returncode == 0
            }

        except subprocess.TimeoutExpired:
            execution_time_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "exit_code": 124,
                "stdout": "",
                "stderr": f"Execution timed out after {settings.SANDBOX_TIMEOUT_SECONDS} seconds.",
                "execution_time_ms": execution_time_ms,
                "result_data": None,
                "is_success": False,
                "error_type": "TIMEOUT"
            }
        except Exception as e:
            execution_time_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "exit_code": 1,
                "stdout": "",
                "stderr": str(e),
                "execution_time_ms": execution_time_ms,
                "result_data": None,
                "is_success": False,
                "error_type": "SUBPROCESS_ERROR"
            }
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
