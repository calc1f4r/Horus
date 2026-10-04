---
# Core Classification
protocol: Art Gobblers
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25419
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-artgobblers
source_link: https://code4rena.com/reports/2022-09-artgobblers
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[18]  Duplicated `require()`/`revert()` checks should be refactored to a modifier or function

### Overview

See description below for full details.

### Original Finding Content

The compiler will inline the function, which will avoid `JUMP` instructions usually associated with functions

*There are 2 instances of this issue:*
```solidity
File: src/ArtGobblers.sol

705:          if (gobblerId < FIRST_LEGENDARY_GOBBLER_ID) revert("NOT_MINTED");

```
https://github.com/code-423n4/2022-09-artgobblers/blob/d2087c5a8a6a4f1b9784520e7fe75afa3a9cbdbe/src/ArtGobblers.sol#L705

```solidity
File: lib/solmate/src/tokens/ERC721.sol

158:          require(to != address(0), "INVALID_RECIPIENT");

```
https://github.com/transmissions11/solmate/blob/26572802743101f160f2d07556edfc162896115e/src/tokens/ERC721.sol#L158

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-09-artgobblers-findings/issues/323#issuecomment-1278336100):**
 > **[01] Don't roll your own crypto**<br>
 > `Refactoring` for this specific case as I'm not convinced the entropy to be misused. Recommend following up with sponsor if you find further info.
>
 > **[02] Chainlink's VRF V1 is deprecated**<br>
 > `Refactoring`, as system enables swapping.
>
 > **[03] Rinkeby is not supported for Chainlink's VRF**<br>
 > `Refactoring`, nice find
>
 > **[04] Missing checks for address(0x0) when assigning values to address state variables**<br>
 > `Low`
>
 > **[05] requestId is always zero**<br>
 > `Non-critical`
>
 > **[06] Don't use periods with fragments**<br>
 > I don't have an opinion about this one
>
 > **[07] Contract implements interface without extending the interface**<br>
 > `Refactoring`
>
 > **[08] public functions not called by the contract should be declared external instead**<br>
 > `Refactoring`
> 
 > **[09] constants should be defined rather than using magic numbers**<br>
 > `Refactoring`
>
 > **[10] Use a more recent version of solidity**<br>
 > `Refactoring`
>
 > **[12] Constant redefined elsewhere**<br>	
 > This one looks off as those are immutable and not known until deploy time.
>
 > **[13] Variable names that consist of all capital letters should be reserved for constant/immutable variables**<br>
 > `Refactoring`
>
 > **[14] File is missing NatSpec**<br>
 > `Non-Critical`
>
 > **[15] NatSpec is incomplete**<br>
 > `Non-Critical`
>
 > **[16]	Event is missing indexed fields**<br>
 > I still don't get why you'd index "gibberish" values if it doesn't even save gas.
>
 > **[17]	Not using the named return variables anywhere in the function is confusing**<br>
 > `Refactoring`
>
 > **[18]	Duplicated require()/revert() checks should be refactored to a modifier or function**<br>
 > `Refactoring`
>
 > Overall, pretty good report with some interesting ideas. Of the automated ones, definitely the best.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Art Gobblers |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-artgobblers
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-09-artgobblers

### Keywords for Search

`vulnerability`

