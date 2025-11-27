import os
import csv
import time
from github import Github, Auth
from dotenv import load_dotenv

load_dotenv()

def collect_training_data():
    token = os.getenv("GITHUB_TOKEN")
    if not token: raise ValueError("GITHUB_TOKEN missing")

    g = Github(auth=Auth.Token(token))
    repo = g.get_repo("flutter/flutter") # High volume, reliable text
    
    csv_file = "dataset.csv"
    # KEY CHANGE: We are capturing 'title' and 'body' for the LSTM
    headers = ["pr_id", "state", "user", "title", "body", "files_changed", "is_merged"]
    
    TARGET = 60 # Small batch for speed (30 merged, 30 closed)
    count_merged = 0
    count_closed = 0

    print(f"[*] Mining {repo.name} for LSTM training data...")
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Fetch closed PRs (contains both merged and unmerged)
        pulls = repo.get_pulls(state='closed', sort='updated', direction='desc')[:300]
        
        for pr in pulls:
            if count_merged >= TARGET/2 and count_closed >= TARGET/2:
                break
                
            try:
                is_merged = pr.merged
                
                # Balance classes
                if is_merged and count_merged >= TARGET/2: continue
                if not is_merged and count_closed >= TARGET/2: continue
                
                # Text Cleaning (Minimal)
                title = pr.title.replace('\n', ' ').replace(',', ' ')
                # Handle None bodies
                body = (pr.body or "").replace('\n', ' ').replace(',', ' ')[:1000] 
                
                row = [
                    pr.number,
                    pr.state,
                    pr.user.login,
                    title,  # FEATURE A
                    body,   # FEATURE B
                    pr.changed_files,
                    1 if is_merged else 0
                ]
                
                writer.writerow(row)
                
                if is_merged: count_merged += 1
                else: count_closed += 1
                
                print(f"\r[+] Merged: {count_merged} | Closed: {count_closed}", end="", flush=True)
                
            except Exception as e:
                pass

    print(f"\n[SUCCESS] Generated {csv_file} with raw text features.")

if __name__ == "__main__":
    collect_training_data()
