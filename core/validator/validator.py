"""
Validator - Milestone 2

PEP-257 validation and code metrics.
"""

import subprocess
import json
from typing import List, Dict
from radon.complexity import cc_visit
from radon.metrics import mi_visit


def validate_docstrings(file_path: str) -> List[Dict]:
    """
    Validate docstrings against PEP-257 using pydocstyle.
    
    Args:
        file_path (str): Path to Python file
        
    Returns:
        List[Dict]: List of violations
    """
    
    try:
        result = subprocess.run(
            ['pydocstyle', file_path],
            capture_output=True,
            text=True
        )
        
        violations = []
        
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line and ':' in line:
                    parts = line.split(':', 3)
                    if len(parts) >= 3:
                        violations.append({
                            'file': parts[0],
                            'line': parts[1],
                            'code': parts[2].strip(),
                            'message': parts[3].strip() if len(parts) > 3 else ''
                        })
        
        return violations
        
    except FileNotFoundError:
        print("⚠️  pydocstyle not installed. Install: pip install pydocstyle")
        return []
    except Exception as e:
        print(f"⚠️  Validation error: {e}")
        return []


def compute_complexity(source_code: str) -> Dict:
    """
    Compute cyclomatic complexity of code.
    
    Args:
        source_code (str): Python source code
        
    Returns:
        Dict: Complexity metrics per function
    """
    
    try:
        results = cc_visit(source_code)
        
        complexity_data = {}
        
        for item in results:
            complexity_data[item.name] = {
                'complexity': item.complexity,
                'lineno': item.lineno,
                'endline': item.endline,
                'rank': complexity_rank(item.complexity)
            }
        
        return complexity_data
        
    except Exception as e:
        print(f"⚠️  Complexity calculation error: {e}")
        return {}


def complexity_rank(complexity: int) -> str:
    """
    Get complexity rank.
    
    Args:
        complexity (int): Cyclomatic complexity value
        
    Returns:
        str: Rank (A-F)
    """
    
    if complexity <= 5:
        return 'A'  # Simple
    elif complexity <= 10:
        return 'B'  # Moderate
    elif complexity <= 20:
        return 'C'  # Complex
    elif complexity <= 30:
        return 'D'  # Very complex
    elif complexity <= 40:
        return 'E'  # Extremely complex
    else:
        return 'F'  # Unmaintainable


def compute_maintainability(source_code: str) -> float:
    """
    Compute maintainability index.
    
    Args:
        source_code (str): Python source code
        
    Returns:
        float: Maintainability index (0-100)
    """
    
    try:
        result = mi_visit(source_code, multi=True)
        
        if result:
            return round(result, 2)
        
        return 0.0
        
    except Exception as e:
        print(f"⚠️  Maintainability calculation error: {e}")
        return 0.0


def get_quality_score(file_path: str) -> Dict:
    """
    Get overall quality score for a file.
    
    Args:
        file_path (str): Path to Python file
        
    Returns:
        Dict: Quality metrics
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        violations = validate_docstrings(file_path)
        complexity = compute_complexity(source)
        maintainability = compute_maintainability(source)
        
        # Calculate score
        violation_penalty = len(violations) * 5
        complexity_penalty = sum(
            10 for c in complexity.values() if c['complexity'] > 10
        )
        
        base_score = 100
        final_score = max(0, base_score - violation_penalty - complexity_penalty)
        
        # Adjust by maintainability
        if maintainability > 0:
            final_score = (final_score + maintainability) / 2
        
        return {
            'file_path': file_path,
            'score': round(final_score, 2),
            'violations': len(violations),
            'high_complexity_functions': sum(
                1 for c in complexity.values() if c['complexity'] > 10
            ),
            'maintainability_index': maintainability,
            'grade': score_to_grade(final_score)
        }
        
    except Exception as e:
        print(f"⚠️  Error computing quality score: {e}")
        return {
            'file_path': file_path,
            'score': 0,
            'error': str(e)
        }


def score_to_grade(score: float) -> str:
    """Convert score to letter grade."""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


if __name__ == '__main__':
    # Test
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        print(f"\n🔍 Validating: {file_path}\n")
        
        violations = validate_docstrings(file_path)
        
        if violations:
            print("❌ PEP-257 Violations:")
            for v in violations:
                print(f"   Line {v['line']}: {v['code']} - {v['message']}")
        else:
            print("✅ No PEP-257 violations")
        
        with open(file_path, 'r') as f:
            source = f.read()
        
        print(f"\n📊 Maintainability Index: {compute_maintainability(source)}")
        
        quality = get_quality_score(file_path)
        print(f"\n🎯 Quality Score: {quality['score']}/100 (Grade: {quality['grade']})")
    else:
        print("Usage: python validator.py <file_path>")