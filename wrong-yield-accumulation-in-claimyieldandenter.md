---
# Core Classification
protocol: Timeless
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6761
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
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
  - liquid_staking
  - yield
  - yield_aggregator
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - JayJonah
  - Christoph Michel
---

## Vulnerability Title

Wrong yield accumulation in claimYieldAndEnter

### Overview


This bug report is regarding the Gate.sol#L590 function called claimYieldAndEnter. This function does not accrue yield to the Gate contract itself in case xPYT is specified. This leads to the Gate contract receiving a larger yield amount than it should have. 

The recommendation is to accrue yield to the address receiving the minted tokens. The code needs to be changed such that if xPYT is not address 0, then the yield should be accrued to the address receiving the minted tokens. The Timeless team implemented this fix in PR #5. Spearbit acknowledged this.

### Original Finding Content

## High Risk Report

## Severity 
**High Risk**

## Context
`Gate.sol#L590`

## Description
The `claimYieldAndEnter` function does not accrue yield to the Gate contract itself (this) in case `xPYT` was specified. The idea is to accrue yield for the mint recipient first before increasing/reducing their balance to not interfere with the yield rewards computation. However, in case `xPYT` is used, tokens are minted to the Gate before its yield is accrued.

Currently, the transfer from this to `xPYT` through the `xPYT.deposit` call accrues yield for this after the tokens have been minted to it:

```
userPYTBalance * (updatedYieldPerToken - actualUserYieldPerToken) / PRECISION
```

and its balance increased. This leads to it receiving a larger yield amount than it should have.

## Recommendation
Accrue yield to the address receiving the minted tokens.

```solidity
// accrue yield to recipient
// no need to do it if the recipient is msg.sender, since
// we already accrued yield in _claimYield
if (pytRecipient != msg.sender) {
    if (address(xPYT) != address(0) || pytRecipient != msg.sender) {
        _accrueYield(
            vault,
            pyt,
            address(xPYT) == address(0) ? pytRecipient : address(this),
            updatedPricePerVaultShare
        );
    }
}
```

### Minting Tokens
```solidity
// mint NYTs and PYTs
yieldTokenTotalSupply[vault] += yieldAmount;
nyt.gateMint(nytRecipient, yieldAmount);
if (address(xPYT) == address(0)) {
    // mint raw PYT to recipient
    pyt.gateMint(pytRecipient, yieldAmount);
} else {
    // mint PYT and wrap in xPYT
    pyt.gateMint(address(this), yieldAmount);
    if (pyt.allowance(address(this), address(xPYT)) < yieldAmount) {
        // set PYT approval
        pyt.approve(address(xPYT), type(uint256).max);
    }
    xPYT.deposit(yieldAmount, pytRecipient);
}
```

## Timeless
Yes, if we use `sweep` below we can accrue yield in the same way as in `_enter`. Fix implemented in PR #5.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Timeless |
| Report Date | N/A |
| Finders | JayJonah, Christoph Michel |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

