---
# Core Classification
protocol: Curve DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17768
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
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
finders_count: 3
finders:
  - Gustavo Grieco
  - Josselin Feist
  - Michael Colburn
---

## Vulnerability Title

Spam attack would prevent LiquidityGauge ’s integral from being updated

### Overview


This bug report is about an access control issue in the ERC20CV.vy target. The bug is rated as high difficulty and involves an attacker spamming the LiquidityGauge, which prevents the integral from being updated. This means that users will not earn any interest. The attacker is able to prevent the integral from being updated by calling the contract frequently, and the attack is partially mitigated by the gas cost, but miners can still perform the attack without paying any gas.

The exploit scenario involves a malicious miner, Eve, who adds a call to LiquidityGauge on every block. This prevents the LiquidityGauge from earning any interest.

The short-term recommendation is to ensure that the system's parameters always make the rate * last_weight greater than the _working_supply. The long-term recommendation is to take into consideration short and long time period increases in the tests and consider using Echidna and Manticore to identify unexpected behaviors allowed by these increases.

### Original Finding Content

## Access Controls

**Target:** ERC20CV.vy

**Difficulty:** High

## Description
An attacker spamming `LiquidityGauge` can prevent the integral from being updated. As a result, users will not earn interest.

On every balance’s update, `LiquidityGauge._checkpoint` is executed and updates the integral based on the time elapsed since the last update:

```python
@private
def _checkpoint(addr: address):
    _integrate_checkpoint: timestamp = self.integrate_checkpoint
    [..]
    dt = as_unitless_number(block.timestamp - _integrate_checkpoint)
    [..]
    _integrate_inv_supply += rate * last_weight * dt / _working_supply
```

_Figure 6.1: LiquidityGauge.vy#L92-L146_

If `rate * last_weight * dt < _working_supply`, the integral will not be updated. `dt` is the time elapsed since the last call to `_checkpoint` and is directly controllable by the caller.

An attacker can prevent the integral from being updated by calling the contract frequently. The attack is partially mitigated by the gas cost, but miners can perform the attack without paying any gas.

## Exploit Scenario
Eve is a malicious miner and adds a call to `LiquidityGauge` on every block. As a result, Eve prevents the `LiquidityGauge` from earning interest.

## Recommendation
Short term, ensure that the system’s parameters always make `rate * last_weight` greater than `_working_supply`.

Long term, take into consideration short and long time period increases in the tests, and consider using Echidna and Manticore to identify unexpected behaviors allowed by these increases.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Curve DAO |
| Report Date | N/A |
| Finders | Gustavo Grieco, Josselin Feist, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf

### Keywords for Search

`vulnerability`

