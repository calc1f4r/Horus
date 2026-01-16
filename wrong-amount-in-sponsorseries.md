---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6793
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Denis Milicevic
  - Gerard Persoon
---

## Vulnerability Title

Wrong Amount in sponsorSeries

### Overview


This bug report is about a situation in the function sponsorSeries() in the Periphery.sol#L66-76 file. The issue is that when the number of decimals of the stake token is not equal to 18, a different amount is used with safeTransferFrom() than with safeApprove(). The recommendation is to double check which of these two amounts is the right amount and update the code, as well as consider adding unit tests with Stake tokens with less than 18 decimals. The issue has been fixed by getting rid of _convertToBase so that the amount should just be stakeSize.

### Original Finding Content

## Severity: High Risk

## Context
Periphery.sol#L66-76

## Situation
In function `sponsorSeries()`, a different amount is used with `safeTransferFrom()` than with `safeApprove()`, if the number of decimals of the stake token is not equal to 18. Normally, `safeTransferFrom()` and `safeApprove()` should be the same amount.

```solidity
function sponsorSeries(address adapter, uint48 maturity) external returns (address zero, address claim) {
    // Transfer stakeSize from sponsor into this contract
    uint256 stakeDecimals = ERC20(stake).decimals();
    ERC20(stake).safeTransferFrom(msg.sender, address(this), _convertToBase(stakeSize, stakeDecimals)); // amount 1
    // Approve divider to withdraw stake assets
    ERC20(stake).safeApprove(address(divider), stakeSize); // amount 2
}
```

## Recommendation
Spearbit recommends double checking which of these two amounts is the right amount and updating the code. We also recommend considering adding unit tests with stake tokens that have less than 18 decimals.

## Sense
Fixed here. We’ve gotten rid of `_convertToBase` so the amount should just be `stakeSize`.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sense |
| Report Date | N/A |
| Finders | Max Goodman, Denis Milicevic, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

