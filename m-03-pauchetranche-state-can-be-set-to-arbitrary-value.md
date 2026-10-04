---
# Core Classification
protocol: Beta Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28977
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-11-betafinance
source_link: https://code4rena.com/reports/2023-11-betafinance
github_link: https://github.com/code-423n4/2023-11-betafinance-findings/issues/27

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
  - ladboy233
---

## Vulnerability Title

[M-03] paucheTranche state can be set to arbitrary value

### Overview


This bug report is about the Omni Protocol, a protocol for lending and borrowing. The issue is that the pauseTranche state can be set to arbitrary value. This can happen when liquidation occurs and the borrowTrueValue is greater than the depositTrueValue. In this case, the pauseTranche is set to the borrower tier. This defeats the check of `require(_trancheId < IOmniPool(omniPool).pauseTranche(), "OmniToken::withdraw: Tranche paused.");` which prevents users from withdrawing if the tranche is paused. This could lead to a user with a lower borrower tier being able to withdraw before the higher borrower tier, even if the higher borrower tier is subject to liquidation.

The recommended mitigation step is to change the code to `pauseTranche = max(borrowTier, pauseTranche)` which will ensure that the pauseTranche is set to the highest borrower tier. After discussion, it was determined that this issue is of medium severity as it requires the bad debt to arise and users can withdraw their assets before socialize loss. BetaFinance confirmed that they will fix this issue using the recommended code.

### Original Finding Content


<https://github.com/code-423n4/2023-11-betafinance/blob/0f1bb077afe8e8e03093c8f26dc0b7a2983c3e47/Omni_Protocol/src/OmniPool.sol#L348> 

<https://github.com/code-423n4/2023-11-betafinance/blob/0f1bb077afe8e8e03093c8f26dc0b7a2983c3e47/Omni_Protocol/src/OmniToken.sol#L180>

paucheTranche state can be set to arbitrary value

### Proof of Concept

The protocol has this concept of tranche id and borrower tier, the higher borrower tier means higher risk.

Lower borrower tier means lower risk.

When liquidation happens, if the borrowTrueValue is greater than depositTrueValue, which can happen because of the underlying oracle price can change:

```solidity
if (evalAfter.borrowTrueValue > evalAfter.depositTrueValue) {
	pauseTranche = borrowTier;
	emit PausedTranche(borrowTier);
}
```

When the pauseTranche id is set to the borrower tier in this [line of code](https://github.com/code-423n4/2023-11-betafinance/blob/0f1bb077afe8e8e03093c8f26dc0b7a2983c3e47/Omni_Protocol/src/OmniPool.sol#L348), the user that deposited below the paused tranche id should not be able to withdraw / tranche id share because [this check](https://github.com/code-423n4/2023-11-betafinance/blob/0f1bb077afe8e8e03093c8f26dc0b7a2983c3e47/Omni_Protocol/src/OmniToken.sol#L180) is in-place:

    require(_trancheId < IOmniPool(omniPool).pauseTranche(), "OmniToken::withdraw: Tranche paused.");

The problem is that the paucheTranche state can be set to arbitrary value.

Suppose a user has borrower tier 10 and borrowTrueValue exceed depositTrueValue, the pauseTranche is set to 10, then a second user has borrower tier 0, he is subject to liquidation as well.

borrowTrueValue exceed depositTrueValue as well.

The pauseTranche is reset to 0 again, which defeats the check of:

    require(_trancheId < IOmniPool(omniPool).pauseTranche(), "OmniToken::withdraw: Tranche paused.");

### Recommended Mitigation Steps

Change the code to:

    if (evalAfter.borrowTrueValue > evalAfter.depositTrueValue) {
    	pauseTranche = max(borrowTier, pauseTranche)
    	emit PausedTranche(borrowTier);
    }

**[cccz (Judge) commented](https://github.com/code-423n4/2023-11-betafinance-findings/issues/27#issuecomment-1797832516):**
 > Nice Find!

> `pauseTranche` is used to disallow the user from calling `withdraw()` to withdraw assets before `socializeLoss()` is called.
> As for severity, I'm not so sure it's a High, need more thought on that.

**[Ladboy233 (Warden) commented](https://github.com/code-423n4/2023-11-betafinance-findings/issues/27#issuecomment-1798287715):**
> I submitted as High because this finding allows user to perform privilege escalation and act as admin to pause arbitrary tranche.
> 
> Users can select a tranche and deposit and borrow and liquidation themselves to set pauseTranche to any value.
> 
> Unless admin kept a step into to unpause, all other user's withdraw transaction can revert because of this check.
> 
> ```solidity
> require(_trancheId < IOmniPool(omniPool).pauseTranche(), "OmniToken::withdraw: Tranche paused.");
> ```


**[cccz (Judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-11-betafinance-findings/issues/27#issuecomment-1799060067):**
 > This requires not only that the user can be liquidated, but also that the bad debt arises (there is big gap between the two), so I think it would be very difficult for an attacker to actively exploit this issue to set pauseTranche.

> And as `TRST-M-1 Users can avoid losses by withdrawing assets before pausing due to bad debt` noted, users can withdraw preemptively to prevent socializeLoss() from causing losses.

 > Users can't actively arise bad debt, medium likelihood.

> Users can withdraw their assets before socialize loss, medium impact.

> So consider it medium severity.

**[allenjlee (BetaFinance) confirmed and commented](https://github.com/code-423n4/2023-11-betafinance-findings/issues/27#issuecomment-1807187753):**
 > Agree with judge's assessment, medium severity. There should be no loss to users, and this situation arises in the case only where a higher tranche has bad debt after a lower tranche has bad debt. The worst case scenario, is that one depositor is left with all the bad debt, which is unintended by the protocol but does not cause loss of funds compared to existing protocols -- which rely on manual pause intervention, which the protocol also has as we inherit `Pausable`, so this is medium severity. 
> 
> We will fix to the latest recommendation, which is using the `pauseTranche = borrowTier > pauseTranche ? pauseTranche : borrowTier;`

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Beta Finance |
| Report Date | N/A |
| Finders | ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-11-betafinance
- **GitHub**: https://github.com/code-423n4/2023-11-betafinance-findings/issues/27
- **Contest**: https://code4rena.com/reports/2023-11-betafinance

### Keywords for Search

`vulnerability`

