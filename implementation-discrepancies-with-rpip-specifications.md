---
# Core Classification
protocol: Rocketpool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53685
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/rocket-pool/rocket-pool-8-houston-pdao/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/rocket-pool/rocket-pool-8-houston-pdao/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Implementation Discrepancies With RPIP Specifications

### Overview

See description below for full details.

### Original Finding Content

## Description

The following implementation discrepancies with the RPIP specifications were observed:

- **RPIP-31** - "As the controller of the RPL for a node, I MUST be able to trigger a claim of RPL rewards and restake a portion. If a node’s RPL withdrawal address is set, the call MUST come from the current RPL withdrawal address." However, based on the implementation of `claimAndStake()` on line [76] from `RocketMerkleDistributorMainnet`, it currently allows for the call to come from one of: the node’s primary withdrawal address, node’s address, or RPL withdrawal address:
  
  ```
  require(msg.sender == _nodeAddress || msg.sender == withdrawalAddress || msg.sender == rplWithdrawalAddress, "Can only claim from node or withdrawal addresses");
  ```

- **RPIP-33** - Some fixed values from the parameter table do not match:
    - Line [49] from `RocketDAOProtocolSettingsInflation` - `rpl.inflation.interval.rate` should be > 1
    - Line [32] from `RocketDAOProtocolSettingsSecurity` - `_value` should be < 0.75
    - Line [46] from `RocketDAOProtocolSettingsNetwork` - `network.submit.balances.frequency` should be > 1 hour

## Recommendations

Modify identified implementations to align with RPIP specs, or clearly document implementation specifics and note any deviations from proposed RPIPs.

## Resolution

The issue for RPIP-31 has been addressed in commit `a747457`.

For RPIP-33, the RocketPool team provided the following comment:  
"The RPIP-33 values are correct in code and need to be updated in the RPIP."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Rocketpool |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/rocket-pool/rocket-pool-8-houston-pdao/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/rocket-pool/rocket-pool-8-houston-pdao/review.pdf

### Keywords for Search

`vulnerability`

