---
# Core Classification
protocol: Securitize Onofframp Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64276
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
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

Missing validation check for liquidityToken

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `CollateralLiquidityProvider::initialize()` function does **not verify** that the `liquidityToken` of the passed `securitizeOffRamp`'s `liquidityProvider()` matches the expected token. This check is present in `setExternalCollateralRedemption()` but missing here.

**Impact:** A mismatched `liquidityToken` could lead to misconfiguration, loss of funds, or unintended asset interactions.

 **Recommended Mitigation:**
Add a check in the `initialize()` function to verify that the `liquidityToken` of the `securitizeOffRamp`’s liquidity provider matches the `_liquidityToken` parameter:

```solidity
function initialize(
    address _liquidityToken,
    address _recipient,
    address _securitizeOffRamp
) public onlyProxy initializer {
    if (_recipient == address(0) || _liquidityToken == address(0) || _securitizeOffRamp == address(0)) {
        revert NonZeroAddressError();
    }

    address expectedToken = ILiquidityProvider(
        ISecuritizeOffRamp(_securitizeOffRamp).liquidityProvider()
    ).liquidityToken();

    if (expectedToken != _liquidityToken) {
        revert LiquidityTokenMismatch();
    }

    __BaseContract_init();
    recipient = _recipient;
    liquidityToken = IERC20(_liquidityToken);
    securitizeOffRamp = ISecuritizeOffRamp(_securitizeOffRamp);
}
```

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Onofframp Bridge |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

