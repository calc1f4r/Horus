---
# Core Classification
protocol: Tsunami GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47812
audit_firm: OtterSec
contest_link: https://tsunami.finance/
source_link: https://tsunami.finance/
github_link: https://github.com/Tsunami-Finance/tsunami-contracts

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Invalid Event Field

### Overview

See description below for full details.

### Original Finding Content

## swapETHToTokens Function

The `swapETHToTokens` function allows users to swap Ether for tokens along a specified token path. It updates the price through a Pyth oracle and ensures that the received token amount meets or exceeds a specified minimum threshold.

## Function Implementation

```solidity
function swapETHToTokens(
    address[] memory _path, 
    uint256 _minOut, 
    address _receiver, 
    bytes[] calldata _pythUpdateData
) external payable {
    uint256 _pythUpdateFee = _updatePythPrices(_pythUpdateData);
    require(_path[0] == weth, "Router: invalid _path");
    _transferETHToVault(_pythUpdateFee);
    uint256 amountOut = _swap(_path, _minOut, _receiver);
    emit Swap(msg.sender, _path[0], _path[_path.length - 1], msg.value, amountOut);
}
```

## Important Notes

- The current implementation of `swapETHToTokens` emits the `Swap` event with `msg.value` as `amountIn`, reporting the total amount of Ether sent along with the transaction.
- However, `amountIn` should represent the amount of Ether explicitly sent for the swap, excluding any fees paid for the Pyth price update (`_pythUpdateFee`). The program deducts this fee from `msg.value` to cover the cost of updating token prices through the Pyth oracle.
- Consequently, this discrepancy in the event data may result in off-chain parties, such as web front ends or bots, misinterpreting the on-chain events.

## Remediation

Set the `amountIn` field in the `Swap` event to `msg.value - _pythUpdateFee`, ensuring that it accurately reflects the amount of Ether specifically spent for the swap.

## Patch

Fixed in commit `18460e8`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tsunami GMX |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: https://tsunami.finance/
- **GitHub**: https://github.com/Tsunami-Finance/tsunami-contracts
- **Contest**: https://tsunami.finance/

### Keywords for Search

`vulnerability`

