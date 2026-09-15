---
# Core Classification
protocol: Rocket Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16560
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
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
  - Dominik Teiml
  - Devashish Tomar
  - Maximilian Krüger
---

## Vulnerability Title

Potential collisions between eternal storage and Solidity mapping storage slots

### Overview

See description below for full details.

### Original Finding Content

## Description
The Rocket Pool code uses eternal storage to store many named mappings. A named mapping is one that is identified by a string (such as “minipool.exists”) and maps a key (like `contractAddress` in Figure 8.1) to a value.

```solidity
setBool(keccak256(abi.encodePacked("minipool.exists", contractAddress)), true);
```
_**Figure 8.1:** `RocketMinipoolManager.sol#L216`_

Given a mapping whose state variable appears at index N in the code, Solidity stores the value associated with the key at a slot that is computed as follows:

- `h = type(key) == string || type(key) == bytes ? keccak256 : left_pad_to_32_bytes`
- `slot = keccak256(abi.encodePacked(h(key), N))`

_**Figure 8.2:** Pseudocode of the Solidity computation of a mapping’s storage slot_

The first item in a Rocket Pool mapping is the identifier, which could enable an attacker to write values into a mapping that should be inaccessible to the attacker. We set the severity of this issue to informational because such an attack does not currently appear to be possible.

## Exploit Scenario
Mapping A stores its state variable at slot n. Rocket Pool developers introduce new code, making it possible for an attacker to change the second argument to `abi.encodePacked` in the `setBool` setter (shown in Figure 8.1). The attacker passes in a first argument of 32 bytes and can then pass in n as the second argument and set an entry in Mapping A.

## Recommendations
- **Short Term:** Switch the order of arguments such that a mapping’s identifier is the last argument and the key (or keys) is the first (as in `keccak256(key, unique_identifier_of_mapping)`).
- **Long Term:** Carefully examine all raw storage operations and ensure that they cannot be used by attackers to access storage locations that should be inaccessible to them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Rocket Pool |
| Report Date | N/A |
| Finders | Dominik Teiml, Devashish Tomar, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf

### Keywords for Search

`vulnerability`

