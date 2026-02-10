import os
import requests
import re
from datetime import datetime

def get_leetcode_stats(username):
    """Fetch LeetCode stats using GraphQL API"""
    url = "https://leetcode.com/graphql"
    
    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
            userContestRanking {
                rating
                globalRanking
                topPercentage
            }
        }
    }
    """
    
    variables = {"username": username}
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.post(url, json={"query": query, "variables": variables}, 
                               headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            print(f"GraphQL Error: {data['errors']}")
            return None
            
        return data.get("data", {}).get("matchedUser")
    except Exception as e:
        print(f"Error fetching LeetCode data: {e}")
        return None

def format_leetcode_stats(stats):
    """Format LeetCode stats for README"""
    if not stats:
        return None
    
    user_stats = stats.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
    contest_ranking = stats.get("userContestRanking", {})
    
    total_solved = sum(item["count"] for item in user_stats)
    easy = next((item["count"] for item in user_stats if item["difficulty"] == "Easy"), 0)
    medium = next((item["count"] for item in user_stats if item["difficulty"] == "Medium"), 0)
    hard = next((item["count"] for item in user_stats if item["difficulty"] == "Hard"), 0)
    
    rating = contest_ranking.get("rating", "N/A")
    global_rank = contest_ranking.get("globalRanking", "N/A")
    top_percentage = contest_ranking.get("topPercentage", "N/A")
    
    # Calculate percentages for progress bars
    easy_pct = int((easy / total_solved * 100) / 5) if total_solved > 0 else 0
    medium_pct = int((medium / total_solved * 100) / 5) if total_solved > 0 else 0
    hard_pct = int((hard / total_solved * 100) / 5) if total_solved > 0 else 0
    
    section = f"""### 📊 Problem Solving Statistics

```
Total Solved      {'█' * 20}░ {total_solved} Problems  (100%)
Easy              {'█' * easy_pct}{'░' * (20 - easy_pct)} {easy} Problems  ({easy/total_solved*100:.1f}%)
Medium            {'█' * medium_pct}{'░' * (20 - medium_pct)} {medium} Problems  ({medium/total_solved*100:.1f}%)
Hard              {'█' * hard_pct}{'░' * (20 - hard_pct)} {hard} Problems  ({hard/total_solved*100:.1f}%)
```

### 🎯 Contest Performance

| Metric | Value |
|:----:|:----:|
| **Rating** | {rating} ⭐ |
| **Global Rank** | Top {top_percentage}% 🚀 |
| **Problems Solved** | {total_solved} |"""
    
    return section

def update_readme(new_section):
    """Update README with new LeetCode section"""
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the LeetCode section
    pattern = r"### 📊 Problem Solving Statistics\n\n```[\s\S]*?```\n\n### 🎯 Contest Performance\n\n\| Metric \| Value \|\n\|:----:\|:----:\|\n\| \*\*Rating\*\* \| [\s\S]*?\*\*Problems Solved\*\* \| \d+ \|"
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ README.md updated successfully!")
        return True
    else:
        print("⚠️ Could not find LeetCode section to update - format may have changed")
        return False

def main():
    username = os.getenv("LEETCODE_USERNAME", "piyushmaurya132")
    print(f"🔄 Fetching LeetCode stats for: {username}")
    
    stats = get_leetcode_stats(username)
    if stats:
        new_section = format_leetcode_stats(stats)
        if new_section:
            update_readme(new_section)
            print(f"✨ Updated at: {datetime.now().isoformat()}")
        else:
            print("Failed to format LeetCode section")
    else:
        print("Failed to fetch LeetCode stats")

if __name__ == "__main__":
    main()
