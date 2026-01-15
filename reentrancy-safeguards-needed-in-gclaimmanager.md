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
solodit_id: 6806
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

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

Reentrancy Safeguards Needed In GClaimManager

### Overview


This bug report discusses a potential reentrancy vulnerability in the exit() function of the GClaimManager.sol smart contract. The problem lies in the fact that the token burning is done at the end of the function, after multiple external calls have already been made. This means that a malicious adapter contract could potentially reenter the function and cause unexpected behavior.

To address this issue, the report recommends adding a nonReentrant modifier to any functions in the GClaimManager.sol smart contract that make external calls. Although the GClaimManager will likely be deprecated in the future, this issue is included for completeness.

### Original Finding Content

## Security Vulnerability Report

## Severity
**Medium Risk**

## Context
**File**: GClaimManager.sol  
**Lines**: 77-104

## Situation
In the function `exit()` of `GClaimManager.sol`, the burning of the tokens is done at the end. This does not conform to the Checks-Effects-Interactions pattern, and no non-Reentrant modifier is employed. Therefore, reentrancy is possible with a malicious adapter contract, and there are potential risks in other situations as well.

Here is an excerpt of the relevant code:

```solidity
function exit(address adapter, uint48 maturity, uint256 uBal) external {
    // External call
    uint256 collected = Claim(claim).collect();
    
    // External call
    uint256 tBal = uBal.fdiv(gclaims[claim].totalSupply(), total);
    
    // External call
    ERC20(Adapter(adapter).target()).safeTransfer(msg.sender, tBal);
    
    // External call
    ERC20(claim).safeTransfer(msg.sender, uBal);
    
    // Burn the user's gclaims
    // Completed at the very end with potential reentrancy above
    gclaims[claim].burn(msg.sender, uBal);
}
```

## Recommendation
To improve security, add a `nonReentrant` modifier on functions of `GClaimManager` that perform external calls.

## Note
`GClaimManager` will most likely be deprecated. This issue is included for completeness.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

