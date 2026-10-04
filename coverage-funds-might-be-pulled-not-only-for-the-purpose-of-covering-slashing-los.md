---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7004
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective2-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Danyal Ellahi
  - Emanuele Ricci
  - Optimum
  - Matt Eccentricexit
---

## Vulnerability Title

Coverage funds might be pulled not only for the purpose of covering slashing losses

### Overview


This bug report is about a smart contract called CoverageFundV1 which holds ETH to cover a potential lsETH price decrease due to unexpected slashing events. The issue is that the contract is using _maxIncrease as a mandatory growth factor in the context of coverage funds, which might cause the pulling of funds from the coverage fund to ensure _maxIncrease of revenue in case fees are not high enough. This could result in funds being pulled from the CoverageFundV1 even when there is no slashing event.

The recommended solution is to replace the current code with a different code which takes into account the fees and the previous validator total balance. This issue is limited in its impact, as the coverage fund should only hold ETH in the event of a slashing event.

### Original Finding Content

## Severity
**Medium Risk**

## Context
OracleManager.1.sol#L108-L113

## Description
The newly introduced coverage fund is a smart contract that holds ETH to cover a potential lsETH price decrease due to unexpected slashing events. Funds might be pulled from CoverageFundV1 to the River contract through `setConsensusLayerData` to cover the losses and keep the share price stable. In practice, however, it is possible that these funds will be pulled not only in emergency events. 

`_maxIncrease` is used as a measure to enforce the maximum difference between `prevTotalEth` and `postTotalEth`, but in practice, it is being used as a mandatory growth factor in the context of coverage funds, which might cause the pulling of funds from the coverage fund to ensure `_maxIncrease` of revenue in case fees are not high enough.

## Recommendation
Consider replacing:

```solidity
if (((_maxIncrease + previousValidatorTotalBalance) - executionLayerFees) > _validatorTotalBalance) {
    coverageFunds = _pullCoverageFunds(
        ((_maxIncrease + previousValidatorTotalBalance) - executionLayerFees) - _validatorTotalBalance
    );
}
```

with:

```solidity
if (previousValidatorTotalBalance > _validatorTotalBalance + executionLayerFees) {
    coverageFunds = _pullCoverageFunds(
        ((_maxIncrease + previousValidatorTotalBalance) - executionLayerFees) - _validatorTotalBalance
    );
}
```

## Alluvial
Trying to clarify the use-case and the sequence of operations here:

- **Use case**: Liquid Collective partners with Nexus Mutual (NXM) and possibly other actors to cover for slashing losses. Each time Liquid Collective adds a validator key to the system, we will submit the key to NXM so they can monitor it and cover it in case of slashing. In case one of the validator's keys gets slashed (slashing being defined according to NXM policy), NXM will reimburse part or all of the lost ETH. The period between the slashing event occurs and the reimbursement that happens can go from 30 days up to 365 days. The reimbursement will go to the CoverageFund contract and subsequently be pulled into the core system respecting maximum bounds.

- **Sequence of Operations**:
  1. Liquid Collective submits a validator key to NXM to be covered.
  2. A slashing event occurs (e.g., a validator key gets slashed 1 ETH).
  3. NXM monitoring catches the slashing event.
  4. 30 days to 365 days later, NXM reimburses 1 ETH to the CoverageFund.
  5. 1 ETH gets progressively pulled from the CoverageFund into River respecting the bounds.

## Spearbit
Acknowledged as discussed with the Alluvial team, the impact of this issue is limited since the coverage fund should hold ETH only in case of a slashing event.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Danyal Ellahi, Emanuele Ricci, Optimum, Matt Eccentricexit |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective2-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

