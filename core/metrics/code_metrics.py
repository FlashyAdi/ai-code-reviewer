"""
Code Metrics - Milestone 3

Calculate complexity and maintainability metrics.
"""

from radon.complexity import cc_visit, average_complexity
from radon.metrics import mi_visit, mi_parameters
from radon.raw import analyze
from typing import Dict, List


def get_complexity_metrics(source_code: str) -> Dict:
    """
    Get cyclomatic complexity metrics for source code.
    
    Args:
        source_code (str): Python source code
        
    Returns:
        Dict: Complexity metrics
    """
    
    try:
        results = cc_visit(source_code)
        
        metrics = {
            'functions': [],
            'average_complexity': 0.0,
            'max_complexity': 0,
            'total_functions': len(results)
        }
        
        for item in results:
            metrics['functions'].append({
                'name': item.name,
                'complexity': item.complexity,
                'rank': get_complexity_rank(item.complexity),
                'lineno': item.lineno,
                'col_offset': item.col_offset,
                'endline': item.endline
            })
        
        if results:
            metrics['average_complexity'] = round(average_complexity(results), 2)
            metrics['max_complexity'] = max(item.complexity for item in results)
        
        return metrics
        
    except Exception as e:
        print(f"⚠️  Error calculating complexity: {e}")
        return {
            'functions': [],
            'average_complexity': 0.0,
            'max_complexity': 0,
            'total_functions': 0,
            'error': str(e)
        }


def get_complexity_rank(complexity: int) -> str:
    """
    Convert complexity score to rank.
    
    Args:
        complexity (int): Cyclomatic complexity value
        
    Returns:
        str: Rank A-F
    """
    
    if complexity <= 5:
        return 'A'  # Simple, low risk
    elif complexity <= 10:
        return 'B'  # More complex, moderate risk
    elif complexity <= 20:
        return 'C'  # Complex, high risk
    elif complexity <= 30:
        return 'D'  # Very complex
    elif complexity <= 40:
        return 'E'  # Extremely complex
    else:
        return 'F'  # Unmaintainable


def get_maintainability_index(source_code: str) -> float:
    """
    Calculate maintainability index.
    
    Args:
        source_code (str): Python source code
        
    Returns:
        float: Maintainability index (0-100)
    """
    
    try:
        mi = mi_visit(source_code, multi=True)
        return round(mi, 2) if mi else 0.0
    except Exception as e:
        print(f"⚠️  Error calculating MI: {e}")
        return 0.0


def get_raw_metrics(source_code: str) -> Dict:
    """
    Get raw code metrics (LOC, comments, etc).
    
    Args:
        source_code (str): Python source code
        
    Returns:
        Dict: Raw metrics
    """
    
    try:
        analysis = analyze(source_code)
        
        return {
            'loc': analysis.loc,  # Lines of code
            'lloc': analysis.lloc,  # Logical lines of code
            'sloc': analysis.sloc,  # Source lines of code
            'comments': analysis.comments,
            'multi': analysis.multi,  # Multi-line strings
            'blank': analysis.blank,
            'single_comments': analysis.single_comments
        }
        
    except Exception as e:
        print(f"⚠️  Error analyzing raw metrics: {e}")
        return {
            'loc': 0,
            'lloc': 0,
            'sloc': 0,
            'comments': 0,
            'multi': 0,
            'blank': 0,
            'single_comments': 0,
            'error': str(e)
        }


def get_comprehensive_metrics(file_path: str) -> Dict:
    """
    Get all metrics for a file.
    
    Args:
        file_path (str): Path to Python file
        
    Returns:
        Dict: Complete metrics
    """
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        complexity = get_complexity_metrics(source)
        maintainability = get_maintainability_index(source)
        raw = get_raw_metrics(source)
        
        # Calculate quality score
        score = calculate_quality_score(complexity, maintainability, raw)
        
        return {
            'file_path': file_path,
            'complexity': complexity,
            'maintainability_index': maintainability,
            'raw_metrics': raw,
            'quality_score': score,
            'grade': score_to_grade(score)
        }
        
    except Exception as e:
        print(f"⚠️  Error getting metrics for {file_path}: {e}")
        return {
            'file_path': file_path,
            'error': str(e)
        }


def calculate_quality_score(complexity: Dict, maintainability: float, raw: Dict) -> float:
    """
    Calculate overall quality score.
    
    Args:
        complexity (Dict): Complexity metrics
        maintainability (float): MI value
        raw (Dict): Raw metrics
        
    Returns:
        float: Quality score (0-100)
    """
    
    score = 100.0
    
    # Penalty for high complexity
    avg_complexity = complexity.get('average_complexity', 0)
    if avg_complexity > 10:
        score -= (avg_complexity - 10) * 2
    
    max_complexity = complexity.get('max_complexity', 0)
    if max_complexity > 20:
        score -= (max_complexity - 20) * 1.5
    
    # Bonus for good maintainability
    if maintainability > 80:
        score += 5
    elif maintainability < 50:
        score -= 10
    
    # Penalty for low comment ratio
    loc = raw.get('loc', 1)
    comments = raw.get('comments', 0)
    comment_ratio = (comments / loc * 100) if loc > 0 else 0
    
    if comment_ratio < 5:
        score -= 5
    
    return max(0, min(100, round(score, 2)))


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


def print_metrics_report(metrics: Dict):
    """
    Print formatted metrics report.
    
    Args:
        metrics (Dict): Metrics data
    """
    
    print("\n" + "="*60)
    print(f"📊 CODE METRICS REPORT")
    print("="*60)
    
    print(f"\n📄 File: {metrics.get('file_path', 'Unknown')}")
    
    # Maintainability
    mi = metrics.get('maintainability_index', 0)
    print(f"\n🔧 Maintainability Index: {mi}/100")
    
    if mi > 85:
        print("   Status: 🟢 Excellent")
    elif mi > 65:
        print("   Status: 🟡 Good")
    else:
        print("   Status: 🔴 Needs Improvement")
    
    # Complexity
    complexity = metrics.get('complexity', {})
    avg_complexity = complexity.get('average_complexity', 0)
    max_complexity = complexity.get('max_complexity', 0)
    
    print(f"\n⚙️  Cyclomatic Complexity:")
    print(f"   Average: {avg_complexity}")
    print(f"   Maximum: {max_complexity}")
    
    # Quality Score
    score = metrics.get('quality_score', 0)
    grade = metrics.get('grade', 'F')
    
    print(f"\n🎯 Quality Score: {score}/100 (Grade: {grade})")
    
    # Raw metrics
    raw = metrics.get('raw_metrics', {})
    print(f"\n📏 Lines of Code:")
    print(f"   Total LOC: {raw.get('loc', 0)}")
    print(f"   Source LOC: {raw.get('sloc', 0)}")
    print(f"   Comments: {raw.get('comments', 0)}")
    print(f"   Blank: {raw.get('blank', 0)}")
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        metrics = get_comprehensive_metrics(file_path)
        print_metrics_report(metrics)
    else:
        print("Usage: python code_metrics.py <file_path>")