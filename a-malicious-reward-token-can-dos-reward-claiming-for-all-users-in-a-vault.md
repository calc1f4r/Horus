---
# Core Classification
protocol: Infrared Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49852
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
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
  - 0xRajeev
  - Chinmay Farkya
  - Cryptara
  - Noah Marconi
---

## Vulnerability Title

A malicious reward token can DoS reward claiming for all users in a vault

### Overview


The report discusses a bug in the MultiRewards.sol code, specifically in lines 231-240. The bug allows a malicious reward token to cause a denial of service (DoS) attack on the reward claiming process for all users in a vault. This is because the code transfers reward tokens in a loop, and if any of these tokens are malicious or paused, the process will fail for all users in that vault. The impact of this bug is high, but the likelihood is low since the tokens are whitelisted by governance. The report recommends implementing logic to skip failed token transfers, allowing governance to remove reward tokens from a vault, using a safe call function, and implementing a strict whitelist process. The bug has been fixed in PR 401 and has been reviewed by Spearbit. 

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
MultiRewards.sol#L231-L240

## Summary
A malicious reward token can DoS reward claims for all users in a vault to which it is added. This affects the claiming process for all the reward tokens because they are transferred in a loop, which can be forced to revert.

## Finding Description
In `getRewardForUser()`, after the rewards state is updated, the reward tokens earned by the user are transferred to them iteratively in a loop. However, if any of these reward tokens become malicious (or are paused, where pausing is controlled by external token governance), then the reward claiming process can be forced to revert for all users in that particular InfraredVault.

While there is a way to remove whitelisting of a reward token from the Infrared system by infrared governance, there is no way to remove a reward token from a vault once it's added to it. In an InfraredVault, governance can only add more reward tokens but not remove any. The entire `rewardTokens` list is always processed in a `getRewardForUser()` call.

## Impact Explanation
**High**, because the reward claim process cannot succeed for any tokens and any users in an infrared vault with a malicious reward token.

## Likelihood Explanation
**Low**, because the tokens are whitelisted by infrared governance. This problem can occur even if one of the reward tokens is paused, for example, by the external token's governance.

## Recommendation
Consider using one or more of the following:
1. Logic in the reward transfer loop to skip past failing token transfers.
2. A function for the governance to remove reward tokens from the `rewardTokens` list of an InfraredVault.
3. Nomad's `ExcessivelySafeCall.sol` to prevent return bomb attacks.
4. A stringent whitelist process to only add well-known tokens.

## Infrared
Fixed in PR 401.

## Spearbit
Reviewed that PR 401 adopts recommendation (1) by using a low-level call with gas: 200000.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Infrared Contracts |
| Report Date | N/A |
| Finders | 0xRajeev, Chinmay Farkya, Cryptara, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Infrared-Spearbit-Security-Review-January-2025.pdf

### Keywords for Search

`vulnerability`

