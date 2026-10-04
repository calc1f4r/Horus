---
# Core Classification
protocol: Contracts V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52268
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/lucid-labs/contracts-v1
source_link: https://www.halborn.com/audits/lucid-labs/contracts-v1
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
  - Halborn
---

## Vulnerability Title

Missing Zero Amount Check in Cross-Chain Bridge Functions

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `burnAndBridge()` and `burnAndBridgeMulti()` functions in AssetController.sol lack input validation for the amount parameter. This allows transactions to be executed with zero amounts:

```
function burnAndBridge(
    address recipient,
    uint256 amount,
    bool unwrap,
    uint256 destChainId,
    address bridgeAdapter
) public payable nonReentrant whenNotPaused {
    uint256 _currentLimit = burningCurrentLimitOf(bridgeAdapter);
    if (_currentLimit < amount) revert IXERC20_NotHighEnoughLimits();
    _useBurnerLimits(bridgeAdapter, amount);
    IXERC20(token).burn(_msgSender(), amount);// @audit - amount is not checked for > 0// ...
}

function burnAndBridgeMulti(
    address recipient,
    uint256 amount,
    bool unwrap,
    uint256 destChainId,
    address[] memory adapters,
    uint256[] memory fees
) public payable nonReentrant whenNotPaused {
// ...
    IXERC20(token).burn(_msgSender(), amount);// @audit - amount is not checked for > 0// ...
}
```

  

The absence of zero-amount validation allows unnecessary transactions that consume gas without transferring value

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

It is recommended to add a zero-amount check at the start of both functions:

```
function burnAndBridge(...) public payable nonReentrant whenNotPaused {
    if (amount == 0) revert InvalidAmount();
// rest of the function
}

function burnAndBridgeMulti(...) public payable nonReentrant whenNotPaused {
    if (amount == 0) revert InvalidAmount();
// rest of the function
}
```

##### Remediation

**SOLVED:** Zero-amount check has been added.

##### Remediation Hash

<https://github.com/LucidLabsFi/demos-contracts-v1/commit/cb840eb7f7df4b63ac7207a41fdb74af617fb6b4>

##### References

[LucidLabsFi/demos-contracts-v1/contracts/modules/chain-abstraction/AssetController.sol#L235](https://github.com/LucidLabsFi/demos-contracts-v1/blob/main/contracts/modules/chain-abstraction/AssetController.sol#L235)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Contracts V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/lucid-labs/contracts-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/lucid-labs/contracts-v1

### Keywords for Search

`vulnerability`

