---
# Core Classification
protocol: Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51789
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/altcoinist/staking
source_link: https://www.halborn.com/audits/altcoinist/staking
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

No slippage protection for swaps

### Overview


This bug report discusses a potential vulnerability in the code of a protocol that could result in a loss of funds through malicious attacks. The code allows for a minimum of 0 output tokens from a swap, making it susceptible to MEV bot sandwich attacks. The report recommends implementing a maximum slippage or minimum amount of output tokens that must be received from the swap, with a sensible default if not specified by the user. The team responsible for the code has accepted the risk and references specific code lines that need to be addressed.

### Original Finding Content

##### Description

The code lines mentioned in the `References` section indicates that a minimum amount of 0 output tokens from the swap is acceptable, opening up the protocol to a loss of funds via MEV bot sandwich attacks.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:L/D:M/Y:N/R:N/S:U (6.9)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:L/D:M/Y:N/R:N/S:U)

##### Recommendation

Allow the caller to specify a maximum slippage or minimum amount of output tokens to be received from the swap, such that the swap will revert if it wouldn't return the caller-specified minimum amount of output tokens.

Also provide a sensible default if the caller doesn't specify a value, but user-specified slippage parameters must always override defaults.

##### Remediation

**RISK ACCEPTED**: The **Altcoinist team** accepted the risk of this issue.

##### References

[altcoinist-com/contracts/src/ALTT.sol#L92-L93](https://github.com/altcoinist-com/contracts/blob/master/src/ALTT.sol#L92-L93)

[altcoinist-com/contracts/src/StakingVault.sol#L216-L217](https://github.com/altcoinist-com/contracts/blob/master/src/StakingVault.sol#L216-L217)

[altcoinist-com/contracts/src/SubscribeRegistry.sol#L225-L226](https://github.com/altcoinist-com/contracts/blob/master/src/SubscribeRegistry.sol#L225-L226)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Staking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/altcoinist/staking
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/altcoinist/staking

### Keywords for Search

`vulnerability`

