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
solodit_id: 36898
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-benddao
source_link: https://code4rena.com/reports/2024-07-benddao
github_link: https://github.com/code-423n4/2024-07-benddao-findings/issues/9

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
finders_count: 2
finders:
  - 0x73696d616f
  - SpicyMeatball
---

## Vulnerability Title

[M-16] Borrower can prevent yield position repayment and closure by the bot

### Overview


This bug report discusses a potential issue with the code of a yield contract. The issue is that a user may be able to revoke the approval for the underlying asset, which can prevent the contract from repaying the debt and closing the user's position. This can result in losses for the protocol. 

The report includes a proof of concept that highlights the specific code causing the issue. It suggests separating the logic for debt repayment and NFT unlocking to prevent this issue from occurring. The report also mentions that the issue has been confirmed and fixed by the BendDAO team.

### Original Finding Content


User may revoke the underlying asset approval from the yield contract and prevent the `botAdmin` from repaying and closing his position. As a result, the debt will not be repaid, leaving the protocol at a loss.

### Proof of Concept

Let's take a closer look at the `_repay` function:

```solidity
  function _repay(uint32 poolId, address nft, uint256 tokenId) internal virtual {
    RepayLocalVars memory vars;
    ---SNIP---
    // withdraw yield from protocol and repay if possible

    vars.claimedYield = protocolClaimWithdraw(sd);

    vars.nftDebt = _getNftDebtInUnderlyingAsset(sd);
    vars.nftDebtWithFine = vars.nftDebt + sd.unstakeFine;

    // compute repay value
    if (vars.claimedYield >= vars.nftDebtWithFine) {
      vars.remainAmount = vars.claimedYield - vars.nftDebtWithFine;
    } else {
>>    vars.extraAmount = vars.nftDebtWithFine - vars.claimedYield;
    }

    // transfer eth from sender
    if (vars.extraAmount > 0) {
>>    underlyingAsset.safeTransferFrom(vars.nftOwner, address(this), vars.extraAmount);
    }

    if (vars.remainAmount > 0) {
      underlyingAsset.safeTransfer(vars.nftOwner, vars.remainAmount);
    }

    // repay lending pool
    poolYield.yieldRepayERC20(poolId, address(underlyingAsset), vars.nftDebt);

    poolYield.yieldSetERC721TokenData(poolId, nft, tokenId, false, address(underlyingAsset));

    // update shares
    accountYieldInWithdraws[address(vars.yieldAccout)] -= sd.withdrawAmount;
    totalDebtShare -= sd.debtShare;

    delete stakeDatas[nft][tokenId];

    emit Repay(msg.sender, nft, tokenId, vars.nftDebt);
  }
```

If the yield collected by the position is not enough to cover the entire debt and fines, the protocol will attempt to collect `extraAmount` from the position owner, but he may revoke ERC20 approval and cancel the `safeTransferFrom` function call. As a result, `nftDebt` will not be repaid and will continue to collect interest, increasing the protocol's losses.

### Recommended Mitigation Steps

It is recommended to separate the logic of debt repayment and NFT unlocking. The `_repay` function will reduce the debt of the position using the collected yield and unlock the NFT only if `extraAmount` is zero. In case `extraAmount` is greater than zero, leave the token locked and allow the NFT owner to unlock it only after he has repaid the remaining debt.

**[thorseldon (BendDAO) confirmed and commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/9#issuecomment-2300176089):**
 > Fixed [here](https://github.com/BendDAO/bend-v2/commit/f06e1e13cf66526904a8da899be39b0f36481106).

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
| Finders | 0x73696d616f, SpicyMeatball |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-benddao
- **GitHub**: https://github.com/code-423n4/2024-07-benddao-findings/issues/9
- **Contest**: https://code4rena.com/reports/2024-07-benddao

### Keywords for Search

`vulnerability`

