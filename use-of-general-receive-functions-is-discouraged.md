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
solodit_id: 53609
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
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

Use of General receive() Functions is Discouraged

### Overview

See description below for full details.

### Original Finding Content

## Description

In several locations, general `receive()` functions are used. It is recommended to use more specific receive functions. 

For example, instead of:

```solidity
receive() external payable {}
(bool sent,) = payable(withdrawalManager).call{ value: amount }("")
```

it is recommended to use:

```solidity
function receiveFromUnstakingVault() external payable override {}
withdrawalManager.receiveFromUnstakingVault{value: amount}()
```

## Advantages of Specific Functions

Some of the advantages to these more specific functions are:
- **More readable and verbose:** It shows who the intended sender is and what the intent of the transfer is.
- **Avoids accidental ETH transfers from users:** This is especially important for contracts such as `LRTDepositPool.sol`.
- **Extra access control could potentially be placed on these functions:** For example, `msg.sender` must equal `unstakingVault` in `receiveFromUnstakingVault()`.

Certain `receive{}` functions can of course not be replaced. For example, EigenLayer will send ETH to the `receive()` function.

## Recommendations

Review code in question and make alterations as deemed applicable.

## Resolution

The development team has fixed the issue by implementing specific receive functions, as seen in commit `9248e7b`.

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

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-updates/review.pdf

### Keywords for Search

`vulnerability`

