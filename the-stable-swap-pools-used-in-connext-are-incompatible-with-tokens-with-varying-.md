---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7193
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
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
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Xiaoming90
  - Blockdev
  - Gerard Persoon
  - Sawmon and Natalie
  - Csanuragjain
---

## Vulnerability Title

The stable swap pools used in Connext are incompatible with tokens with varying decimals

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- `TokenFacet.sol#L164`
- `TokenFacet.sol#L399`
- `SwapAdminFacet.sol#L140`
- `SwapAdminFacet.sol#L143`
- `SwapAdminFacet.sol#L169`
- `StableSwap.sol#L100`
- `SwapUtilsExternal.sol#L407`
- `SwapUtils.sol#L370`

## Description
The stable swap functionality used in Connext calculates and stores for each token in a pool, the token's precision relative to the pool's precision. The token precision calculation uses the token's decimals. Since this precision is only set once, for a token that can have its decimals changed at a later time, the precision used might not always be accurate in the future. Thus, in the event of a token decimal change, the swap calculations involving this token would be inaccurate. 

For example in `_xp(...)`:

```solidity
function _xp(uint256[] memory balances, uint256[] memory precisionMultipliers)
    internal
    pure
    returns (uint256[] memory)
{
    uint256 numTokens = balances.length;
    require(numTokens == precisionMultipliers.length, "mismatch multipliers");
    uint256[] memory xp = new uint256[](numTokens);
    for (uint256 i; i < numTokens; ) {
        xp[i] = balances[i] * precisionMultipliers[i];
        unchecked {
            ++i;
        }
    }
    return xp;
}
```

We are multiplying in `xp[i] = balances[i] * precisionMultipliers[i]`, and cannot use division for tokens that have higher precision than the pool's default precision.

## Recommendation
Document the procedure of what tokens are allowed to be included in stable swap pools and what actions Connext would take when a decimal change happens. Leave a comment for users/devs whether only fixed decimal tokens are allowed or not in the protocol.

### Connext
The intention with the current construction is to manually update assets whose decimals change (by removing them and setting them up again). A comment was added for devs in PR 2453.

### Spearbit
This issue needs off-chain monitoring and enforcement. The Connext team would need to monitor all tokens used in the protocol for this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | Xiaoming90, Blockdev, Gerard Persoon, Sawmon and Natalie, Csanuragjain |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

