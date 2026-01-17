---
# Core Classification
protocol: Caviar
chain: everychain
category: uncategorized
vulnerability_type: first_depositor_issue

# Attack Vector Details
attack_type: first_depositor_issue
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6098
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-caviar-contest
source_link: https://code4rena.com/reports/2022-12-caviar
github_link: https://github.com/code-423n4/2022-12-caviar-findings/issues/442

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - first_depositor_issue

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 43
finders:
  - 0x52
  - yixxas
  - ladboy233
  - koxuan
  - HE1M
---

## Vulnerability Title

[H-03] First depositor can break minting of shares

### Overview


This bug report describes a vulnerability in the code of the Pair.sol contract that allows an attacker to manipulate the total asset amount and cause users to not receive shares in exchange for their deposits. The vulnerability is caused by the lack of a condition in the addQuote() function that requires the number of LP tokens to be minted to be non-zero. 

The attack vector and impact is the same as TOB-YEARN-003, which is described in the audit report from July 19, 2021. In the addQuote() function, the amount of LP token minted is calculated as a fraction of existing reserves. An attacker can exploit this vulnerability by creating and adding a small amount of tokens to the pair, then transferring a large amount of tokens directly to the pair. This will cause the LP token to be worth a large amount, and users who add liquidity to the pool will receive 0 LP tokens because of rounding division.

The recommended mitigation steps are to send the first min liquidity LP tokens to the zero address when lpTokenSupply is 0, and to ensure the number of LP tokens to be minted is non-zero in the add() function.

### Original Finding Content


The attack vector and impact is the same as [TOB-YEARN-003](https://github.com/yearn/yearn-security/blob/master/audits/20210719\_ToB_yearn_vaultsv2/ToB\_-\_Yearn_Vault_v\_2\_Smart_Contracts_Audit_Report.pdf), where users may not receive shares in exchange for their deposits if the total asset amount has been manipulated through a large “donation”.

### Proof of Concept

In `Pair.add()`, the amount of LP token minted is calculated as

```solidity
function addQuote(uint256 baseTokenAmount, uint256 fractionalTokenAmount) public view returns (uint256) {
    uint256 lpTokenSupply = lpToken.totalSupply();
    if (lpTokenSupply > 0) {
        // calculate amount of lp tokens as a fraction of existing reserves
        uint256 baseTokenShare = (baseTokenAmount * lpTokenSupply) / baseTokenReserves();
        uint256 fractionalTokenShare = (fractionalTokenAmount * lpTokenSupply) / fractionalTokenReserves();
        return Math.min(baseTokenShare, fractionalTokenShare);
    } else {
        // if there is no liquidity then init
        return Math.sqrt(baseTokenAmount * fractionalTokenAmount);
    }
}
```

An attacker can exploit using these steps

1.  Create and add `1 wei baseToken - 1 wei quoteToken` to the pair. At this moment, attacker is minted `1 wei LP token` because `sqrt(1 * 1) = 1`
2.  Transfer large amount of `baseToken` and `quoteToken` directly to the pair, such as `1e9 baseToken - 1e9 quoteToken`. Since no new LP token is minted, `1 wei LP token` worths `1e9 baseToken - 1e9 quoteToken`.
3.  Normal users add liquidity to pool will receive `0` LP token if they add less than `1e9` token because of rounding division.

```solidity
baseTokenShare = (X * 1) / 1e9;
fractionalTokenShare = (Y * 1) / 1e9;
```

### Recommended Mitigation Steps

*   [Uniswap V2 solved this problem by sending the first 1000 LP tokens to the zero address](https://github.com/Uniswap/v2-core/blob/master/contracts/UniswapV2Pair.sol#L119-L124). The same can be done in this case i.e. when `lpTokenSupply == 0`, send the first min liquidity LP tokens to the zero address to enable share dilution.
*   In `add()`, ensure the number of LP tokens to be minted is non-zero:

```solidity
require(lpTokenAmount != 0, "No LP minted");
```

**[outdoteth (Caviar) confirmed and commented](https://github.com/code-423n4/2022-12-caviar-findings/issues/442#issuecomment-1373902458):**
 > Fixed in: https://github.com/outdoteth/caviar/pull/3



***
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Caviar |
| Report Date | N/A |
| Finders | 0x52, yixxas, ladboy233, koxuan, HE1M, Tointer, bytehat, supernova, carrotsmuggler, minhquanym, eyexploit, KingNFT, aviggiano, Franfran, fs0c, hihen, immeas, cccz, 0xDecorativePineapple, haku, Koolex, Tricko, hansfriese, chaduke, ak1, __141345__, UNCHAIN, lumoswiz, rvierdiiev, Apocalypto, cozzetti, SamGMK, Jeiwan, izhelyazkov, rjs, ElKu, BAHOZ, dipp, unforgiven, rajatbeladiya, seyni |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-caviar
- **GitHub**: https://github.com/code-423n4/2022-12-caviar-findings/issues/442
- **Contest**: https://code4rena.com/contests/2022-12-caviar-contest

### Keywords for Search

`First Depositor Issue`

