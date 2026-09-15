---
# Core Classification
protocol: Althea Gravity Bridge
chain: everychain
category: uncategorized
vulnerability_type: bridge

# Attack Vector Details
attack_type: bridge
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 722
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-08-gravity-bridge-contest
source_link: https://code4rena.com/reports/2021-08-gravitybridge
github_link: https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/6

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
  - bridge

protocol_categories:
  - dexes
  - bridge
  - cdp
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - nascent
---

## Vulnerability Title

[H-04] Large Validator Sets/Rapid Validator Set Updates May Freeze the Bridge or Relayers

### Overview


This bug report details a vulnerability in the Cosmos Gravity Bridge that could cause both the eth_oracle_main_loop and relayer_main_loop to fall into a state of perpetual errors. The vulnerability is triggered when a validator set is sufficiently large or rapidly updated, which causes the web3 call "check_for_events" to continuously return an error if the logs in a 5000 block range are in excess of 10mb. This will freeze the bridge by disallowing attestations to take place. 

The recommended solution is to handle the error more concretely and check if a byte limit error has occurred. If so, the search size should be chunked into 2 and repeated as necessary, with the results combined.

### Original Finding Content

_Submitted by nascent_

In a similar vein to "Freeze The Bridge Via Large ERC20 Names/Symbols/Denoms", a sufficiently large validator set or sufficiently rapid validator update, could cause both the `eth_oracle_main_loop` and `relayer_main_loop` to fall into a state of perpetual errors. In `find_latest_valset`, [we call](https://github.com/althea-net/cosmos-gravity-bridge/blob/92d0e12cea813305e6472851beeb80bd2eaf858d/orchestrator/relayer/src/find_latest_valset.rs#L33-L40):

```rust
let mut all_valset_events = web3
    .check_for_events(
        end_search.clone(),
        Some(current_block.clone()),
        vec![gravity_contract_address],
        vec![VALSET_UPDATED_EVENT_SIG],
    )
    .await?;
```

Which if the validator set is sufficiently large, or sufficiently rapidly updated, continuoussly return an error if the logs in a 5000 (see: `const BLOCKS_TO_SEARCH: u128 = 5_000u128;`) block range are in excess of 10mb. Cosmos hub says they will be pushing the number of validators up to 300 (currently 125). At 300, each log would produce 19328 bytes of data (4\*32+64\*300). Given this, there must be below 517 updates per 5000 block range otherwise the node will fall out of sync.

This will freeze the bridge by disallowing attestations to take place.

This requires a patch to reenable the bridge.

#### Recommendation

Handle the error more concretely and check if you got a byte limit error. If you did, chunk the search size into 2 and try again. Repeat as necessary, and combine the results.

**[jkilpatr (Althea) confirmed](https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/6#issuecomment-916968683):**
 > This is a solid report with detailed computations to back it up. I appreciate it and will take actions in our web3 library to prevent this exact scenario.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Althea Gravity Bridge |
| Report Date | N/A |
| Finders | nascent |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-gravitybridge
- **GitHub**: https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/6
- **Contest**: https://code4rena.com/contests/2021-08-gravity-bridge-contest

### Keywords for Search

`Bridge`

