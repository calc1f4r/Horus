---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25848
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/54

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - KIntern\_NA
  - ladboy233
---

## Vulnerability Title

[M-32] Certain function can be blocked if the ERC20 token revert in 0 amount transfer after `PublicVault#transferWithdrawReserve` is called

### Overview


This bug report is about a function called `transferWithdrawReserve` in the Public Vault smart contract which has no access control. This function transfers the token balance to a withdrawProxy, but some tokens (e.g. LEND) revert when transferring a zero value amount. This can cause a transaction to revert if the address has no ERC20 token balance and the ERC20 token reverts in 0 amount transfer after PublicVault#transferWithdrawReserve is called first. This not only impacts commitToLien, but also impacts `PublicVault.updateVaultAfterLiquidation`.

The recommended mitigation step is for the protocol to just return and do nothing when `PublicVault#transferWithdrawReserve` is called if the address has no ERC20 token balance. This has been confirmed by androolloyd (Astaria).

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/VaultImplementation.sol#L295><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L421><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L359><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L372><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/PublicVault.sol#L384>

The function transferWithdrawReserve in Public Vault has no access control.

```solidity
  function transferWithdrawReserve() public {
    VaultData storage s = _loadStorageSlot();

    if (s.currentEpoch == uint64(0)) {
      return;
    }

    address currentWithdrawProxy = s
      .epochData[s.currentEpoch - 1]
      .withdrawProxy;
    // prevents transfer to a non-existent WithdrawProxy
    // withdrawProxies are indexed by the epoch where they're deployed
    if (currentWithdrawProxy != address(0)) {
      uint256 withdrawBalance = ERC20(asset()).balanceOf(address(this));

      // prevent transfer of more assets then are available
      if (s.withdrawReserve <= withdrawBalance) {
        withdrawBalance = s.withdrawReserve;
        s.withdrawReserve = 0;
      } else {
        unchecked {
          s.withdrawReserve -= withdrawBalance.safeCastTo88();
        }
      }

      ERC20(asset()).safeTransfer(currentWithdrawProxy, withdrawBalance);
      WithdrawProxy(currentWithdrawProxy).increaseWithdrawReserveReceived(
        withdrawBalance
      );
      emit WithdrawReserveTransferred(withdrawBalance);
    }

    address withdrawProxy = s.epochData[s.currentEpoch].withdrawProxy;
    if (
      s.withdrawReserve > 0 &&
      timeToEpochEnd() == 0 &&
      withdrawProxy != address(0)
    ) {
      address currentWithdrawProxy = s
        .epochData[s.currentEpoch - 1]
        .withdrawProxy;
      uint256 drainBalance = WithdrawProxy(withdrawProxy).drain(
        s.withdrawReserve,
        s.epochData[s.currentEpoch - 1].withdrawProxy
      );
      unchecked {
        s.withdrawReserve -= drainBalance.safeCastTo88();
      }
      WithdrawProxy(currentWithdrawProxy).increaseWithdrawReserveReceived(
        drainBalance
      );
    }
  }
```

If this function is called, the token balance is transfered to withdrawProxy

```solidity
uint256 withdrawBalance = ERC20(asset()).balanceOf(address(this));
```

and

```solidity
ERC20(asset()).safeTransfer(currentWithdrawProxy, withdrawBalance);
```

However, according to

<https://github.com/d-xo/weird-erc20#revert-on-zero-value-transfers>

Some tokens (e.g. LEND) revert when transfering a zero value amount.

If `ERC20(asset()).balanceOf(address(this))` return 0, the transfer revert.

The impact is that transferWithdrawReserve is also used in the other place:

```solidity
  function commitToLien(
    IAstariaRouter.Commitment calldata params,
    address receiver
  )
    external
    whenNotPaused
    returns (uint256 lienId, ILienToken.Stack[] memory stack, uint256 payout)
  {
    _beforeCommitToLien(params);
    uint256 slopeAddition;
    (lienId, stack, slopeAddition, payout) = _requestLienAndIssuePayout(
      params,
      receiver
    );
    _afterCommitToLien(
      stack[stack.length - 1].point.end,
      lienId,
      slopeAddition
    );
  }
```

which calls:

```solidity
_beforeCommitToLien(params);
```

which calls:

```solidity
  function _beforeCommitToLien(IAstariaRouter.Commitment calldata params)
    internal
    virtual
    override(VaultImplementation)
  {
    VaultData storage s = _loadStorageSlot();

    if (s.withdrawReserve > uint256(0)) {
      transferWithdrawReserve();
    }
    if (timeToEpochEnd() == uint256(0)) {
      processEpoch();
    }
  }
```

which calls transferWithdrawReserve() which revert in 0 amount transfer.

Consider the case below:

1.  User A calls commitToLien transaction is pending in mempool.
2.  User B front-run User A's transaction by calling  transferWithdrawReserve() and the PublicVault has no ERC20 token balance or User B just want to call  transferWithdrawReserve and not try to front-run user A, but the impact and result is the same.
3.  User B's transaction executes first,
4.  User A first his transaction revert because the ERC20 token asset revert in 0 amount transfer in transferWithdrawReserve() call

```solidity
uint256 withdrawBalance = ERC20(asset()).balanceOf(address(this));

// prevent transfer of more assets then are available
if (s.withdrawReserve <= withdrawBalance) {
withdrawBalance = s.withdrawReserve;
s.withdrawReserve = 0;
} else {
unchecked {
  s.withdrawReserve -= withdrawBalance.safeCastTo88();
}
}

ERC20(asset()).safeTransfer(currentWithdrawProxy, withdrawBalance);
```

This revertion not only impacts commitToLien, but also impacts `PublicVault.sol#updateVaultAfterLiquidation`

```solidity
function updateVaultAfterLiquidation(
uint256 maxAuctionWindow,
AfterLiquidationParams calldata params
) public onlyLienToken returns (address withdrawProxyIfNearBoundary) {
VaultData storage s = _loadStorageSlot();

_accrue(s);
unchecked {
  _setSlope(s, s.slope - params.lienSlope.safeCastTo48());
}

if (s.currentEpoch != 0) {
  transferWithdrawReserve();
}
uint64 lienEpoch = getLienEpoch(params.lienEnd);
_decreaseEpochLienCount(s, lienEpoch);

uint256 timeToEnd = timeToEpochEnd(lienEpoch);
if (timeToEnd < maxAuctionWindow) {
  _deployWithdrawProxyIfNotDeployed(s, lienEpoch);
  withdrawProxyIfNearBoundary = s.epochData[lienEpoch].withdrawProxy;

  WithdrawProxy(withdrawProxyIfNearBoundary).handleNewLiquidation(
	params.newAmount,
	maxAuctionWindow
  );
}
```

Transaction can revert in above code when calling

```solidity
if (s.currentEpoch != 0) {
  transferWithdrawReserve();
}
uint64 lienEpoch = getLienEpoch(params.lienEnd);
```

If the address has no ERC20 token balance and the ERC20 token revert in 0 amount transfer after PublicVault#transferWithdrawReserve is called first.

### Recommended Mitigation Steps

We recommend the protocol just return and do nothing when `PublicVault#transferWithdrawReserve` is called if the address has no ERC20 token balance.

**[androolloyd (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/54)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | KIntern\_NA, ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/54
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

