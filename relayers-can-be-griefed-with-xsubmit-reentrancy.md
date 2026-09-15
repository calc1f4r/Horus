---
# Core Classification
protocol: Omni Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53659
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
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

Relayers Can Be Griefed With xsubmit() Reentrancy

### Overview


The report describes a bug where an attacker can use a smart contract to initiate multiple transactions in a specific order, causing problems for the relayer who is processing the transactions. This can result in the relayer spending a lot of gas to revert the transactions. To fix this issue, the recommendation is to prevent reentrancy in a specific function by using a tool called OpenZeppelin's `ReentrancyGuard`. This issue has been resolved by adding a modifier called `nonReentrant` in the affected function.

### Original Finding Content

## Description
An attacker can initiate an XMsg that calls a smart contract that reenters into `OmniPortal.xsubmit()` to submit subsequent XMsgs in the XBlock. Since XMsgs from the same source chain need to be executed in order, this attack will cause the relayer’s submission to fail if they have included any XMsgs after the attacker’s, as the XMsgs would have already been executed.

This issue has a medium severity as the attacker can grief the relayer, causing them to spend lots of gas for reverting transactions. To do this, they can front-run the relayer with a transaction that posts the submission data to the attacker contract, so that it can be used to call `xsubmit()` inside the XCall. Front-running the relayer makes it impossible for them to simulate and detect the revert scenario before submitting their transaction on-chain.

## Recommendations
Avoid allowing reentrancy in `xsubmit()`. This can be achieved via OpenZeppelin’s `ReentrancyGuard`.

## Resolution
The `nonReentrant` modifier has been added to the function `xsubmit()` in PR #1074 as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Omni Network |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/omni-network/Sigma%20Prime%20-%20Omni%20Network%20-%20Omni%20Portal%20-%20Security%20Assessment%20Report%20-%20v2.1.pdf

### Keywords for Search

`vulnerability`

