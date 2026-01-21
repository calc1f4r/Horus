---
# Core Classification
protocol: Op Enclave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58270
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 4
finders:
  - Zigtur
  - 0xTylerholmes
  - 0xIcingdeath
  - CarrotSmuggler
---

## Vulnerability Title

DeployChain calls can be front-run to deny chain deployments

### Overview


This bug report describes a medium risk vulnerability in the `DeployChain` contract. The `deploy` function in this contract is permissionless, meaning anyone can deploy proxies with an arbitrary chain ID. This can be exploited by an attacker who can call `deploy` before a legitimate transaction is executed, causing the transaction to fail. To fix this vulnerability, the report recommends making the `deployProxy` function internal and implementing an access control on the `deploy` function. This issue has been fixed in the latest version of the contract.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
- `DeployChain.sol#L119-L141`
- `DeployChain.sol#L161-L163`

## Description
The deploy function is permissionless. The chain ID given as input is used as a salt to derive the proxies address. However, as this deployment is permissionless, any user can deploy these proxies with an arbitrary chain ID without being tracked off-chain. This vulnerability can be exploited through the `deploy` and `deployProxy` functions.

## Scenario
Bob wants to deploy a L3 on Base. The chain ID `12345` is given by Coinbase and a call to `deploy` is made. However, Alice (i.e. the attacker) calls `deploy` with this given chain ID before the legit transaction is executed. This call deploys the proxies. Finally, Bob's transaction reverts because the proxies deployment failed.

## Recommendation
1. The `deployProxy` function must not be exposed publicly. Consider making this function internal.
2. Consider setting an access control on the `deploy` function. If this access control is not expected, do not allow the user to pass an arbitrary chain ID. This can be implemented through an incremental counter within a specified range as a chain ID.

## Base
Fixed in PR 45.

## Spearbit
Fixed. The `DeployChain` contract is now Ownable, and only the owner can deploy new chains. Additionally, the `deployProxy` function is now internal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Op Enclave |
| Report Date | N/A |
| Finders | Zigtur, 0xTylerholmes, 0xIcingdeath, CarrotSmuggler |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

