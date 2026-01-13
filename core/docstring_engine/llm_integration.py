"""
LLM Integration for Docstring Content Generation
Uses GROQ API
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def generate_docstring_llm(fn_name: str, fn_source: str, style: str) -> str:
    """
    Generate HIGH-QUALITY Python docstring using GROQ LLM.
    
    Args:
        fn_name (str): Function name
        fn_source (str): Function source code
        style (str): Docstring style (google, numpy, rest)
        
    Returns:
        str: Generated docstring text
    """
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment")
    
    client = Groq(api_key=api_key)
    
    style_map = {
        "google": "Google style",
        "numpy": "NumPy style",
        "rest": "reStructuredText (reST) style"
    }
    
    prompt = f"""
You are a senior Python engineer.

Generate a HIGH-QUALITY Python docstring in {style_map[style]}.

STRICT RULES:
- Start summary with an IMPERATIVE VERB (Add, Calculate, Return, Validate)
- DO NOT use words like "Process"
- End summary with a period
- Include Args, Returns only if applicable
- Do NOT include markdown
- Do NOT include code fences
- Return ONLY the docstring text

Function source:
{fn_source}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    return response.choices[0].message.content.strip()


if __name__ == '__main__':
    # Test
    test_fn = '''
def add(a: int, b: int) -> int:
    return a + b
'''
    
    result = generate_docstring_llm("add", test_fn, "google")
    print(result)
