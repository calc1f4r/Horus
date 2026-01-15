---
# Core Classification
protocol: Deriverse Dex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64539
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
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
finders_count: 4
finders:
  - RajKumar
  - Ctrus
  - Alexzoid
  - JesJupyter
---

## Vulnerability Title

Users can provide old price feeds to trade in their favor

### Overview


The function set_underlying_px is used in many parts of the code to set the underlying price for an oracle feed provided by the user. However, the function does not check the freshness of the data, meaning that an old or intentionally frozen price can be accepted as current. This could lead to incorrect trade calculations and allow attackers to over or under-pay. The recommended solution is to check the timestamp of the feed to ensure it is recent, and to not accept prices that are too old. The team at Deriverse is currently excluding oracle support, and the issue has been verified by Cyfrin.

### Original Finding Content

**Description:** The function [set_underlying_px](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/state/instrument.rs#L224) is being called from many places in code, its setting the underlying price from user provided oracle feed if oracle is set. `set-underlying-px` relays on user provided feed but never verifies the price publish time or confidence interval. A price that is hours old (or intentionally frozen) is accepted as fresh. It  doesnt check whether the oracle data is fresh, whether the oracle slot/timestamp is recent, whether the oracle confidence is good, the only check in place is feed account address matches expected.
```rust
            let feed_id = next_account_info!(accounts_iter)?;
            if self.header.feed_id == *feed_id.key {
                let oracle_px =
                    i64::from_le_bytes(feed_id.data.borrow()[73..81].try_into().unwrap());
                let oracle_exponent =
                    9 + i32::from_le_bytes(feed_id.data.borrow()[89..93].try_into().unwrap());
                let mut dc: i64 = 1;
```
Even if the account is the correct feed ID, the data inside may be old, because we currently do not check any of the feed's fields like Pyth format has timestamp, slot, conf, etc., which tells us how fresh the feed is.

**Impact:** Trade may be computed from obsolete data, letting attackers over or under-pay.

**Recommended Mitigation:** Check the feed's timestamp to ensure its recent, we can allow upto certain minutes old prices and if the interval if more than allowed, dont accept it.

**Deriverse**
We exclude oracle support.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Deriverse Dex |
| Report Date | N/A |
| Finders | RajKumar, Ctrus, Alexzoid, JesJupyter |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

