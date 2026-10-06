import sys
import io
import json
import traceback

def run_code_payload(code_str: str):
    """Executes code payload in restricted scope with allowed analytical modules."""
    output_buffer = io.StringIO()
    sys.stdout = output_buffer
    
    # Safe allowed builtins
    safe_builtins = {
        "__import__": __import__,
        "print": print,
        "range": range,
        "len": len,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "set": set,
        "round": round,
        "min": min,
        "max": max,
        "abs": abs,
        "sum": sum,
        "zip": zip,
        "enumerate": enumerate,
        "isinstance": isinstance,
        "type": type,
        "Exception": Exception,
        "ValueError": ValueError,
        "KeyError": KeyError,
        "TypeError": TypeError
    }
    
    global_scope = {
        "__builtins__": safe_builtins
    }
    
    try:
        exec(code_str, global_scope)
        sys.stdout = sys.__stdout__
        return {
            "exit_code": 0,
            "stdout": output_buffer.getvalue(),
            "stderr": "",
            "is_success": True
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        return {
            "exit_code": 1,
            "stdout": output_buffer.getvalue(),
            "stderr": traceback.format_exc(),
            "is_success": False
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        code_filepath = sys.argv[1]
        with open(code_filepath, "r", encoding="utf-8") as f:
            code_str = f.read()
    else:
        code_str = sys.stdin.read()
    
    res = run_code_payload(code_str)
    print(json.dumps(res))
