---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62659
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Tapio/README.md#1-initial-mint-front-run-inflation-attack
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3.5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Initial Mint Front-Run Inflation Attack

### Overview


This report discusses a bug found in the `mint()` function of the `SelfPeggingAsset` contract. The bug allows an attacker to front-run the initial liquidity provider by depositing a minimal amount before the legitimate provider, resulting in the legitimate provider receiving fewer LP tokens than expected and suffering a loss of assets. The bug is classified as critical because it can cause significant financial loss and damage user confidence. The report recommends minting a small "dead share" or initializing the pool in a paused state to prevent this attack.

### Original Finding Content

##### Description
This issue has been identified within the `mint()` function of the `SelfPeggingAsset` contract.

An attacker can front-run the initial liquidity provider by depositing a minimal amount (for example, 1 wei) before the first legitimate mint, bypassing the `_minMintAmount` protection. As a result, the legitimate provider may receive substantially fewer LP tokens than expected, effectively suffering a loss of deposited assets.

**Attack Scenario**
* The attacker front-runs the initial mint operation by first transferring 1 wei of each token. They then mint themselves 1 wei of shares by depositing 1 wei of either token and subsequently transfer the same amounts of tokens that the legitimate minter intended to deposit, thereby inflating the exchange rate.
* The transaction of the initial minter bypasses the `minMintAmount` check because it involves passing the amounts of tokens (not shares) to `poolToken.mintShares`. Inside `poolToken.mintShares`, the amount of tokens is rounded down, resulting in 0 shares being minted.
* As a result, the legitimate provider, attempting to mint even with a slippage `minMintAmount` parameter being set, is effectively undercut and receives no newly minted shares, while the attacker ends up with nearly all of them.

The issue is classified as **critical** severity because it enables the theft of the entire initial liquidity deposit, causing significant financial loss and severely damaging user confidence.

##### Recommendation

We recommend minting a small “dead share” (e.g., `1000 wei`) as part of the initial LPToken mint to ensure that a strict minimum number of shares is always created in the first deposit. Alternatively, consider initializing the pool in a paused state, allowing only the admin to perform the initial mint. Additionally, consider minting shares equal to the sum of the `totalSupply` and `_tokenAmount` if the current `totalShares` value of the LPToken is zero. This approach ensures that the exchange rate cannot be unfairly inflated during the first deposit, effectively preventing this front-running attack.


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3.5/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Tapio/README.md#1-initial-mint-front-run-inflation-attack
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

