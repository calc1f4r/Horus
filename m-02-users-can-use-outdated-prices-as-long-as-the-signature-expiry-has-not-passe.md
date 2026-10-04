---
# Core Classification
protocol: Beraji Ko
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49518
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Beraji-KO-Security-Review.md
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

protocol_categories:
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-02] Users Can Use Outdated Prices As Long As The Signature Expiry Has Not Passed

### Overview


This report discusses a bug in the code of the StakingKo smart contract, which affects the calculation of rewards for stakers. The bug allows users to manipulate the amount of aSugar tokens they receive by using outdated price information. This is due to the fact that the contract accepts any valid signature, even if it is based on an old price. The impact of this bug is considered medium risk. The team has acknowledged the issue and recommends adding an ID to the message hash to prevent outdated prices from being used.

### Original Finding Content

## Severity

Medium Risk

## Description

Pool prices influence how much `aSugar` gets minted to stakers when they stake. For this to happen `aSugarSigner` will produce signatures for the staking token prices during each stake and full claim reward.

The message hashes of these signatures are composed of:

- stakeToken address
- price
- expired time

One signature can be used as long as it is not expired which means there can be overlapping between price updates. In cases of high volatility, this could be crucial.

Let's say the expiry time of the signature is 15 minutes, right after this signature is created there could be a drop in price and the following produced signatures are at a price of -50%. Now the user can decide in this 15-minute window which signature to use because both the 1 USD price and the 0.5 USD price will be accepted by the contract as valid.

This way user can manipulate their `aSugar` minting amounts.

## Location of Affected Code

File: [contracts/StakingKo.sol](https://github.com/Beraji-Labs/staking-ko/blob/290103f27365cc419fe0a934feaf5f18e6e12d3a/contracts/StakingKo.sol)

```solidity
modifier updatePoolPrice(uint256 _poolId, uint256 _stPrice, uint256 _expriedTime, bytes memory _sig) {
    require(block.timestamp < _expriedTime, "Expired");
    Pool memory pool = pools[_poolId];
@>  bytes32 message = keccak256(abi.encode(pool.stakingToken, _stPrice, _expriedTime));
    address signer = _recoverSigner(message, _sig);
    require(signer == aSugarSigner, "Invalid signer");
    pools[_poolId].stPrice = _stPrice;
    _;
}
```

## Impact

Users can use outdated prices as long as the signature expiry has not passed.

## Recommendation

Add an ID to the message hash that will be incremented on each price change. On each signature usage, the contract will check if the signature counter is less than the one recorded in contract storage. If it is then revert. This way only the newest price is going to be accepted.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Beraji Ko |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Beraji-KO-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

