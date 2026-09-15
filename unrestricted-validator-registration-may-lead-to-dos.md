---
# Core Classification
protocol: Ditto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48542
audit_firm: OtterSec
contest_link: https://www.dittofinance.io/
source_link: https://www.dittofinance.io/
github_link: github.com/dittosis/ditto-research-ditto-staking.

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
  - OtterSec
  - Harrison Green
  - Fineas Silaghi
---

## Vulnerability Title

Unrestricted Validator Registration May Lead To DoS

### Overview

The Ditto protocol has a bug where a malicious user can register a large number of fake validators, causing an increase in gas usage and potentially preventing the protocol from operating. To fix this issue, a hard limit on the number of validators will be imposed and active validators will be required to maintain a minimum level of activity or stake. Additionally, the protocol will launch with the whitelist feature enabled and a configuration parameter will be implemented to set a maximum number of validators.

### Original Finding Content

## Validator Security in the Ditto Protocol

Validators can join the Ditto protocol by invoking `ditto_staking::add_validator`. When the validator whitelist is disabled, there are no restrictions on validator entry. Each new validator occupies space in the `ValidatorState` table and `ValidatorLockupBuffer` stored on the `@ditto_staking` account. Many of the computations that interact with validator state run linear time algorithms over these structures and therefore require gas usage roughly linear to the number of validators.

## Risk of Malicious Validation

A malicious user could register a large number of fake validators in order to increase the usage of the associated validator tables and therefore increase the computation requirement on all subsequent instructions. In the worst case, a malicious user may be able to register enough validators to hit the computation limit and therefore prevent the protocol from operating entirely.

## Remediation Strategies

- Impose a hard limit on the number of validators.
- Require all active validators to maintain a minimum level of activity or stake, such that a malicious user cannot easily add a bunch of fake validators.

## Patch

After discussion with the team, Ditto will be launching with their whitelist feature enabled for the foreseeable future to mitigate against such attack vectors. Additionally, Ditto has implemented a `max_n_validators` configuration parameter which sets a hard limit on the number of validators.

© 2022 OtterSec LLC. All Rights Reserved. 6 / 13

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Ditto |
| Report Date | N/A |
| Finders | OtterSec, Harrison Green, Fineas Silaghi |

### Source Links

- **Source**: https://www.dittofinance.io/
- **GitHub**: github.com/dittosis/ditto-research-ditto-staking.
- **Contest**: https://www.dittofinance.io/

### Keywords for Search

`vulnerability`

