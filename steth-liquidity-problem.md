---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33849
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#1-steth-liquidity-problem
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

stETH liquidity problem

### Overview


The L2ERC20Bridge is not minting the corresponding amount of wstETH on L2, which can cause issues for users who have bridged wstETH and wrapped them to stETH. This can lead to insolvency problems and may require users to transfer stETH from L2 to L1, wrap it back to wstETH on L1, and then transfer it back to L2. To fix this, we recommend minting wstETH on L2, locking them on the stETH contract, and transferring stETH to users on L2.

### Original Finding Content

##### Description
L2ERC20Bridge mints stETH without minting a corresponding amount of wstETH on L2 https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/L2ERC20ExtendedTokensBridge.sol#L172. This can lead to insolvency issues, affecting users who have bridged wstETH on L2 and wrapped them to stETH. There is a chance (this can be forced by a malicious user without any losses) that the stETH contract on L2 might lack wstETH in its balance. This will require users who wrapped wstETH to stETH on L2 to:
- transfer stETH from L2 to L1;
- wrap stETH to wstETH on L1;
- transfer wstETH from L1 to L2.

##### Recommendation
We recommend minting wstETH on L2, locking them on the stETH contract, and subsequently transferring stETH to the user on L2.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#1-steth-liquidity-problem
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

