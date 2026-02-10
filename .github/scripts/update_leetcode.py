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
            username
            profile {
                realName
                userAvatar
                reputation
                location
                websiteUrl
                countryName
            }
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
                totalSubmissionNum {
                    difficulty
                    count
                }
            }
            userContestRanking {
                rating
                globalRanking
                totalParticipatedContests
                topPercentage
            }
            languageProblemCount {
                languageName
                problemsSolved
            }
            problemsSolvedBeatsStats {
                difficulty
                percentage
            }
        }
    }
    """
    
    variables = {"username": username}
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            print(f"GraphQL Error: {data['errors']}")
            return None
            
        return data.get("data", {}).get("matchedUser")
    except Exception as e:
        print(f"Error fetching LeetCode data: {e}")
        return None

def format_leetcode_section(stats):
    """Format LeetCode section for README"""
    if not stats:
        return None
    
    user_stats = stats.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
    contest_ranking = stats.get("userContestRanking", {})
    languages = stats.get("languageProblemCount", [])
    beats = stats.get("problemsSolvedBeatsStats", [])
    
    # Calculate total problems
    total_solved = sum(item["count"] for item in user_stats)
    
    # Get difficulty breakdown
    easy = next((item["count"] for item in user_stats if item["difficulty"] == "Easy"), 0)
    medium = next((item["count"] for item in user_stats if item["difficulty"] == "Medium"), 0)
    hard = next((item["count"] for item in user_stats if item["difficulty"] == "Hard"), 0)
    
    # Get contest stats
    rating = contest_ranking.get("rating", "N/A")
    global_rank = contest_ranking.get("globalRanking", "N/A")
    top_percentage = contest_ranking.get("topPercentage", "N/A")
    
    # Get language stats
    lang_stats = sorted(languages, key=lambda x: x["problemsSolved"], reverse=True)[:3]
    lang_text = "\n".join([f"- **{lang['languageName']}:** {lang['problemsSolved']} problems solved ⭐" 
                            for lang in lang_stats])
    
    # Get performance beats
    beats_text = ", ".join([f"{beat['percentage']:.2f}%" for beat in beats])
    
    # Calculate max streak (approximation - would need additional API call)
    section = f"""## 💻 LeetCode Profile

### Problem Solving Statistics
- **Total Problems Solved:** {total_solved}
- **Contest Rating:** {rating}
- **Global Ranking:** {global_rank}
- **Top Percentage:** {top_percentage}%

### Problem Breakdown by Difficulty
- 🟢 **Easy:** {easy}
- 🟡 **Medium:** {medium}
- 🔴 **Hard:** {hard}

### Languages & Performance
{lang_text}

- **Performance Beats:** {beats_text}
- **Badges Earned:** Multiple achievement badges 🏅

**[View Full LeetCode Profile](https://leetcode.com/u/piyushmaurya132/)**

---"""
    
    return section

def update_readme(new_section):
    """Update README.md with new LeetCode section"""
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the LeetCode section
    pattern = r"## 💻 LeetCode Profile\n\n.*?\n---\n"
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_section + "\n", content, flags=re.DOTALL)
    else:
        # If section doesn't exist, insert before GitHub Statistics
        pattern = r"(## 📊 Statistics & Analytics)"
        new_content = re.sub(pattern, new_section + "\n\n\\1", content)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ README.md updated successfully!")
    return True

def main():
    username = os.getenv("LEETCODE_USERNAME", "piyushmaurya132")
    print(f"Fetching LeetCode stats for: {username}")
    
    stats = get_leetcode_stats(username)
    if stats:
        new_section = format_leetcode_section(stats)
        if new_section:
            update_readme(new_section)
            print(f"Updated at: {datetime.now().isoformat()}")
        else:
            print("Failed to format LeetCode section")
    else:
        print("Failed to fetch LeetCode stats")

if __name__ == "__main__":
    main()
