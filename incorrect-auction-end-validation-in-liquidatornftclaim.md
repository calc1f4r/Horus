---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7290
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
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
  - validation
  - business_logic

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

Incorrect auction end validation in liquidatorNFTClaim()

### Overview


This bug report is about a possible exploit scenario in the CollateralToken.sol file at line 119. The exploit occurs when a user calls the liquidatorNFTClaim() function and sets the params.endTime to be less than the block.timestamp. This allows them to transfer the underlying asset to the liquidator. To fix this issue, the parameter passed to liquidatorNFTClaim() needs to be validated against the parameters created for the Seaport auction. This can be done by updating the collateralIdToAuction mapping so it maps from collateralId to Seaport order hash, and updating usages of collateralIdToAuction to include a check for the order hash. Additionally, liquidatorNFTClaim() should verify that the hash of params matches the value stored in the collateralIdToAuction mapping, to validate that params.endTime is not spoofed. Astaria has already fixed the issue in PR 210, and Spearbit has verified the fix.

### Original Finding Content

## Severity: High Risk

## Context
`CollateralToken.sol#L119`

## Description
The function `liquidatorNFTClaim()` includes a check to determine if a Seaport auction has ended:

```solidity
if (block.timestamp < params.endTime) {
    // auction hasn't ended yet
    revert InvalidCollateralState(InvalidCollateralStates.AUCTION_ACTIVE);
}
```

In this scenario, `params` is completely controlled by users. To bypass this check, the caller can set `params.endTime` to a value less than `block.timestamp`. 

A possible exploit scenario occurs when `AstariaRouter.liquidate()` is called to list the underlying asset on Seaport, which also sets the liquidator address. Consequently, anyone can call `liquidatorNFTClaim()` to transfer the underlying asset to the liquidator by setting `params.endTime < block.timestamp`.

## Recommendation
The parameter passed to `liquidatorNFTClaim()` should be validated against the parameters created for the Seaport auction. To achieve this:

- Update the `collateralIdToAuction` mapping, which currently maps `collateralId` to a boolean value indicating an active auction, to instead map from `collateralId` to the Seaport order hash.
- All usages of `collateralIdToAuction` should be updated. For instance, `isValidOrder()` and `isValidOrderIncludingExtraData()` should be modified as follows:

```solidity
return
    s.collateralIdToAuction[uint256(zoneHash)] == orderHash
        ? ZoneInterface.isValidOrder.selector
        : bytes4(0xffffffff);
```

- The `liquidatorNFTClaim()` function should verify that the hash of `params` matches the value stored in the `collateralIdToAuction` mapping. This validation ensures that `params.endTime` is not spoofed.

## Astaria
Fixed in PR 210.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`Validation, Business Logic`

