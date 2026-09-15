---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53712
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Rewards_Coordinator_Security_Assessment_Report_v1.1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Rewards_Coordinator_Security_Assessment_Report_v1.1.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Lack Of Access Control Checks On initialize()

### Overview

See description below for full details.

### Original Finding Content

## Security Audit Report

## EG4-02 - No Access Control on Initialization Function

### Status
Open

### Rating
Severity: Low  
Impact: Low  
Likelihood: Low  

### Description
There are no access control checks on the `initialize()` function used to configure the contract during deployment. If there is a period when the contracts have been deployed but not initialised, an attacker could front-run the initialisation process by calling `initialize()` to set their own parameters, such as owner address or protocol-specific values.

### Recommendations
Implement access controls on the `initialize()` function to ensure it can only be called by specific, trusted addresses. Ideally, ensure the entire deployment and initialisation process is performed in a single transaction. Note that, depending on the current deployment procedure, it is possible that this issue is already addressed.

---

## EG4-03 - Rounding In Calculations Leaves Tokens Unassigned

### Asset
EigenLayer Rewards Calculation

### Status
Open

### Rating
Severity: Low  
Impact: Low  
Likelihood: Low  

### Description
There are two instances in the reward calculation where rounding will leave tokens from a reward range unassigned and thus locked in the contract. Note that the number of locked tokens would be very low, so the impact of this issue is minimal.

The first instance is in the "Active Rewards" section:

```sql
SELECT amount / (duration / 86400) as tokens_per_day
```

`duration` is always a multiple of `86400`. The maximum duration multiple in the test suite is 70. Taking that as a reference point, the resultant expression `amount / 70` could lose, at most, 69 tokens for each of 70 days, which is 4830 wei per range.

The second instance is in the "Total-Tokens" section:

```sql
SELECT *,
cast(cast(staker_proportion AS DECIMAL(38,15)) * tokens_per_day AS DECIMAL(38,0)) as total_staker_operator_payout
FROM staker_proportion
```

As explained in the document, the decimal places are truncated to 15 for the double storage format in the database. Since this format is used to calculate the column "Total Staker Operator Payouts," a maximum of 999 wei can be lost per staker per reward hash per day. This could potentially accumulate to millions of wei of each reward token. In all known cases, this is still a small total value and could only become more of a concern if a token was used with an exceptionally high unit value, such that millions of wei became a problem.

### Recommendations
Consider calculating unassigned tokens per day and paying them back to the appropriate AVS, which could potentially be done using the existing Merkle rewards system.

---

## EG4-04 - Unnecessary Same Day Registration Calculation

### Asset
EigenLayer Rewards Calculation

### Status
Open

### Rating
Informational

### Description
In the section "Operator AVS Registration Windows," registrations and deregistrations done on the same day are specifically filtered out by targeted queries. However, same-day registrations would all have their end date equal to or before their start time. It would therefore be possible to remove these registrations in step 5 by changing this condition:

```sql
WHERE start_time != end_time
```

to:

```sql
WHERE start_time < end_time
```

### Recommendations
Consider implementing the suggested simplification.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Rewards_Coordinator_Security_Assessment_Report_v1.1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Rewards_Coordinator_Security_Assessment_Report_v1.1.pdf

### Keywords for Search

`vulnerability`

