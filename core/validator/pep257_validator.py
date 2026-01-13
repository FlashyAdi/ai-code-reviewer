import pydocstyle

def validate_file(file_path: str):
    """
    Validate a Python file against PEP-257 rules.
    Returns list of violations.
    """
    issues = []

    try:
        for error in pydocstyle.check([file_path]):
            issues.append({
                "code": error.code,
                "line": error.line,
                "message": error.message
            })
    except Exception as e:
        issues.append({
            "code": "ERROR",
            "line": "-",
            "message": str(e)
        })

    return issues
