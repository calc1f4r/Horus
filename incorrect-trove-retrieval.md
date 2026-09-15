---
# Core Classification
protocol: Fluid Protocol (Hydrogen Labs)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46889
audit_firm: OtterSec
contest_link: https://fluidprotocol.xyz/
source_link: https://fluidprotocol.xyz/
github_link: https://github.com/Hydrogen-Labs/fluid-protocol

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - James Wang
  - Alpha Toure
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Incorrect Trove Retrieval

### Overview


The bug report states that there is an issue with the function "require_no_undercollateralized_troves" which checks for undercollateralized troves in the system. The problem is that the troves are being retrieved incorrectly from a sorted list, where the troves with the highest Instantaneous Collateral Ratio (ICR) appear first and the troves with the lowest ICR appear last. However, the function is retrieving the first trove from the list, assuming it is the most at risk for undercollateralization, when it should actually be looking at the troves with lower ICRs. This can be fixed by replacing the function "get_first" with "get_last" to access the trove with the lowest ICR. The bug has been resolved in a recent patch.

### Original Finding Content

## Issue in `require_no_undercollateralized_troves`

In `require_no_undercollateralized_troves`, which checks to ensure that there are no undercollateralized troves in the system, the troves are incorrectly retrieved from the sorted structure. The troves are sorted by their Instantaneous Collateral Ratio (ICR) from high to low. This implies that the trove with the highest ICR (most collateralized) appears first in the sorted list, while the trove with the lowest ICR (potentially undercollateralized) appears last.

```sway
fn require_no_undercollateralized_troves() {
    let sorted_troves = abi(SortedTroves, storage.sorted_troves_contract.read().into());
    let mut i = 0;
    while i < storage.valid_assets.len() {
        let price = oracle.get_price();
        let first = sorted_troves.get_first(asset);
        require(
            first == Identity::Address(Address::zero()) || trove_manager
                .get_current_icr(first, price) > MCR,
            "StabilityPool: There are undercollateralized troves",
        );
        i += 1;
    }
}
```

Thus, utilizing `get_first` will give the trove with the highest ICR. However, the current method retrieves the first asset from `sorted_troves`, assuming that this position will be the most at risk for undercollateralization, when, in fact, it should be examining the troves with lower ICRs, as they are the ones more likely to be at risk.

## Remediation

Replace `get_first` with `get_last` to directly access the trove with the lowest ICR.

## Patch

Resolved in `19bb35e`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Fluid Protocol (Hydrogen Labs) |
| Report Date | N/A |
| Finders | James Wang, Alpha Toure, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://fluidprotocol.xyz/
- **GitHub**: https://github.com/Hydrogen-Labs/fluid-protocol
- **Contest**: https://fluidprotocol.xyz/

### Keywords for Search

`vulnerability`

