---
# Core Classification
protocol: Ocean Vesting Wallet Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32962
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ocean-vesting-wallet-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Insufficient Input Validation for Vesting Schedule

### Overview


The bug report states that there is a problem with the input arguments of the constructor in a specific code. This can cause issues such as using a timestamp that has already passed or is too far in the future, setting a value of zero for a certain function, and allowing users to instantly release all allocated tokens and Ether. To fix this, it is suggested to add specific limits for each argument in the constructor to prevent these problems from occurring. This issue has been resolved in a recent update.

### Original Finding Content

The input arguments of the [`constructor`](https://github.com/oceanprotocol/vw-cli/blob/0397c74da60ae50db5c6414307849120b899af6e/contracts/VestingWalletHalving.sol#L38-L52) are not sufficiently validated. Some problematic scenarios will arise from this, including:  
       • `startTimestamp` can be a timestamp that has already passed or is too far away in the              future.  
       • `halfLife` can be zero, causing the [`getAmount function`](https://github.com/oceanprotocol/vw-cli/blob/0397c74da60ae50db5c6414307849120b899af6e/contracts/VestingWalletHalving.sol#L179-L187) to always revert.  
       • `duration` can be zero, allowing a user to instantly release all allocated tokens and Ether.


Consider adding sensible lower and upper bounds for all arguments of the constructor to ensure none of the outlined scenarios occur.


***Update:** Resolved in pull [request #42](https://github.com/oceanprotocol/vw-cli/pull/42) at commit [a009de2](https://github.com/oceanprotocol/vw-cli/pull/42/commits/a009de280b46f865d137ff7f39757d51d75216b2).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ocean Vesting Wallet Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ocean-vesting-wallet-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

