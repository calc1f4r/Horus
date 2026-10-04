---
# Core Classification
protocol: Securitize Redeem Swap Vault Na
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64251
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
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
  - Hans
---

## Vulnerability Title

Missing PausableUpgradable initialization in SecuritizeSwap contract initialization

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `SecuritizeSwap` contract inherits from `PausableUpgradeable` (through `BaseSecuritizeSwap`) but doesn't call `__Pausable_init()` during initialization. While this currently doesn't affect functionality since the default state (paused = false) matches the initialization state, it's a deviation from best practices.

**Recommended Mitigation:** For completeness and following best practices, add the Pausable initialization:
```solidity
function initialize(...) public override initializer onlyProxy {
    BaseSecuritizeSwap.initialize(
        _dsToken,
        _stableCoin,
        _erc20Token,
        _issuerWallet,
        _liquidityProvider,
        _externalCollateralRedemption,
        _collateralToken,
        _swapMode
    );
    __BaseDSContract_init();
    __Pausable_init();
}
```

**Securitize:** Fixed in commit [637bcc](https://bitbucket.org/securitize_dev/securitize-swap/commits/637bcce49acab125b54caeaa98fffc1790782b60).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Redeem Swap Vault Na |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

