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
solodit_id: 53604
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
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

Checks-Effects-InteractionsPattern Violations In NodeDelegator

### Overview


The bug report is about a problem in the NodeDelegator code, which violates the Checks-Effects-Interactions (CEI) pattern. This pattern is used to ensure that functions in the code are executed in a specific order to avoid errors. The specific issue is in the `stake32Eth()` function, where the EigenLayer contract takes control of the execution flow while the Kelp contracts are in an intermediate state. This leads to a broken price invariant and incorrect prices for `rsETH`, which can result in losses for the protocol. The report recommends restructuring the code to follow the CEI pattern, and the development team has already made changes to address the issue.

### Original Finding Content

## Description

NodeDelegator implements several functions that violate the Checks-Effects-Interactions (CEI) pattern. Most notably in `stake32Eth()` on line [163], the EigenLayer contract gets control of the execution flow while the Kelp contracts are in an intermediate state. Specifically, the `stakedButUnverifiedNativeETH` price invariant is broken - 32 ETH has left the Kelp contracts but `stakedButUnverifiedNativeETH` has not yet been increased. This means that the EigenLayer contracts, or any sub-call, could call `updateRSETHPrice()` and get an incorrect `rsETH` price. Deposits and withdrawals could then be made assuming this incorrect price, leading to protocol losses:

## NodeDelegator.sol

```solidity
153 function stake32Eth(
155     bytes calldata pubkey,
156     bytes calldata signature,
157     bytes32 depositDataRoot
158 )
159 external
160     whenNotPaused
161     onlyLRTOperator
162 {
163     IEigenPodManager eigenPodManager = IEigenPodManager(lrtConfig.getContract(LRTConstants.EIGEN_POD_MANAGER));
164     eigenPodManager.stake{ value: 32 ether }(pubkey, signature, depositDataRoot);
165     // tracks staked but unverified native ETH
166     stakedButUnverifiedNativeETH += 32 ether;
167     emit ETHStaked(pubkey, 32 ether);
168 }
```

## Other functions where CEI violations occur:

- `stake32EthValidated()` on line [196]
- `verifyWithdrawalCredentials()` on line [226]
- `completeUnstaking()` on line [345]

## Recommendations

Restructure the functions in question to follow the Checks-Effects-Interactions pattern.

## Resolution

The development team has restructured the code where relevant, as seen in `0534d17`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf

### Keywords for Search

`vulnerability`

