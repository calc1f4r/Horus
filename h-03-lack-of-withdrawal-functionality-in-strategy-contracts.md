---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44983
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] Lack of withdrawal functionality in strategy contracts

### Overview


The Lido and DSR strategies are responsible for managing deposits of ETH and DAI to earn yields. However, these strategies do not have withdrawal functionality, preventing the protocol from retrieving deposited tokens and accumulated rewards. This can result in the protocol not being able to maintain reserves and users losing access to their funds. The recommendation is to implement withdrawal functionality and integrate the withdrawal process with the secondary market.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The `LidoStrategy` and `DSRStrategy` contracts are responsible for managing `ETH` and `DAI` deposits into `Lido` and `sDAI`, respectively, to earn yields.

These strategies are integrated with the `DepositETH` and `DepositUSD` contracts, which handle user deposits and facilitate interactions with `Lido` and `sDAI`.

```solidity
function executeStrategies(StrategyExecution[] memory _executionData) external override {
    if(msg.sender!=strategyExecutor) revert IncorrectStrategyExecutor(msg.sender);
    unchecked{
        for(uint i=0;i<_executionData.length;i++){
            if(!IStrategyManager(strategyManager)
                .strategyExists(_executionData[i].strategy)) revert IncorrectStrategy(_executionData[i].strategy);
@>          (bool success, bytes memory returndata) =
                _executionData[i].strategy.delegatecall(_executionData[i].executionData);
            if(!success){
                if (returndata.length == 0) revert CallFailed();
                assembly {
                    revert(add(32, returndata), mload(returndata))
                }
            }
---
}
```

However, the `LidoStrategy` and `DSRStrategy` contracts lack withdrawal functionality. As a result, the `DepositETH` and `DepositUSD` contracts cannot retrieve deposited tokens along with their accumulated rewards.

This limitation prevents the protocol from redeeming assets when needed, leaving it unable to maintain reserves required to fulfill users’ share redemptions, ultimately resulting in users losing access to their funds.

## Recommendations

Implement withdrawal functionality to the `LidoStrategy` and `DSRStrategy` contracts, enabling the protocol to retrieve deposited tokens along with accumulated rewards.

Moreover, for the `Lido` strategy, the withdrawal from Lido (primary market) requires the request and claim process to integrate with their withdrawal queue so the protocol will need to handle the withdrawal request and claim process or choose to integrate withdrawal with the secondary market.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

