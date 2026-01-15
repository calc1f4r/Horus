---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53769
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/tracer/tracer-3/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/tracer/tracer-3/review.pdf
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
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Miscellaneous Tracer Perpetual Pools V2General Comments

### Overview

See description below for full details.

### Original Finding Content

## Description

This section details miscellaneous findings in the contracts repository discovered by the testing team that do not have direct security implications:

1. **LeveragedPool.sol**
   - **Stale Code**  
     On line [336], there is commented-out code that is not used; this should be removed.
   - **Similar Variable Names**  
     In the function `feeTransfer()` on line [334], there is a local variable called `secondaryFee` and also a global variable called `secondaryFees`. It is recommended to change the name of the local variable so that it is more than one character different from the global variable to avoid confusion and the risk of typos altering the output of code.

2. **PoolCommitter.sol**
   - **Differing Limits for mintingFee**  
     The use of constant `MAX_MINTING_FEE` to act as a bound for `mintingFee` is inconsistent. In function `updateMintingFee()`, we can set `mintingFee == PoolSwapLibrary.MAX_MINTING_FEE`. However, in function `setMintingFee()`, this value is not allowed as line [881] states `mintingFee < PoolSwapLibrary.MAX_MINTING_FEE`. The choice of `mintingFee` upper boundary should be made consistent.
   - **Missing Event**  
     On line [852], the function `setPool()` states it emits an event on success when it does not emit any events. The missing `SettlementAndPoolChanged` event should be added, or if it is not needed, then the comment on line [852] should be removed.
   - **Misleading Comments**  
     Line [628] states "Prevent underflow by setting mintingFee to lowest possible value (0)" however `mintingFee` is an IEEE 754 number and so supports negative numbers, meaning 0 is not its lowest possible value. The comment should be changed to something like "Prevent underflow by setting mintingFee to lowest acceptable value (0)."

3. **InvariantCheck.sol**
   - **Event Always Emitted**  
     On line [45], the event `InvariantsHold` is emitted regardless of the outcome. This means that if the `if` clause on line [41] has triggered, then the event `InvariantsFail` will be emitted, immediately followed by the `InvariantsHold` event. This could confuse any off-chain bots or alert systems. This can be solved by adding a `break` command on line [44] inside the `if` clause.

4. **SMAOracle.sol**
   - **Additional Notation Needed**  
     On line [72], we have the variable `updateInterval`; this duration should have a comment outlining the expected time units it should be supplied in.

5. **PoolSwapLibrary.sol**
   - **Equation Clarity**  
     On line [302], use brackets for clarity on the intended order of operation.
   - **Incorrect Comments**  
     The comment on line [426] should read "settlement tokens to return" as no settlement tokens are being burnt.
   - **Incomplete Zero Checks**  
     Functions `getMint()` and `getBurn()` both contain a zero price check on line [433] and line [447] respectively. However, as they are checking IEEE 754 standard numbers, they should also check for negative zero.

6. **PoolFactory.sol**
   - **Constant Name**  
     Constant `DAYS_PER_LEAP_YEAR` on line [42] has a misleading name, as it actually records the number of seconds in a leap year.

7. **KeeperRewards.sol**
   - **Unclear Comments**  
     The comment on line [107] is unclear; the `_keeperGas` variable is actually denoted in the settlement token quantity, not wei, which suggests it is an ETH quantity. The number format is already made clear by the "WAD formatted" comment. Changing the comment to "keeper gas cost in settlement tokens." would make its meaning clearer.
   - **Additional Comment Required**  
     Adding a comment to line [54] that the price returned by the oracle must always match the 18d.p. style of Chainlink ETH/Token oracles will help prevent future mistakes should a different external oracle be chosen.

8. **AutoClaim.sol**
   - **Typo**  
     On line [182], "where the all supplied" should be "where all the supplied."

9. **CalldataLogic.sol**
   - **Typo**  
     On line [10], "bite array" should be "byte array."
   - **Specify Intent**  
     On lines [63-66], the use of inline assembly could be improved by clarifying the aims of this code to help catch errors. There should be a comment documenting that due to line [63], the outputted amount is implicitly capped by `uint128.max` even though it is a `uint256`.

10. **vendors/ERC20_Cloneable.sol**
    - **Missing Zero Address Check**  
      The function `transferOwnership()` contains a zero address check for setting `owner`, however the `initialize()` function is lacking one when `owner` is initially set.
    - **Missing Event**  
      The function `transferOwnership()` has no event to record a transfer of ownership. This could help off-chain bots detect and monitor ownership of the pool tokens.
    - **Missing Visibility**  
      The visibility of `_decimals` on line [34] is not explicitly set; this should be stated for clarity.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/tracer/tracer-3/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/tracer/tracer-3/review.pdf

### Keywords for Search

`vulnerability`

