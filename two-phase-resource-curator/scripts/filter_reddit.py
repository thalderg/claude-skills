#!/usr/bin/env python3
"""
Reddit Post/Comment Statistical Filter
Filters using percentile-based ranking (no hard thresholds).
Adapts to any subreddit size and engagement level.
"""

import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict
import requests
import statistics

# Platform-specific metric weights for Reddit
REDDIT_WEIGHTS = {
    'score': 0.40,       # Upvotes are strong signal
    'recency': 0.30,     # Tech content ages
    'comments': 0.20,    # Discussion indicates value
    'ratio': 0.10,       # Polarizing ≠ bad, but consider
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

def fetch_reddit_data(url: str) -> Dict:
    """Fetch Reddit data using JSON endpoint (no auth needed)"""
    json_url = url.rstrip('/') + '.json' if not url.endswith('.json') else url
    headers = {'User-Agent': 'ResourceCurator/2.0'}
    response = requests.get(json_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Reddit API error: {response.status_code}")
    
    return response.json()

def parse_subreddit_posts(subreddit: str, limit: int = 1000, time_filter: str = 'all') -> List[Dict]:
    """Fetch posts from subreddit"""
    posts = []
    after = None
    headers = {'User-Agent': 'ResourceCurator/2.0'}
    
    while len(posts) < limit:
        params = {'limit': 100, 't': time_filter}
        if after:
            params['after'] = after
        
        url = f'https://www.reddit.com/r/{subreddit}/top.json'
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            break
        
        data = response.json()
        children = data.get('data', {}).get('children', [])
        
        if not children:
            break
        
        for child in children:
            posts.append(child['data'])
        
        after = data.get('data', {}).get('after')
        if not after:
            break
    
    return posts[:limit]

def calculate_recency_score(created_utc: float) -> float:
    """Calculate recency score (0-100) based on age"""
    created_date = datetime.fromtimestamp(created_utc)
    days_old = (datetime.now() - created_date).days
    
    if days_old <= 30:
        return 100
    elif days_old <= 90:
        return 85
    elif days_old <= 180:
        return 70
    elif days_old <= 365:
        return 50
    elif days_old <= 730:
        return 25
    else:
        return max(0, 25 - (days_old - 730) / 365 * 10)

def calculate_composite_score(post: Dict, all_data: Dict, weights: Dict) -> tuple:
    """Calculate composite percentile score"""
    scores = {}
    
    # Score/upvotes percentile
    score = post.get('score', 0)
    scores['score'] = percentile_rank(score, all_data['all_scores'])
    
    # Comments percentile
    num_comments = post.get('num_comments', 0)
    scores['comments'] = percentile_rank(num_comments, all_data['all_comments'])
    
    # Upvote ratio (absolute, not relative - >0.75 is universally good)
    ratio = post.get('upvote_ratio', 0) * 100  # Convert to 0-100 scale
    scores['ratio'] = ratio
    
    # Recency score (absolute)
    created_utc = post.get('created_utc', 0)
    scores['recency'] = calculate_recency_score(created_utc)
    
    # Weighted composite
    composite = sum(scores[metric] * weights[metric] for metric in weights.keys())
    
    return round(composite, 2), scores

def determine_cutoff_percentile(collection_size: int) -> int:
    """Determine cutoff based on collection size"""
    if collection_size <= 100:
        return 50
    elif collection_size <= 500:
        return 60
    elif collection_size <= 1000:
        return 70
    else:
        return 75

def filter_posts(posts: List[Dict], weights: Dict) -> tuple:
    """Statistical filtering using percentile ranking"""
    
    # Basic sanity filter first
    basic_filtered = []
    for post in posts:
        # Skip if: deleted, removed, or obviously spam
        if post.get('removed_by_category'):
            continue
        if post.get('author') == '[deleted]':
            continue
        # Must have at least some engagement
        if post.get('score', 0) < 1 and post.get('num_comments', 0) < 1:
            continue
        basic_filtered.append(post)
    
    if not basic_filtered:
        return [], {}
    
    # Collect metrics for statistical analysis
    all_scores = [p.get('score', 0) for p in basic_filtered]
    all_comments = [p.get('num_comments', 0) for p in basic_filtered]
    
    all_data = {
        'all_scores': all_scores,
        'all_comments': all_comments,
    }
    
    # Calculate composite scores
    scored_posts = []
    for post in basic_filtered:
        composite, breakdowns = calculate_composite_score(post, all_data, weights)
        
        created_utc = post.get('created_utc', 0)
        created_date = datetime.fromtimestamp(created_utc)
        days_old = (datetime.now() - created_date).days
        
        simplified_post = {
            'title': post.get('title'),
            'url': f"https://reddit.com{post.get('permalink')}",
            'score': post.get('score'),
            'upvote_ratio': post.get('upvote_ratio'),
            'num_comments': post.get('num_comments'),
            'created_date': created_date.strftime('%Y-%m-%d'),
            'days_old': days_old,
            'author': post.get('author'),
            'subreddit': post.get('subreddit'),
            'composite_score': composite,
            'score_breakdown': breakdowns,
        }
        
        scored_posts.append(simplified_post)
    
    # Determine cutoff
    cutoff_percentile = determine_cutoff_percentile(len(basic_filtered))
    
    # Filter by cutoff
    filtered = [p for p in scored_posts if p['composite_score'] >= cutoff_percentile]
    
    # Sort by composite score descending
    filtered.sort(key=lambda x: x['composite_score'], reverse=True)
    
    return filtered, all_data

def main():
    parser = argparse.ArgumentParser(description='Filter Reddit posts using statistical percentiles')
    parser.add_argument('--subreddit', help='Subreddit name (without r/)')
    parser.add_argument('--url', help='Reddit post or subreddit URL')
    parser.add_argument('--limit', type=int, default=1000, help='Maximum posts to fetch')
    parser.add_argument('--output', default='filtered_reddit.json', help='Output file path')
    
    args = parser.parse_args()
    
    # Determine what we're fetching
    if args.url:
        print(f"📊 Fetching Reddit data from URL...")
        data = fetch_reddit_data(args.url)
        if isinstance(data, list) and len(data) > 0:
            posts = [child['data'] for child in data[0]['data']['children']]
        else:
            posts = []
    elif args.subreddit:
        print(f"📊 Fetching posts from r/{args.subreddit}...")
        posts = parse_subreddit_posts(args.subreddit, args.limit)
    else:
        print("Error: Must provide either --url or --subreddit")
        sys.exit(1)
    
    print(f"✅ Found {len(posts)} posts")
    
    if len(posts) == 0:
        print("⚠️  No posts found.")
        sys.exit(0)
    
    # Calculate statistics
    print(f"\n📈 Calculating statistical metrics...")
    all_scores = [p.get('score', 0) for p in posts]
    all_comments = [p.get('num_comments', 0) for p in posts]
    print(f"   Scores: median={statistics.median(all_scores):.0f}, p75={percentile(all_scores, 75):.0f}, p90={percentile(all_scores, 90):.0f}")
    print(f"   Comments: median={statistics.median(all_comments):.0f}, p75={percentile(all_comments, 75):.0f}")
    
    # Filter posts
    print(f"\n🔍 Filtering using percentile-based ranking...")
    filtered, all_data = filter_posts(posts, REDDIT_WEIGHTS)
    
    cutoff_used = determine_cutoff_percentile(len(posts))
    
    # Prepare output
    output = {
        'original_count': len(posts),
        'filtered_count': len(filtered),
        'reduction': f"{((len(posts) - len(filtered)) / len(posts) * 100):.1f}%" if len(posts) > 0 else "0%",
        'platform': 'reddit',
        'source': args.url or f"r/{args.subreddit}",
        'filtering_method': 'statistical_percentile',
        'cutoff_percentile_used': cutoff_used,
        'weights_used': REDDIT_WEIGHTS,
        'statistics': {
            'score_median': statistics.median(all_data['all_scores']) if all_data.get('all_scores') else 0,
            'score_p75': percentile(all_data['all_scores'], 75) if all_data.get('all_scores') else 0,
            'comments_median': statistics.median(all_data['all_comments']) if all_data.get('all_comments') else 0,
        },
        'resources': filtered[:500],
        'next_steps': 'Review filtered list, or request Phase 2 for deep analysis'
    }
    
    # Save to file
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Filtering complete!")
    print(f"📊 Original: {len(posts)} posts")
    print(f"📊 Filtered: {len(filtered)} posts ({output['reduction']} reduction)")
    print(f"📊 Cutoff: {cutoff_used}th percentile")
    print(f"💾 Output saved to: {args.output}")
    
    if len(filtered) > 0:
        print(f"\n🏆 Top 5 posts by composite score:")
        for i, post in enumerate(filtered[:5], 1):
            print(f"{i}. {post['title'][:60]}...")
            print(f"   Score: {post['composite_score']:.1f}/100 | Upvotes: {post['score']} | Comments: {post['num_comments']}")

if __name__ == '__main__':
    main()
