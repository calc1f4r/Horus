---
# Core Classification
protocol: Knox Finance
chain: everychain
category: logic
vulnerability_type: bypass_limit

# Attack Vector Details
attack_type: bypass_limit
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3391
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/4
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-knox-judging/issues/75

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - bypass_limit
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-4: Users can avoid performance fees by withdrawing before the end of the epoch forcing other users to pay their fees

### Overview


This bug report is about the vulnerability found in the VaultInternal.sol code, which allows users to avoid performance fees by withdrawing before the end of the epoch, forcing other users to pay their fees. This vulnerability was found by manual review and was located at VaultInternal.sol#L504-L532. 

The code in question takes both the current assets of the vault and the total value of withdrawals that happened during the epoch into account when calculating the performance fees. This means that when a user withdraws during the epoch, their withdrawal value is added to the adjusted assets of the vault, and they don't pay any performance fee, but the fee is still taken from the vault collateral. 

The impact of this vulnerability is that users can avoid performance fees and force other users to pay them. The recommendation to fix this issue is to take fees on withdrawals that occur before the vault is settled.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-knox-judging/issues/75 

## Found by 
0x52

## Summary

No performance fees are taken when user withdraws early from the vault but their withdrawal value will be used to take fees, which will be taken from other users.

## Vulnerability Detail

    uint256 adjustedTotalAssets = _totalAssets() + l.totalWithdrawals;

    if (adjustedTotalAssets > l.lastTotalAssets) {
        netIncome = adjustedTotalAssets - l.lastTotalAssets;

        feeInCollateral = l.performanceFee64x64.mulu(netIncome);

        ERC20.safeTransfer(l.feeRecipient, feeInCollateral);
    }

When taking the performance fees, it factors in both the current assets of the vault as well as the total value of withdrawals that happened during the epoch. Fees are paid from the collateral tokens in the vault, at the end of the epoch. Paying the fees like this reduces the share price of all users, which effectively works as a fee applied to all users. The problem is that withdraws that take place during the epoch are not subject to this fee and the total value of all their withdrawals are added to the adjusted assets of the vault. This means that they don't pay any performance fee but the fee is still taken from the vault collateral. In effect they completely avoid the fee force all there other users of the vault to pay it for them.

## Impact

User can avoid performance fees and force other users to pay them

## Code Snippet

[VaultInternal.sol#L504-L532](https://github.com/sherlock-audit/2022-09-knox/blob/main/knox-contracts/contracts/vault/VaultInternal.sol#L504-L532)

## Tool used

Manual Review

## Recommendation

Fees should be taken on withdrawals that occur before vault is settled

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Knox Finance |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-knox-judging/issues/75
- **Contest**: https://app.sherlock.xyz/audits/contests/4

### Keywords for Search

`Bypass limit, Business Logic`

