---
# Core Classification
protocol: Remora Pledge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61212
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
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
  - Stalin
---

## Vulnerability Title

Retrieve and enforce token decimal precision

### Overview

See description below for full details.

### Original Finding Content

**Description:** Retrieve and enforce token decimal precision using [`IERC20Metadata`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/IERC20Metadata.sol). For example:

1) `PledgeManager::initialize`
```diff
    constructor(
        address authority,
        address _holderWallet,
        address _propertyToken,
        address _stablecoin,
-       uint16 _stablecoinDecimals,
        uint32 _fundingGoal,
        uint32 _deadline,
        uint32 _withdrawDuration,
        uint32 _pledgeFee,
        uint32 _earlySellPenalty,
        uint32 _pricePerToken
    ) AccessManaged(authority) ReentrancyGuardTransient() {
        holderWallet = _holderWallet;
        propertyToken = _propertyToken;
        stablecoin = _stablecoin;
-       stablecoinDecimals = _stablecoinDecimals;
+       stablecoinDecimals = IERC20Metadata(_stablecoin).decimals();
        fundingGoal = _fundingGoal;
        deadline = _deadline;
        postDeadlineWithdrawPeriod = _withdrawDuration;
        pledgeFee = _pledgeFee;
        earlySellPenalty = _earlySellPenalty;
        pricePerToken = _pricePerToken;
        tokensSold = 0;
    }
```

2) `TokenBank::initialize`
```diff
        stablecoin = _stablecoin; //must be 6 decimal stablecoin
+       require(IERC20Metadata(stablecoin).decimals() == 6, "Wrong decimals");
```

**Remora:** This was resolved by adding the `remoraToNativeDecimals` which always converts from internal Remora precision to external stablecoin precision, so the protocol can now work with different decimal stablecoins.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Remora Pledge |
| Report Date | N/A |
| Finders | Dacian, Stalin |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

