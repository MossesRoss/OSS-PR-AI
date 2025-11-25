import os
from github import Github, Auth
from dotenv import load_dotenv
from risk_engine import RiskEngine

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN not found in .env file")

auth = Auth.Token(token)
g = Github(auth=auth)

engine = RiskEngine()

def analyze_repo_risks(repo_name):
    print(f"[*] Initializing OSS PR AI for target: {repo_name}...")
    try:
        repo = g.get_repo(repo_name)
        pulls = repo.get_pulls(state='all', sort='created', direction='desc')[:3]
        
        print(f"[+] Data stream established. Processing last 3 PRs...\n")
        
        for pr in pulls:
            pr_data = {
                'user': pr.user.login,
                'title': pr.title,
                'body': pr.body,
                'files': pr.changed_files
            }
            
            risk_assessment = engine.analyze_pr(pr_data)
            
            print(f"PR #{pr.number}: {pr.title}")
            print(f"   User: {pr.user.login}")
            print(f"   RISK SCORE: {risk_assessment['risk_score']} [{risk_assessment['risk_level']}]")
            if risk_assessment['flags']:
                print(f"   Flags: {risk_assessment['flags']}")
            print("-" * 60)
            
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    target_repo = "flutter/flutter"
    analyze_repo_risks(target_repo)
