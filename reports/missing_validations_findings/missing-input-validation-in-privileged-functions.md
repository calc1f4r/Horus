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
solodit_id: 64249
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

Missing input validation in privileged functions

### Overview

See description below for full details.

### Original Finding Content

**Description:** Admin functions lack proper parameter validation, which could lead to unintended state changes if incorrect values are provided. While admin users are expected to act correctly, human error remains possible.

```solidity
SecuritizeRedemption.sol
75:     function initialize(address _asset, address _navProvider) public onlyProxy initializer navProviderNonZero(_navProvider) {
76:         __BaseDSContract_init();
77:         asset = IERC20(_asset);//@audit-issue INFO non zero check
78:         navProvider = ISecuritizeNavProvider(_navProvider);
79:     }
80:

SecuritizeRedemption.sol
81:     function updateLiquidityProvider(address _liquidityProvider) onlyOwner external {
82:         address oldProvider = address(liquidityProvider);
83:         liquidityProvider = ILiquidityProvider(_liquidityProvider);//@audit-issue INFO non zero check
84:         emit LiquidityProviderUpdated(oldProvider, address(liquidityProvider));
85:     }

SecuritizeRedemption.sol
87:     function updateNavProvider(address _navProvider) onlyOwner navProviderNonZero(_navProvider) external {
88:         address oldProvider = address(navProvider);
89:         navProvider = ISecuritizeNavProvider(_navProvider);//@audit-issue INFO non zero check
90:         emit NavProviderUpdated(oldProvider, address(navProvider));
91:     }
```

```solidity
CollateralLiquidityProvider.sol
66:     function initialize(address _recipient, address _liquidityToken, address _securitizeRedemption) public onlyProxy initializer {
67:         __BaseDSContract_init();
68:         recipient = _recipient;//@audit-issue LOW sanity check
69:         liquidityToken = IERC20(_liquidityToken);
70:         securitizeRedemption = ISecuritizeRedemption(_securitizeRedemption);
71:     }

98:
99:     function setCollateralProvider(address _collateralProvider) external onlyOwner {
100:         address oldAddress = address(collateralProvider);
101:         collateralProvider = _collateralProvider;//@audit-issue LOW sanity check
102:         emit CollateralProviderUpdated(oldAddress, address(collateralProvider));
103:     }
```

```solidity
AllowanceLiquidityProvider.sol
65:     function initialize(address _recipient, address _liquidityToken, address _securitizeRedemption) public onlyProxy initializer {
66:         __BaseDSContract_init();
67:         recipient = _recipient;//@audit-issue LOW sanity check
68:         liquidityToken = IERC20(_liquidityToken);
69:         securitizeRedemption = ISecuritizeRedemption(_securitizeRedemption);
70:     }

85:     function setAllowanceProviderWallet(address _liquidityProviderWallet) external onlyOwner {
86:         address oldAddress = liquidityProviderWallet;
87:         liquidityProviderWallet = _liquidityProviderWallet;//@audit-issue sanity check
88:         emit AllowanceLiquidityProviderWalletUpdated(oldAddress, liquidityProviderWallet);
89:     }
```

**Securitize:** Fixed in commit [8254e8](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/8254e84a8bd2579780cc7b3b1ffa4b9821bcd505).

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

