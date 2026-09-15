---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: external_call

# Attack Vector Details
attack_type: external_call
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7230
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
rarity_score: 4

# Context Tags
tags:
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

Malicious call data can steal unclaimed tokens in the Executor contract

### Overview


This bug report is about a vulnerability in the Executor.sol contract on line 211. Users can provide an arbitrary destination contract and calldata when doing a cross-chain transfer, which can be exploited to steal tokens from the executor. This is because the executor has excess tokens and there are no restrictions on the destination contract and calldata. The exploiters can grant an allowance to themselves by setting the calldata to abi.encodeWithSelector(ERC20.approve.selector, exploiter, type(uint256).max); and the args.to to the token address, allowing them to get an infinite allowance of any token. 

The protocol has recommended a callback function to communicate with the callee contract, which would be more gas efficient as the callees do not have to query origin, originSender, and amount through three separate external calls. However, this way arbitrary calls are not possible anymore. Connext has proposed a new policy of "any funds left in the Executor following a transfer are claimable by anyone" to force implementers to think carefully about the calldata, and Spearbit has acknowledged this.

### Original Finding Content

## Vulnerability Report

## Severity: High Risk

### Context
`Executor.sol#L211`

### Description
Users can provide a destination contract `args.to` and arbitrary data `_args.callData` when doing a cross-chain transfer. The protocol will provide the allowance to the callee contract and triggers the function call through `ExcessivelySafeCall.excessivelySafeCall`.

```solidity
contract Executor is IExecutor {
    function execute(ExecutorArgs memory _args) external payable override onlyConnext returns (bool, bytes memory) {
        ...
        SafeERC20.safeIncreaseAllowance(IERC20(_args.assetId), _args.to, _args.amount);
        ...
        // Try to execute the callData
        // the low level call will return `false` if its execution reverts
        (success, returnData) = ExcessivelySafeCall.excessivelySafeCall(
            _args.to,
            gas,
            isNative ? _args.amount : 0,
            MAX_COPY,
            _args.callData
        );
        ...
    }
}
```

Since there aren’t restrictions on the destination contract and calldata, exploiters can steal the tokens from the executor.

**Note:** The executor does have excess tokens, see: Kovan executor.

**Note:** See issue "Tokens can get stuck in Executor contract."

Tokens can be stolen by granting an allowance. Setting 
```solidity
calldata = abi.encodeWithSelector(ERC20.approve.selector, exploiter, type(uint256).max);
args.to = tokenAddress;
```
allows the exploiter to get an infinite allowance of any token, effectively stealing any unclaimed tokens left in the executor.

### Recommendation
The protocol could communicate with the callee contract through a callback function. A possible specification of the callback:

```solidity
function connextExecute(uint32 origin, address adoptedToken, address originSender, uint256 amount, bytes calldata callData) returns(bytes4);
```

This results in higher gas efficiency because callees do not have to query `origin`, `originSender`, and `amount` through three separate external calls.

**Note:** This way, arbitrary calls are not possible anymore.

### Connext
New policy: "any funds left in the Executor following a transfer are claimable by anyone." This forces implementers to think carefully about the calldata. Thus, leave the issues as is.

### Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`External Call`

