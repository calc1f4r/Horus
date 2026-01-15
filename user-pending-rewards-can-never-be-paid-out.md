---
# Core Classification
protocol: IntentX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59427
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/intent-x/a195e62f-30b6-4219-b9e5-42af8a9e2fd5/index.html
source_link: https://certificate.quantstamp.com/full/intent-x/a195e62f-30b6-4219-b9e5-42af8a9e2fd5/index.html
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
finders_count: 3
finders:
  - Mustafa Hasan
  - Adrian Koegl
  - Cameron Biniamow
---

## Vulnerability Title

User Pending Rewards Can Never Be Paid Out

### Overview


The client reported a bug in the `StakedINTX.sol` file where the `claim()` function was not working properly. The issue was that the `_amountOut` variable was being set to zero instead of the correct value, causing the user's pending rewards to be lost. The recommendation is to set the `_owner` variable to the caller's address to fix the bug.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `31182abb586743450bcfb4359b26b5eee34b7f4d`. The client provided the following explanation:

> Now, _msgSender is used for pendingRewards[].

**File(s) affected:**`StakedINTX.sol`

**Description:** The `claim()` function performs the following two lines of code:

```
address _owner;
uint _amountOut = pendingRewards[_owner];
```

As can be seen, the `_amountOut` initial value is set before the `_owner` address is set to the output of `_ownerOf(_tokenId)` later on in the function logic. This means that `_amountOut` will always be initialized to zero instead of the initial `pendingRewards` entry of the transaction sender.

After adding up the rewards of each `xINTX` token and the pending rewards (`0`), the caller's pending rewards are reset to zero, resulting in the user's pending rewards being lost forever.

**Recommendation:** Set the local variable, `_owner`, as the caller's address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | IntentX |
| Report Date | N/A |
| Finders | Mustafa Hasan, Adrian Koegl, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/intent-x/a195e62f-30b6-4219-b9e5-42af8a9e2fd5/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/intent-x/a195e62f-30b6-4219-b9e5-42af8a9e2fd5/index.html

### Keywords for Search

`vulnerability`

