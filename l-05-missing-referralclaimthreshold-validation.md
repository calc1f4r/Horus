---
# Core Classification
protocol: Gacha_2025-01-27
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53308
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Gacha-security-review_2025-01-27.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-05] Missing `referralClaimThreshold` validation

### Overview

See description below for full details.

### Original Finding Content

Users can claim their `referral rewards` accrued in the contract by calling the `GachaTickets::claimReferralFees` function :

```solidity
function claimReferralFees() external nonReentrant {
    Storage storage $ = _getOwnStorage();
    Referral storage ref = $.referrals[msg.sender];

    uint256 amount = ref.awardedAmount - ref.claimedAmount;
    if (amount == 0) revert InsufficientBalance();

    ref.claimedAmount += amount;

    IERC20($.paymentToken).transferFrom($.feeWallet, msg.sender, amount);

    emit GachaLib.ClaimReferral(msg.sender, amount);
}
```

However, the `documented behavior states` that `referrals should only be able to claim their rewards once they hit a referralClaimThreshold`.

Despite this, the `referralClaimThreshold` parameter is set in the `GachaConfig::setConfig` function, but `it is never enforced` in the `GachaTickets::claimReferralFees` function during `referral reward` withdrawal.

Due to the above missing threshold implementation following consequences can occur :

1. Users can claim referral fees below the intended threshold\*\*

   - Users can `repeatedly` claim small amounts, leading to `high transaction costs and inefficiencies`.

2. Increased On-Chain activity & gas costs :

   - The `protocol may experience relatively higher gas costs` due to frequent, small-value claims.

3. Deviation from the documented behavior :
   - The `contract does not align with its intended and documented functionality`, which may lead to `user confusion or misaligned behavior`.

It is recommended to enforce the `referralClaimThreshold` before processing a claim.

Modify `claimReferralFees` function to `only allow claims if the amount exceeds referralClaimThreshold`:

```solidity
function claimReferralFees() external nonReentrant {
    Storage storage $ = _getOwnStorage();
    Referral storage ref = $.referrals[msg.sender];

    uint256 amount = ref.awardedAmount - ref.claimedAmount;
    if (amount == 0) revert InsufficientBalance();

    // Enforce referral claim threshold
    require(amount >= $.referralClaimThreshold, "Claim amount below threshold");

    ref.claimedAmount += amount;

    IERC20($.paymentToken).transferFrom($.feeWallet, msg.sender, amount);

    emit GachaLib.ClaimReferral(msg.sender, amount);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Gacha_2025-01-27 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Gacha-security-review_2025-01-27.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

