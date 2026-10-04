---
# Core Classification
protocol: Polygon zkEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53613
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Aggregator Rewards Are Averaged Across Forced Batches & Rollups

### Overview


The report describes a bug where the single batch fee shared across all rollups causes issues when there is high throughput. This results in increased gas fees for users and mismatched rewards for aggregators. The recommendation is to add modularization for each rollup and keep track of forced batch fees to accurately distribute rewards. However, the development team has decided to close the issue as they believe the fee pricing mechanism works as intended and there are fallback mechanisms in place. They also mention that the high force batch fee is meant as a disincentive for users and not an incentive for aggregators.

### Original Finding Content

## Description

There is a single batch fee shared across all rollups. It is set based off throughput, increasing when there is high throughput and decreasing when there is low throughput. Since there is only a single batch fee, rollups with large throughput will increase the batch fee for rollups with low throughput.

The sequencer will only include batches if there is sufficient reward in the gas fees and MEV to cover the batch fee. Hence, when the batch fee is increasing, the sequencer will increase the L2 gas price users must pay to have their transaction included in a block. Therefore, if there is a single rollup which has high throughput, this will increase gas fees paid by users on all rollups.

Additionally, aggregator rewards are based off the contract’s POL balance divided by the number of sequenced batches but not aggregated. The rewards distributed for aggregating a batch are not directly matched to the fee charged for the batch.

```solidity
function calculateRewardPerBatch() public view returns (uint256) {
    uint256 currentBalance = pol.balanceOf(address(this));
    // Total Batches to be verified = total Sequenced Batches - total verified Batches
    uint256 totalBatchesToVerify = totalSequencedBatches - totalVerifiedBatches;
    if (totalBatchesToVerify == 0) return 0;
    return currentBalance / totalBatchesToVerify;
}
```

The function `calculateRewardPerBatch()` calculates aggregator rewards by taking the total balance of the contract and dividing it by the total number of sequenced batches. Thus, the fee paid when sequencing a batch is not directly aligned with the amount rewarded to the aggregator for verifying a batch.

Forced batches will incur a higher sequence batch fee, to which the aggregator will not receive the entirety of the forced batch fee. Furthermore, if the batch fee has increased or decreased significantly from when the batch was sequenced, the aggregator will not receive exactly the original fee paid.

## Recommendations

It is recommended to add further modularisation such that there is a batch fee for each rollup. Additionally, this would require to internally account for the POL fees contributed by each rollup. Thus, when an aggregator verifies a batch they will receive rewards only associated with that rollup.

Keeping track of forced batch fees awaiting sequencing would enable accurate transmission of the forced batch fee to the PolygonRollupManager contract. However, the testing team acknowledges that including this extra logic will complicate the sequencing fee system and increase gas costs as a result. Therefore, as forced batches are likely to be rare, it may also be adequate to document the behavior of forced batch rewards to make aggregators aware.

## Resolution

The development team has acknowledged the comments above and decided to close the issue with the following rationale:

- The fee pricing mechanism works as intended. A higher throughput would result in more machines being spun up to aggregate in parallel and would thus not result in an increased batch fee. Additionally, there are several fallback mechanisms to fix any issues in case they arise.
- The (high) force batch fee is intended as a disincentive to the user, not as an incentive to the aggregator. As such, the high fee can be used to accelerate the aggregation of the following batches.
- Having one common pool of POL is useful since it smoothes out the rewards for the aggregators. Furthermore, it makes it easy to incentivize faster aggregation by sending POL to the pool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Polygon zkEVM |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf

### Keywords for Search

`vulnerability`

