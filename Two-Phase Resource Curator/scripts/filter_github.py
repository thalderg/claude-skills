#!/usr/bin/env python3
"""
GitHub Repository/File Statistical Filter
Filters using percentile-based ranking (no hard thresholds).
Adapts to any niche - works for N8n (low engagement) or React (high engagement).
"""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional
import requests
import statistics

# Platform-specific metric weights
GITHUB_WEIGHTS = {
    'recency': 0.40,     # Tech moves fast
    'stars': 0.35,       # Popularity indicator
    'forks': 0.15,       # Actual usage
    'file_size': 0.10,   # Quality check
}

def percentile(data: List[float], p: int) -> float:
    """Calculate percentile of dataset"""
    if not data:
        return 0
    sorted_data = sorted(data)
    index = (len(sorted_data) - 1) * p / 100
    floor = int(index)
    ceil = floor + 1
    if ceil >= len(sorted_data):
        return sorted_data[-1]
    return sorted_data[floor] + (sorted_data[ceil] - sorted_data[floor]) * (index - floor)

def percentile_rank(value: float, data: List[float]) -> float:
    """Calculate what percentile a value is in dataset (0-100)"""
    if not data or value is None:
        return 0
    count_below = sum(1 for x in data if x < value)
    count_equal = sum(1 for x in data if x == value)
    return ((count_below + 0.5 * count_equal) / len(data)) * 100

def parse_github_url(url: str) -> tuple:
    """Extract owner and repo from GitHub URL"""
    parts = url.replace('https://github.com/', '').replace('http://github.com/', '').split('/')
    if len(parts) >= 2:
        return parts[0], parts[1]
    raise ValueError(f"Invalid GitHub URL: {url}")

def get_repo_metadata(owner: str, repo: str, token: Optional[str] = None) -> Dict:
    """Fetch repository metadata from GitHub API"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    # Check for token in order of priority:
    # 1. Explicitly passed token argument
    # 2. GITHUB_PUB_TOKEN10F26 environment variable (expires May 11, 2026)
    # 3. GITHUB_TOKEN environment variable (fallback)
    if not token:
        token = os.environ.get('GITHUB_PUB_TOKEN10F26') or os.environ.get('GITHUB_TOKEN')
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")
    
    return response.json()

def get_repo_files(owner: str, repo: str, path: str = '', token: Optional[str] = None, max_depth: int = 3, current_depth: int = 0) -> List[Dict]:
    """Recursively get files (with depth limit to avoid rate limits)"""
    if current_depth >= max_depth:
        return []
    
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    # Check for token in order of priority:
    # 1. Explicitly passed token argument
    # 2. GITHUB_PUB_TOKEN10F26 environment variable (expires May 11, 2026)
    # 3. GITHUB_TOKEN environment variable (fallback)
    if not token:
        token = os.environ.get('GITHUB_PUB_TOKEN10F26') or os.environ.get('GITHUB_TOKEN')
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []
    
    contents = response.json()
    if not isinstance(contents, list):
        return []
    
    files = []
    for item in contents:
        if item['type'] == 'file':
            # Skip obvious non-workflow files
            name = item.get('name', '').lower()
            if not any(skip in name for skip in ['.md', 'license', '.txt', '.gitignore', '.yml', '.yaml', 'readme']):
                files.append(item)
        elif item['type'] == 'dir' and current_depth < max_depth - 1:
            # Recursively get files from subdirectories
            files.extend(get_repo_files(owner, repo, item['path'], token, max_depth, current_depth + 1))
    
    return files

def calculate_recency_score(updated_at_str: str) -> float:
    """Calculate recency score (0-100) based on age"""
    updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
    days_old = (datetime.now(updated_at.tzinfo) - updated_at).days
    
    # Exponential decay: newer = better
    if days_old <= 30:
        return 100
    elif days_old <= 90:
        return 90
    elif days_old <= 180:
        return 75
    elif days_old <= 365:
        return 50
    elif days_old <= 730:
        return 25
    else:
        return max(0, 25 - (days_old - 730) / 365 * 10)

def calculate_composite_score(resource: Dict, all_data: Dict, repo_metadata: Dict, weights: Dict) -> float:
    """Calculate composite percentile score using statistical ranking"""
    scores = {}
    
    # Stars percentile
    stars = repo_metadata.get('stargazers_count', 0)
    scores['stars'] = percentile_rank(stars, all_data['all_stars'])
    
    # Recency score (absolute, not relative - recency matters universally)
    recency_score = calculate_recency_score(repo_metadata.get('updated_at', '2020-01-01'))
    scores['recency'] = recency_score
    
    # Forks percentile
    forks = repo_metadata.get('forks_count', 0)
    scores['forks'] = percentile_rank(forks, all_data['all_forks'])
    
    # File size percentile (within this collection)
    file_size = resource.get('size', 0)
    scores['file_size'] = percentile_rank(file_size, all_data['all_sizes'])
    
    # Weighted composite
    composite = sum(scores[metric] * weights[metric] for metric in weights.keys())
    
    return round(composite, 2), scores

def determine_cutoff_percentile(collection_size: int) -> int:
    """Determine what percentile to use as cutoff based on collection size"""
    if collection_size <= 100:
        return 50  # Keep top 50% (generous for small collections)
    elif collection_size <= 500:
        return 60  # Keep top 40%
    elif collection_size <= 1000:
        return 70  # Keep top 30%
    elif collection_size <= 3000:
        return 80  # Keep top 20%
    else:
        return 85  # Keep top 15% (strict for huge collections)

def filter_resources(resources: List[Dict], repo_metadata: Dict, weights: Dict) -> tuple:
    """Statistical filtering using percentile ranking"""
    
    # Collect all metric values for statistical analysis
    all_stars = [repo_metadata.get('stargazers_count', 0)] * len(resources)  # Repo-level, same for all files
    all_forks = [repo_metadata.get('forks_count', 0)] * len(resources)  # Repo-level
    all_sizes = [r.get('size', 0) for r in resources]
    
    # Basic sanity filtering first (avoid completely trivial files)
    basic_filtered = []
    for resource in resources:
        # Skip files that are obviously not valuable
        name = resource.get('name', '').lower()
        size = resource.get('size', 0)
        
        # Skip if: too small (<500 bytes) OR obvious test/example/demo file
        if size < 500:
            continue
        if any(skip in name for skip in ['test', 'example', 'demo', 'sample', '.min.', 'backup']):
            continue
            
        basic_filtered.append(resource)
    
    if not basic_filtered:
        return [], {'all_stars': all_stars, 'all_forks': all_forks, 'all_sizes': all_sizes}
    
    # Recalculate after basic filtering
    all_sizes = [r.get('size', 0) for r in basic_filtered]
    
    all_data = {
        'all_stars': all_stars,
        'all_forks': all_forks,
        'all_sizes': all_sizes,
    }
    
    # Calculate composite scores
    scored_resources = []
    for resource in basic_filtered:
        composite, breakdowns = calculate_composite_score(resource, all_data, repo_metadata, weights)
        
        resource['composite_score'] = composite
        resource['score_breakdown'] = breakdowns
        resource['stars'] = repo_metadata.get('stargazers_count')
        resource['forks'] = repo_metadata.get('forks_count')
        resource['last_updated'] = repo_metadata.get('updated_at')
        
        scored_resources.append(resource)
    
    # Determine cutoff
    cutoff_percentile = determine_cutoff_percentile(len(basic_filtered))
    
    # Filter by cutoff
    filtered = [r for r in scored_resources if r['composite_score'] >= cutoff_percentile]
    
    # Sort by composite score descending
    filtered.sort(key=lambda x: x['composite_score'], reverse=True)
    
    return filtered, all_data

def main():
    parser = argparse.ArgumentParser(description='Filter GitHub resources using statistical percentiles')
    parser.add_argument('--url', required=True, help='GitHub repository URL')
    parser.add_argument('--token', help='GitHub API token (recommended for rate limits)')
    parser.add_argument('--output', default='filtered_github.json', help='Output file path')
    parser.add_argument('--max-depth', type=int, default=3, help='Max directory depth to scan')
    
    args = parser.parse_args()
    
    # Parse URL
    try:
        owner, repo = parse_github_url(args.url)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"📊 Fetching repository metadata for {owner}/{repo}...")
    
    # Get repo metadata
    try:
        repo_metadata = get_repo_metadata(owner, repo, args.token)
    except Exception as e:
        print(f"Error fetching repo metadata: {e}")
        sys.exit(1)
    
    print(f"⭐ Repository: {repo_metadata.get('stargazers_count', 0)} stars, {repo_metadata.get('forks_count', 0)} forks")
    
    # Get all files
    print(f"📂 Fetching repository files (max depth: {args.max_depth})...")
    files = get_repo_files(owner, repo, '', args.token, args.max_depth)
    
    print(f"✅ Found {len(files)} files in repository")
    
    if len(files) == 0:
        print("⚠️  No files found. Repository might be empty or all files were filtered out.")
        sys.exit(0)
    
    # Calculate statistics
    print(f"\n📈 Calculating statistical metrics...")
    all_sizes = [f.get('size', 0) for f in files]
    print(f"   File sizes: median={statistics.median(all_sizes)}, p75={percentile(all_sizes, 75)}, p90={percentile(all_sizes, 90)}")
    
    # Filter resources
    print(f"\n🔍 Filtering using percentile-based ranking...")
    filtered, all_data = filter_resources(files, repo_metadata, GITHUB_WEIGHTS)
    
    cutoff_used = determine_cutoff_percentile(len(files))
    
    # Prepare output
    output = {
        'original_count': len(files),
        'filtered_count': len(filtered),
        'reduction': f"{((len(files) - len(filtered)) / len(files) * 100):.1f}%" if len(files) > 0 else "0%",
        'platform': 'github',
        'repository': f"{owner}/{repo}",
        'filtering_method': 'statistical_percentile',
        'cutoff_percentile_used': cutoff_used,
        'weights_used': GITHUB_WEIGHTS,
        'repo_metadata': {
            'stars': repo_metadata.get('stargazers_count'),
            'forks': repo_metadata.get('forks_count'),
            'last_updated': repo_metadata.get('updated_at'),
            'description': repo_metadata.get('description'),
        },
        'statistics': {
            'file_size_median': statistics.median(all_sizes) if all_sizes else 0,
            'file_size_p75': percentile(all_sizes, 75),
            'file_size_p90': percentile(all_sizes, 90),
        },
        'resources': filtered[:500],  # Limit to top 500
        'next_steps': 'Review filtered list, or request Phase 2 for deep analysis'
    }
    
    # Save to file
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Filtering complete!")
    print(f"📊 Original: {len(files)} files")
    print(f"📊 Filtered: {len(filtered)} files ({output['reduction']} reduction)")
    print(f"📊 Cutoff: {cutoff_used}th percentile")
    print(f"💾 Output saved to: {args.output}")
    
    if len(filtered) > 0:
        print(f"\n🏆 Top 5 resources by composite score:")
        for i, resource in enumerate(filtered[:5], 1):
            print(f"{i}. {resource['name']}")
            print(f"   Score: {resource['composite_score']:.1f}/100 | Size: {resource['size']} bytes")
            print(f"   Breakdown: recency={resource['score_breakdown']['recency']:.0f}, stars={resource['score_breakdown']['stars']:.0f}, size={resource['score_breakdown']['file_size']:.0f}")

if __name__ == '__main__':
    main()
