---
# Core Classification
protocol: Sablier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40562
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ebb8649e-6999-4e9e-b6ab-e823ae9c47ff
source_link: https://cdn.cantina.xyz/reports/cantina_sablier_apr2024.pdf
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
  - RustyRabbit
---

## Vulnerability Title

Calls to untrusted contracts on Blast are incentivized to steal gas from users 

### Overview


The report discusses a potential security issue in the SablierV2Lockup contract. The issue involves untrusted contracts being able to exploit callback functions to inflate gas usage and steal gas from users. This could happen when users withdraw funds or cancel a stream. The report recommends limiting gas usage for calls to untrusted contracts or finding alternative solutions. However, the Sablier team has decided not to make any changes, as it could limit the functionality of the contract. The issue exists on all chains, but there is an additional incentive for exploitation on the Blast chain. The report has been acknowledged by Cantina Managed.

### Original Finding Content

## Security Context Analysis

## Context
- `SablierV2Lockup.sol#L610-L615`
- `SablierV2Lockup.sol#L395-L400`
- `SablierV2Lockup.sol#L599`

## Description
On Blast, every contract can claim the gas fees paid by the users executing their code. When calling out to untrusted contracts (e.g., callbacks to receiver and sender, but also the `transferFrom` calls on the underlying tokens), these can be exploited by the owners of those contracts to inflate gas usage and steal gas from Sablier's users.

The callback function `onLockupStreamWithdrawn` could be utilized by a scam project to create an airstream with the sole intent to steal gas whenever a user withdraws, either in small increments or with maximum gas usage (gas bombs). This vulnerability also applies to any novel token that behaves similarly during token transfers, which is used in the `withdraw()` and `cancel()` functions. Furthermore, the `onLockupStreamCanceled` function could be exploited by a recipient as an incentivized griefing attack if the stream gets canceled.

Note that this issue exists on all chains, but on Blast, there is actually an extra incentive in the form of Blast gas refunds.

## Recommendation
On Blast, consider limiting the gas used for calls to untrusted contracts or provide alternatives that do not invoke the callback hooks at all.

## Responses
**Sablier:** Thank you for the insights, and we acknowledge the problem. However, limiting the gas would also restrict the capabilities of the hooks in supporting complex transactions. Therefore, we have decided to keep it unchanged.

**Cantina Managed:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sablier |
| Report Date | N/A |
| Finders | RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sablier_apr2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ebb8649e-6999-4e9e-b6ab-e823ae9c47ff

### Keywords for Search

`vulnerability`

