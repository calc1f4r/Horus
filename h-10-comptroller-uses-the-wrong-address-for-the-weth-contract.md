---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25221
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/46

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-10] Comptroller uses the wrong address for the WETH contract

### Overview


This bug report was submitted by Ruhum and also found by 0xf15ers, cccz, hake, Soosh, and WatchPug. It states that the Comptroller contract uses a hardcoded address for the WETH contract which is not the correct one. This means that users will not be able to claim their COMP rewards, resulting in a loss of funds. This was confirmed by tkkwon1998 (Canto) and Alex the Entreprenerd (judge) commented that the misconfiguration will guarantee that any function calling `grantCompInternal` as well as `claimComp` will revert. 

The proof of concept is provided with a link to the Comptroller’s `getWETHAddress()` function and it is used by the `grantCompInternal()` function which is called by the `claimComp()` function. If there is a contract stored in the hardcoded address and it doesn't adhere to the interface, the transaction will revert. If there is no contract, the call will succeed without having any effect.

The recommended mitigation step is to parse the WETH contract's address to the Comptroller through the constructor or another function instead of being hardcoded.

### Original Finding Content

_Submitted by Ruhum, also found by 0xf15ers, cccz, hake, Soosh, and WatchPug_

The Comptroller contract uses a hardcoded address for the WETH contract which is not the correct one. Because of that, it will be impossible to claim COMP rewards. That results in a loss of funds so I rate it as HIGH.

### Proof of Concept

The Comptroller's `getWETHAddress()` function: <https://github.com/Plex-Engineer/lending-market/blob/755424c1f9ab3f9f0408443e6606f94e4f08a990/contracts/Comptroller.sol#L1469>

It's a left-over from the original compound repo: <https://github.com/compound-finance/compound-protocol/blob/master/contracts/Comptroller.sol#L1469>

It's used by the `grantCompInternal()` function: <https://github.com/Plex-Engineer/lending-market/blob/755424c1f9ab3f9f0408443e6606f94e4f08a990/contracts/Comptroller.sol#L1377>

That function is called by `claimComp()`: <https://github.com/Plex-Engineer/lending-market/blob/755424c1f9ab3f9f0408443e6606f94e4f08a990/contracts/Comptroller.sol#L1365>

If there is a contract stored in that address and it doesn't adhere to the interface (doesn't have a `balanceOf()` and `transfer()` function), the transaction will revert. If there is no contract, the call will succeed without having any effect. In both cases, the user doesn't get their COMP rewards.

### Recommended Mitigation Steps

The WETH contract's address should be parsed to the Comptroller through the constructor or another function instead of being hardcoded.

**[tkkwon1998 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-findings/issues/46)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/46#issuecomment-1211353848):**
 > The warden has shown how the address for WETH / comp is hardcoded and the address is pointing to Mainnet's COMP.
> 
> This misconfiguration will guarantee that any function calling `grantCompInternal` as well as `claimComp` will revert.
> 
> Because the functionality is hampered, I agree with High Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/46
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

