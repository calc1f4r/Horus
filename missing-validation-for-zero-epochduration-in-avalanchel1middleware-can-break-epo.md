---
# Core Classification
protocol: Suzaku Core
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61264
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
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
  - 0kage
  - Farouk
---

## Vulnerability Title

Missing validation for zero `epochDuration` in AvalancheL1Middleware can break epoch based accounting

### Overview

See description below for full details.

### Original Finding Content

**Description:** `AvalancheL1Middleware::EPOCH_DURATION` is an immutable parameter set in the constructor. The current implementation only checks that `slashingWindow` is not less than `epochDuration` but doesn't verify that `epochDuration` itself is greater than zero.

```solidity
constructor(
    AvalancheL1MiddlewareSettings memory settings,
    address owner,
    address primaryAsset,
    uint256 primaryAssetMaxStake,
    uint256 primaryAssetMinStake,
    uint256 primaryAssetWeightScaleFactor
) AssetClassRegistry(owner) {
    // Other validations...

    if (settings.slashingWindow < settings.epochDuration) {
        revert AvalancheL1Middleware__SlashingWindowTooShort(settings.slashingWindow, settings.epochDuration);
    }

    //@audit No check for zero epochDuration!

    START_TIME = Time.timestamp();
    EPOCH_DURATION = settings.epochDuration;
    // Other assignments...
}
```

The check `settings.slashingWindow < settings.epochDuration` will pass as long as slashingWindow is also zero.

**Impact:** Contract functions such as `getEpochAtTs` rely on division by EPOCH_DURATION, which would cause divide-by-zero errors.


**Recommended Mitigation:** Consider adding an explicit validation check for the `epochDuration` parameter in the constructor.

**Suzaku:**
Acknowledged.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Suzaku Core |
| Report Date | N/A |
| Finders | 0kage, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

