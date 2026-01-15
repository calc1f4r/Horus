---
# Core Classification
protocol: JPEG'd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1925
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-jpegd-contest
source_link: https://code4rena.com/reports/2022-04-jpegd
github_link: https://github.com/code-423n4/2022-04-jpegd-findings/issues/4

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

protocol_categories:
  - lending
  - dexes
  - cdp
  - services
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 17
finders:
  - reassor
  - JMukesh
  - 0xkatana
  - cccz
  - 0xDjango
---

## Vulnerability Title

[M-10] Chainlink pricer is using a deprecated API

### Overview


This bug report is about a vulnerability found in the code of the FungibleAssetVaultForDAO.sol and NFTVault.sol contracts. The vulnerability is related to the use of the deprecated latestAnswer function, which might suddenly stop working if Chainlink stops supporting deprecated APIs and can return stale data. To mitigate this vulnerability, it is recommended to use the latestRoundData function to get the price instead and to add checks on the return data with proper revert messages if the price is stale or the round is incomplete.

### Original Finding Content

_Submitted by cccz, also found by 0xDjango, 0xkatana, berndartmueller, Cr4ckM3, defsec, horsefacts, hyh, JMukesh, joshie, Jujic, pedroais, peritoflores, rayn, reassor, Ruhum, and WatchPug_

According to Chainlink's documentation, the latestAnswer function is deprecated. This function might suddenly stop working if Chainlink stops supporting deprecated APIs. And the old API can return stale data.

### Proof of Concept

[FungibleAssetVaultForDAO.sol#L105](https://github.com/code-423n4/2022-04-jpegd/blob/main/contracts/vaults/FungibleAssetVaultForDAO.sol#L105)<br>
[NFTVault.sol#L459](https://github.com/code-423n4/2022-04-jpegd/blob/main/contracts/vaults/NFTVault.sol#L459)<br>

### Recommended Mitigation Steps

Use the latestRoundData function to get the price instead. Add checks on the return data with proper revert messages if the price is stale or the round is uncomplete.<br>
<https://docs.chain.link/docs/price-feeds-api-reference/>

**[spaghettieth (JPEG'd) confirmed](https://github.com/code-423n4/2022-04-jpegd-findings/issues/4)**

**[spaghettieth (JPEG'd) resolved and commented](https://github.com/code-423n4/2022-04-jpegd-findings/issues/4#issuecomment-1099244659):**
 > Fixed in [jpegd/core#9](https://github.com/jpegd/core/pull/9).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | JPEG'd |
| Report Date | N/A |
| Finders | reassor, JMukesh, 0xkatana, cccz, 0xDjango, Ruhum, Jujic, WatchPug, berndartmueller, pedroais, peritoflores, rayn, joshie, Cr4ckM3, hyh, horsefacts, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-jpegd
- **GitHub**: https://github.com/code-423n4/2022-04-jpegd-findings/issues/4
- **Contest**: https://code4rena.com/contests/2022-04-jpegd-contest

### Keywords for Search

`vulnerability`

