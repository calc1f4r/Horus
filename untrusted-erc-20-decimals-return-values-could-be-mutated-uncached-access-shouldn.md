---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6796
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Denis Milicevic
  - Gerard Persoon
---

## Vulnerability Title

Untrusted ERC-20 decimals() Return Values Could Be Mutated, Uncached Access Shouldn’t Be Considered Reliable

### Overview


This bug report is about the risk of using cached access when calling the decimals() function of Target.sol and Underlying.sol. It is possible for an attacker to mutate the variable returned by decimals() multiple times intra-transaction. This could lead to exploits due to the return value for decimals() being used for calculating balance transfers and other important logic. An example of an EvilToken contract is given to demonstrate this.

The recommendation is to pass logical preconditions when making external calls and store the result in internal contracts. This way, the value can be reused when the result is expected to be constant. The adapter should save any constants pertaining to Target and Underlying tokens, rather than doing an external call each time. 

It is important to show which adapters have been audited and are seen as safe. This way, users can know which adapters are secure to use.

### Original Finding Content

## Severity: High Risk

## Context:
- Space.sol#L133
- GClaimManager.sol#L59
- CAdapter.sol#L96
- CAdapter.sol#L109
- CAdapter.sol#L113-115
- Divider.sol#L426-427
- Periphery.sol#L70-71
- Periphery.sol#L546-548
- Divider.sol#L676

## Situation:
Numerous parts of the logic above perform repeated calls to the `decimals()` function of `Target.sol` and `Underlying.sol`. At times, these are used in various calculations.

An attacker is able to mutate the variable returned by `decimals()` multiple times intra-transaction if they so wished, when it comes to a permissionless or untrusted ERC-20 target or underlying. This could lead to exploits due to the return value for `decimals()` used for calculating balance transfers and other important logic.

Here is a proof of concept example of an `EvilToken` contract cast with Rari’s ERC-20 abstract, returning different `decimals()` results based on timestamp:

```solidity
import { ERC20 } from "contracts/ERC20.sol"; // Rari ERC20
contract EvilToken {
    function decimals() view public returns (uint8) {
        return uint8(block.timestamp % 18);
    }
}

contract Victim {
    function getTokensDecimals(address token) view public returns (uint8) {
        return ERC20(token).decimals();
    }
}
```

## Recommendation:
Any external calls should pass some logical pre-conditions. The result of those external calls should be stored in internal contracts and be re-used when the result is expected to be constant, as is the case with `decimals()`.

In this case, the external call to `decimals()` or other external "constants" should be consolidated in one call backed by preconditions. When these preconditions are met, the call should accept it, cache the value in its respective adapter, and have future dependent reads of this constant from that location, rather than from an external call to `decimals()`.

After they pass logical preconditions, the adapter should save any constants pertaining to `Target` and `Underlying` tokens, rather than doing an external call each time. The danger with external calls is that they could return a different result, bypass initial logical preconditions, and mutate the result to achieve an exploit.

## Sense:
We’ve decided to cache some values from adapters here & here, but for others (like target decimals), we’ve decided to leave them out under the assumption that a malicious actor can cause problems in many ways, and we can’t make strong guarantees about them without reviewing the code. The onus will be on us to clearly communicate which adapters have been audited and are seen as safe.

## Spearbit:
It is indeed important to show which adapters are audited.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sense |
| Report Date | N/A |
| Finders | Max Goodman, Denis Milicevic, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

