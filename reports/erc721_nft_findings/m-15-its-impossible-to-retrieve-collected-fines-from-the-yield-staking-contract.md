---
# Core Classification
protocol: BendDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36897
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-benddao
source_link: https://code4rena.com/reports/2024-07-benddao
github_link: https://github.com/code-423n4/2024-07-benddao-findings/issues/10

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
  - lending

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - 0x73696d616f
  - bin2chen
  - oakcobalt
  - SpicyMeatball
---

## Vulnerability Title

[M-15] It's impossible to retrieve collected fines from the yield staking contract

### Overview


This bug report is about a staking contract that does not have a way to retrieve collected fines. This means that if a user's stake is forcefully unstaked by the botAdmin, they will have to pay an additional fine when they want to get their stake back. The code provided in the report shows that the fine is not being transferred to the admin, so it will remain in the contract forever. To fix this, the report recommends implementing a function for the admin to collect fines from the contract. The type of bug is classified as a Token-Transfer issue and has been confirmed and fixed by the BendDAO team. 

### Original Finding Content


<https://github.com/code-423n4/2024-07-benddao/blob/main/src/yield/YieldStakingBase.sol#L329-L337><br><https://github.com/code-423n4/2024-07-benddao/blob/main/src/yield/YieldStakingBase.sol#L407><br><https://github.com/code-423n4/2024-07-benddao/blob/main/src/yield/YieldStakingBase.sol#L426>

### Impact

No means to retrieve collected fines from the staking contract.

### Proof of Concept

If `botAdmin` forcefully unstakes a position, a staker will have to pay an additional fine when the stake is repayed:

```solidity
  function _repay(uint32 poolId, address nft, uint256 tokenId) internal virtual {
    ---SNIP---

    vars.nftDebt = _getNftDebtInUnderlyingAsset(sd);
>>  vars.nftDebtWithFine = vars.nftDebt + sd.unstakeFine;

    // compute repay value
    if (vars.claimedYield >= vars.nftDebtWithFine) {
      vars.remainAmount = vars.claimedYield - vars.nftDebtWithFine;
    } else {
      vars.extraAmount = vars.nftDebtWithFine - vars.claimedYield;
    }

    // transfer eth from sender
    if (vars.extraAmount > 0) {
>>    underlyingAsset.safeTransferFrom(vars.nftOwner, address(this), vars.extraAmount);
    }

    if (vars.remainAmount > 0) {
      underlyingAsset.safeTransfer(vars.nftOwner, vars.remainAmount);
    }

    // repay lending pool
>>  poolYield.yieldRepayERC20(poolId, address(underlyingAsset), vars.nftDebt);

    poolYield.yieldSetERC721TokenData(poolId, nft, tokenId, false, address(underlyingAsset));

    // update shares
    accountYieldInWithdraws[address(vars.yieldAccout)] -= sd.withdrawAmount;
    totalDebtShare -= sd.debtShare;

    delete stakeDatas[nft][tokenId];

    emit Repay(msg.sender, nft, tokenId, vars.nftDebt);
  }
```

Note that the user's total debt consists of the actual NFT debt and the fine. When the stake is paid off, only the `nftDebt` is sent to the pool, and the `unstakeFine` remains in the contract. However, there are no functions that send the collected funds to the admin, and so they will remain in the contract forever.

### Recommended Mitigation Steps

Implement a function that allows admin to collect fines from the yield staking contract.

### Assessed type

Token-Transfer

**[thorseldon (BendDAO) confirmed and commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/10#issuecomment-2297851634):**
 > Fixed [here](https://github.com/BendDAO/bend-v2/commit/80d3bb38dd6eaed5438f4bb63f6dac348741bbaf).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | 0x73696d616f, bin2chen, oakcobalt, SpicyMeatball |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-benddao
- **GitHub**: https://github.com/code-423n4/2024-07-benddao-findings/issues/10
- **Contest**: https://code4rena.com/reports/2024-07-benddao

### Keywords for Search

`vulnerability`

