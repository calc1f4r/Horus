---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34408
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#1-the-implementation-can-be-destroyed-by-the-owner
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

The implementation can be destroyed by the `owner`

### Overview

See description below for full details.

### Original Finding Content

##### Description
`owner` has rights to add any sender and bridge adapter on the implementation: https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/CrossChainController.sol#L12-L31 It can be used to call `selfdestruct` in some chains.
The implementation will be deployed by an EOA and the private key of the EOA can be stolen, or EOA can turns out a malicious actor.

##### Recommendation
We recommend transferring the ownership of the implementation to the `ZERO_ADDRESS`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#1-the-implementation-can-be-destroyed-by-the-owner
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

