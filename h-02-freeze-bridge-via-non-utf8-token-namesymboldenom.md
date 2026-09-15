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
solodit_id: 720
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-08-gravity-bridge-contest
source_link: https://code4rena.com/reports/2021-08-gravitybridge
github_link: https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/4

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

[H-02] Freeze Bridge via Non-UTF8 Token Name/Symbol/Denom

### Overview


A bug has been identified in the Cosmos Gravity Bridge that affects the parsing of logs. Manual insertion of non-utf8 characters in a token name will break parsing of logs and will always result in the oracle getting in a loop of failing and early returning an error. This bug can be triggered by sending a specific call data to the Gravity contract. The log output of this call data will be invalid utf8, which will cause the validator and orchestrator to not process the event nonce. This means that the validators and orchestrators will not be able to process attestations and the bridge will be effectively stopped until a new Gravity contract is deployed. A possible fix for this bug is to check in the solidity contract if the name contains valid utf8 strings for denom, symbol and name. Alternatively, validators can be required to sign ERC20 creation requests and perform checks before the transaction is sent.

### Original Finding Content

_Submitted by nascent_

Manual insertion of non-utf8 characters in a token name will break parsing of logs and will always result in the oracle getting in a loop of failing and early returning an error. The fix is non-trivial and likely requires significant redesign.

### Proof of Concept
Note the `c0` in the last argument of the call data (invalid UTF8).

It can be triggered with:

```solidity
data memory bytes = hex"f7955637000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000000000461746f6d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000046e616d6500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000673796d626fc00000000000000000000000000000000000000000000000000000";
gravity.call(data);
```

The log output is as follows:
```solidity
    ERC20DeployedEvent("atom", "name", ❮utf8 decode failed❯: 0x73796d626fc0, 18, 2)
```

Which hits [this code path](https://github.com/althea-net/cosmos-gravity-bridge/blob/92d0e12cea813305e6472851beeb80bd2eaf858d/orchestrator/gravity_utils/src/types/ethereum_events.rs#L431-L438):

```rust
    let symbol = String::from_utf8(input.data[index_start..index_end].to_vec());
    trace!("Symbol {:?}", symbol);
    if symbol.is_err() {
        return Err(GravityError::InvalidEventLogError(format!(
            "{:?} is not valid utf8, probably incorrect parsing",
            symbol
        )));
    }
```

And would cause an early return [here](https://github.com/althea-net/cosmos-gravity-bridge/blob/92d0e12cea813305e6472851beeb80bd2eaf858d/orchestrator/orchestrator/src/ethereum_event_watcher.rs#L99):

```rust
let erc20_deploys = Erc20DeployedEvent::from_logs(&deploys)?;
```

Never updating last checked block and therefore, this will freeze the bridge by disallowing any attestations to take place. This is an extremely low cost way to bring down the network.

#### Recommendation
This is a hard one. Re-syncing is permanently borked because, on the Go side, there is seemingly no way to ever process the event nonce because protobufs do not handle non-utf8 strings. The validator would report they need event nonce `N` from the orchestrator, but they can never parse the event `N`. Seemingly, validators & orchestrators would have to know to ignore that specific event nonce. But it is a permissionless function, so it can be used to effectively permanently stop attestations & the bridge until a new `Gravity.sol` is deployed.

One potential fix is to check in the solidity contract if the name contains valid utf8 strings for denom, symbol and name. This likely will be expensive though. Alternatively, you could require that validators sign ERC20 creation requests and perform checks before the transaction is sent.

**[jkilpatr (Althea) confirmed](https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/4#issuecomment-917151454):**
 > This is a valid and well considered bug.
>
> I do disagree about the difficulty of the fix though, if we fail to parse the token name as utf8 we can just encode the bytes themselves in hex and pass that along. The result will be perfectly valid if a little unergonomic.

**[albertchon (judge) commented](https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/4#issuecomment-925867313):**
 > Clever, great catch



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
- **GitHub**: https://github.com/code-423n4/2021-08-gravitybridge-findings/issues/4
- **Contest**: https://code4rena.com/contests/2021-08-gravity-bridge-contest

### Keywords for Search

`Bridge`

