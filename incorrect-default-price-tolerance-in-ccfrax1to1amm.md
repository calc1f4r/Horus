---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17925
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

Incorrect default price tolerance in CCFrax1to1AMM

### Overview

See description below for full details.

### Original Finding Content

## Difficulty: Undetermined

## Type: Patching

## Target: CCFrax1to1AMM.sol

## Description
The `price_tolerance` state variable of the `CCFrax1to1AMM` contract is set to 50,000, which, when using the fixed point scaling factor, is inconsistent with the variable’s inline comment, which indicates the number 5,000, corresponding to 0.005. A price tolerance of 0.05 is probably too high and can lead to unacceptable arbitrage activities; this suggests that `price_tolerance` should be set to the value indicated in the code comment.

```solidity
uint256 public price_tolerance = 50000;  // E6. 5000 = .995 to 1.005
```

**Figure 12.1:** The `price_tolerance` state variable (CCFrax1to1AMM.sol#56)

## Exploit Scenario
This issue exacerbates the exploit scenario presented in issue TOB-FRSOL-008. Given that scenario, but with a price tolerance of 50,000, Alice is able to gain $5459 through arbitrage. A higher price tolerance leads to higher arbitrage profits.

## Recommendations
- **Short term:** Set the price tolerance to 5,000 both in the code and on the deployed contract.
- **Long term:** Ensure that comments are in sync with the code and that constants are correct.

---

### Trail of Bits
Frax Solidity Security Assessment  
PUBLIC

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`

