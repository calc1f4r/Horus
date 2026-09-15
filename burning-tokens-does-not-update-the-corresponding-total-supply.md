---
# Core Classification
protocol: Golem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17021
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/golem.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/golem.pdf
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
finders_count: 5
finders:
  - Gustavo Grieco
  - 2018: April 5
  - 2018: Initial report delivered Retest report delivered
  - Changelog March 23
  - Chris Evans
---

## Vulnerability Title

Burning tokens does not update the corresponding total supply

### Overview


This bug report is about a Denial of Service vulnerability in the GolemTokenNetworkBatching contract. The burn function in this contract does not update the totalSupply in the GolemTokenNetwork, leading to an incorrect value being reported. This could be exploited by a malicious third party to destabilize the Golem network by manipulating the economics of additional token minting.

One possible mitigation is to implement a similar function to burn tokens in the GolemTokenNetwork contract and call it using the token infrastructure from GolemTokenNetworkBatching. It is also recommended to consolidate token logic and management to a central core contract that allows token creation, burning, and locking. This will ensure that the consistency is maintained and accurately reflects the tokens in circulation.

### Original Finding Content

## Type: Denial of Service
## Target: GolemTokenNetworkBatching

### Difficulty: High

### Description
The burn function in `GolemTokenNetworkBatching` does not update the `totalSupply` in the `GolemTokenNetwork`. Since the burned tokens are deleted and no longer associated with one particular address (e.g. `0x0`), the `GolemTokenNetwork` reports more tokens than it should. This issue may cause code or logic that depends on the value of `totalSupply` (for instance, code that calculates the value of a Golem token) to report an incorrect value.

### Exploit Scenario
Bob is a malicious third party intent on destabilizing the Golem network. He burns a significant amount of tokens in the `TokenProxy` contract to cause an internal inconsistency between the amount of tokens in circulation and tracked token supply count. He can use this information by either manipulating the economics of additional token minting or by causing an invariant failure in token supply conditions for a contract migration.

### Recommendations
One possible mitigation is to implement a similar function to burn tokens in the `GolemTokenNetwork` contract and call it using the token infrastructure from `GolemTokenNetworkBatching`. Nevertheless, a naive implementation is not recommended to avoid other security issues such as TOB-Golem-12.

In the long term, it is strongly recommended to consolidate token logic and management to a central core contract that allows token creation, burning, and locking. Rather than implementing proxy classes that manage internal state independently, migrate users to a single token instance that is interoperable with all Golem smart contracts. This will ensure that the consistency is maintained and accurately reflects the tokens in circulation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Golem |
| Report Date | N/A |
| Finders | Gustavo Grieco, 2018: April 5, 2018: Initial report delivered Retest report delivered, Changelog March 23, Chris Evans |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/golem.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/golem.pdf

### Keywords for Search

`vulnerability`

