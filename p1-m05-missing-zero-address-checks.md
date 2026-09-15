---
# Core Classification
protocol: Eco Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11644
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/eco-contracts-audit/
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

protocol_categories:
  - dexes
  - yield
  - cross_chain
  - launchpad
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[P1-M05] Missing zero address checks

### Overview


This bug report is about two components, `deploy` and `proxy`, which are part of the BeamNetwork/currency repository. The bug is that functions that take an address as an argument are not validating that the address is not `0`. This means that a mistake could be made by passing a `0` address. The report provides four examples of functions that are affected by this bug.

To fix this issue, the report suggests adding a require statement to check that the address is different from `address(0)`. This issue has been fixed in the `EcoBootstrap.sol` file, and the report provides a statement from the Eco team about why they chose not to disallow the `0` address in code.

### Original Finding Content

###### Medium


Components: [`deploy`](https://github.com/BeamNetwork/currency/tree/af3428020545e3f3ae2f3567b94e1fbc5e5bdb4c/contracts/deploy) and [`proxy`](https://github.com/BeamNetwork/currency/tree/af3428020545e3f3ae2f3567b94e1fbc5e5bdb4c/contracts/proxy)


The functions that take an address as an argument are not validating that the address is not `0`.


For example:


* [`BeamBootstrap.sol`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamBootstrap.sol#L14)[:L14](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamBootstrap.sol#L14)
* [`BeamInitializable.sol`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamInitializable.sol#L11)[:L11](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/BeamInitializable.sol#L11)
* [`ForwardProxy.sol`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/ForwardProxy.sol#L13)[:L13](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/ForwardProxy.sol#L13)
* [`ForwardTarget.sol`](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/ForwardTarget.sol#L21)[:L21](https://github.com/BeamNetwork/beam-bootstrap-chain/blob/96beab1c5cfd41310bfba733ab7216426caf4a38/contracts/ForwardTarget.sol#L21)


In most cases, passing a `0` address is a mistake.


Consider adding a require statement to check that the address is different from `address(0)`.


***Update:*** *Fixed only in* [*EcoBootstrap.sol*](https://github.com/BeamNetwork/currency/blob/af3428020545e3f3ae2f3567b94e1fbc5e5bdb4c/contracts/deploy/EcoBootstrap.sol#L30)*. Eco’s statement for this issue:*



> Thorough testing prevents our system from mistakenly passing the 0 address when initializing a contract or configuring a proxy. Inserting code to prevent the 0 address from being passed at all also prevents us from doing so intentionally, so as a practice we avoid disallowing the 0 address in code.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Eco Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/eco-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

