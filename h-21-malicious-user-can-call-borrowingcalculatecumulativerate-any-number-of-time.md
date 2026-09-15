---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45474
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/778

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
finders_count: 15
finders:
  - volodya
  - Audinarey
  - 0xAadi
  - KobbyEugene
  - RampageAudit
---

## Vulnerability Title

H-21: Malicious user can call `borrowing::calculateCumulativeRate()` any number of times to inflate debt rate as `lastEventTime` is not updated

### Overview


This report discusses a bug found in a blockchain project. The bug allows a malicious user to inflate the debt rate by repeatedly calling a function called `borrowing::calculateCumulativeRate()`. This is because the function does not update a variable called `lastEventTime`. This can result in borrowers having to repay a significantly higher amount of debt. The bug was found by multiple users and can be exploited by depositing cds and borrowing. The impact of this bug is significant as it can cause borrowers to suffer large financial losses. To fix this issue, the developers need to update the `lastEventTime` variable in the function. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/778 

## Found by 
0x37, 0x73696d616f, 0xAadi, Audinarey, Cybrid, EgisSecurity, John44, KobbyEugene, PeterSR, RampageAudit, almurhasan, durov, onthehunt, super\_jack, volodya

### Summary

[borrowing::calculateCumulativeRate()](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowing.sol#L530) does not update `lastEventTime`, so the cumulative rate may be increased unbounded, forcing users to repay much more debt.

### Root Cause

In `borrowing::calculateCumulativeRate()`, `lastEventTime` is not updated.

### Internal pre-conditions

None.

### External pre-conditions

None.

### Attack Path

1. Users deposit cds.
2. Users borrow.
3. Malicious user calls `borrowing::calculateCumulativeRate()` any number of times.
4. Borrowers have to repay much more debt.

### Impact

Borrowers take massive losses as they have to repay much more.

### PoC

See links above.

### Mitigation

Update `lastEventTime`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | volodya, Audinarey, 0xAadi, KobbyEugene, RampageAudit, durov, Cybrid, 0x73696d616f, PeterSR, almurhasan, EgisSecurity, 0x37, onthehunt, John44, super\_jack |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/778
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

