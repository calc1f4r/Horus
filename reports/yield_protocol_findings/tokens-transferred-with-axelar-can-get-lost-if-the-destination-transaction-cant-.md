---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7037
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
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
  - fund_lock

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

Tokens transferred with Axelar can get lost if the destination transaction can’t be executed

### Overview


This bug report is concerning a contract called Executor, which is a part of a larger system. It is considered a high-risk bug because of the potential to lose tokens. The problem is that if the function _executeWithToken fails, there is no way to return the tokens or send them elsewhere. This means that the tokens would be lost if the call cannot be made to work.

The recommendation is to consider sending the tokens to a recovery address in case the transaction fails. For comparison, the Connext Executor has logic to do this. This bug has been fixed with a pull request (#44) and verified by Spearbit.

### Original Finding Content

## Security Report

## Severity
**High Risk**

## Context
`Executor.sol#L293-L316`

## Description
If `executeWithToken()` reverts, then the transaction can be retried, possibly with additional gas.  
See Axelar recovery. However, there is no option to return the tokens or send them elsewhere. This means that tokens would be lost if the call cannot be made to work.

```solidity
contract Executor is IAxelarExecutable, Ownable, ReentrancyGuard, ILiFi {
    function _executeWithToken(...) ... {
        ...
        (bool success, ) = callTo.call(callData);
        if (!success) revert ExecutionFailed();
    }
}
```

## Recommendation
Consider sending the tokens to a recovery address in case the transaction fails.  
For comparison: The Connext executor has logic to do this.

## Status
**LiFi:** Fixed with PR #44  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`Fund Lock`

