---
# Core Classification
protocol: Debridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56153
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-09-16-DeBridge.md
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

An attacker, could make a malicious smart contract that is going to borrow money from the flash loan function, and in the flashCallback function that he implements, he could call the send function from the DeBridgeGate contract, adding the balance back in the contract but also emitting a Send event, that will be captured by the validators and tokens will be minted on the other chains. After that, he can burn the tokens from the other chains to retrieve them back in the original chain and stole all the liqui

### Overview


This bug report recommends adding a modifier called nonReentrant to prevent a potential attack. This modifier will cause the send function to revert if it is called multiple times from within the flashCallback function. This will help prevent any issues that may arise from the function being called multiple times.

### Original Finding Content

**Recommendation**:

You can prevent this attack by adding the nonReentrant modifier on the send function, so
when the flashCallback function will call the send function it will revert because it already was
previously in the flash function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Debridge |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-09-16-DeBridge.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

