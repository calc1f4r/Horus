---
# Core Classification
protocol: Buffer Finance
chain: everychain
category: reentrancy
vulnerability_type: reentrancy

# Attack Vector Details
attack_type: reentrancy
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3628
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/24
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/112

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 5

# Context Tags
tags:
  - reentrancy
  - erc777
  - cei

protocol_categories:
  - dexes
  - yield
  - services
  - yield_aggregator
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

M-2: When tokenX is an ERC777 token, users can bypass maxLiquidity

### Overview


This bug report is about an issue found in the BufferBinaryPool._provide function when tokenX is an ERC777 token. It was found by cccz and the vulnerability detail is that when the user calls provide again in tokensToSend, since BufferBinaryPool has not received tokens at this time, totalTokenXBalance() has not increased, and the checks can be bypassed, so that users can provide liquidity exceeding maxLiquidity. The impact of this is that users can provide liquidity exceeding maxLiquidity. The tool used was Manual Review and the recommendation is to change the code snippet to the one provided. Lastly, it was discussed that neither tokenX (USDC or BFR) are ERC777, so not applicable to current contracts.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/112 

## Found by 
cccz

## Summary
When tokenX is an ERC777 token, users can use callbacks to provide liquidity exceeding maxLiquidity
## Vulnerability Detail
In BufferBinaryPool._provide, when tokenX is an ERC777 token, the tokensToSend function of account will be called in tokenX.transferFrom before sending tokens. When the user calls provide again in tokensToSend, since BufferBinaryPool has not received tokens at this time, totalTokenXBalance() has not increased, and the following checks can be bypassed, so that users can provide liquidity exceeding maxLiquidity.
```solidity
         require(
             balance + tokenXAmount <= maxLiquidity,
             "Pool has already reached it's max limit"
         );
```
## Impact
users can provide liquidity exceeding maxLiquidity.

## Code Snippet
https://github.com/sherlock-audit/2022-11-buffer/blob/main/contracts/contracts/core/BufferBinaryPool.sol#L216-L240
## Tool used

Manual Review

## Recommendation
Change to
```diff
    function _provide(
        uint256 tokenXAmount,
        uint256 minMint,
        address account
    ) internal returns (uint256 mint) {
+        bool success = tokenX.transferFrom(
+            account,
+            address(this),
+            tokenXAmount
+        );
        uint256 supply = totalSupply();
        uint256 balance = totalTokenXBalance();

        require(
            balance + tokenXAmount <= maxLiquidity,
            "Pool has already reached it's max limit"
        );

        if (supply > 0 && balance > 0)
            mint = (tokenXAmount * supply) / (balance);
        else mint = tokenXAmount * INITIAL_RATE;

        require(mint >= minMint, "Pool: Mint limit is too large");
        require(mint > 0, "Pool: Amount is too small");

-        bool success = tokenX.transferFrom(
-            account,
-            address(this),
-            tokenXAmount
-        );
```

## Discussion

**0x00052**

Neither tokenX (USDC or BFR) are ERC777, so not applicable to current contracts. Something to consider if the team plans to add and ERC777

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Buffer Finance |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/112
- **Contest**: https://app.sherlock.xyz/audits/contests/24

### Keywords for Search

`Reentrancy, ERC777, CEI`

