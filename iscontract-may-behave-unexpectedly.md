---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17900
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

isContract() may behave unexpectedly

### Overview

See description below for full details.

### Original Finding Content

## Type: Configuration  
## Target: CurveAMO_V3.sol  

## Difficulty: Medium

## Description  
The FRAX system relies on the `isContract()` function in `Address.sol` to check whether there is a contract at the target address. However, in Solidity, there is no general way to definitively determine that, as there are several edge cases in which the underlying function `extcodesize()` can return unexpected results. In addition, there is no way to guarantee that an address that is that of a contract (or one that is not) will remain that way in the future.

```solidity
function isContract(address account) internal view returns (bool) {
    // This method relies on extcodesize, which returns 0 for contracts in
    // construction, since the code is only stored at the end of the
    // constructor execution.
    uint256 size;
    // solhint-disable-next-line no-inline-assembly
    assembly { size := extcodesize(account) }
    return size > 0;
}
```
_Figure 20.1: FRAXStablecoin/Address.sol#L25-L34_

## Exploit Scenario  
A function, `f`, within the FRAX codebase calls `isContract()` internally to guarantee that a certain method is not callable by another contract. An attacker creates a contract that calls `f` from within its constructor, and the call to `isContract()` within `f` returns `false`, violating the “guarantee.”

## Recommendations  
**Short term:** Clearly document for developers that `isContract()` is not guaranteed to return an accurate value, and emphasize that it should never be used to provide an assurance of security.  

**Long term:** Be mindful of the fact that the Ethereum core developers consider it poor practice to attempt to differentiate between end users and contracts. Try to avoid this practice entirely if possible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

