---
# Core Classification
protocol: Accountable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62975
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
github_link: none

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

protocol_categories:
  - options_vault
  - liquidity_manager
  - insurance
  - uncollateralized_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Immeas
  - Chinmay
  - Alexzoid
---

## Vulnerability Title

`transferWhitelist` checks are missing in `AccountableVault::_checkTransfer`

### Overview


The AccountableVault.sol contract has a feature called "transferWhitelist" that is supposed to allow certain addresses to transfer vault shares, overriding other restrictions. However, this feature is not working and is not being checked in the transfer functions. This means that the whitelist does not have any effect and any address can transfer shares. To fix this, the _checkTransfer() function needs to be updated to include a check for the transferWhitelist. Additionally, a method to set the whitelist should be added to the strategy contracts. This issue has been fixed in the Accountable contract, but it is still present in the Cyfrin contract.

### Original Finding Content

**Description:** AccountableVault.sol employs a "transferWhitelist" feature to help select addresses that should be allowed to transfer vault shares, overriding the other restrictions checked in `_checkTransfer()`.

Both `transfer()` and `transferFrom()` functions internally call `_checkTransfer()`, but the "transferWhitelist" check is missing in all transfer flows.

**Impact:** The transferWhitelist feature does not work, so it does not make a difference if an address was whitelisted or not.

```solidity
    /// @notice Mapping of addresses that can override transfer restrictions
    mapping(address => bool) public transferWhitelist;
```

The comment above says "Mapping of addresses that can override transfer restrictions" which does not hold true as transferWhitelist is never being checked.

A method to call vault.setTransferWhitelist() is also missing in both the current strategy contracts, so when fixing keep note of it.

**Recommended Mitigation:**
```solidity
    function _checkTransfer(uint256 amount, address from, address to) private {

+++      if(transferWhitelist[from] && transferWhitelist[to]) return;

        if (amount == 0) revert ZeroAmount();
        if (!transferableShares) revert SharesNotTransferable();
        if (!isVerified(to, msg.data)) revert Unauthorized();
        if (throttledTransfers[from] > block.timestamp) revert TransferCooldown();
    }
```

Also consider adding a method to the AccountableFixedTerm and AccountableOpenTerm strategy contracts (one that calls vault.setTransferWhitelist()) if it is required in context of that strategy.

**Accountable:** Whitelist removed in commit [`6a81e38`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/6a81e389513ad690216fc8c037ec69513f3121c7)

**Cyfrin:** Verified. Whitelist removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Accountable |
| Report Date | N/A |
| Finders | Immeas, Chinmay, Alexzoid |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

