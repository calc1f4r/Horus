---
# Core Classification
protocol: Starbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43955
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2024/08/starbase/
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
  - Sergii Kravchenko
  -  Vladislav Yaroshuk
                        
---

## Vulnerability Title

Missing Validation of receiver in AggregatedSwapRouter ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



In the `d81b6f90d52b12dcfd6f05f023b19ca6e9a8c9e2` commit provided for the fix review the finding has been partially fixed using the provided recommendation, the check hasn’t been added to `swapFromEth`, `defiSwapFromEth` functions, also, the check should be done as a modifier to make the code cleaner and more gas efficient.


**Update (commit hash `7bd9750abbf283970167a4b9b475633481a38d50`):** Fixed.




#### Description


In the following functions:


* `swap`
* `defiSwap`
* `defiSwapForEth`
* `swapForEth`
* `defiSwapFromEth`
* `swapFromEth`


there is no validation to ensure that the `receiver` address is not the zero address, the `_CallSwapTool` address, or the `AggregatedSwapRouter` address. Allowing a transaction to proceed with a zero address as the `receiver` can lead to unintended behavior, such as tokens being irretrievably lost and burned at the zero address, resulting in a loss for the original caller.


#### Examples


**starbase\_swap/contracts/AggregatedSwapRouter.sol:L19\-L24**



```
function swap(
    uint amountIn,
    uint amountOutMin,
    address tokenIn,
    address tokenOut,
    address receiver,

```
**starbase\_swap/contracts/AggregatedSwapRouter.sol:L48\-L53**



```
function defiSwap(
    uint amountIn,
    uint amountOutMin,
    address tokenIn,
    address tokenOut,
    address receiver,

```
**starbase\_swap/contracts/AggregatedSwapRouter.sol:L70\-L74**



```
function defiSwapForEth(
    uint amountIn,
    uint amountOutMin,
    address tokenIn,
    address payable receiver,

```
**starbase\_swap/contracts/AggregatedSwapRouter.sol:L87\-L91**



```
function swapForEth(
    uint amountIn,
    uint amountOutMin,
    address tokenIn,
    address payable receiver,

```
**starbase\_swap/contracts/AggregatedSwapRouter.sol:L111\-L114**



```
function defiSwapFromEth(
    uint amountOutMin,
    address tokenOut,
    address receiver,

```
**starbase\_swap/contracts/AggregatedSwapRouter.sol:L142\-L145**



```
function swapFromEth(
    uint amountOutMin,
    address tokenOut,
    address receiver,

```
#### Recommendation


We recommend adding a modifier with validation to ensure that the `receiver` is not a zero address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Starbase |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Vladislav Yaroshuk
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2024/08/starbase/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

