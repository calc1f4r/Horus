---
# Core Classification
protocol: Ondo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6412
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-ondo-finance-contest
source_link: https://code4rena.com/reports/2023-01-ondo
github_link: https://github.com/code-423n4/2023-01-ondo-findings/issues/265

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - leveraged_farming
  - rwa
  - services
  - cdp
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hansfriese
---

## Vulnerability Title

[M-01] Admin should be able to refund or redeem the sanctioned users

### Overview


This bug report is about a vulnerability in the CashManager.sol code. The vulnerability is that funds of sanctioned users are locked, even if the protocol team knows about it. The funds are locked because the KYC is checked for the redeemers and refundees in the function completeRedemptions(). As a result, the funds are completely locked and even the admin has no control over it. The bug was discovered through manual review. The recommended mitigation step is to remove KYC check for the redeemers and refundees, assuming the MANAGER_ADMIN can be trusted.

### Original Finding Content


Sanctioned user's funds are locked.

### Proof of Concept

It is understood that the sanctioned users can not mint nor redeem because the functions `requestMint()` and `requestRedemption()` are protected by the modifier `checkKYC()`.

And it is also understood that the protocol team knows about this.

But I still believe the admin should be able to refund or redeem those funds.

And it is not possible for now because the KYC is checked for the `redeemers` and `refundees` in the function `completeRedemptions()`.

So as long as the user becomes unverified (due to several reasons including the signature expiry), the funds are completely locked and even the admin has no control over it.

```solidity
CashManager.sol
707:   function completeRedemptions(
708:     address[] calldata redeemers,
709:     address[] calldata refundees,
710:     uint256 collateralAmountToDist,
711:     uint256 epochToService,
712:     uint256 fees
713:   ) external override updateEpoch onlyRole(MANAGER_ADMIN) {
714:     _checkAddressesKYC(redeemers);
715:     _checkAddressesKYC(refundees);
716:     if (epochToService >= currentEpoch) {
717:       revert MustServicePastEpoch();
718:     }
719:     // Calculate the total quantity of shares tokens burned w/n an epoch
720:     uint256 refundedAmt = _processRefund(refundees, epochToService);
721:     uint256 quantityBurned = redemptionInfoPerEpoch[epochToService]
722:       .totalBurned - refundedAmt;
723:     uint256 amountToDist = collateralAmountToDist - fees;
724:     _processRedemption(redeemers, amountToDist, quantityBurned, epochToService);
725:     collateral.safeTransferFrom(assetSender, feeRecipient, fees);
726:     emit RedemptionFeesCollected(feeRecipient, fees, epochToService);
727:   }

```

### Recommended Mitigation Steps

Assuming that the `MANAGER_ADMIN` can be trusted, I suggest removing KYC check for the redeemers and refundees.

**[ali2251 (Ondo Finance) disputed and commented](https://github.com/code-423n4/2023-01-ondo-findings/issues/265#issuecomment-1410626479):**
> It's not in scope as mentioned in README, specifically in Not in scope -> 
> > KYC/Sanction related edge cases specifically when a user’s KYC status or Sanction status changes in between different actions, leaving them at risk of their funds being locked in the protocols or being liquidated in Flux

**[Trust (judge) commented](https://github.com/code-423n4/2023-01-ondo-findings/issues/265#issuecomment-1411581435):**
> I don't believe this clause includes the described case, i.e. even admin cannot move the locked funds.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Ondo Finance |
| Report Date | N/A |
| Finders | hansfriese |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-ondo
- **GitHub**: https://github.com/code-423n4/2023-01-ondo-findings/issues/265
- **Contest**: https://code4rena.com/contests/2023-01-ondo-finance-contest

### Keywords for Search

`vulnerability`

