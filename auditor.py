

# import os
# import requests
# import json

# # Configuration
# TOKEN = os.getenv("AUDIT_TOKEN")
# HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
# BASE_URL = "https://api.github.com"
# CRITICAL_THRESHOLD = 70

# # Risk Weights
# POLICIES = {
#     "public_repo": {"weight": 40, "label": "Severity:Critical", "desc": "Repository is Public"},
#     "no_protection": {"weight": 30, "label": "Severity:High", "desc": "Main branch not protected"},
#     "no_license": {"weight": 10, "label": "Severity:Low", "desc": "Legal Compliance: No License"},
# }

# def create_remediation_issue(repo_full_name, failed_policies):
#     """Automatically opens a security issue in the non-compliant repo."""
#     url = f"{BASE_URL}/repos/{repo_full_name}/issues"
#     issue_body = {
#         "title": "🚨 Sentinel GRC: Automated Compliance Failure",
#         "body": "## Security Governance Audit\nThis repository failed the following policies:\n\n- " + 
#                 "\n- ".join(failed_policies) + 
#                 "\n\n**Action Required:** Remediate these issues to restore compliance score.",
#         "labels": ["governance-alert", "security"]
#     }
#     requests.post(url, headers=HEADERS, json=issue_body)

# def audit_repositories():
#     print("Initializing Sentinel GRC Engine...")
#     repos = requests.get(f"{BASE_URL}/user/repos?type=owner", headers=HEADERS).json()
    
#     report_data = []

#     for repo in repos:
#         name = repo['full_name']
#         score = 100
#         failures = []

#         # 1. Privacy Check
#         if not repo['private']:
#             score -= POLICIES['public_repo']['weight']
#             failures.append(POLICIES['public_repo']['desc'])

#         # 2. Branch Protection Check
#         branch_url = f"{BASE_URL}/repos/{name}/branches/main/protection"
#         res = requests.get(branch_url, headers=HEADERS)
#         if res.status_code != 200:
#             score -= POLICIES['no_protection']['weight']
#             failures.append(POLICIES['no_protection']['desc'])

#         # 3. License Check
#         if not repo.get('license'):
#             score -= POLICIES['no_license']['weight']
#             failures.append(POLICIES['no_license']['desc'])

#         # Trigger Remediation if Score is low
#         if score < CRITICAL_THRESHOLD and failures:
#             print(f"Alert: {name} is Non-Compliant ({score}). Opening Issue...")
#             create_remediation_issue(name, failures)

#         report_data.append({"repo": name, "score": score, "status": "PASS" if score >= 80 else "FAIL"})

#     # Generate a simple JSON artifact for the dashboard
#     with open("compliance_summary.json", "w") as f:
#         json.dump(report_data, f, indent=4)
    
#     print("Audit Complete. Artifact generated.")

# if __name__ == "__main__":
#     audit_repositories()

import os
import requests
from datetime import datetime

# Configuration
TOKEN = os.getenv("AUDIT_TOKEN")
HEADERS = {
    "Authorization": f"token {TOKEN}", 
    "Accept": "application/vnd.github.v3+json"
}
BASE_URL = "https://api.github.com"

# Visual Dashboard Template - Corrected with escaped braces
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GRC Security Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #f4f7f6; color: #333; margin: 40px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #2c3e50; color: white; }}
        .PASS {{ background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px; font-weight: bold;}}
        .FAIL {{ background-color: #e74c3c; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px; font-weight: bold;}}
    </style>
</head>
<body>
    <h1>Enterprise Security & Governance Dashboard</h1>
    <p>Last Scan: {timestamp}</p>
    <table>
        <tr><th>Repository</th><th>Risk Score</th><th>Status</th><th>Automated Remediation Log</th></tr>
        {table_rows}
    </table>
</body>
</html>
"""

def enable_vulnerability_alerts(repo_full_name):
    """AUTOMATED REMEDIATION: Force-enables Dependabot/Vulnerability alerts."""
    url = f"{BASE_URL}/repos/{repo_full_name}/vulnerability-alerts"
    res = requests.put(url, headers=HEADERS)
    return res.status_code == 204 # 204 means successfully enabled

def run_audit():
    print("Initiating Sentinel GRC Scan...")
    repos = requests.get(f"{BASE_URL}/user/repos?type=owner", headers=HEADERS).json()
    
    html_rows = ""

    for repo in repos:
        name = repo['full_name']
        score = 100
        remediation_log = []

        # 1. Privacy Check (Governance)
        if not repo['private']:
            score -= 30
            remediation_log.append("Violated Policy: Public Repository.")

        # 2. Automated Remediation: Vulnerability Alerts Check (Risk)
        vuln_url = f"{BASE_URL}/repos/{name}/vulnerability-alerts"
        vuln_check = requests.get(vuln_url, headers=HEADERS)
        
        # If alerts are not enabled, the API returns a 404
        if vuln_check.status_code == 404:
            score -= 40
            print(f"[{name}] Vulnerability alerts disabled. Triggering auto-remediation...")
            
            # Trigger Auto-Fix
            if enable_vulnerability_alerts(name):
                remediation_log.append("✅ Auto-Remediated: Vulnerability Alerts Enabled via API.")
                score += 40 # Restore score because the system fixed it
            else:
                remediation_log.append("❌ Auto-Remediation Failed.")
        else:
            remediation_log.append("Vulnerability Alerts: Compliant.")

        # Determine Final Status
        status_class = "PASS" if score >= 80 else "FAIL"
        log_text = "<br>".join(remediation_log)
        
        # Add to Dashboard
        html_rows += f"<tr><td>{name}</td><td>{score}/100</td><td><span class='{status_class}'>{status_class}</span></td><td>{log_text}</td></tr>"

    # Generate the Visual Report
    final_html = HTML_TEMPLATE.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        table_rows=html_rows
    )
    
    with open("dashboard.html", "w") as f:
        f.write(final_html)
    
    print("Audit Complete. Dashboard generated at dashboard.html")

if __name__ == "__main__":
    run_audit()