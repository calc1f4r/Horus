---
# Core Classification
protocol: Ondo RWA Internal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62321
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-May-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-May-2025.pdf
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - CarrotSmuggler
  - Anurag Jain
  - Desmond Ho
---

## Vulnerability Title

Missing onUSD refund on mints

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
GMTokenManager.sol#L196-L206

## Description
The `mintWithAttestation` allows paying with tokens other than `onUSD`. The issue is in that case, the user is charged the entire specified amount `depositTokenAmount` instead of the actual cost `mintOnusdValue`. 

When minting with other tokens, the user's funds are first passed into the `onUSDManager` contract, which mints temporary `onUSD` tokens for the purchase. Suppose the user is using some tokens that can have a volatile exchange rate with respect to `onUSD` tokens. In that case, they will need to specify a higher than necessary input amount to ensure their transaction goes through reliably.

These funds are then used to mint `onUSD` tokens, which are then burnt to mint the actual GM tokens. The price for the GM tokens is calculated in the `mintOnusdValue` variable. The contract only burns `mintOnusdValue` worth of `onUSD` tokens but does not pay out the remainder of the tokens. Therefore, if users specify `depositTokenAmount` to be higher than the required amount to account for the potential volatility of the payment token, they are charged the full amount even though they should only be charged `mintOnusdValue` amount.

## Proof of Concept
```diff
diff --git a/forge-tests/globalMarkets/tokenManager/GMTokenManagerPSMIntegrationTest.t.sol b/forge-tests/globalMarkets/tokenManager/GMTokenManagerPSMIntegrationTest.t.sol
index d480e39..2988795 100644
--- a/forge-tests/globalMarkets/tokenManager/GMTokenManagerPSMIntegrationTest.t.sol
+++ b/forge-tests/globalMarkets/tokenManager/GMTokenManagerPSMIntegrationTest.t.sol
@@ -251,9 +251,9 @@ contract onUSDManagerTest_ETH is OUSG_InstantManager_BasicDeployment {
bytes memory signature = _createAttestation(attesterPrivateKey, quote);
// Approve manager to spend user's onUSD
- deal(address(USDC), user, usdcDepositAmount);
+ deal(address(USDC), user, 2 * usdcDepositAmount);
vm.startPrank(user);
- USDC.approve(address(gmTokenManager), usdcDepositAmount);
+ USDC.approve(address(gmTokenManager), 2 * usdcDepositAmount);
// Token supply before subscription/burn
uint256 onUsdSupply = onusd.totalSupply();
@@ -262,7 +262,7 @@ contract onUSDManagerTest_ETH is OUSG_InstantManager_BasicDeployment {
quote,
signature,
address(USDC),
- usdcDepositAmount
+ 2 * usdcDepositAmount
);
vm.stopPrank();
Output tokens remain the same even though the input USDC amount doubles.
```

## Recommendation
As long as `onUSD` and the `depositToken` maintain their peg, only `mintOnusdValue` worth of tokens should be charged (for a 1:1 peg). For unpegged `depositToken`, consider refunding the unused amount of `onUSD` tokens.

```solidity
uint256 depositedOnusdValue = onUSDManager.subscribe(
    depositToken,
    depositTokenAmount,
    mintOnusdValue
);
uint256 refund = depositedOnusdValue - mintOnusdValue;
```

**Ondo Finance:** Fixed in PR 435.

**Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Ondo RWA Internal |
| Report Date | N/A |
| Finders | CarrotSmuggler, Anurag Jain, Desmond Ho |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-May-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-May-2025.pdf

### Keywords for Search

`vulnerability`

