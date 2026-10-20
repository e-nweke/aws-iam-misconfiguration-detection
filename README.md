[README.md](https://github.com/user-attachments/files/33665109/README.md)
# AWS IAM Misconfiguration: Detection & Mitigation (Experimental Evaluation)

**MSc Cybersecurity Individual Project - Coventry University (Distinction)**

## Overview
Identity and Access Management (IAM) misconfigurations are one of the leading causes of cloud security breaches. This project set up a controlled AWS environment, deliberately introduced realistic IAM misconfigurations, exploited them through simulated privilege escalation and lateral movement attacks, and then evaluated how well industry-standard detection tools caught the exploitation compared to a custom log-based detection script I built myself.

## Problem
Most IAM misconfiguration detection relies on static policy analysis. This project asked: **how well do these tools actually perform against real exploit behaviour, not just bad configuration on paper?**

## Environment
Built in AWS (Free Tier) using:
- **EC2** — compute resource / attacker interaction point
- **S3** — storage target for access control and data exposure testing
- **Lambda** — serverless cross-service permission testing
- **IAM** — the core target: users, roles, policies, trust relationships
- **CloudTrail** — full API activity logging across all regions

## Misconfigurations Implemented
| Misconfiguration | Description | Impact |
|---|---|---|
| `OverPermissiveFullAccess` | Wildcard `Action: "*", Resource: "*"` policy | Full administrative access |
| `S3WildcardAccess` | Unrestricted access to all S3 buckets | Data exposure |
| `EscalationRole` trust policy | `Principal: "*"` any entity could assume the role | Unauthorised role assumption |
| Cross-service permissions | Excessive EC2/Lambda role permissions | Lateral movement |

## Attack Simulation
1. **Privilege escalation** — used `sts:AssumeRole` to exploit the misconfigured trust relationship and obtain temporary elevated credentials
2. **Verification** — confirmed escalation via `aws sts get-caller-identity`
3. **Lateral movement** — used the elevated credentials to enumerate and access S3 buckets via the wildcard policy

All steps were traceable end-to-end through CloudTrail logs.

## Detection Tools Evaluated
| Tool | Type | Result |
|---|---|---|
| AWS IAM Access Analyzer | Native AWS | Flagged the insecure trust relationship, but missed the full escalation path |
| Prowler | Rule-based auditing (CIS benchmarks) | Best static-tool coverage — flagged excessive permissions and escalation risk |
| ScoutSuite | Visual/multi-cloud auditing | Moderate coverage, useful dashboard, missed multi-step attack chains |
| **Custom log-based detection script (Python)** | Runtime/behavioural, built on CloudTrail | **Only approach that detected the actual `AssumeRole` exploitation event in real time** |

**Key finding:** static analysis tools are good at spotting bad configuration, but none of them detected the live exploit behaviour. Only log-based, runtime monitoring caught the actual attack as it happened.

## Mitigation & Validation
- Removed wildcard policies, replaced with least-privilege scoped permissions
- Restricted the `EscalationRole` trust policy to specific AWS services only
- Reduced EC2/Lambda roles to only their required permissions
- **Re-ran the full attack after mitigation** — privilege escalation attempt failed (`AccessDenied`), confirming the fix worked

| Security Aspect | Before | After |
|---|---|---|
| Privilege Escalation | Successful | Blocked |
| S3 Access | Unrestricted | Restricted |
| Trust Relationships | Open (`*`) | Secured |
| Detection Capability | Partial | Improved |

## Key Takeaway
Combining **secure configuration practices** (least privilege, restricted trust policies) with **continuous runtime monitoring** (CloudTrail + behavioural detection) is significantly more effective than relying on static policy analysis alone which is the core argument of the dissertation and the main practical insight for anyone securing IAM in production.

## Tools & Technologies
`AWS IAM` `EC2` `S3` `Lambda` `CloudTrail` `AWS STS` `Python` `AWS CLI` `IAM Access Analyzer` `Prowler` `ScoutSuite`

## Full Report
The full dissertation is available on request. Feel free to connect with me on LinkedIn.

---
*Supervised by Dr Xingang Wang, Coventry University, 2025/26*
