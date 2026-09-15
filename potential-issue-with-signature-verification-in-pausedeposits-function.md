---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41242
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#20-potential-issue-with-signature-verification-in-pausedeposits-function
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
  - MixBytes
---

## Vulnerability Title

Potential Issue with Signature Verification in `pauseDeposits` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [pauseDeposits](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/DepositSecurityModule.sol#L384) function of the contract `DepositSecurityModule`. The current implementation of the function relies on the `ECDSA.recover` method to verify the signature provided by the guardian. However, there is a very low probability that the `recover` function can return a random address if the signature is invalid, potentially allowing the check to pass unexpectedly. This could result in unauthorized parties influencing the decision to pause deposits, which could pose a security risk.

##### Recommendation
We recommend adding an index to the message that is signed by the guardian. This will ensure that each guardian's approval is uniquely identifiable and prevent the possibility of an invalid signature inadvertently passing the check.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#20-potential-issue-with-signature-verification-in-pausedeposits-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

