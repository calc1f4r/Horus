---
# Core Classification
protocol: Notional V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18573
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/59
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-notional-judging/issues/193

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
  - liquid_staking
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - iglyx
  - bin2chen
  - xiaoming90
  - chaduke
  - mstpr-brainbot
---

## Vulnerability Title

H-6: Excess funds withdrawn from the money market

### Overview


This bug report is about an issue where excessive amounts of assets are being withdrawn from the money market. The problem is found in the TokenHandler.sol file, line 270. If the current balance is 999,900 USDC and the withdraw amount external is 1,000,000 USDC, then there is insufficient balance in the contract, and additional funds need to be withdrawn from the money market. However, instead of withdrawing 100 USDC from the money market, Notional withdraws 1,000,000 USDC from the market as per the oracle.getRedemptionCalldata(withdrawAmountExternal) function. This leads to an excessive amount of assets idling in Notional and not generating any returns or interest in the money market, which leads to a loss of assets for the users as they would receive a lower interest rate than expected and incur opportunity loss. Attackers could potentially abuse this to pull the funds Notional invested in the money market leading to griefing and loss of returns/interest for the protocol. The recommended solution is to consider withdrawing only the shortfall amount from the money market.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-notional-judging/issues/193 

## Found by 
bin2chen, chaduke, iglyx, mstpr-brainbot, xiaoming90
## Summary

Excessive amounts of assets are being withdrawn from the money market.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/internal/balances/TokenHandler.sol#L270

```solidity
File: TokenHandler.sol
256:     function _redeemMoneyMarketIfRequired(
257:         uint16 currencyId,
258:         Token memory underlying,
259:         uint256 withdrawAmountExternal
260:     ) private {
261:         // If there is sufficient balance of the underlying to withdraw from the contract
262:         // immediately, just return.
263:         mapping(address => uint256) storage store = LibStorage.getStoredTokenBalances();
264:         uint256 currentBalance = store[underlying.tokenAddress];
265:         if (withdrawAmountExternal <= currentBalance) return;
266: 
267:         IPrimeCashHoldingsOracle oracle = PrimeCashExchangeRate.getPrimeCashHoldingsOracle(currencyId);
268:         // Redemption data returns an array of contract calls to make from the Notional proxy (which
269:         // is holding all of the money market tokens).
270:         (RedeemData[] memory data) = oracle.getRedemptionCalldata(withdrawAmountExternal);
271: 
272:         // This is the total expected underlying that we should redeem after all redemption calls
273:         // are executed.
274:         uint256 totalUnderlyingRedeemed = executeMoneyMarketRedemptions(underlying, data);
275: 
276:         // Ensure that we have sufficient funds before we exit
277:         require(withdrawAmountExternal <= currentBalance.add(totalUnderlyingRedeemed)); // dev: insufficient redeem
278:     }
```

If the `currentBalance` is `999,900` USDC and the `withdrawAmountExternal` is `1,000,000` USDC, then there is insufficient balance in the contract, and additional funds need to be withdrawn from the money market (e.g. Compound).

Since the contract already has `999,900` USDC, only an additional `100` USDC needs to be withdrawn from the money market to fulfill the withdrawal request of `1,000,000` USDC

However, instead of withdrawing `100` USDC from the money market, Notional withdraw `1,000,000` USDC from the market as per the `oracle.getRedemptionCalldata(withdrawAmountExternal)` function. As a result, an excess of `990,000` USDC is being withdrawn from the money market

## Impact

This led to an excessive amount of assets idling in Notional and not generating any returns or interest in the money market, which led to a loss of assets for the users as they would receive a lower interest rate than expected and incur opportunity loss. 

Attackers could potentially abuse this to pull the funds Notional invested in the money market leading to griefing and loss of returns/interest for the protocol.

## Code Snippet

https://github.com/sherlock-audit/2023-03-notional/blob/main/contracts-v2/contracts/internal/balances/TokenHandler.sol#L270

## Tool used

Manual Review

## Recommendation

Consider withdrawing only the shortfall amount from the money market.

```diff
- (RedeemData[] memory data) = oracle.getRedemptionCalldata(withdrawAmountExternal);
+ (RedeemData[] memory data) = oracle.getRedemptionCalldata(withdrawAmountExternal - currentBalance);
```



## Discussion

**jeffywu**

Valid Issue

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional V3 |
| Report Date | N/A |
| Finders | iglyx, bin2chen, xiaoming90, chaduke, mstpr-brainbot |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-notional-judging/issues/193
- **Contest**: https://app.sherlock.xyz/audits/contests/59

### Keywords for Search

`vulnerability`

