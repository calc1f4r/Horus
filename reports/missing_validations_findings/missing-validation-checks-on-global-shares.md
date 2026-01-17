---
# Core Classification
protocol: Blueberry StakeUp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47278
audit_firm: OtterSec
contest_link: https://www.blueberry.garden/
source_link: https://www.blueberry.garden/
github_link: https://github.com/Blueberryfi/StakeUp

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
finders_count: 2
finders:
  - Robert Chen
  - Matteo Oliva
---

## Vulnerability Title

Missing Validation Checks On Global Shares

### Overview

See description below for full details.

### Original Finding Content

## Reliance on `CrossChainLST::_syncShares`

The reliance on `CrossChainLST::_syncShares` to update the `_globalShares` value across chains introduces a potential issue if the Layer Zero endpoint experiences downtime. `_syncShares` utilizes Layer Zero for communication between chains. If the Layer Zero endpoint becomes unavailable due to technical issues, messages containing updates to `_globalShares` will not be delivered to other chains. As a result of the downtime, the `_globalShares` value on some chains may become outdated. Several key protocols, states, and actions rely on this value.

## `_syncShares` Function in Solidity

```solidity
function _syncShares(
    uint256 shares,
    bool increase,
    LZMessageSettings calldata msgSettings,
    address refundRecipient
) internal returns (MessagingReceipt[] memory) {
    uint256 prevGlobalShares = _globalShares;
    [...]
    return
        IStakeUpMessenger(_messenger).syncShares{
            value: msgSettings.fee.nativeFee
        }(
            prevGlobalShares,
            shares,
            increase,
            peerEids,
            msgSettings.options,
            refundRecipient
        );
}
```

`_accrueYield` relies on `getSupplyIndex`, which utilizes `_globalShares` to calculate the total USD value attached to each unit of share. If `_globalShares` is outdated, the yield calculation will be inaccurate, resulting in incorrect distribution of rewards. `_withdraw` utilizes the ratio between shares and `_totalUsd` (derived from `_globalShares`) to determine the amount of underlying assets to withdraw. An outdated `_globalShares` value will result in users withdrawing more or less than they are entitled to.

## Remediation

Disallow minting and burning if the Layer Zero endpoint is down or the last update of `_globalShares` is stale.

---

© 2024 Otter Audits LLC. All Rights Reserved.  
Stake Up Protocol Audit 05 — General Findings  
Fixed in PR #74.  
© 2024 Otter Audits LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Blueberry StakeUp |
| Report Date | N/A |
| Finders | Robert Chen, Matteo Oliva |

### Source Links

- **Source**: https://www.blueberry.garden/
- **GitHub**: https://github.com/Blueberryfi/StakeUp
- **Contest**: https://www.blueberry.garden/

### Keywords for Search

`vulnerability`

