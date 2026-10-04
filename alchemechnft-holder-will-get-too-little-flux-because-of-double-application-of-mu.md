---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38220
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31479%20-%20%5bSC%20-%20High%5d%20alchemechNFT%20holder%20will%20get%20too%20little%20FLUX%20be....md

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Holterhus
---

## Vulnerability Title

`alchemechNFT` holder will get too little FLUX because of double application of multipliers

### Overview


This report highlights a bug in the smart contract for the Alchemix DAO on Github. The bug affects the calculation of FLUX tokens for alchemicNFT holders, resulting in a significant decrease in the amount of FLUX they receive. This is due to a mistake in the code where the calculation is multiplied twice, resulting in a 250x decrease in the amount of FLUX. This bug is permanent and cannot be fixed, causing a loss of FLUX for alchemicNFT holders. A test can be added to the contract to demonstrate the incorrect calculation.

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/FluxToken.sol

Impacts:
- Permanent freezing of unclaimed royalties

## Description
## Brief/Intro

When `alchemicNFT` holders claim FLUX, the amount to claim is calculated relative to the amount that Patron NFT holders claim, which dramatically underestimates the amount to claim.

## Vulnerability Details

When NFT holders claim FLUX, the calculated amount should either by multiplied by 0.4% (for Patron NFT holders) or 0.05% (for alchemicNFT holders).

However, in the implementation of `getClaimableFlux()`, we first multiply by 0.4% to get the Patron NFT holder amount. Then, if it's an Alchemic NFT holder, we multiply that resulting value by 0.05% to get the final amount.

The result is that Alchemic NFT holders receive 0.4% * 0.05% = 0.0002% of the calculated amount, which is 250x less than they should.

## Impact Details

Alchemic NFT holders will receive 250x less FLUX than they should when claiming. This loss of FLUX amount is permanent and can't be fixed.

## References

`FluxToken.sol`


## Proof of Concept

The following test can be added to `FluxToken.t.sol`. It should return 0.05% of `500_000`, which would equal `250`, but instead returns `1`.

```solidity
function test_InflatedAlchemicNFTClaim() external {
    uint256 amount = 500_000;
    uint256 bptCalculation = flux.getClaimableFlux(amount, alchemechNFT);
    assertEq(bptCalculation, 1);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | Holterhus |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31479%20-%20%5bSC%20-%20High%5d%20alchemechNFT%20holder%20will%20get%20too%20little%20FLUX%20be....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

