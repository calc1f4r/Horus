---
# Core Classification
protocol: Kelp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53651
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Missing Input Checks In completeUnstaking()

### Overview

See description below for full details.

### Original Finding Content

## Description

The function `completeUnstaking()` in the `LRTUnstakingVault` contract does not check that the parameter `assets` has the same length as `queuedEigenLayerWithdrawal.shares`, even though this is implicitly assumed in the for-loop on line [111]. Additionally, no checks are performed to ensure that the length of `assets` is larger than zero.

## LRTUnstakingVault.sol

```solidity
96 function completeUnstaking(
IStrategy.QueuedWithdrawal calldata queuedEigenLayerWithdrawal,
98 IERC20[] calldata assets,
uint256 middlewareTimesIndex
100 )
external
102 onlyLRTManager
nonReentrant
104 {
address eigenlayerStrategyManagerAddress = lrtConfig.getContract(LRTConstants.EIGEN_STRATEGY_MANAGER);
106
// Finalize withdrawal with Eigenlayer Strategy Manager
108 IEigenStrategyManager(eigenlayerStrategyManagerAddress).completeQueuedWithdrawal(
queuedEigenLayerWithdrawal, assets, middlewareTimesIndex, true
110 );
for (uint256 i = 0; i < assets.length;) {
112 sharesUnstaking[address(assets[i])] -= queuedEigenLayerWithdrawal.shares[i];
unchecked {
114 i++;
}
116 }
emit EigenLayerWithdrawalCompleted(
118 queuedEigenLayerWithdrawal.depositor, queuedEigenLayerWithdrawal.withdrawerAndNonce.nonce, msg.sender
);
120 }
```

## Recommendations

Consider implementing input validation checks to avoid unexpected behaviour and improve the readability of error messages.

## Resolution

The development team has fixed the above issue in commit `931965c`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf

### Keywords for Search

`vulnerability`

