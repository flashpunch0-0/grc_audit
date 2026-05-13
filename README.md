
# Sentinel GRC: Automated Governance & Remediation Engine

**Sentinel GRC** is a Python-based Technical Governance, Risk, and Compliance (GRC) framework designed to automate the oversight of GitHub repository security postures. Moving beyond static auditing, Sentinel implements a **weighted risk model** and **zero-touch remediation** to ensure infrastructure remains compliant with organizational security policies.

---

## 🚀 Core Features

* **Weighted Risk Scoring:** Evaluates repositories based on a custom risk algorithm, assigning a Security Posture Score ($0-100$).
* **Automated Remediation:** Actively patches non-compliant settings (e.g., Vulnerability Alerts/Dependabot) via the GitHub REST API without manual intervention.
* **Continuous Monitoring:** Integrated with **GitHub Actions** for scheduled, persistent compliance checks (Governance-as-Code).
* **Executive Reporting:** Generates a styled HTML Security Dashboard for transparent stakeholder visibility and audit evidence.

---

## 🛠 The Technical Logic

### 1. Risk Quantification

Sentinel doesn't treat all failures equally. It uses a weighted formula to determine the urgency of a finding:

$$Score = 100 - \sum (Weight_{i} \times Status_{i})$$

| Policy | Weight | Domain |
| --- | --- | --- |
| **Vulnerability Alerts Disabled** | 40 | Risk Management |
| **Public Repository (Sensitive)** | 30 | Data Governance |
| **Main Branch Unprotected** | 20 | Engineering Standards |
| **Missing License** | 10 | Legal Compliance |

### 2. Remediation Flow

When a critical vulnerability is detected (e.g., `vulnerability-alerts: disabled`), the engine initiates a `PUT` request to the GitHub API to force-enable the control, effectively reducing the organization's attack surface in real-time.

---

## 📂 Architecture

```text
├── .github/
│   └── workflows/
│       └── audit.yml      # Continuous Monitoring Pipeline
├── auditor.py             # Risk Engine & Remediation Logic
├── requirements.txt       # Environment Dependencies
└── README.md              # Documentation

```

---

## ⚙️ Setup & Deployment

### 1. Prerequisites

* Python 3.10+
* A GitHub **Personal Access Token (PAT)** with `repo` and `security_events` scopes.

### 2. Configuration

Add your PAT to your repository secrets:

1. Navigate to `Settings > Secrets and variables > Actions`.
2. Create a New Repository Secret named `GA_AUDIT_TOKEN`.

### 3. Usage

The system is configured to run automatically every Sunday at midnight. To trigger a manual audit:

1. Go to the **Actions** tab in GitHub.
2. Select **Continuous GRC Monitoring**.
3. Click **Run workflow**.

---

## 📊 Audit Evidence (Artifacts)

Upon completion, the workflow generates a `GRC-Executive-Dashboard`. This HTML artifact serves as a point-in-time "proof of compliance" for auditors (SOC2, ISO 27001), showcasing:

* Initial Risk Score
* Remediation Actions Taken
* Final Compliance Status

---

## 🛡 Security Impact

By shifting from manual spreadsheets to **Automated Governance**, this project reduces the "Mean Time to Remediate" (MTTR) for configuration drift from days to minutes. It demonstrates a proactive approach to the **Security Development Lifecycle (SDL)** and cloud infrastructure management.

---
