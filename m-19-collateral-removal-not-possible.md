---
# Core Classification
protocol: Polynomial Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20256
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-03-polynomial
source_link: https://code4rena.com/reports/2023-03-polynomial
github_link: https://github.com/code-423n4/2023-03-polynomial-findings/issues/16

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
finders_count: 5
finders:
  - csanuragjain
  - rbserver
  - DadeKuma
  - KIntern\_NA
  - bytes032
---

## Vulnerability Title

[M-19] Collateral removal not possible

### Overview


This bug report is about a problem in the Polynomial Protocol that occurs when a collateral, which has been previously approved, introduces a fee on transfer. The current deposit logic in the Protocol cannot handle a fee on transfer token and would give more funds to the user than actually obtained by the contract. 

To illustrate the bug, assume that the Protocol is supporting a collateral, X (say USDT which has a fee currently set as 0). After some time, the collateral introduces a fee on transfer. The Protocol does not have a way to remove a whitelisted collateral, so the problem begins once a user starts depositing such collateral. In this case, the amount is transferred from the user to the contract but the contract will only receive the amount minus the fees. The contract will still adjust the position with the full amount instead of the amount minus the fees, which is incorrect.

To mitigate this bug, it is recommended to add a way to disapprove collateral so that if there are any policy changes for a particular collateral in the future, the Protocol can stop supporting it. This way, it would only have to deal with existing collateral which can be wiped out slowly using public announcements.

### Original Finding Content


If an approved collateral has later started say taking fees on transfer then protocol has no way to remove such collateral. The current deposit logic cannot handle fee on transfer token and would give more funds to user then actually obtained by contract

### Proof of Concept

1.  Assume protocol was supporting collateral X (say USDT which has fee currently set as 0)
2.  After some time collateral introduces fee on transfer
3.  Protocol does not have a way to remove a whitelisted collateral
4.  Problem begins once user starts depositing such collateral

```
    function _addCollateral(uint256 positionId, uint256 amount) internal {
    ...
    ERC20(shortPosition.collateral).safeTransferFrom(msg.sender, address(this), amount);
            ERC20(shortPosition.collateral).safeApprove(address(shortCollateral), amount);

            shortToken.adjustPosition(
                positionId,
                msg.sender,
                shortPosition.collateral,
                shortPosition.shortAmount,
                shortPosition.collateralAmount + amount
            );
            shortCollateral.collectCollateral(shortPosition.collateral, positionId, amount);
    ...
    }
```

5.  In this case `amount` is transferred from user to contract but contract will only receive `amount-fees`. But contract will still adjust position with full `amount` instead of `amount-fees` which is incorrect.

### Recommended Mitigation Steps

Add a way to disapprove collateral so that if in future some policy changes for a particular collateral, protocol can stop supporting it. This will it would only have to deal with existing collateral which can be wiped out slowly using public announcement.

**[Dravee (judge) commented](https://github.com/code-423n4/2023-03-polynomial-findings/issues/16#issuecomment-1478987449):**
 > Not a duplicate of https://github.com/code-423n4/2023-03-polynomial-findings/issues/178 as Fee-on-transfer tokens are only mentioned as a scenario that may make the protocol want to disapprove a collateral.
> 
> Due to a real lack of way to disapprove a collateral, I believe this finding is valid.

**[mubaris (Polynomial) confirmed](https://github.com/code-423n4/2023-03-polynomial-findings/issues/16#issuecomment-1497061603)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Polynomial Protocol |
| Report Date | N/A |
| Finders | csanuragjain, rbserver, DadeKuma, KIntern\_NA, bytes032 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-03-polynomial
- **GitHub**: https://github.com/code-423n4/2023-03-polynomial-findings/issues/16
- **Contest**: https://code4rena.com/reports/2023-03-polynomial

### Keywords for Search

`vulnerability`

