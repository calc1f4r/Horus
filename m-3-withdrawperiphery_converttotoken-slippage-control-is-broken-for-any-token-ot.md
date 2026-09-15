---
# Core Classification
protocol: Rage Trade
chain: everychain
category: uncategorized
vulnerability_type: usdc

# Attack Vector Details
attack_type: usdc
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3515
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/16
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-rage-trade-judging/issues/55

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - usdc
  - decimals

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-3: WithdrawPeriphery#_convertToToken slippage control is broken for any token other than USDC

### Overview


This bug report is about an issue found in WithdrawPeriphery, a contract that allows users to redeem junior share vaults to any token available on GMX. A fixed percentage slippage is applied to prevent users from losing large amounts of value to MEV, but this slippage calculation always returns the number of tokens to 6 decimals regardless of the token being requested. This works for tokens with 6 decimals like USDC, but is ineffective for tokens with more than 6 decimals. This means users withdrawing tokens other than USDC can suffer huge loss of funds due to virtually no slippage protection.

The recommended solution is to adjust minTokenOut to match the decimals of the token, by adding a line of code to the existing code snippet. The severity level of this issue was discussed and ultimately downgraded from high to medium, since loss of funds is not possible due to chainlink oracles being used for pricing the tokens.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-rage-trade-judging/issues/55 

## Found by 
0x52

## Summary

WithdrawPeriphery allows the user to redeem junior share vaults to any token available on GMX, applying a fixed slippage threshold to all redeems. The slippage calculation always returns the number of tokens to 6 decimals. This works fine for USDC but for other tokens like WETH or WBTC that are 18 decimals the slippage protection is completely ineffective and can lead to loss of funds for users that are withdrawing.

## Vulnerability Detail

    function _convertToToken(address token, address receiver) internal returns (uint256 amountOut) {
        // this value should be whatever glp is received by calling withdraw/redeem to junior vault
        uint256 outputGlp = fsGlp.balanceOf(address(this));

        // using min price of glp because giving in glp
        uint256 glpPrice = _getGlpPrice(false);

        // using max price of token because taking token out of gmx
        uint256 tokenPrice = gmxVault.getMaxPrice(token);

        // apply slippage threshold on top of estimated output amount
        uint256 minTokenOut = outputGlp.mulDiv(glpPrice * (MAX_BPS - slippageThreshold), tokenPrice * MAX_BPS);

        // will revert if atleast minTokenOut is not received
        amountOut = rewardRouter.unstakeAndRedeemGlp(address(token), outputGlp, minTokenOut, receiver);
    }

WithdrawPeriphery allows the user to redeem junior share vaults to any token available on GMX. To prevent users from losing large amounts of value to MEV the contract applies a fixed percentage slippage. minToken out is returned to 6 decimals regardless of the token being requested. This works for tokens with 6 decimals like USDC, but is completely ineffective for the majority of tokens that aren't.  

## Impact

Users withdrawing tokens other than USDC can suffer huge loss of funds due to virtually no slippage protection

## Code Snippet

https://github.com/sherlock-audit/2022-10-rage-trade/blob/main/dn-gmx-vaults/contracts/periphery/WithdrawPeriphery.sol#L147-L161

## Tool used

Manual Review

## Recommendation

Adjust minTokenOut to match the decimals of the token:

        uint256 minTokenOut = outputGlp.mulDiv(glpPrice * (MAX_BPS - slippageThreshold), tokenPrice * MAX_BPS);
    +   minTokenOut = minTokenOut * 10 ** (token.decimals() - 6);

## Discussion

**0xDosa**

Agreed on the issue but the severity level should be medium since loss of funds is not possible. While swapping on GMX, there is min-max spread and fees but no slippage due to them using chainlink oracles for pricing the tokens, so a direct sandwich attack would not work.

**Evert0x**

Downgrading to medium

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Rage Trade |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-rage-trade-judging/issues/55
- **Contest**: https://app.sherlock.xyz/audits/contests/16

### Keywords for Search

`USDC, Decimals`

