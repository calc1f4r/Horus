---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25443
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-frax
source_link: https://code4rena.com/reports/2022-09-frax
github_link: https://github.com/code-423n4/2022-09-frax-findings/issues/18

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-06] frxETHMinter: Non-conforming ERC20 tokens not recoverable

### Overview


This bug report is about a function called `recoverERC20` in a smart contract that is meant to rescue any ERC20 tokens that were accidentally sent to the contract. However, the bug is that there are tokens that do not return a value on success, which will cause the call to revert, even when the transfer would have been successful. This means that those tokens will be stuck forever and not be recoverable.

As an example, someone accidentally transferred USDT, one of the most commonly used ERC20 tokens, to the contract. Because USDT's transfer does not return a boolean, it will not be possible to recover those tokens and they will be stuck forever.

The recommended mitigation step is to use OpenZeppelin's `safeTransfer` to prevent this issue from happening. This bug report has been marked as a Medium risk because assets are not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.

### Original Finding Content

_Submitted by Lambda, also found by 0x1f8b, 0x5rings, 0xSky, 0xSmartContract, 8olidity, brgltd, Chom, CodingNameKiki, hansfriese, IllIllI, m9800, magu, pashov, pedroais, peritoflores, prasantgupta52, rokinot, Ruhum, seyni, and Sm4rty_

There is a function `recoverERC20` to rescue any ERC20 tokens that were accidentally sent to the contract. However, there are tokens that do not return a value on success, which will cause the call to revert, even when the transfer would have been successful. This means that those tokens will be stuck forever and not be recoverable.

### Proof Of Concept

Someone accidentally transfers USDT, one of the most commonly used ERC20 tokens, to the contract. Because USDT's transfer [does not return a boolean](https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7#code), it will not be possible to recover those tokens and they will be stuck forever.

### Recommended Mitigation Steps

Use OpenZeppelin's `safeTransfer`.

**[FortisFortuna (Frax) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/18#issuecomment-1257283698):**
 > Not really medium risk. Technically you could use safeTransfer, but if someone were to accidentally send something to this contract, it would most likely be either ETH, FRAX, frxETH, or sfrxETH, all of which are transfer compliant.

**[0xean (judge) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/18#issuecomment-1275309622):**
 > I think this qualifies as a Medium risk.  Sponsor has created functionality to recover ERC20 tokens.  Wardens have shown a path to which this functionality does not work correctly. 
> 
> > 2 — Med: Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-frax
- **GitHub**: https://github.com/code-423n4/2022-09-frax-findings/issues/18
- **Contest**: https://code4rena.com/reports/2022-09-frax

### Keywords for Search

`vulnerability`

