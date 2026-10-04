---
# Core Classification
protocol: Dharma Labs Smart Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16794
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
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
finders_count: 2
finders:
  - eric.rafaloﬀ@trailofbits.com Dominik Czarnota
  - Eric Rafaloﬀ
---

## Vulnerability Title

Missing validation in contract initialization function

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

## Target
Multiple Files

## Difficulty
Medium

## Description
The `initialize` function in the `AdharmaSmartWalletImplementation` contract is missing address validation for the key parameter, as highlighted in Figure 5.1.

```
// Keep the initializer function on the contract in case a smart wallet has
// not yet been deployed but the account still contains user funds.
function initialize(address key) external {
    // Ensure that this function is only callable during contract construction.
    assembly { if extcodesize(address) { revert(0, 0) } }
    // Set up the user's key.
    _key = key;
}
```
*Figure 5.1: The initialize function.*

## Exploit Scenario
Due to human error or a bug in a deployment script, an address of zero is passed to the initialization function, incorrectly setting the user’s key to zero.

## Recommendation
- **Short term**: Validate that a supplied key is not equal to zero.
- **Long term**: Add additional unit testing to check that invalid input is rejected from the `initialize` function.

© 2019 Trail of Bits  
Dharma Labs Smart Wallet Review | 17

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Dharma Labs Smart Wallet |
| Report Date | N/A |
| Finders | eric.rafaloﬀ@trailofbits.com Dominik Czarnota, Eric Rafaloﬀ |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf

### Keywords for Search

`vulnerability`

