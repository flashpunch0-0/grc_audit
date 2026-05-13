# import os
# import requests

# # Use the environment variable from GitHub Actions
# TOKEN = os.getenv("AUDIT_TOKEN")
# HEADERS = {"Authorization": f"token {TOKEN}"}
# BASE_URL = "https://api.github.com"

# def run_audit():
#     print("--- GOVERNANCE AUDIT REPORT ---")
#     repos = requests.get(f"{BASE_URL}/user/repos?type=owner", headers=HEADERS).json()
    
#     if not isinstance(repos, list):
#         print("Error: Could not fetch repositories. Check your token.")
#         return

#     for repo in repos:
#         name = repo['name']
#         is_private = repo['private']
        
#         # Policy 1: No Public Repos (for sensitive accounts)
#         policy_public = "PASS" if is_private else "FAIL (Public Repo)"
        
#         # Policy 2: Check for LICENSE
#         has_license = repo.get('license') is not None
#         policy_license = "PASS" if has_license else "FAIL (No License)"

#         print(f"Repo: {name.ljust(20)} | Privacy: {policy_public} | License: {policy_license}")

# if __name__ == "__main__":
#     run_audit()

import os
import requests
import json

# Configuration
TOKEN = os.getenv("AUDIT_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
BASE_URL = "https://api.github.com"
CRITICAL_THRESHOLD = 70

# Risk Weights
POLICIES = {
    "public_repo": {"weight": 40, "label": "Severity:Critical", "desc": "Repository is Public"},
    "no_protection": {"weight": 30, "label": "Severity:High", "desc": "Main branch not protected"},
    "no_license": {"weight": 10, "label": "Severity:Low", "desc": "Legal Compliance: No License"},
}

def create_remediation_issue(repo_full_name, failed_policies):
    """Automatically opens a security issue in the non-compliant repo."""
    url = f"{BASE_URL}/repos/{repo_full_name}/issues"
    issue_body = {
        "title": "🚨 Sentinel GRC: Automated Compliance Failure",
        "body": "## Security Governance Audit\nThis repository failed the following policies:\n\n- " + 
                "\n- ".join(failed_policies) + 
                "\n\n**Action Required:** Remediate these issues to restore compliance score.",
        "labels": ["governance-alert", "security"]
    }
    requests.post(url, headers=HEADERS, json=issue_body)

def audit_repositories():
    print("Initializing Sentinel GRC Engine...")
    repos = requests.get(f"{BASE_URL}/user/repos?type=owner", headers=HEADERS).json()
    
    report_data = []

    for repo in repos:
        name = repo['full_name']
        score = 100
        failures = []

        # 1. Privacy Check
        if not repo['private']:
            score -= POLICIES['public_repo']['weight']
            failures.append(POLICIES['public_repo']['desc'])

        # 2. Branch Protection Check
        branch_url = f"{BASE_URL}/repos/{name}/branches/main/protection"
        res = requests.get(branch_url, headers=HEADERS)
        if res.status_code != 200:
            score -= POLICIES['no_protection']['weight']
            failures.append(POLICIES['no_protection']['desc'])

        # 3. License Check
        if not repo.get('license'):
            score -= POLICIES['no_license']['weight']
            failures.append(POLICIES['no_license']['desc'])

        # Trigger Remediation if Score is low
        if score < CRITICAL_THRESHOLD and failures:
            print(f"Alert: {name} is Non-Compliant ({score}). Opening Issue...")
            create_remediation_issue(name, failures)

        report_data.append({"repo": name, "score": score, "status": "PASS" if score >= 80 else "FAIL"})

    # Generate a simple JSON artifact for the dashboard
    with open("compliance_summary.json", "w") as f:
        json.dump(report_data, f, indent=4)
    
    print("Audit Complete. Artifact generated.")

if __name__ == "__main__":
    audit_repositories()