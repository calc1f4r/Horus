---
# Core Classification
protocol: Swell
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19636
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/swell/swell-2/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/swell/swell-2/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Reentrancy protection is recommended for staking vault

### Overview


This bug report is about a reentrancy vulnerability in the staking vault contract. Reentrancy is when a user can call a function multiple times, allowing an exploit contract to steal assets from the first user. The main reentrancy threat occurs when a call is made to balancerVault.joinPool() on line 132. If the call passes control flow to an exploit contract, the BPTbalance of the vault on line 150 would include the BPT tokens of the first depositor and be deposited into aura under the exploit contract’s address. In order to prevent this, a reentrancy guard was added to the function SwellStakeVaultHelper.stakeAndVault() using the nonReentrant modifier from OpenZeppelin ReentrancyGuard in commit 8acccd8.

### Original Finding Content

## Description

The staking vault contract makes external calls, which would allow a reentrant to the contract to steal the assets of the first user. It is not within the scope of this review to fully assess whether any of the external calls do contain a reentrancy risk but, as they are not controlled by Swell, it is best to assume that some threat potential is present.

The main reentrancy threat occurs during the call to `balancerVault.joinPool()` on line [132]. If the call to this function passes control flow to an exploit contract after BPT contracts have been transferred to the vault, that contract would be able to call `SwellStakeVaultHelper.stakeAndVault()` with a very small amount of ETH. During this reentrancy call, the BPT balance of the vault on line [150] would include the BPT tokens of the first depositor. These would then be deposited into aura under the exploit contract’s address. The original depositor’s call to `SwellStakeVaultHelper.stakeAndVault()` would then resolve, with amount on line [150] being zero.

## Recommendations

Add a reentrancy guard to `SwellStakeVaultHelper.stakeAndVault()`.

## Resolution

The `nonReentrant` modifier from OpenZeppelin ReentrancyGuard has been added to the function `SwellStakeVaultHelper.stakeAndVault()` as recommended in commit `8acccd8`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Swell |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/swell/swell-2/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/swell/swell-2/review.pdf

### Keywords for Search

`vulnerability`

