---
# Core Classification
protocol: Nftcapsule
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31400
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-11-01-NFTCapsule.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[H-01] Incorrect `IPETHNFTVault::borrow` assumption breaks the protocol

### Overview


This bug report discusses a problem with the `depositNft` method in `Capsule`, which affects the functionality of the protocol. The issue arises when the code tries to use the `_borrowAmount` value as the amount of `PETH` to provide as liquidity to a Curve pool. However, this value is not accurate as the `borrow` method of the `IPETHNFTVault` always takes a fee, resulting in a lower amount of `PETH` being received. This makes it impossible to provide liquidity and renders the protocol unusable. The report recommends using only the `PETH` received from borrowing for providing liquidity and addressing the issue in the `increaseBorrowAmount` method as well.

### Original Finding Content

**Severity**

**Impact:**
Medium, as the protocol will have to be redeployed

**Likelihood:**
High, as it it certain to happen

**Description**

The `depositNft` method in `Capsule` calls `IPETHNFTVault::borrow` with a `_borrowAmount` argument. Later, the code actually tries using the `_borrowAmount` value as the amount of `PETH` to provide as liquidity to a Curve pool. The problem is that the `borrow` method of those vaults always takes a fee, so `Capsule` will have received less than `_borrowAmount` of `PETH`. Quoted from `IPETHNFTVault::borrow`'s NatSpec:

> /// @param \_amount The amount of PUSD to be borrowed. Note that the user will receive less than the amount requested,
> /// the borrow fee and insurance automatically get removed from the amount borrowed

This means that the liquidity provision will always fail due to insufficient `PETH` balance, making the protocol unusable.

Even if the fee value is currently zero it can be changed and the protocol will be broken.

**Recommendations**

Use only the `PETH` received from borrowing for providing liquidity as well as for the `newPosition.amountBorrowed` value in `depositNft`. The issue is also present in `increaseBorrowAmount` and should be addressed there as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nftcapsule |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-11-01-NFTCapsule.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

