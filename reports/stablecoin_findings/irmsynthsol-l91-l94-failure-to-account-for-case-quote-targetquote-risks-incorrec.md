---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54148
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55
source_link: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
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
finders_count: 3
finders:
  - 0xSCSamurai
  - T1MOH
  - XDZIBECX
---

## Vulnerability Title

IRMSynth.sol - L91-L94: Failure to account for case quote == targetQuote risks incorrect in- terest rate calculations for synthetic tokens 

### Overview

See description below for full details.

### Original Finding Content

## Analysis of the _computeRate() Function Bug

## Context
(No context files were provided by the reviewer)

## Description
The `_computeRate()` function fails to accommodate the case when `quote == targetQuote`. Currently, it bundles this case together with `quote > targetQuote`, which could lead to incorrect rate calculations, as demonstrated by initial proof of concept tests.

Tests were run, differing mostly in a conditional statement: `else {` vs. `else if (quote > targetQuote) {`.

### Impact
- **High**: Incorrect interest rate calculations.
  
### Likelihood
- **Medium-high**: There is definitely not a low chance of reaching a scenario where `quote == targetQuote`.

### Issues Observed
- Incorrect interest rate calculations occur whenever `quote == targetQuote`.
- Passing the `if` check on line 97 (`rate < BASE_RATE`) is a more likely outcome due to a decrease in rate on line 93.
- Generally, the more regular outcome would be within the min and max range but still at a lower rate than it would have been without this bug.
- The bytecode size was smaller in tests using `else if (quote > targetQuote) {`, around 109 bytes of code smaller.
- Gas consumption was also lower in tests using `else if (quote > targetQuote) {`, consuming about 211 less gas.

## Proof of Concept
The buggy function under scrutiny:
```solidity
function _computeRate(IRMData memory irmCache) internal view returns (uint216 rate, bool updated) {
    updated = false;
    rate = irmCache.lastRate;
    rate = BASE_RATE * 2; /// @audit added for PoC/testing purposes
    // If not time to update yet, return the last rate
    // if (block.timestamp < irmCache.lastUpdated + ADJUST_INTERVAL) {
    // return (rate, updated);
    // }
    
    uint256 quote = oracle.getQuote(quoteAmount, synth, referenceAsset);
    quote = targetQuote; /// @audit added for PoC/testing purposes
    updated = true;
    
    if (quote < targetQuote) {
        // If the quote is less than the target, increase the rate
        rate = rate * ADJUST_FACTOR / ADJUST_ONE;
    } else { /// @audit-issue the bug
        //} else if (quote > targetQuote) { /// @audit added for PoC/testing purposes >>> bugfix line commented out for testing purposes
        // If the quote is greater than the target, decrease the rate
        rate = rate * ADJUST_ONE / ADJUST_FACTOR;
    }
    
    // Apply the min and max rates
    if (rate < BASE_RATE) {
        rate = BASE_RATE;
    } else if (rate > MAX_RATE) {
        rate = MAX_RATE;
    }
    return (rate, updated);
}
```

## Tests
- The first test result is with the bug, and the second test result is without the bug (i.e., the bug fix added and active).
- The lower bytecode count and lower gas consumption are secondary benefits after removing the bug.
- The primary benefit is correct interest rate calculations.

### Existing Protocol Tests
I used several existing tests, specifically demonstrating/proving the bug with the following modified test:
```solidity
function test_computeInterestRateView() public {
    oracle.setPrice(synth, REFERENCE_ASSET, irm.targetQuote() / 2);
    uint256 rate = irm.computeInterestRateView(address(0), 0, 0);
    irm.computeInterestRate(address(0), 0, 0);
    IRMSynth.IRMData memory irmData = irm.getIRMData();
    //assertEq(rate, irmData.lastRate);
    skip(irm.ADJUST_INTERVAL());
    rate = irm.computeInterestRateView(address(0), 0, 0);
    irmData = irm.getIRMData();
    //assertNotEq(rate, irmData.lastRate);
    irm.computeInterestRate(address(0), 0, 0);
    irmData = irm.getIRMData();
    //assertEq(rate, irmData.lastRate);
}
```

### Results of Tests
The results showed differences based on whether `else {` or `else if (quote > targetQuote) {` was used. Each combination revealed varying bytecode sizes and gas consumption, highlighting the importance of the fix.

### Differences in Results
- **Before Fix**: `IRMData({ lastUpdated: 3601, lastRate: 288079440971013007 [2.88e17] })`
- **After Fix**: `IRMData({ lastUpdated: 3601, lastRate: 316887385068114308 [3.168e17] })`

After fixing the bug, the rate is significantly higher, indicating that the function correctly calculates the rate with `else if`.

### Recommendations
To resolve the identified issue, it is recommended to adjust the conditional statement as follows:
```solidity
if (quote < targetQuote) {
    // If the quote is less than the target, increase the rate
    rate = rate * ADJUST_FACTOR / ADJUST_ONE;
} else if (quote > targetQuote) {
    // If the quote is greater than the target, decrease the rate
    rate = rate * ADJUST_ONE / ADJUST_FACTOR;
}
``` 

This adjustment ensures that cases when `quote == targetQuote` are not mishandled alongside other conditions, preventing incorrect calculations and optimizing performance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | 0xSCSamurai, T1MOH, XDZIBECX |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

