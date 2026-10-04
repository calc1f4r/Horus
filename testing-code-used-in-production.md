---
# Core Classification
protocol: Drift Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17523
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-12-driftlabs-driftprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-12-driftlabs-driftprotocol-securityreview.pdf
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
  - Anders Helsing
  - Samuel Moelius
---

## Vulnerability Title

Testing code used in production

### Overview

See description below for full details.

### Original Finding Content

## Drift Protocol Security Assessment

**Difficulty:** Undetermined

**Type:** Data Validation

**Target:** programs/drift/src/state/{oracle_map.rs, perp_market.rs}

## Description

In some locations in the Drift Protocol codebase, testing code is mixed with production code with no way to discern between them. Testing code should be clearly indicated as such and guarded by `#[cfg(test)]` to avoid being called in production.

Examples appear in Figures 10.1 and 10.2. The `OracleMap` struct has a `quote_asset_price_data` field that is used only when `get_price_data` is passed a default `Pubkey`. Similarly, the AMM implementation contains functions that are used only for testing and are not guarded by `#[cfg(test)]`.

```rust
pub struct OracleMap<'a> {
    oracles: BTreeMap<Pubkey, AccountInfoAndOracleSource<'a>>,
    price_data: BTreeMap<Pubkey, OraclePriceData>,
    pub slot: u64,
    pub oracle_guard_rails: OracleGuardRails,
    pub quote_asset_price_data: OraclePriceData,
}
impl <'a> OracleMap<'a> {
    ...
    pub fn get_price_data(&mut self, pubkey: &Pubkey) -> DriftResult<&OraclePriceData> {
        if pubkey == &Pubkey::default() {
            return Ok(&self.quote_asset_price_data);
        }
    }
}
```
*Figure 10.1: programs/drift/src/state/oracle_map.rs#L22–L47*

```rust
impl AMM {
    pub fn default_test() -> Self {
        let default_reserves = 100 * AMM_RESERVE_PRECISION;
        // make sure tests don't have the default sqrt_k = 0
        AMM {
            ...
        }
    }
}
```
*Figure 10.2: programs/drift/src/state/perp_market.rs#L490–L494*

Drift Protocol has indicated that the `quote_asset_price_data` field (Figure 10.1) is used in production. This raises concerns because there is currently no way to set the contents of this field, and no asset’s price is perfectly constant (e.g., even stablecoins’ prices fluctuate). For this reason, we have changed this finding’s severity from Informational to Undetermined.

## Exploit Scenario

Alice, a Drift Protocol developer, introduces code that calls the `default_test` function, not realizing it is intended only for testing. Alice introduces a bug as a result.

## Recommendations

Short term, to the extent possible, avoid mixing testing and production code by, for example, using separate data types and storing the code in separate files. When testing and production code must be mixed, clearly mark the testing code as such, and guard it with `#[cfg(test)]`. These steps will help to ensure that testing code is not deployed in production.

Long term, as new code is added to the codebase, ensure that the aforementioned standards are maintained. Testing code is not typically held to the same standards as production code, so it is more likely to include bugs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Drift Protocol |
| Report Date | N/A |
| Finders | Anders Helsing, Samuel Moelius |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-12-driftlabs-driftprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-12-driftlabs-driftprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

