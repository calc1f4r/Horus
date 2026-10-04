---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7314
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - decimals

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

claim() will underflow and revert for all tokens without 18 decimals

### Overview


This bug report is about the "claim()" function in the WithdrawProxy.sol code. The issue is that if the number of decimals in the token is under 17 and the withdraw ratio is greater than 10%, it will lead to an underflow and cause the function to revert. The recommendation is to adjust the code to include a "+ 1e18 - s.withdrawRatio" to the calculation of the amount to decrease the Y intercept of the vault. This will ensure that the token's decimals don't matter and the vault's y-intercept is measured correctly. This bug report is important because the code is planned to be generalized to accept all ERC20s.

### Original Finding Content

## Severity
Medium Risk

## Context
WithdrawProxy.sol#238-244

## Description
In the `claim()` function, the amount to decrease the Y intercept of the vault is calculated as:

```
(s.expected - balance).mulWadDown(10**ERC20(asset()).decimals() - s.withdrawRatio)
```

`s.withdrawRatio` is represented as a WAD (18 decimals). As a result, using any token with a number of decimals under 17 (assuming the withdraw ratio is greater than 10%) will lead to an underflow and cause the function to revert.

In this situation, the token's decimals don't matter. They are captured in `s.expected` and `balance`, and are also the scale at which the vault's y-intercept is measured, so there's no need to adjust for them.

**Note**: I know this isn't a risk in the current implementation, since it's WETH only, but since you are planning to generalize to accept all ERC20s, this is important.

## Recommendation
```solidity
if (balance < s.expected) {
    PublicVault(VAULT()).decreaseYIntercept(
        (s.expected - balance).mulWadDown(
            -10**ERC20(asset()).decimals() - s.withdrawRatio
            + 1e18 - s.withdrawRatio
        )
    );
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Decimals`

