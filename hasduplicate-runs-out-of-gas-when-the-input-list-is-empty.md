---
# Core Classification
protocol: Set Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17304
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/setprotocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/setprotocol.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Robert Tonic | ​Trail of Bits Michael Colburn | ​Trail of Bits Gustavo Grieco | ​Trail of Bits JP Smith | ​Trail of Bits
---

## Vulnerability Title

​hasDuplicate runs out of gas when the input list is empty

### Overview


This bug report is about a data validation issue in the ExchangeExecution.sol file. The hasDuplicate function is intended to return true if a list of addresses contains duplicates and false otherwise. However, when called with an empty dynamic array, it triggers an unsigned integer underflow when calculating the loop bound, which can lead to a security or correctness issue.

To fix the issue in the short term, the implementation of hasDuplicate should be updated to return the correct value when the input list is empty. For the long term, the Set Protocol team should consider using the Echidna fuzzer or the Manticore symbolic executor to check the correctness of the hasDuplicate function.

### Original Finding Content

## Data Validation Report

**Type:** Data Validation  
**Target:** ExchangeExecution.sol  

**Difficulty:** High  

## Description  
The `hasDuplicate` function is incorrectly implemented. The `hasDuplicate` function, which determines if a list of addresses contains duplicates, is shown in Figure 1. Its documentation states that it returns true if it finds duplicates and false otherwise.

```solidity
/**
 * Returns whether or not there's a duplicate. Runs in O(n^2).
 * @param A Array to search
 * @return Returns true if duplicate, false otherwise
 */
function hasDuplicate(address[] memory A) internal pure returns (bool) {
    for (uint256 i = 0; i < A.length; i++) {
        for (uint256 j = i + 1; j < A.length; j++) {
            if (A[i] == A[j]) {
                return true;
            }
        }
    }
    return false;
}
```

**Figure 1:** The complete `hasDuplicate` function

However, this function has a flaw: if it is called using an empty dynamic array, it will trigger an unsigned integer underflow when calculating the loop bound (`A.length - 1`), causing it to run out of gas.

## Exploit Scenario  
The Set Protocol team uses the `hasDuplicate` function elsewhere in the system, introducing a potential security (e.g., denial of service) or correctness issue.

## Recommendation  
- **Short term:** Fix the implementation of `hasDuplicate` to return the correct value when the input list is empty.  
- **Long term:** Consider using the **Echidna** fuzzer or the **Manticore** symbolic executor to check the correctness of the `hasDuplicate` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Set Protocol |
| Report Date | N/A |
| Finders | Robert Tonic | ​Trail of Bits Michael Colburn | ​Trail of Bits Gustavo Grieco | ​Trail of Bits JP Smith | ​Trail of Bits |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/setprotocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/setprotocol.pdf

### Keywords for Search

`vulnerability`

