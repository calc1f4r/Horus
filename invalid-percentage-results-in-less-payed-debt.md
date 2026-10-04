---
# Core Classification
protocol: SCProtection
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50754
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/degis/scprotection-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/degis/scprotection-smart-contract-security-assessment
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

INVALID PERCENTAGE RESULTS IN LESS PAYED DEBT

### Overview


The `payDebt` function in the `IncidentReport` section of the code is not working properly. It is using the wrong value to calculate debt percentages. The code states that the `DEBT_RATIO` is 80%, but it is actually using 0.8%. This is causing issues with the function. This bug has a medium impact and a low likelihood of occurring. The recommended solution is to change the calculation to use a maximum ratio of 100:1 between the two values.

### Original Finding Content

##### Description

The `payDebt` function under `IncidentReport` is using an invalid numeric value to perform debt percentage calculations. The `DEBT_RATIO` is stated as `uint256 constant DEBT_RATIO = 80; // 80% as the debt to unlock veDEG` while the actual used value corresponds to `0.8%` instead of the expected `80%`.

Code Location
-------------

#### src/voting/incidentReport/IncidentReport.sol

```
function payDebt(uint256 _id, address _user) external {
    UserVote memory userVote = votes[_user][_id];
    uint256 finalResult = reports[_id].result;

    if (finalResult == 0) revert IncidentReport__NotSettled();
    if (userVote.choice == finalResult || finalResult == TIED_RESULT)
        revert IncidentReport__NotWrongChoice();
    if (userVote.paid) revert IncidentReport__AlreadyPaid();

    uint256 debt = (userVote.amount * DEBT_RATIO) / 10000;


```

![percentage_issue.png](https://halbornmainframe.com/proxy/audits/images/659ea53fa1aa3698c0ebdb6b)

##### Score

Impact: 5  
Likelihood: 3

##### Recommendation

**SOLVED**: The client stated the following: The debt is paid in the form of "DEG". And here user's voting amount is calculated by "veDEG". The max generation ratio between DEG and veDEG is 100（1 DEG max generate 100veDEG) and we all treat it as this max ratio. So, the 10000 is composited of 100\*100.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | SCProtection |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/degis/scprotection-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/degis/scprotection-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

