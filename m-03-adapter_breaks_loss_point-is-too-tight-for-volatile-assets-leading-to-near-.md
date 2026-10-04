---
# Core Classification
protocol: Adapterfi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55663
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-05-03-AdapterFi.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - @IAm0x52
---

## Vulnerability Title

[M-03] ADAPTER_BREAKS_LOSS_POINT is too tight for volatile assets leading to near constant adapter blocking

### Overview


The bug report discusses an issue with the FundsAllocator contract in the AdapterVault repository. The problem is related to the stop loss point, which has been set too tight, causing the contract to be nonfunctional for volatile assets. The recommendation is to either remove the stop loss functionality or widen it significantly. The issue has been fixed by updating the stop loss point to 5%.

### Original Finding Content

**Details**

[FundsAllocator.vy#L14](https://github.com/adapter-fi/AdapterVault/blob/3c2895a69ad5eb2c4be16d454f63a6f2f074f351/contracts/FundsAllocator.vy#L14)

    ADAPTER_BREAKS_LOSS_POINT : constant(decimal) = 0.00001

As seen above the stop loss point has been set exceedingly tight

[FundsAllocator.vy#L133-L138](https://github.com/adapter-fi/AdapterVault/blob/3c2895a69ad5eb2c4be16d454f63a6f2f074f351/contracts/FundsAllocator.vy#L133-L138)

    adapter_brakes_limit : uint256 = adapter.last_value - convert(convert(adapter.last_value, decimal) * ADAPTER_BREAKS_LOSS_POINT, uint256)
    if adapter.current < adapter_brakes_limit:
        # We've lost value in this adapter! Don't give it more money!
        blocked_adapters[blocked_pos] = adapter.adapter
        blocked_pos += 1
        adapter.delta = 0 # This will result in no tx being generated.

The PT tokens held by the contract are highly volatile and will trip this stop loss near constantly. The result is that the vault will be effectively nonfunctional for any volatile asset.

**Lines of Code**

[FundsAllocator.vy#L14](https://github.com/adapter-fi/AdapterVault/blob/3c2895a69ad5eb2c4be16d454f63a6f2f074f351/contracts/FundsAllocator.vy#L14)

**Recommendation**

The stoploss functionality is vestigial from when the fund allocator was meant to function with non-volatile lending platforms. This should either be removed entirely or widened significantly.

**Remediation**

Fixed by updating ADAPTER_BREAKS_LOSS_POINT to 0.05 (5%)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Adapterfi |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-05-03-AdapterFi.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

