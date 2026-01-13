"""
Python AST Parser - Milestone 1

Extracts:
- Functions (top-level, class methods, nested)
- Docstrings
- Arguments with type hints
- Return types
- Decorators
- Line numbers
"""

import ast
import os
from typing import List, Dict, Optional


def parse_file(file_path: str) -> Optional[Dict]:
    """
    Parse a single Python file and extract metadata.
    
    Args:
        file_path (str): Path to Python file
        
    Returns:
        Optional[Dict]: Parsed metadata or None if error
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        tree = ast.parse(source, filename=file_path)
        
        result = {
            'file_path': file_path,
            'functions': []
        }
        
        # Extract all functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = extract_function_info(node, source)
                if func_info:
                    result['functions'].append(func_info)
        
        return result
        
    except SyntaxError as e:
        print(f"⚠️  Syntax error in {file_path}: {e}")
        return None
    except Exception as e:
        print(f"⚠️  Error parsing {file_path}: {e}")
        return None


def extract_function_info(node: ast.FunctionDef, source: str) -> Dict:
    """
    Extract detailed information from a function node.
    
    Args:
        node (ast.FunctionDef): AST function node
        source (str): Source code
        
    Returns:
        Dict: Function metadata
    """
    
    # Get docstring
    docstring = ast.get_docstring(node)
    has_docstring = docstring is not None and len(docstring.strip()) > 0
    
    # Get arguments
    args = []
    for arg in node.args.args:
        arg_info = {
            'name': arg.arg,
            'annotation': get_annotation(arg.annotation)
        }
        args.append(arg_info)
    
    # Get return type
    returns = get_annotation(node.returns)
    
    # Get decorators
    decorators = [get_decorator_name(dec) for dec in node.decorator_list]
    
    # Calculate indentation
    indent = get_indentation(node, source)
    
    # Get exceptions raised (if any)
    raises = extract_raises(node)
    
    return {
        'name': node.name,
        'has_docstring': has_docstring,
        'docstring': docstring or '',
        'args': args,
        'returns': returns,
        'decorators': decorators,
        'start_line': node.lineno - 1,  # Line after 'def'
        'end_line': node.end_lineno,
        'indent': indent,
        'raises': raises
    }


def get_annotation(annotation) -> Optional[str]:
    """Get string representation of type annotation."""
    if annotation is None:
        return None
    
    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Constant):
        return str(annotation.value)
    elif isinstance(annotation, ast.Subscript):
        # For List[int], Dict[str, int], etc.
        return ast.unparse(annotation)
    else:
        try:
            return ast.unparse(annotation)
        except:
            return str(annotation)


def get_decorator_name(decorator) -> str:
    """Get decorator name as string."""
    if isinstance(decorator, ast.Name):
        return decorator.id
    elif isinstance(decorator, ast.Call):
        if isinstance(decorator.func, ast.Name):
            return decorator.func.id
    return ast.unparse(decorator)


def get_indentation(node: ast.FunctionDef, source: str) -> int:
    """Calculate indentation level of function."""
    lines = source.split('\n')
    if node.lineno <= len(lines):
        line = lines[node.lineno - 1]
        return len(line) - len(line.lstrip())
    return 0


def extract_raises(node: ast.FunctionDef) -> List[str]:
    """Extract exception types that function raises."""
    raises = []
    
    for child in ast.walk(node):
        if isinstance(child, ast.Raise):
            if child.exc:
                if isinstance(child.exc, ast.Call):
                    if isinstance(child.exc.func, ast.Name):
                        raises.append(child.exc.func.id)
                elif isinstance(child.exc, ast.Name):
                    raises.append(child.exc.id)
    
    return list(set(raises))  # Remove duplicates


def parse_path(path: str) -> List[Dict]:
    """
    Parse all Python files in a directory or single file.
    
    Args:
        path (str): Directory or file path
        
    Returns:
        List[Dict]: List of parsed file metadata
    """
    
    results = []
    
    if os.path.isfile(path):
        if path.endswith('.py'):
            result = parse_file(path)
            if result:
                results.append(result)
    
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            # Skip common excluded directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', '.venv', 'node_modules']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    result = parse_file(file_path)
                    if result:
                        results.append(result)
    
    return results


# Test function
if __name__ == '__main__':
    # Test with examples directory
    results = parse_path('examples')
    
    for file_data in results:
        print(f"\n📄 File: {file_data['file_path']}")
        print(f"   Functions: {len(file_data['functions'])}")
        
        for fn in file_data['functions']:
            status = "✅" if fn['has_docstring'] else "❌"
            print(f"   {status} {fn['name']}()")