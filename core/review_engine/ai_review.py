import ast
import difflib
import json
import os
from datetime import datetime

from core.parser.python_parser import parse_functions
from core.docstring_engine.llm_generator import generate_docstring_llm

LOG_FILE = "storage/review_logs.json"


# ======================================================
# REVIEW FILE
# ======================================================
def review_file(file_path: str, style: str):
    results = []
    functions = parse_functions(file_path)

    for fn in functions:
        if not fn["docstring"]:
            generated = generate_docstring_llm(
                fn_name=fn["name"],
                fn_source=fn.get("source", ""),
                style=style
            )
            results.append({
                "function": fn["name"],
                "status": "fix",
                "before": None,
                "after": generated
            })
        else:
            results.append({
                "function": fn["name"],
                "status": "ok",
                "before": fn["docstring"],
                "after": fn["docstring"]
            })

    return results


# ======================================================
# APPLY DOCSTRING  ✅ (IMPORT ERROR FIX HERE)
# ======================================================
def apply_docstring(file_path: str, function_name: str, new_docstring: str):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            doc_node = ast.Expr(
                value=ast.Constant(new_docstring.strip())
            )

            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
            ):
                node.body[0] = doc_node
            else:
                node.body.insert(0, doc_node)
            break

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ast.unparse(tree))


# ======================================================
# DIFF
# ======================================================
def generate_diff(before, after):
    before = before or ""
    diff = difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        lineterm=""
    )
    return "\n".join(diff)


# ======================================================
# LOG ACCEPT
# ======================================================
def log_accept(file_path: str, function_name: str, style: str):
    os.makedirs("storage", exist_ok=True)

    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    data.append({
        "file": file_path,
        "function": function_name,
        "style": style,
        "timestamp": datetime.now().isoformat()
    })

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ======================================================
# COVERAGE
# ======================================================
def calculate_coverage(file_path: str):
    functions = parse_functions(file_path)
    total = len(functions)

    if total == 0:
        return 100.0

    documented = sum(1 for f in functions if f["docstring"])
    return round((documented / total) * 100, 2)
