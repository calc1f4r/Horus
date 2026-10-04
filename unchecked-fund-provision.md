---
# Core Classification
protocol: Tsunami GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47811
audit_firm: OtterSec
contest_link: https://tsunami.finance/
source_link: https://tsunami.finance/
github_link: https://github.com/Tsunami-Finance/tsunami-contracts

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
finders_count: 3
finders:
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Unchecked Fund Provision

### Overview

See description below for full details.

### Original Finding Content

## Pyth Price Update Issue in Contracts

In the `GlpManager`, `PositionRouter`, and `Router` contracts, when updating Pyth prices, the invoker of `updatePriceFeeds` must pay an update fee. The contracts assume that the caller (i.e., `msg.sender`) is responsible for covering the update fees. However, there is no check in place to ensure that `msg.value` is larger than the update fees, and in such cases, the contract depletes its own Ether instead.

## Affected Code

### File: `contracts/core/PositionManager.sol` (SOLIDITY)

```solidity
function _updatePythPrices(bytes[] calldata _pythUpdateData) internal {
    IPyth pyth = IVault(vault).getPyth();
    uint updateFee = pyth.getUpdateFee(_pythUpdateData);
    pyth.updatePriceFeeds{value: updateFee}(_pythUpdateData);
}

function liquidatePosition(
    /* ... */
    bytes[] calldata _pythUpdateData
) external payable nonReentrant onlyLiquidator {
    _updatePythPrices(_pythUpdateData);
    /* ... */
}
```

## Exploitation Details

Users may exploit this to deplete all Ether present in the contract by repeatedly invoking Pyth price feed updates. However, the severity of this issue is low for two reasons: 

1. The likelihood of this attack is low because all contracts above wrap Ether in WETH and thus do not have a balance.
2. Even if there is Ether, it cannot be stolen and is only depleted, which is not motivating from the attacker’s perspective.

## Remediation

In `_updatePythPrices`, assert the equivalence of `msg.value` and `updateFee`.

## Patch

Fixed in commit `18460e8`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tsunami GMX |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: https://tsunami.finance/
- **GitHub**: https://github.com/Tsunami-Finance/tsunami-contracts
- **Contest**: https://tsunami.finance/

### Keywords for Search

`vulnerability`

