---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8746
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/205

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-09] `GolomToken.sol` doesn't contain a function to mint treasury tokens

### Overview


A bug has been found in the GolomToken.sol code which may lead to potential downtime in GolomTrader. This is because GolomTrader.sol calls RewardDistributor.sol#addFees each time there is a filled order. When the epoch changes, RewardDistributor.sol will try to call the mint function in GolomToken.sol. However, because of the 24 hour timelock, there will be at least a 24 hours period where RewardDistributor.sol is not the minter and doesn't have the permission to mint. This means that during that period all trades will revert. To mitigate this, a function should be added to GolomToken.sol to mint the treasury tokens similar to the mintAirdrop() and mintGenesisReward() functions.

### Original Finding Content


[GolomToken.sol#L14-L73](https://github.com/code-423n4/2022-07-golom/blob/7bbb55fca61e6bae29e57133c1e45806cbb17aa4/contracts/governance/GolomToken.sol#L14-L73)<br>

Potential downtime in GolomTrader

### Proof of Concept

GolomToken.sol doesn't have a function to mint the treasury tokens as specified in the docs (<https://docs.golom.io/tokenomics-and-airdrop>). In order for these tokens to be minted, the minter would have to be changed via `setMinter()` and `executeSetMinter()` to a contract that can mint the treasury tokens. Because of the 24 hour timelock, this would lead to downtime for GolomTrader.sol if trading has already begun. This is because GolomTrader.sol calls `RewardDistributor.sol#addFees` each time there is a filled order. When the epoch changes, RewardDistributor.sol will try to call the mint function in GolomToken.sol. Because of the timelock, there will be at least a 24 hours period where RewardDistributor.sol is not the minter and doesn't have the permission to mint. This means that during that period all trades will revert.

### Recommended Mitigation Steps

Add a function to GolomToken.sol to mint the treasury tokens similar to the `mintAirdrop()` and `mintGenesisReward()` functions.

**[0xsaruman (Golom) confirmed, but disagreed with severity](https://github.com/code-423n4/2022-07-golom-findings/issues/205)**

**[0xsaruman (Golom) resolved and commented](https://github.com/code-423n4/2022-07-golom-findings/issues/205#issuecomment-1236300333):**
 > https://github.com/golom-protocol/contracts/commit/746507ea6f71a017be178f7eeb66d2dbf92a4524



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/205
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

