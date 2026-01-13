"""
Coverage Reporter - Milestone 1

Computes docstring coverage percentage.
"""

import json
from typing import Dict, List


def compute_coverage(parsed_files: List[Dict]) -> Dict:
    """
    Compute docstring coverage for parsed files.
    
    Args:
        parsed_files (List[Dict]): List of parsed file data
        
    Returns:
        Dict: Coverage statistics
    """
    
    total_functions = 0
    documented = 0
    
    file_details = []
    
    for file_data in parsed_files:
        file_total = len(file_data.get('functions', []))
        file_documented = sum(1 for fn in file_data.get('functions', []) 
                             if fn.get('has_docstring'))
        
        total_functions += file_total
        documented += file_documented
        
        file_coverage = (file_documented / file_total * 100) if file_total > 0 else 100
        
        file_details.append({
            'file_path': file_data['file_path'],
            'total_functions': file_total,
            'documented': file_documented,
            'coverage_percent': round(file_coverage, 2)
        })
    
    overall_coverage = (documented / total_functions * 100) if total_functions > 0 else 100
    
    return {
        'total_functions': total_functions,
        'documented': documented,
        'missing': total_functions - documented,
        'coverage_percent': round(overall_coverage, 2),
        'files': file_details
    }


def write_report(coverage: Dict, output_path: str):
    """
    Write coverage report to JSON file.
    
    Args:
        coverage (Dict): Coverage statistics
        output_path (str): Output file path
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(coverage, f, indent=2)
    
    print(f"✅ Report written to: {output_path}")


def print_coverage_summary(coverage: Dict):
    """
    Print coverage summary to console.
    
    Args:
        coverage (Dict): Coverage statistics
    """
    
    print("\n" + "="*60)
    print("📊 DOCSTRING COVERAGE REPORT")
    print("="*60)
    
    percent = coverage['coverage_percent']
    total = coverage['total_functions']
    documented = coverage['documented']
    missing = coverage['missing']
    
    print(f"\n  Total Functions:     {total}")
    print(f"  Documented:          {documented}")
    print(f"  Missing Docstrings:  {missing}")
    print(f"  Coverage:            {percent}%")
    
    # Status
    if percent >= 90:
        status = "🟢 Excellent"
    elif percent >= 70:
        status = "🟡 Good"
    else:
        status = "🔴 Needs Improvement"
    
    print(f"  Status:              {status}")
    print("\n" + "="*60)
    
    # Per-file breakdown
    print("\n📁 Per-File Breakdown:\n")
    
    for file_data in coverage.get('files', []):
        file_name = file_data['file_path'].split('/')[-1]
        file_percent = file_data['coverage_percent']
        
        if file_percent == 100:
            badge = "✅"
        elif file_percent >= 70:
            badge = "⚠️"
        else:
            badge = "❌"
        
        print(f"  {badge} {file_name:<40} {file_percent:>5}%")
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    # Test
    from core.parser.python_parser import parse_path
    
    parsed = parse_path('examples')
    coverage = compute_coverage(parsed)
    print_coverage_summary(coverage)
    write_report(coverage, 'storage/coverage_report.json')