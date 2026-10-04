---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7223
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
rarity_score: 3

# Context Tags
tags:
  - validation
  - external_call

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

Add checks to xcall()

### Overview


A bug report has been filed regarding the function xcall() in the BridgeFacet.sol and Executor.sol smart contracts. The bug has been classified as high risk. It is noted that the function does some sanity checks, but more should be added to prevent issues later on. The primary issue is that if the parameters recovery and agent are set to 0, then funds can be sent to the 0 address or locked forever respectively. Additionally, if the destination domain is set to s.domain, and the slippageTol is set to a value greater than s.LIQUIDITY_FEE_DENOMINATOR, then funds can be locked as xcall() will allow for the user to provide the local asset, avoiding any swap.

The recommendation is to add the following checks: recovery !=0, agent !=0, _args.params.destinationDomain != s.domain, and _args.params.slippageTol <=s.LIQUIDITY_FEE_DENOMINATOR. It is also recommended to double check if any additional checks are useful. The bug has been solved in PR 1536 and has been verified.

### Original Finding Content

## Security Vulnerability Report

**Severity**: High Risk  
**Context**: 
- BridgeFacet.sol#L240-L339
- BridgeFacet.sol#L400-L419
- Executor.sol#L142-L280

**Description**:  
The function `xcall()` does some sanity checks; nevertheless, more checks should be added to prevent issues later on in the use of the protocol. 

- If `args.recovery == 0`, then `sendToRecovery()` will send funds to the 0 address, effectively losing them.
- If `params.agent == 0`, then `forceReceiveLocal` can’t be used, and funds might be locked forever.
- The `args.params.destinationDomain` should never be `s.domain`, although this is also implicitly checked via `_mustHaveRemote()` assuming a correct configuration.
- If `args.params.slippageTol` is set to something greater than `s.LIQUIDITY_FEE_DENOMINATOR`, then funds can be locked as `xcall()` allows for the user to provide the local asset, avoiding any swap while `_handleExecuteLiquidity()` in `execute()` may attempt to perform a swap on the destination chain.

```solidity
function xcall(XCallArgs calldata _args) external payable nonReentrant whenNotPaused returns (bytes32) {
    // Sanity checks.
    ...
}
```

**Recommendation**:  
Consider adding the following checks:
- `recovery != 0`
- `agent != 0`
- `_args.params.destinationDomain != s.domain`
- `_args.params.slippageTol <= s.LIQUIDITY_FEE_DENOMINATOR`

Also, double-check if any additional checks are useful.

**Connext**: Solved in PR 1536.  
**Spearbit**: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, External Call`

