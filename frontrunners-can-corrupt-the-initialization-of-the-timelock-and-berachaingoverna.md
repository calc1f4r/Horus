---
# Core Classification
protocol: Berachain Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52849
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Governance-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Governance-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 2
finders:
  - Tnch
  - Xmxanuel
---

## Vulnerability Title

Frontrunners can corrupt the initialization of the TimeLock and BerachainGovernance contracts

### Overview


This bug report discusses a medium risk issue with the deployment process in a smart contract called DeployGovernance.s.sol. The process involves deploying two contracts, BerachainGovernance and TimeLock, but the initialization of these contracts is done in separate transactions, leaving them temporarily in an uninitialized state. This allows for potential malicious actors to interfere with the initialization process and corrupt the deployment. The recommendation is to make the deployment and initialization operations atomic by moving them to a single smart contract. This bug has been fixed in a recent commit for Berachain, and has been resolved for Spearbit.

### Original Finding Content

## Medium Risk Severity Report

## Context
- `DeployGovernance.s.sol#L49`
- `DeployGovernance.s.sol#L63`

## Description
The deployment process implemented in `DeployGovernance.s.sol` begins with two transactions (see `DeployGovernance.s.sol#L39-L44`) that deploy the corresponding implementation and proxy contracts for **BerachainGovernance** and **TimeLock**.

However, the initialization of the proxies' state is not done in those deployment transactions. Instead, it's done afterwards, in two individual transactions that call the contracts' `initialize` function (see `DeployGovernance.s.sol#L49` and `DeployGovernance.s.sol#L63`).

This means that, after the deployment transactions and before the initialization transactions, the proxies are temporarily left in an uninitialized state. Consequently, anyone can frontrun the initialization transactions and initialize the proxies of TimeLock and BerachainGovernance with malicious parameters to corrupt the deployment process.

## Recommendation
The deployment and initialization operations should be done atomically, ensuring that proxies are never left in an uninitialized state. One possible implementation could involve moving the deployment process to a single smart contract that can deploy the contracts and initialize the proxies in a single transaction.

## Resolution
- **Berachain:** Fixed in commit `60195c68`.
- **Spearbit:** Resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Berachain Governance |
| Report Date | N/A |
| Finders | Tnch, Xmxanuel |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Governance-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Governance-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

