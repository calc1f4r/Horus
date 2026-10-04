---
# Core Classification
protocol: Sherlock Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16641
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Sherlockv2.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Sherlockv2.pdf
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
  - Alexander Remie Simone Monica
---

## Vulnerability Title

Missing input validation in setMinActiveBalance could cause a confusing event to be emitted

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Medium

## Type: Undeﬁned Behavior

## Description
The `setMinActiveBalance` function’s input validation is incomplete: it should check that the `minActiveBalance` has not been set to its existing value, but this check is missing. Additionally, if the `minActiveBalance` is set to its existing value, the emitted `MinBalance` event will indicate that the old and new values are identical. This could confuse systems monitoring the contract that expect this event to be emitted only when the `minActiveBalance` changes.

```solidity
function setMinActiveBalance(uint256 _minActiveBalance) external override onlyOwner {
  // Can't set a value that is too high to be reasonable
  require(_minActiveBalance < MIN_BALANCE_SANITY_CEILING, 'INSANE');
  emit MinBalance(minActiveBalance, _minActiveBalance);
  minActiveBalance = _minActiveBalance;
}
```
*Figure 7.1: contracts/managers/SherlockProtocolManager.sol:422-428*

## Exploit Scenario
An off-chain monitoring system controlled by the Sherlock protocol is listening for events that indicate that a contract configuration value has changed. When such events are detected, the monitoring system sends an email to the admins of the Sherlock protocol. Alice, a contract owner, calls `setMinActiveBalance` with the existing `minActiveBalance` as input. The off-chain monitoring system detects the emitted event and notifies the Sherlock protocol admins. The Sherlock protocol admins are confused since the value did not change.

## Recommendations
- **Short term:** Add input validation that causes `setMinActiveBalance` to revert if the proposed `minActiveBalance` value equals the current value.
- **Long term:** Document and test the expected behavior of all the system’s events. Consider using a blockchain-monitoring system to track any suspicious behavior in the contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Sherlock Protocol V2 |
| Report Date | N/A |
| Finders | Alexander Remie Simone Monica |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Sherlockv2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Sherlockv2.pdf

### Keywords for Search

`vulnerability`

