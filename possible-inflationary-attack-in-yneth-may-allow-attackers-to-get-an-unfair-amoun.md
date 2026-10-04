---
# Core Classification
protocol: Yieldnest
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35545
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-07-YieldNest.md
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
  - Zokyo
---

## Vulnerability Title

Possible Inflationary Attack In ynETH May Allow Attackers To Get An Unfair Amount of Shares

### Overview


The ynETH.sol contract has a bug where malicious users can unfairly receive a large amount of ynETH tokens by depositing a small amount of Ether. This is because the contract relies on the execution and consensus layers to determine the amount of tokens to distribute, and anyone can trigger the rewards distribution function. The first user to deposit will also receive a disproportionate amount of tokens compared to subsequent users. It is recommended to bootstrap deposits in a similar way to the ynLSD contract to make this bug more expensive to trigger. The bug has been resolved.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

The ynETH.sol contract relies on the execution layer receiver and the consensus layer receivers to determine the amount of shares to distribute to the user in the form of ynETH tokens. Malicious users could forcibly transfer a certain amount of Eth into the execution layer receiver, trigger processRewards (which anybody can call) in the rewards distributor then deposit 1 wei of Ether into ynETH to cause the next user to receive an unfair amount of tokens. In addition to this, the initial user may be minted a disproportionate amount of ynETH tokens as the first depositor will be minted at a rate of 1:1 indefinitely and subsequent users are minted less (depending on the balance of incoming rewards in which case, significantly less). 

**Recommendation**: 

It’s recommended that deposits in the ynETH contract are bootstrapped similarly to the ynLSD contract to make the bug considerably more expensive to trigger.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Yieldnest |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-07-YieldNest.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

