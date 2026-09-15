---
# Core Classification
protocol: LI.FI
chain: everychain
category: logic
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7051
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
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
  - fund_lock
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jonah1005
  - DefSec
  - Gerard Persoon
---

## Vulnerability Title

What if the receiver of Axelar _executeWithToken() doesn’t claim all tokens

### Overview


The bug report is about a function in a contract called Executor.sol. The function, _executeWithToken(), approves tokens and then calls a function called callTo. If that contract doesn't retrieve the tokens, then the tokens stay within the Executor and are lost. This is considered a medium risk bug. 

The recommendation for this bug is to consider sending the remaining tokens to a recovery address and to document the token handling in AxelarFacet.md. The LiFi bug has been fixed with PR #62 and the Spearbit bug has been verified.

### Original Finding Content

## Security Assessment Report

## Severity
**Medium Risk**

## Context
`Executor.sol#L293-L316`

## Description
The function `_executeWithToken()` approves tokens and then calls `callTo`. If that contract doesn’t retrieve the tokens, then the tokens stay within the Executor and are lost. 

Also see: "Remaining tokens can be swept from the LiFi Diamond or the Executor."

```solidity
contract Executor is IAxelarExecutable, Ownable, ReentrancyGuard, ILiFi {
    function _executeWithToken(...) ... {
        ...
        // transfer received tokens to the recipient
        IERC20(tokenAddress).approve(callTo, amount);
        (bool success, ) = callTo.call(callData);
        ...
    }
}
```

## Recommendation
Consider sending the remaining tokens to a recovery address. Document the token handling in `AxelarFacet.md`.

## References
- **LiFi**: Fixed with PR #62.
- **Spearbit**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf

### Keywords for Search

`Fund Lock, Business Logic`

