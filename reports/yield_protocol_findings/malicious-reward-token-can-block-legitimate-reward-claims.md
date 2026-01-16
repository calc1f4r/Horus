---
# Core Classification
protocol: Eco Inc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52981
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/cf70074c-8e59-45f6-9745-55523de0394e
source_link: https://cdn.cantina.xyz/reports/cantina_eco_february2025.pdf
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
finders_count: 2
finders:
  - 0xRajeev
  - phaze
---

## Vulnerability Title

Malicious reward token can block legitimate reward claims 

### Overview


The IntentVault contract has a vulnerability that allows intent creators to trick solvers by including a malicious token alongside legitimate reward tokens. This prevents solvers from claiming their rewards and allows the intent creator to reclaim all rewards. This can be used to create deceptive intents that appear profitable but are actually uncollectible. The impact of this vulnerability is high as it allows intent creators to effectively steal from solvers. The likelihood of this attack is medium as it requires malicious intent from the creator, but it is relatively easy to execute. The recommendation is to handle individual reward token transfers using low level calls. This issue has been fixed in a recent commit.

### Original Finding Content

## IntentVault Contract Vulnerability

## Context
[IntentVault.sol#L52-L83](https://github.com/path/to/repo/IntentVault.sol#L52-L83)

## Summary
The IntentVault contract attempts to transfer all reward tokens atomically when an intent is fulfilled. A malicious token in the reward list can prevent the transfer of legitimate reward tokens, allowing intent creators to trick solvers with honeypot intents containing both legitimate and malicious reward tokens.

## Description
When an intent is fulfilled, the vault tries to transfer all reward tokens to the claimant in a single transaction. If any token transfer fails (e.g., due to a malicious token that reverts on transfer), the entire claim transaction will revert. An intent creator can exploit this by including a malicious token alongside legitimate reward tokens:
1. Create an intent with legitimate rewards (e.g., 100 USDC) plus a seemingly worthless token (e.g., 1 XYZ).
2. The malicious XYZ token is programmed to revert on transfers.
3. A solver fills the intent, focusing on the USDC reward value.
4. When claiming rewards, the transfer of XYZ reverts, preventing access to the USDC.
5. After the deadline passes, the intent creator can reclaim all rewards.

This vulnerability can be used to create honeypot intents that appear profitable but are uncollectible.
- Solvers may not thoroughly validate every reward token.
- The malicious token could initially appear legitimate but be upgraded to revert.
- The economic incentive is significant as it allows reclaiming valuable tokens.

## Impact Explanation
The impact is high. This vulnerability allows intent creators to effectively steal from solvers by preventing them from claiming legitimate rewards after they've fulfilled the intent.

## Likelihood Explanation
The likelihood is medium. While it requires malicious intent from the intent creator, the attack is relatively simple to execute by creating a malicious token and including it alongside legitimate rewards. The potential for profit makes this an attractive attack vector.

## Recommendation
Consider individual reward token transfers to fail using low level calls.

## Eco
Fixed in commit `73b7652`.

## Cantina Managed
Verified that commit `73b7652` fixes the issue by handling transfer calls as recommended.

## COMMENTS
- **Nishaad (client):** Should suffice to just transfer via low-level call, right?

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Eco Inc |
| Report Date | N/A |
| Finders | 0xRajeev, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_eco_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/cf70074c-8e59-45f6-9745-55523de0394e

### Keywords for Search

`vulnerability`

