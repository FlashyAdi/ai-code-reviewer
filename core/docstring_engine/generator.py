"""
Docstring Generator - Milestones 1 & 2
Generates docstrings in Google, NumPy, and reST styles using LLM
"""

from typing import Dict
from core.docstring_engine.llm_integration import generate_docstring_llm


def generate_google_docstring(fn: Dict, content: str) -> str:
    """
    Format docstring in Google style.
    
    Args:
        fn (Dict): Function metadata
        content (str): LLM-generated content
        
    Returns:
        str: Formatted Google-style docstring
    """
    
    return f'"""\n{content}\n"""'


def generate_numpy_docstring(fn: Dict, content: str) -> str:
    """
    Format docstring in NumPy style.
    
    Args:
        fn (Dict): Function metadata
        content (str): LLM-generated content
        
    Returns:
        str: Formatted NumPy-style docstring
    """
    
    return f'"""\n{content}\n"""'


def generate_rest_docstring(fn: Dict, content: str) -> str:
    """
    Format docstring in reST style.
    
    Args:
        fn (Dict): Function metadata
        content (str): LLM-generated content
        
    Returns:
        str: Formatted reST-style docstring
    """
    
    return f'"""\n{content}\n"""'


def generate_docstring(fn: Dict, style: str = "google") -> str:
    """
    Generate docstring using LLM and format in selected style.
    
    Args:
        fn (Dict): Function metadata from parser
        style (str): Docstring style (google, numpy, rest)
        
    Returns:
        str: Complete formatted docstring
    """
    
    # Build function source for LLM context
    fn_source = f"def {fn['name']}("
    
    if fn.get('args'):
        args_str = ", ".join(
            f"{arg['name']}: {arg.get('annotation', 'Any')}" 
            for arg in fn['args']
        )
        fn_source += args_str
    
    fn_source += ")"
    
    if fn.get('returns'):
        fn_source += f" -> {fn['returns']}"
    
    fn_source += ":\n    pass"
    
    try:
        # Generate content using LLM
        content = generate_docstring_llm(fn['name'], fn_source, style)
        
        # Format according to style
        if style == "google":
            return generate_google_docstring(fn, content)
        elif style == "numpy":
            return generate_numpy_docstring(fn, content)
        elif style == "rest":
            return generate_rest_docstring(fn, content)
        else:
            raise ValueError(f"Unknown style: {style}")
            
    except Exception as e:
        print(f"⚠️  Error generating docstring: {e}")
        
        # Fallback: simple docstring
        summary = f"Short description of `{fn['name']}`."
        return f'"""\n{summary}\n"""'


if __name__ == '__main__':
    # Test
    test_fn = {
        'name': 'calculate_sum',
        'args': [
            {'name': 'a', 'annotation': 'int'},
            {'name': 'b', 'annotation': 'int'}
        ],
        'returns': 'int'
    }
    
    print("Google Style:")
    print(generate_docstring(test_fn, 'google'))
    
    print("\nNumPy Style:")
    print(generate_docstring(test_fn, 'numpy'))
    
    print("\nreST Style:")
    print(generate_docstring(test_fn, 'rest'))