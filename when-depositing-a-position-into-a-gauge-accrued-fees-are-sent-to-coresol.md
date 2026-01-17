---
# Core Classification
protocol: Mellow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40583
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10
source_link: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
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
finders_count: 4
finders:
  - Kaden
  - Saw-mon and Natalie
  - deadrosesxyz
  - Akshay Srivastav
---

## Vulnerability Title

When depositing a position into a gauge, accrued fees are sent to Core.sol 

### Overview


This bug report is about a problem in the VeloAmmModule.sol file. When a user deposits a position into a gauge, the fees they have accrued are supposed to be transferred to them. However, in this case, the fees are being transferred to the wrong person (Core.sol) instead of the user. This means that if the user had any fees before depositing, they will be left in the contract and can be taken by another user. The report recommends that the fees should be sent to the owner of the position instead. The bug has been fixed in the code, so users should no longer experience this issue.

### Original Finding Content

## VeloAmmModule Issue Documentation

## Context
**File:** VeloAmmModule.sol  
**Line:** 185

## Description
When depositing a position into a gauge, `collect` is invoked and it transfers the accrued fees to the `msg.sender`. The problem is that in this case, the `msg.sender` is `Core.sol`. If the user's position had accrued any fees prior to the deposit, they'll be left within the contract, up until another user skims them.

### Code Snippet
```solidity
function deposit(uint256 tokenId) external override nonReentrant {
    require(nft.ownerOf(tokenId) == msg.sender, "NA");
    require(voter.isAlive(address(this)), "GK");
    (,, address _token0, address _token1, int24 _tickSpacing, int24 tickLower, int24 tickUpper,,,,,) =
    nft.positions(tokenId);
    require(token0 == _token0 && token1 == _token1 && tickSpacing == _tickSpacing, "PM");
    
    // trigger update on staked position so NFT will be in sync with the pool
    nft.collect(
        INonfungiblePositionManager.CollectParams({
            tokenId: tokenId,
            recipient: msg.sender,
            amount0Max: type(uint128).max,
            amount1Max: type(uint128).max
        })
    );
}
```

## Recommendation
If during the deposit any fees are collected, send them to the owner of the position.

## Mellow
Fixed in commit `52c0aaf0`.

## Cantina Managed
Fixed. Upon deposit, fees are now sent to the position owner.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Mellow |
| Report Date | N/A |
| Finders | Kaden, Saw-mon and Natalie, deadrosesxyz, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10

### Keywords for Search

`vulnerability`

