---
# Core Classification
protocol: Cally
chain: everychain
category: uncategorized
vulnerability_type: transferfrom_vs_safetransferfrom

# Attack Vector Details
attack_type: transferfrom_vs_safetransferfrom
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2298
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-cally-contest
source_link: https://code4rena.com/reports/2022-05-cally
github_link: https://github.com/code-423n4/2022-05-cally-findings/issues/38

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
  - transferfrom_vs_safetransferfrom
  - erc721

protocol_categories:
  - dexes
  - services
  - synthetics
  - liquidity_manager
  - options_vault

# Audit Details
report_date: unknown
finders_count: 22
finders:
  - berndartmueller
  - FSchmoede
  - catchup
  - MiloTruck
  - minhquanym
---

## Vulnerability Title

[M-09] Use safeTransferFrom instead of transferFrom for ERC721 transfers

### Overview


This bug report is about the use of `transferFrom()` instead of `safeTransferFrom()` in the Cally.sol contract. The `transferFrom()` method is used to save gas, however this is not recommended because OpenZeppelin’s documentation discourages its use and some NFTs have logic in the `onERC721Received()` function which is only triggered in the `safeTransferFrom()` function and not in `transferFrom()`. To mitigate this issue, it is recommended to call the `safeTransferFrom()` method instead of `transferFrom()` for NFT transfers. The `CallyNft` contract should also inherit the `ERC721TokenReceiver` contract.

### Original Finding Content

_Submitted by hickuphh3, also found by antonttc, berndartmueller, catchup, cccz, dipp, FSchmoede, GimelSec, hake, jah, jayjonah8, joestakey, kebabsec, Kenshin, Kumpa, MiloTruck, minhquanym, peritoflores, rfa, shenwilly, WatchPug, and ynnad_

<https://github.com/code-423n4/2022-05-cally/blob/1849f9ee12434038aa80753266ce6a2f2b082c59/contracts/src/Cally.sol#L199>

<https://github.com/code-423n4/2022-05-cally/blob/1849f9ee12434038aa80753266ce6a2f2b082c59/contracts/src/Cally.sol#L295>

<https://github.com/code-423n4/2022-05-cally/blob/1849f9ee12434038aa80753266ce6a2f2b082c59/contracts/src/Cally.sol#L344>

### Details & Impact

The `transferFrom()` method is used instead of `safeTransferFrom()`, presumably to save gas. I however argue that this isn’t recommended because:

*   [OpenZeppelin’s documentation](https://docs.openzeppelin.com/contracts/4.x/api/token/erc721#IERC721-transferFrom-address-address-uint256-) discourages the use of `transferFrom()`, use `safeTransferFrom()` whenever possible
*   Given that any NFT can be used for the call option, there are a few NFTs (here’s an [example](https://github.com/sz-piotr/eth-card-game/blob/master/src/ethereum/contracts/ERC721Market.sol#L20-L31)) that have logic in the `onERC721Received()` function, which is only triggered in the `safeTransferFrom()` function and not in `transferFrom()`

### Recommended Mitigation Steps

Call the `safeTransferFrom()` method instead of `transferFrom()` for NFT transfers. Note that the `CallyNft` contract should inherit the `ERC721TokenReceiver` contract as a consequence.

```solidity
abstract contract CallyNft is ERC721("Cally", "CALL"), ERC721TokenReceiver {...}
```

**[outdoteth (Cally) confirmed and resolved](https://github.com/code-423n4/2022-05-cally-findings/issues/38#issuecomment-1128776476):**
 > the fix for this issue is here; https://github.com/outdoteth/cally/pull/4



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Cally |
| Report Date | N/A |
| Finders | berndartmueller, FSchmoede, catchup, MiloTruck, minhquanym, joestakey, jah, peritoflores, Kenshin, ynnad, cccz, hickuphh3, WatchPug, kebabsec, Kumpa, hake, rfa, shenwilly, antonttc, jayjonah8, dipp, GimelSec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-cally
- **GitHub**: https://github.com/code-423n4/2022-05-cally-findings/issues/38
- **Contest**: https://code4rena.com/contests/2022-05-cally-contest

### Keywords for Search

`transferFrom vs safeTransferFrom, ERC721`

