---
# Core Classification
protocol: Arcadia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31492
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Arcadia-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] `approvedCreditor` not reset after account transfer

### Overview


This bug report discusses a problem with the Arcadia accounts, where a secondary backup creditor can potentially steal funds from a liquidated account. This can happen if the account is transferred and the `approvedCreditor` variable is not reset, allowing the old owner to have a backdoor to the system. This can occur during liquidations when the lending pool internalizes a bad loan, and the `auctionBoughtIn` function is called. The report recommends either resetting the `approvedCreditor` variable when transferring an account or having a per-owner based `approvedCreditor`.

### Original Finding Content

**Severity**

**Impact**: High, user can steal funds from liquidated account

**Likelihood**: Medium, requires either a bad debt account, or L2 to be offline for some time

**Description**

The Arcadia accounts support a secondary backup creditor which is stored in the `approvedCreditor` storage variable, and can be set by the owner. The issue is that when an account is transferred, this variable is not reset, and the old owner essentially can have a backdoor to the system.

The `approvedCreditor` can call the function `flashActionByCreditor` and change the current creditor of the account. This function also calls the `_withdraw` function with some `actionTarget`, and can essentially transfer all assets in the account to that target, provided there are no outstanding loans from the old creditor. So the `approvedCreditor` can basically act like a new creditor and instead empty all the assets in an account.

The protocol prevents users from forcing this upon buyers of positions on secondary markets by requiring a minimum time elapsed between the setting of the `approvedCreditor` and a transfer of the account, and the buyers are expected to be aware of this when buying an account. However, account transfers also happen during liquidations when the lending pool internalizes a bad loan via the `auctionBoughtIn` function.

```solidity
function auctionBoughtIn(
    address recipient
) external onlyLiquidator nonReentrant {
    _transferOwnership(recipient);
}
```

This transfers the account to the lendingPool and needs to be manually liquidated later. But due to the backdoor via `approvedCreditor`, users can steal the assets present in this account.

The `auctionBoughtIn` function is called during liquidation when the liquidation window has passed.

```solidity
else if (block.timestamp > auctionInformation_.cutoffTimeStamp) {
ILendingPool(creditor).settleLiquidationUnhappyFlow(
    account,
    startDebt,
    msg.sender
);
IAccount(account).auctionBoughtIn(
    creditorToAccountRecipient[creditor]
);
```

This can happen if liquidators are not interested in the assets being held in the account, or if the L2 sequencer has been down for some time, preventing liquidations from happening. Since most liquidations happen via MEV bots, during times of high traffic and gas fees MEV bots might not be interested in liquidating small accounts as well, letting the timer hit the cutoff timestamp.

In this case, instead of a safe manual liquidation, the assets can be stolen via the backdoor in the account.

**Recommendations**

Either reset the `approvedCreditor` variable when transferring an account, or have a per-owner based `approvedCreditor`, like handled in `isAssetManager`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Arcadia |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Arcadia-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

