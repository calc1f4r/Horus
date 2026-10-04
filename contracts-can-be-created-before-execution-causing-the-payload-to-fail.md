---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19180
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-aip/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-aip/review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Contracts can be created before execution, causing the payload to fail

### Overview


A Denial of Service attack was discovered that may prevent payload execution. The attack works by deploying contracts GhoToken or GhoFlashMinter before the execution payload attempts to create them. This causes the payload to fail due to the contract address already containing bytecode. To resolve the issue, a new payload needs to be deployed and a second vote must pass to execute the changes. It is recommended to check for the contracts in advance at the predicted addresses and make sure the contract code is as expected. The predicted addresses are checked to ensure that they have no code at 957b050, resolving the issue.

### Original Finding Content

## Description

A Denial of Service attack exists which may prevent payload execution. Either of the contracts `GhoToken` or `GhoFlashMinter` may be deployed before the execution payload attempts to create these contracts. As a result, the payload execution will revert.

The `execute()` function calls the contract at `0x2401ae9bBeF67458362710f90302Eb52b5Ce835a` to deploy new contracts using `CREATE2`. This technique means that the address of the created contract is deterministic and does not depend on the address of the caller. Since the `0x2401ae9bBeF67458362710f90302Eb52b5Ce835a` contract is permissionless, any user may front-run the executor call with the same parameters. This will deploy the contract that the payload would deploy, at the same address.

This would not cause any major security vulnerability in the deployed contracts themselves, as their essential configurations are in their constructors, and so included in their deployment bytecode. However, it would cause the payload itself to fail. The `_deployCreate2()` function would revert when it calls `0x2401ae9bBeF67458362710f90302Eb52b5Ce835a` since the contract address already contains bytecode.

To resolve the issue, a new payload would need to be deployed, and a second vote must pass to execute the changes.

## Recommendations

Consider checking for the contracts in advance at the predicted addresses in `GhoListingPayload` and not deploying if they are already there. In this case, consider also checking that the contract’s code is as expected.

## Resolution

The predicted addresses are checked to ensure that they have no code at `957b050`.

GHO-

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-aip/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-aip/review.pdf

### Keywords for Search

`vulnerability`

