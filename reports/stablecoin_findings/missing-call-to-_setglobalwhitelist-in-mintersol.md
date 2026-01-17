---
# Core Classification
protocol: Syntetika
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62215
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
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
finders_count: 2
finders:
  - Dacian
  - Jorge
---

## Vulnerability Title

Missing call to `_setGlobalWhitelist` in `Minter.sol`

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `Minter.sol` contract inherits the `Whitelist.sol` abstract contract, which manages access control for the `mint ` and `redeem` functions through the `onlyWhitelisted` modifier:

```solidity
  modifier onlyWhitelisted(address addr) {
        require(isAddressWhitelisted(addr), AddressNotWhitelisted());
        _;
    }

    /// @notice Checks if an address is whitelisted.
    /// @param user The address to check.
    /// @return bool True if the address is whitelisted, false otherwise.
    function isAddressWhitelisted(address user) public view returns (bool) {
        if (manualWhitelist[user] || globalWhitelist) { <-------
            return true;
        }

        return complianceChecker.isCompliant(user);
    }

```

The `onlyWhitelisted` modifier checks the `globalWhitelist` flag. The` StakingVault.sol` contract implements the `setGlobalWhitelist ` function, which is crucial because the `StakingVault.sol` contract expects to use it. However, the `Minter.sol` contract, which mints `HilBTC` (the asset for `StakingVault.sol`), does not implement `setGlobalWhitelist`.

**Impact:** The `StakingVault.sol` contract will not work as expected when `setGlobalWhitelist` is enabled because `setGlobalWhitelist` is not implemented in `Minter.sol`.

**Recommended Mitigation:** Consider implementing `setGlobalWhitelist`  in `minter.sol`:

```solidity
 function setGlobalWhitelist(bool enable) external onlyOwner {
        _setGlobalWhitelist(enable);
    }
```

**Syntetika:**
Fixed in commits [1796e5e](https://github.com/SyntetikaLabs/monorepo/commit/1796e5ec7f50e73e5fc4af32365b936244811217), [86c7b2e](https://github.com/SyntetikaLabs/monorepo/commit/86c7b2e30666f4c6522d48b4f4ed05f5d52238b0) by removing the global whitelist functionality as it was not required by the `Minter` contract, and after the fix for L-4 it is not required at all.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Syntetika |
| Report Date | N/A |
| Finders | Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

