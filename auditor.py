import os
import requests

# Use the environment variable from GitHub Actions
TOKEN = os.getenv("AUDIT_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}
BASE_URL = "https://api.github.com"

def run_audit():
    print("--- GOVERNANCE AUDIT REPORT ---")
    repos = requests.get(f"{BASE_URL}/user/repos?type=owner", headers=HEADERS).json()
    
    if not isinstance(repos, list):
        print("Error: Could not fetch repositories. Check your token.")
        return

    for repo in repos:
        name = repo['name']
        is_private = repo['private']
        
        # Policy 1: No Public Repos (for sensitive accounts)
        policy_public = "PASS" if is_private else "FAIL (Public Repo)"
        
        # Policy 2: Check for LICENSE
        has_license = repo.get('license') is not None
        policy_license = "PASS" if has_license else "FAIL (No License)"

        print(f"Repo: {name.ljust(20)} | Privacy: {policy_public} | License: {policy_license}")

if __name__ == "__main__":
    run_audit()