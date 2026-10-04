---
# Core Classification
protocol: Pearlabs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44111
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PearLabs-Security-Review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[H-04] The `withdrawClosedSize()` Function Misses the Situation Where the Funds Are Transferred as `ETH` From the `GMX`

### Overview


The report describes a bug in the GMX protocol where users can close their positions and receive ETH, but the platform does not handle this correctly. This means that the platform fees can be avoided by the user. The affected code is in the GmxAdapter.sol file, specifically in the withdrawClosedSize function. The recommendation is to cover the situation where funds are requested in native tokens. The team has acknowledged and fixed the issue by removing the withdrawal ETH functionality. The impact of this bug is the loss of protocol fees.

### Original Finding Content

## Severity

High Risk

## Description

Users can opt to close their positions with ETH being received, accordingly, they can pass the flag:

File: [src/interfaces/IPearGmxFactory.sol#L48-L49](https://github.com/pear-protocol/pear-sc/blob/00aa0ce64fd6fd95c3207e01871bdbe3267db2c9/src/interfaces/IPearGmxFactory.sol#L48-L49)

```solidity
struct DecreasePositionsArgs {
  bool withdrawETHLong; // @audit Flag to pass true
  bool withdrawETHShort; // @audit Flag to pass true
  ...
}
```

The same call is interpreted on the GMX side as `request.withdrawETH = true`.

Once the position is decreased and closed at the GMX side, the below function is called:

```solidity
function executeDecreasePosition(bytes32 _key, address payable _executionFeeReceiver) public nonReentrant returns (bool) {
  // code
  if (amountOut > 0) {
    if (request.path.length > 1) {
      IERC20(request.path[0]).safeTransfer(vault, amountOut);
      amountOut = _swap(request.path, request.minOut, address(this));
    }

    if (request.withdrawETH) { // @audit The intention is handled here;
      _transferOutETHWithGasLimitFallbackToWeth(amountOut, payable(request.receiver));
    } else {
      IERC20(request.path[request.path.length - 1]).safeTransfer(request.receiver, amountOut);
    }
  }
  // code
}
```

At the `GmxFactory.sol` side, the closing position is handled during the callback as below:

File: [src/Factory/GmxFactory.sol#L646-L667](https://github.com/pear-protocol/pear-sc/blob/00aa0ce64fd6fd95c3207e01871bdbe3267db2c9/src/Factory/GmxFactory.sol#L646-L667)

```solidity
} else if (
  longExecutionState == ExecutionState.Success ||
  shortExecutionState == ExecutionState.Success
) {
  if (!isIncrease) {
    uint256[] memory data = getPosition(adapter);
    if (
      positionDetails[adapter][adapterOwner] ==
      PositionStatus.Opened &&
      data[1] == 0 &&
      data[10] == 0
    ) {
      positionDetails[adapter][adapterOwner] = PositionStatus
        .Closed;
    }

    IPearGmxAdapter(adapter).withdrawClosedSize(
      feeAmount,
      platformLogic,
      collateralToken
    );
  }
 // code
}
```

The `withdrawClosedsize()` function is below:

File: [src/GmxAdapter.sol#L161](https://github.com/pear-protocol/pear-sc/blob/00aa0ce64fd6fd95c3207e01871bdbe3267db2c9/src/GmxAdapter.sol#L161)

```solidity
function withdrawClosedSize(
  uint256 feeAmount,
  address platformLogic,
  address token
) external onlyFactory {
  if (IERC20(token).balanceOf(address(this)) > 0) {
    SafeTransferLib.safeTransfer(token, platformLogic, feeAmount);

    SafeTransferLib.safeTransferAll(token, owner);
  }
}
```

So if the `withdrawETH()` flag is `true`, the `withdrawClosedSize()` implementation doesn't cover this.
Since it's not pushed to the user and to the Pear Side the `adapterOwner` can call below and get away with the platform fees.

File: [src/GmxAdapter.sol#L186](https://github.com/pear-protocol/pear-sc/blob/00aa0ce64fd6fd95c3207e01871bdbe3267db2c9/src/GmxAdapter.sol#L186)

```solidity
/// @inheritdoc IPearGmxAdapter
function withdrawETH(
  address to,
  uint256 amount
) external override onlyOwner returns (bool success) {
  SafeTransferLib.safeTransferETH(to, amount);

  emit EthWithdrawal(to, amount);
  return true;
}
```

## Impact

Loss of protocol fees.

## Location of Affected Code

File: [src/GmxAdapter.sol#L161-L171](https://github.com/pear-protocol/pear-sc/blob/00aa0ce64fd6fd95c3207e01871bdbe3267db2c9/src/GmxAdapter.sol#L161-L171)

```solidity
function withdrawClosedSize(
  uint256 feeAmount,
  address platformLogic,
  address token
) external onlyFactory {
  if (IERC20(token).balanceOf(address(this)) > 0) {
    SafeTransferLib.safeTransfer(token, platformLogic, feeAmount);

    SafeTransferLib.safeTransferAll(token, owner);
  }
}
```

## Recommendation

It's recommended to cover the situation where the funds are requested in native tokens.

## Team Response

Acknowledged and fixed by removing withdrawal ETH functionality.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Pearlabs |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PearLabs-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

