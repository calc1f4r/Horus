---
# Core Classification
protocol: Yearn v2 Vaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16946
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
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
  - Gustavo Grieco
  - Mike Martel
---

## Vulnerability Title

revokeStrategy function can be error-prone

### Overview

See description below for full details.

### Original Finding Content

## Description

The function to revoke strategies may cause errors because of issues in its implementation and documentation. Yearn vaults require strategies to generate yields. A strategy can be added or removed and, in certain cases, revoked:

```solidity
@external
def revokeStrategy(strategy: address = msg.sender):
    assert msg.sender in [strategy, self.governance, self.guardian]
    self._revokeStrategy(strategy)

@internal
def _revokeStrategy(strategy: address):
    self.debtRatio -= self.strategies[strategy].debtRatio
    self.strategies[strategy].debtRatio = 0
    log StrategyRevoked(strategy)
```

*Figure 4.1: A revokeStrategy implementation without comments*

The revokeStrategy implementation has three issues:

- Any address, even that of a non-strategy sender, can successfully call it. While this call should not cause a state change, a StrategyRevoke event with an unexpected value will be emitted.
  
- It does not remove the revoked strategy from the withdrawal queue. While this is intended behavior, it should be clearly explained in the documentation so that callers will not forget to remove strategies if necessary.
  
- The documentation incorrectly states that a strategy "will only revoke itself during emergency shutdown." In actuality, a strategy can do that only in "emergency exit mode."

## Exploit Scenario

Eve repeatedly calls revokeStrategy with different addresses to generate confusing events. Users notice the events and, in a panic, sell their shares, thinking that all the vault’s strategies were suddenly revoked.

## Recommendations

## Short Term

- Prevent senders that are not strategies from calling revokeStrategy.
- Clearly define when a revoked strategy should be removed from the withdrawal queue.
- Correct the part of the documentation that details when a strategy can revoke itself.

Long term, review the access controls of every function and make sure that the documentation is correct and complete.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yearn v2 Vaults |
| Report Date | N/A |
| Finders | Gustavo Grieco, Mike Martel |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf

### Keywords for Search

`vulnerability`

