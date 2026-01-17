---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27857
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Stablecoin%20(crvUSD)/README.md#2-not-formalized-stablecoin-minting-to-addresses
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
  - MixBytes
---

## Vulnerability Title

Not formalized stablecoin minting to addresses

### Overview


The bug report is about the `ControllerFactory` admin being able to mint any amount of stablecoin to any address without verifying if the receiver is among Controllers or PegKeepers. This process is not protected and requires strong admin attention. 

The recommendation is to check that the inputted address in `set_debt_ceiling` is allowed to receive mint stablecoins (is among either Controllers or PegKeepers). This will ensure that only authorized users can receive the minted stablecoins. 

This bug report is important as it highlights a security vulnerability in the system which could be exploited by malicious actors. It is important to fix this bug as soon as possible by implementing the recommended solution.

### Original Finding Content

##### Description

Admin of `ControllerFactory` can mint any amount of stablecoin to any address calling `set_debt_ceiling`. It is designed to mint tokens to Controllers, but the function does not check that a receiver is among Controllers.
- https://github.com/curvefi/curve-stablecoin/blob/0d9265cc2dbd221b0f27f880fac1c590e1f12d28/contracts/ControllerFactory.vy#L306-L313

Moreover, this function is used to mint tokens to PegKeepers, and there are no checks that a receiver is among PegKeepers. The whole process is not protected and requires strong admin attention.

##### Recommendation

We recommend checking that the inputted address in `set_debt_ceiling` is allowed to receive mint stablecoins (is among either Controllers or PegKeepers).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Stablecoin%20(crvUSD)/README.md#2-not-formalized-stablecoin-minting-to-addresses
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

