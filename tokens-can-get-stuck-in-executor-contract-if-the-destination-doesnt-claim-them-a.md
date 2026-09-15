---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7227
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - fund_lock

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

Tokens can get stuck in Executor contract if the destination doesn’t claim them all

### Overview


This bug report concerns a high-risk issue found in the Executor.sol file between lines 142 and 243. The function execute() increases allowance and then calls the recipient, but if the recipient does not use all the tokens, they can become stuck in the Executor contract. The issue was also discussed in the issue "Malicious call data can DOS execute or steal unclaimed tokens in the Executor contract".

The recommendation is to determine what should happen with the unclaimed tokens. There are three suggested solutions: sending the unclaimed tokens to the recovery address, setting the allowance to 0, or allowing the retrieval of unclaimed tokens from the executor contract by an owner. However, the Connext team acknowledges that as it requires some deliberate action to retrieve the tokens, in practice several tokens will stay behind in the executor.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
**Executor.sol#L142-L243**

## Description
The function `execute()` increases allowance and then calls the recipient (`_args.to`). When the recipient does not use all tokens, these could remain stuck inside the Executor contract. 

**Notes:**
- The executor can have excess tokens, see: kovan executor.
- See issue: "Malicious call data can DOS execute or steal unclaimed tokens in the Executor contract".

```solidity
function execute(...) ... {
    ...
    if (!isNative && hasValue) {
        SafeERC20.safeIncreaseAllowance(IERC20(_args.assetId), _args.to, _args.amount);
    }
    ...
    (success, returnData) = ExcessivelySafeCall.excessivelySafeCall(_args.to, ...);
    ...
}
```

## Recommendation
Determine what should happen with unclaimed tokens. Consider one or more of the following suggestions:
- Send the unclaimed tokens to the recovery address via `_sendToRecovery()` (although this further complicates the contract).
- Set the allowance to `0` (before `safeIncreaseAllowance()` or after the call to `excessivelySafeCall()`).
- Allow the retrieval of unclaimed tokens from the executor contract by an owner.

**Connext:** New policy: "any funds left in the Executor following a transfer are claimable by anyone". This forces implementers to think carefully about the calldata. Thus, leave the issues as is.

**Spearbit:** Acknowledged.

**Note:** As it requires some deliberate action to retrieve the tokens, in practice several tokens will stay behind in the executor.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Fund Lock`

