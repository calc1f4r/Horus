---
# Core Classification
protocol: Holograph
chain: everychain
category: uncategorized
vulnerability_type: transferfrom_vs_safetransferfrom

# Attack Vector Details
attack_type: transferfrom_vs_safetransferfrom
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5595
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/456

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - transferfrom_vs_safetransferfrom
  - weird_erc20
  - safetransfer

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 21
finders:
  - d3e4
  - Trust
  - pashov
  - __141345__
  - martin
---

## Vulnerability Title

[M-02] `_payoutToken[s]()` is not compatible with tokens with missing return value

### Overview


This bug report is about the vulnerability in the code of the project 2022-10-holograph, which is hosted on GitHub. It has been determined that the code for the `PA1D._payoutToken()` and `PA1D._payoutTokens()` functions is causing a problem when attempting to transfer tokens to a list of payouts recipients. This is because some tokens do not return a boolean value, which causes the require-statement to revert despite a successful transfer. This means that the token payout is blocked and the tokens are stuck in the contract.

The bug was discovered through code inspection and the recommended mitigation step is to use OpenZeppelin's SafeERC20, which handles the return value check as well as non-standard-compliant tokens. This will ensure that the token payout is successful and the tokens are not stuck in the contract.

### Original Finding Content


[PA1D.sol#L317](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/src/enforcer/PA1D.sol#L317)<br>
[PA1D.sol#L340](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/src/enforcer/PA1D.sol#L340)<br>

Payout is blocked and tokens are stuck in contract.

### Proof of Concept

`PA1D._payoutToken()` and `PA1D._payoutTokens()` call `ERC20.transfer()` in a require-statement to send tokens to a list of payout recipients.<br>
Some tokens do not return a bool (e.g. USDT, BNB, OMG) on ERC20 methods. But since the require-statement expects a `bool`, for such a token a `void` return will also cause a revert, despite an otherwise successful transfer. That is, the token payout will always revert for such tokens.

### Recommended Mitigation Steps

Use [OpenZeppelin's SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol), which handles the return value check as well as non-standard-compliant tokens.

**[alexanderattar (Holograph) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/456#issuecomment-1306632476):**
 > Low priority, but can be updated to ensure compatibility with all ERC20 tokens.

**[alexanderattar (Holograph) linked a PR](https://github.com/code-423n4/2022-10-holograph-findings/issues/456#issuecomment-1306632476):**
 > [Feature/holo 612 royalty smart contract improvements](https://github.com/holographxyz/holograph-protocol/pull/93)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Holograph |
| Report Date | N/A |
| Finders | d3e4, Trust, pashov, __141345__, martin, cccz, Dinesh11G, Jeiwan, joestakey, vv7, brgltd, Lambda, Bnke0x0, RedOneN, 2997ms, chaduke, ballx, V_B |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/456
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`transferFrom vs safeTransferFrom, Weird ERC20, SafeTransfer`

