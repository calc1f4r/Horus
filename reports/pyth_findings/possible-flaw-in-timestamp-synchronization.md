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
solodit_id: 46890
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

Possible Flaw in Timestamp Synchronization

### Overview


The bug report discusses a problem with the timestamp synchronization in the oracle::get_price function in the Pyth oracle. This function uses two different time sources, causing a potential inconsistency in the timestamp. This can result in the code constantly reverting, even when the data from the Pyth oracle is valid. To fix this issue, the code needs to be rewritten using a safer method that does not assume perfect synchronization. This has been resolved in a recent patch.

### Original Finding Content

## Timestamp Synchronization Inconsistency in `oracle::get_price`

There is a timestamp synchronization inconsistency within `oracle::get_price`. The Pyth oracle’s `publish_time` is generated elsewhere, and the Fuel chain’s `timestamp()` is based on the local blockchain. Thus, these time sources may not be perfectly synchronized. As a result, `timestamp()` may be behind `publish_time`.

> _oracle-contract/src/main.sw sway_
> 
> ```sway
> fn get_price() -> u64 {
>     // Determine the current timestamp based on debug mode
>     let current_time = match DEBUG {
>         true => storage.debug_timestamp.read(),
>         false => timestamp(),
>     };
>     // Read the last stored valid price
>     let last_price = storage.price.read();
>     // Step 1: Query the Pyth oracle (primary source)
>     let pyth_price = abi(PythCore, PYTH.bits()).price(PYTH_PRICE_ID);
>     // Check if Pyth data is stale
>     if current_time - pyth_price.publish_time > TIMEOUT {
>         // Step 2: Pyth is stale, query Redstone oracle (fallback source)
>         [...]
>     }
>     [...]
> }
> ```

`get_price` currently checks if the Pyth data is stale by comparing the difference between `timestamp()` and `publish_time`. It subtracts `publish_time` from `current_time` (Fuel’s `timestamp`). If `publish_time` is ahead of `timestamp()` due to clock drift, the difference may be negative, resulting in the code constantly reverting, even when Pyth’s data is valid. This issue is similarly applicable to the Redstone Oracle.

## Remediation

Rewrite the staleness check using a safer method that does not assume perfect synchronization, such as employing a saturating subtraction or a `timestamp() > publish_time + TIMEOUT` check instead.

## Patch

Resolved in `f8006a0`.

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

