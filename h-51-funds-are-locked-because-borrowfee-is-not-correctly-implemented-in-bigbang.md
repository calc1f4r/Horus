---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27541
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/583

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - 0xrugpull\_detector
  - SaeedAlipoor01988
  - Koolex
  - 0xnev
  - 0x007
---

## Vulnerability Title

[H-51] Funds are locked because borrowFee is not correctly implemented in BigBang

### Overview


A bug has been identified in the Tapioca protocol where users are unable to fully repay their borrowed amount. This is due to the fact that the borrowOpeningFee is accumulated over assets as a reward to asset depositors, meaning that when a user attempts to repay their loan, they must pay back more than the amount they initially borrowed. This results in a situation where the user must borrow even more in order to repay the loan, creating a 'bird and egg' situation.

The bug is demonstrated in the proof of concept, which outlines how the borrow function works. The amount minted to the user is higher than the amount borrowed, with the difference being the borrowOpeningFee, meaning that when the user attempts to repay their loan, they must return the amount plus the fee, which is more than the totalSupply. This issue is compounded when there are more users and more minted amount, as more funds are locked.

The recommended mitigation step is that borrowOpeningFee should not be added to userBorrowPart. If fee is to be implemented, then it should go to the fee collector in the form of collateral or USD0 token. This bug has been confirmed by 0xRektora (Tapioca) via duplicate issue 739.

### Original Finding Content


There's borrowOpeningFee for markets. In Singularity, this fee is accumulated over assets as a reward to asset depositors. In BigBang, assets is USD0 which would be minted and burned on borrow, and repay respectively. BigBang does not collect fees, because it uses the same mechanism as Singularity and therefore it would demand more than minted amount from user when it's time to repay.

This results in a bird and egg situation where Users can't fully repay a borrowed amount unless they borrow even more.

### Proof of Concept

Let's look at how [borrow](https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/2286f80f928f41c8bc189d0657d74ba83286c668/contracts/markets/bigBang/BigBang.sol#L742-L767) works

```solidity
function _borrow(
    address from,
    address to,
    uint256 amount
) internal returns (uint256 part, uint256 share) {
    uint256 feeAmount = (amount * borrowOpeningFee) / FEE_PRECISION; // A flat % fee is charged for any borrow

    (totalBorrow, part) = totalBorrow.add(amount + feeAmount, true);
    require(
        totalBorrowCap == 0 || totalBorrow.elastic <= totalBorrowCap,
        "BigBang: borrow cap reached"
    );

    userBorrowPart[from] += part;

    //mint USDO
    IUSDOBase(address(asset)).mint(address(this), amount);

    //deposit borrowed amount to user
    asset.approve(address(yieldBox), amount);
    yieldBox.depositAsset(assetId, address(this), to, amount, 0);

    share = yieldBox.toShare(assetId, amount, false);

    emit LogBorrow(from, to, amount, feeAmount, part);
}
```

As can be seen above, amount would be minted to user, but the userBorrowPart is `amount + fee`. When it's time to repay, user have to return `amount + fee` in other to get all their collateral.

Assuming the user borrowed `1,000 USD0` and borrowOpeningFee is at the default value of `0.5%`. Then the user's debt would be `1,005`. If there's only 1 user, and the totalSupply is indeed `1,000`, then there's no other way for the user to get the extra `5 USD0`. Therefore he can't fully redeem his collateral and would have at least `5 * (1 + collateralizationRate) USD0` worth of collateral locked up. This fund cannot be accessed by the user, nor is it used by the protocol. It would be sitting at yieldbox forever earning yields for no one.

This issue becomes more significant when there are more users and minted amount. If more amount is minted more funds are locked.

It might seem like user Alice could go to the market to buy `5 USD0` to fully repay. But the reality is that he is transferring the unfortunate disaster to another user. Cause no matter what, Owed debts would always be higher than `totalSupply`.

This debt would keep accumulating after each mint and every burn. For example, assuming that one 1 billion of USD0 was minted and 990 million was burned in the first month. totalSupply and hence circulating supply would be 10 million, but user debts would be 15 million USD0. That's 5 million USD that can't be accessed by user nor fee collector.

### Recommended Mitigation Steps

borrowOpeningFee should not be added to userBorrowPart. If fee is to implemented, then fee collector should receive collateral or USD0 token.

**[0xRektora (Tapioca) confirmed via duplicate issue 739](https://github.com/code-423n4/2023-07-tapioca-findings/issues/739)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | 0xrugpull\_detector, SaeedAlipoor01988, Koolex, 0xnev, 0x007 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/583
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

