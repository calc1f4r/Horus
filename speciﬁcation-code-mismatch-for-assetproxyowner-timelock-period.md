---
# Core Classification
protocol: 0x Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17386
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
github_link: none

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
finders_count: 4
finders:
  - Gustavo Grieco
  - Robert Tonic
  - Rajeev Gopalakrishna
  - Michael Colburn
---

## Vulnerability Title

Speciﬁcation-Code mismatch for AssetProxyOwner timelock period

### Overview


This bug report is about an issue with the MultiSigWalletWithTimeLock.sol and AssetProxyOwner.sol contracts. The contracts have a time-lock period that is configurable by the wallet owner, however, the specification for AssetProxyOwner states that the time-lock should be two weeks. This could lead to a situation where Alice, Bob, and Eve, the owners of AssetProxyOwner, submit a transaction expecting a two-week time-lock but it can be executed after only one day.

In the short term, it is recommended that the necessary range checks are implemented to enforce the two-week time-lock mentioned in the specification. If that is not possible, then the specification should be updated to match the intended behavior. In the long term, it is important to make sure that the implementation and the specification are in sync. Testing tools like Echidna or Manticore can be used to ensure that the code properly implements the specification.

### Original Finding Content

## Type: Data Validation
**Target:** multisig/contracts/src/MultiSigWalletWithTimeLock.sol

## Difficulty: High

### Description
The specification for AssetProxyOwner says: "The AssetProxyOwner is a time-locked multi-signature wallet that has permission to perform administrative functions within the protocol. Submitted transactions must pass a 2 week timelock before they are executed." The MultiSigWalletWithTimeLock.sol and AssetProxyOwner.sol contracts' timelock-period implementation/usage does not enforce the two-week period, but is instead configurable by the wallet owner without any range checks. Either the specification is outdated (most likely), or this is a serious flaw.

### Exploit Scenario
Assuming the specification is correct and indeed expects a two-week timelock: Alice, Bob, and Eve are the owners of AssetProxyOwner, which has been configured with a timelock period of one day. One of them submits a transaction assuming a timelock period of two weeks, but it can be executed after one day, which is not what they expect according to the specification.

### Recommendation
Short term, implement the necessary range checks to enforce the timelock described in the specification. Otherwise, correct the specification to match the intended behavior. Long term, make sure implementation and specification are in sync. Use Echidna or Manticore to test that your code properly implements the specification.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | 0x Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco, Robert Tonic, Rajeev Gopalakrishna, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf

### Keywords for Search

`vulnerability`

