---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6931
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
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
  - validation

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

PositionsManagerForAave claimToTreasury could allow sending underlying to 0x address

### Overview


This bug report is about the PositionsManagerForAave smart contract. It states that currently, the claimToTreasury function is not verifying if the treasuryVault address is not equal to address(0). This means that the owner of the contract can burn the underlying token instead of sending it to the intended treasury address. 

The recommendation is to add a check to prevent sending treasury underlying tokens to address(0) and verify that the amountToClaim is not equal to 0. This is to prevent wasting gas and emitting a "false" event. 

Morpho has fixed this bug in PR #562 and Spearbit has acknowledged this.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
PositionsManagerForAave.sol#L223-L232

## Description
The `claimToTreasury` function is currently not verifying if the `treasuryVault` address is not equal to `address(0)`. In the current state, it would allow the owner of the contract to burn the underlying token instead of sending it to the intended treasury address.

## Recommendation
Add a check to prevent sending treasury underlying tokens to `address(0)` and verify that the `amountToClaim` is not equal to `0` to prevent wasting gas and emitting a “false” event.

```solidity
function claimToTreasury(address _poolTokenAddress)
external
onlyOwner
isMarketCreatedAndNotPaused(_poolTokenAddress)
{
    require(treasuryVault != address(0), "treasuryVault != address(0)");
    ERC20 underlyingToken = ERC20(IAToken(_poolTokenAddress).UNDERLYING_ASSET_ADDRESS());
    uint256 amountToClaim = underlyingToken.balanceOf(address(this));
    require(amountToClaim != 0, "amountToClaim != 0");
    underlyingToken.safeTransfer(treasuryVault, amountToClaim);
    emit ReserveFeeClaimed(_poolTokenAddress, amountToClaim);
}
```

## References
- **Morpho**: Fixed in PR #562.
- **Spearbit**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

