---
# Core Classification
protocol: Strata Tranches
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63238
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
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
finders_count: 3
finders:
  - InAllHonesty
  - Arno
  - Stalin
---

## Vulnerability Title

Missing Validation of Fallback APR Values in `AprPairFeed::latestRoundData`

### Overview

See description below for full details.

### Original Finding Content

**Description:** `AprPairFeed::latestRoundData` fetches APRs from a preferred source (feed or strategy provider). If the feed is stale, it falls back to the strategy provider via `provider.getAprPair()` but does not validate the returned values (e.g., via `ensureValidAprs` or bounds checks), unlike potential validations in the feed path. This allows potentially invalid values to be used

```solidity
function latestRoundData() external view returns (TRound memory) {
        TRound memory round = latestRound;

        if (sourcePref == ESourcePref.Feed) {
            uint256 deltaT = block.timestamp - uint256(round.updatedAt);
            if (deltaT < roundStaleAfter) {
                return round;
            }
            // falls back to strategy ↓
        }

        (int64 aprTarget, int64 aprBase, uint64 t1) = provider.getAprPair();
        return TRound({
            aprTarget: aprTarget,
            aprBase: aprBase,
            updatedAt: t1,
            answeredInRound: latestRoundId + 1
        });
    }
```


**Recommended Mitigation:** Add validation after fallback fetch, similar to feed bounds:
```diff
        (int64 aprTarget, int64 aprBase, uint64 t1) = provider.getAprPair();
+       // Add validation, e.g.:
+       ensureValid(aprTarget);
+       ensureValid(aprBase);
        return TRound({
            aprTarget: aprTarget,
            aprBase: aprBase,
            updatedAt: t1,
            answeredInRound: latestRoundId + 1
        });
```

**Strata:**
Fixed in commit [1c4009a](https://github.com/Strata-Money/contracts-tranches/commit/1c4009a61f6aa1802b0a1541c6e63b096d601d1b) by validating `aprTarget` and `aprBase`.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Strata Tranches |
| Report Date | N/A |
| Finders | InAllHonesty, Arno, Stalin |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

