---
# Core Classification
protocol: Particle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40719
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780
source_link: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
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
  - cccz
---

## Vulnerability Title

When owner reduces loan_term, it may cause the borrower to be liquidated immediately 

### Overview


This bug report discusses an issue with a function called isLiquidatable, which is used to determine if a borrower's position can be liquidated. The problem arises when the owner of the NFT (non-fungible token) calls a function called updateLoanTerm to reduce the LOAN_TERM, which is the amount of time the borrower has to close their position before being liquidated. This can cause the borrower to be immediately liquidated if the new LOAN_TERM is shorter than the remaining time they have to close their position. The recommendation is to store a different value in the updateRenewalCutoffTime function to avoid this issue.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
When `block.timestamp > cutoffTime + LOAN_TERM`, the borrower will be liquidated:

```solidity
function isLiquidatable(
    uint128 tokenFromPremium,
    uint128 tokenToPremium,
    uint128 tokenFromOwed,
    uint128 tokenToOwed,
    uint40 tokenId
) public view returns (bool) {
    /// @dev the liquidation condition is that
    /// EITHER (premium is not enough) OR (cutOffTime > 0 AND currentTime > cutOffTime + LOAN_TERM)
    uint32 cutoffTime = lps.getRenewalCutoffTime(tokenId);
    return
        (tokenFromPremium < tokenFromOwed || tokenToPremium < tokenToOwed) ||
        (cutoffTime > 0 && cutoffTime + LOAN_TERM < block.timestamp);
}
```

The problem here is that the owner may call `updateLoanTerm` to reduce the `LOAN_TERM`, which may cause the borrower to be immediately liquidated:

```solidity
function updateLoanTerm(uint256 loanTerm) public override onlyOwner whenNotPaused {
    if (loanTerm > _LOAN_TERM_MAX) revert Errors.InvalidValue();
    LOAN_TERM = loanTerm;
    emit UpdateLoanTerm(loanTerm);
}
```

Considering that the current `LOAN_TERM` is 7 days, the NFT owner calls `reclaimLiquidity` and the borrower must close the position within 7 days; otherwise, it will be liquidated. The borrower plans to close the position on the 5th day, but the owner calls `updateLoanTerm` to reduce `LOAN_TERM` to 3 days, at which time the borrower will be liquidated immediately.

## Recommendation
It is recommended to store `block.timestamp + LOAN_TERM` instead of `block.timestamp` in `updateRenewalCutoffTime`:

```solidity
function updateRenewalCutoffTime(
    mapping(uint256 => Info) storage self,
    uint256 tokenId
) internal returns (uint32 cutOffTime) {
    Info storage info = self[tokenId];
    cutOffTime = uint32(block.timestamp);
    // - info.renewalCutoffTime = cutOffTime;
    info.renewalCutoffTime = cutOffTime + LOAN_TERM;
}
```

...

```solidity
function isLiquidatable(
    uint128 tokenFromPremium,
    uint128 tokenToPremium,
    uint128 tokenFromOwed,
    uint128 tokenToOwed,
    uint40 tokenId
) public view returns (bool) {
    /// @dev the liquidation condition is that
    /// EITHER (premium is not enough) OR (cutOffTime > 0 AND currentTime > cutOffTime + LOAN_TERM)
    uint32 cutoffTime = lps.getRenewalCutoffTime(tokenId);
    return
        (tokenFromPremium < tokenFromOwed || tokenToPremium < tokenToOwed) ||
        // - (cutoffTime > 0 && cutoffTime + LOAN_TERM < block.timestamp);
        (cutoffTime > 0 && cutoffTime < block.timestamp);
}
```

## Particle
Acknowledged. `LOAN_TERM` shouldn't be updated often (initially by multisign, in the future by governance). We store timestamp for simplicity.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Particle |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_particle_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/83468b34-954f-4650-b16d-7d72c5477780

### Keywords for Search

`vulnerability`

