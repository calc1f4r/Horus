---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7233
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
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
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

_handleExecuteLiquidity doesn’t consistently check for receiveLocalOverrides

### Overview


This bug report outlines a potential issue with the BridgeFacet.sol code. The function _handleExecuteLiquidity() initially checks for receiveLocal but does not check for receiveLocalOverrides. This could lead to a portal paying a bridge user in the adopted asset when they opted to override this behaviour. To avoid this, a check for receiveLocalOverrides should be added to the Aave portal eligibility check. The issue has been solved in PR 1644 and verified by Spearbit.

### Original Finding Content

## Security Risk Report

## Severity
**Medium Risk**

## Context
`BridgeFacet.sol#L571-L638`

## Description
The function `_handleExecuteLiquidity()` initially checks for `receiveLocal` but does not check for `receiveLocalOverrides`. Later on, it does check for both values.

```solidity
function _handleExecuteLiquidity(... ) ... {
    ...
    if (
        !_args.params.receiveLocal && // doesn't check for receiveLocalOverrides
        s.routerBalances[_args.routers[0]][_args.local] < toSwap &&
        s.aavePool != address(0)
    ) {
        ...
        if (_args.params.receiveLocal || s.receiveLocalOverrides[_transferId]) { // extra check
            return (toSwap, _args.local);
        }
    }
}
```

As a result, the portal may pay the bridge user in the adopted asset when they opted to override this behaviour to avoid slippage conditions outside of their boundaries, potentially leading to an unwarranted reception of funds denominated in the adopted asset.

## Recommendation
Consider adding a check for `receiveLocalOverrides` to the Aave portal eligibility check.

## Connext
Solved in PR 1644.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

