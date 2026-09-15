---
# Core Classification
protocol: Pudgystrategy
chain: everychain
category: uncategorized
vulnerability_type: 1/64_rule

# Attack Vector Details
attack_type: 1/64_rule
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63044
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PudgyStrategy-Security-Review.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 1.00
financial_impact: low

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:
  - 1/64_rule

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-08] No Way to Recover Locked Tokens in the Vault

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The vault lacks a mechanism to recover arbitrary ERC-20 tokens accidentally sent to it. Over time, stray tokens may become irrecoverable. For example the vault expects ETH and later swaps `ETH`->`HEROSTR`. If a sale is settled in WETH (very common) and the marketplace transfers WETH (ERC-20) to the vault, it just sits there. The contract has no WETH unwrap and no generic ERC-20 withdrawal.

## Location of Affected Code

File: [NFTVault%20Final.sol](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/NFTVault%20Final.sol)

## Impact

Locked tokens

## Recommendation

Add a simple, restricted rescue function:

```solidity
function rescueTokens(address token, uint256 amount, address to) external onlyController nonReentrant {
    require(token != HEROSTR, "cannot rescue HEROSTR");
    IERC20(token).transfer(to, amount);
}
```

## Team Response

**Status: FIXED**

While the vault's normal operation only involves ETH and OCH NFTs, we have implemented a basic token recovery function for edge cases where tokens might get accidentally sent to the vault (such as WETH from marketplace settlements).

**Implementation:**

```solidity
function rescueTokens(address token, uint256 amount, address to) external onlyController nonReentrant {
    require(token != HEROSTR, "cannot rescue HEROSTR");
    IERC20(token).transfer(to, amount);
}
```

## [I-01] Enforse Constraints for `swapThreshold` and `maxSwapAmount` in `setSwapBehavior()` Function

## Severity

Informational Risk

## Description

Owner can set `swapThreshold` and `maxSwapAmount` via `setSwapBehavior()` to arbitrary values (no upper/lower bounds), while elsewhere `setSwapThreshold()` has a safe cap.

## Location of Affected Code

File: [HEROSTR.sol#L623-L633](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/HEROSTR.sol#L623-L633)

```solidity
function setSwapBehavior(bool _enabled, bool _lastOnly, uint256 _threshold, uint256 _max) external onlyOwner {
    swapEnabled = _enabled;
    swapLastTaxOnly = _lastOnly;
    swapThreshold = _threshold;
    maxSwapAmount = _max;
}
```

## Recommendation

Add sanity checks similar to `setSwapThreshold()` (e.g., `_threshold <= totalSupply()/100` and `_max <= totalSupply()/100`).

## Team Response

**Status: FIXED**

We have implemented sanity checks for swap parameters to prevent misconfiguration:

**Implementation:**

```solidity
function setSwapBehavior(bool _enabled, bool _lastOnly, uint256 _threshold, uint256 _max) external onlyOwner {
    require(_threshold <= totalSupply() / 100, "threshold too high");
    require(_max <= totalSupply() / 100, "max amount too high");
    require(_threshold > 0, "threshold must be > 0");
    require(_max >= _threshold, "max must be >= threshold");

    swapEnabled = _enabled;
    swapLastTaxOnly = _lastOnly;
    swapThreshold = _threshold;
    maxSwapAmount = _max;
}
```

## [I-02] Newly Set Recipients Are Not Auto-(Un)Exempted

## Severity

Informational Risk

## Description

The `setRecipients()` replaces the vault/accumulator/team addresses but does not update `isTaxExempt()`/`isCapExempt()`. Newly set recipients may unexpectedly be taxed or restricted, while the previous recipients remain exempt unless the owner manually updates exemptions.

## Location of Affected Code

File: [HEROSTR.sol#L659-L671](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/HEROSTR.sol#L659-L671)

```solidity
function setRecipients( address _vault, address _accumulator, address _team ) external onlyOwner {
    if (_vault == address(0)) revert ZeroAddress();
    if (_accumulator == address(0)) revert ZeroAddress();
    if (_team == address(0)) revert ZeroAddress();

    nftVault = _vault;
    pdgystrAccumulator = _accumulator;
    teamWallet = _team;
}
```

## Impact

- Newly set recipients may be taxed or subject to cap restrictions despite the intended exemption policy.
- Previous recipients remain exempt and could receive preferential treatment unintentionally until manually updated.

## Recommendation

Update `setRecipients()` to atomically (un)exempt old and new recipients, e.g.:

- Clear exemptions for old `nftVault/pdgystrAccumulator/teamWallet`.
- Set exemptions for new `_vault/_accumulator/_team`.

## Team Response

**Status: ACKNOWLEDGED - ACCEPTABLE RISK**

The team acknowledges this behavior. Given that recipient changes are rare administrative actions, manual exemption management provides more explicit control over tax and cap exemptions. This approach allows for intentional review of exemption status when recipients are updated.

## [I-03] Max Wallet Enforced Only on Buys and Can Be Trivially Bypassed via Peer Transfers

## Severity

Informational Risk

## Description

The max wallet check is applied only on buy transfers. Direct peer-to-peer transfers to a holder are not subject to this check, allowing users to exceed the configured max wallet via incoming transfers.

## Location of Affected Code

File: [HEROSTR.sol#L434-L439](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/HEROSTR.sol#L434-L439)

```solidity
function _update( address from, address to, uint256 amount ) internal override {
  // code
  // Check max wallet after tax
  if (maxWalletEnabled && isBuy && !isCapExempt[to]) {
      uint256 maxWallet = (totalSupply() * maxWalletBps) / BPS;
      if (balanceOf(to) > maxWallet) {
          revert ExceedsMaxWallet();
      }
  }
  // code
}
```

## Impact

- Users can bypass max wallet by receiving tokens via direct transfers.
- Without a whitelist mechanism, the number of wallets is effectively unlimited, reducing the practical value of the max wallet feature for distribution control.

## Proof of Concept

1. A single user controls two wallets: Wallet A and Wallet B.
2. The user buys up to the max wallet limit into Wallet A.
3. The user buys up to the max wallet limit into Wallet B.
4. The user transfers tokens from Wallet B to Wallet A via a direct peer transfer.
5. Because the max wallet check runs only on buys, the transfer to Wallet A is not checked, Wallet A now holds more than the configured max wallet (effectively up to 2× the limit in this example).

## Recommendation

Enforce max wallet on all incoming transfers (buys and peer transfers).

## Team Response

**Status: ACKNOWLEDGED - BY DESIGN**

The current implementation focusing on buy transactions is intentional. Max wallet limits are primarily designed to prevent large single purchases during launch, not to restrict peer-to-peer transfers. Enforcing limits on all transfers would create user experience friction without significant security benefits, as determined users can always use multiple wallets.

## [I-04] Swap Deadline Computed at Execution Always Passes

## Severity

Informational Risk

## Description

The deadline is set as `block.timestamp + 600` at execution time inside the vault. Since the router validates `block.timestamp <= deadline` using the same `block.timestamp`, this check always passes and provides no meaningful timeout. The value is also not caller-controlled, so you cannot enforce stricter or different expiry policies per transaction.

## Location of Affected Code

File: [NFTVault%20Final.sol#L236-L241](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/NFTVault%20Final.sol#L236-L241)

```solidity
function burnProceedsETH(uint256 amountEth, uint256 minOut) external onlyController nonReentrant {
  // code
  IUniswapV2Router02(ROUTER).swapExactETHForTokensSupportingFeeOnTransferTokens{value: amountEth}(
      minOut,
      path,
      address(this),
      block.timestamp + 600  // 10 minute deadline
  );
  // code
}
```

## Impact

1. There is effectively no expiry/timebox on the swap path; the deadline always passes.
2. Off-chain automation cannot enforce a specific TTL policy per trade.
3. The hardcoded "+600" may give a false impression of protection while providing none.

## Recommendation

Add a `deadline` parameter to `burnProceedsETH()` and require it to be in the future, optionally cap the maximum horizon to avoid excessively lax expiries.

```diff
- function burnProceedsETH(uint256 amountEth, uint256 minOut) external onlyController nonReentrant {
+ function burnProceedsETH(uint256 amountEth, uint256 minOut, uint256 deadline) external onlyController nonReentrant {
    require(address(this).balance >= amountEth, "insufficient ETH");
    require(amountEth > 0, "zero amount");
    require(minOut > 0, "zero minOut");
+   require(deadline > block.timestamp, "deadline not in future");

    address[] memory path = new address[](2);
    path[0] = WETH;
    path[1] = HEROSTR;

    uint256 herostrBefore = IERC20(HEROSTR).balanceOf(address(this));

    IUniswapV2Router02(ROUTER).swapExactETHForTokensSupportingFeeOnTransferTokens{value: amountEth}(
        minOut,
        path,
        address(this),
+       deadline
    );
    //  code
}
```

## Team Response

**Status: ACKNOWLEDGED - ACCEPTABLE**

The current deadline implementation provides basic protection against extremely delayed transactions. Our design uses `minOut = 0` for reliability combined with small swap tranches for price protection, making additional deadline complexity unnecessary for our use case.

## [I-05] Keeper Docs Collection Address Differs from Contract Immutable

## Severity

Informational Risk

## Description

Keeper documentation lists a different OCH collection address than the vault's immutable `COLLECTION` in code. This configuration drift can cause bots to monitor or trade the wrong collection and create inconsistencies across tooling.

The documentation refers to [GenesisHero (GHERO)](https://abscan.org/token/0x7c47ea32fd27d1a74fc6e9f31ce8162e6ce070eb) collection.

While the Vault1271 contract refers to [OCH_GACHA_WEAPON (OGW)](https://abscan.org/address/0x686bFe70F061507065f3E939C12aC9EE5a564dCf), which might not be correct.

## Location of Affected Code

File: [keeper_documentation](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/keeper_documentation.md)

```
## OCH Heroes System
NFT_VAULT = "0x7E9Ed861B4b998B4fd942216DB11fec1caA93e7B"
NFT_COLLECTION = "0x7c47ea32fd27d1a74fc6e9f31ce8162e6ce070eb" // <@ different address!
SEAPORT = "0x0000000000000068F116a894984e2DB1123eB395"
ROUTER = "0xad1eCa41E6F772bE3cb5A48A6141f9bcc1AF9F7c"
```

File: [NFTVault%20Final.sol#L80](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/NFTVault%20Final.sol#L80)

```solidity
address public immutable COLLECTION = 0x686bFe70F061507065f3E939C12aC9EE5a564dCf;  // OCH Heroes
```

## Impact

Operational mistakes and inconsistent configuration between the contract and the off-chain system.

## Recommendation

Align addresses across code and documentation.

## Team Response

**Status: FIXED**

This discrepancy was due to testing configurations. The team has updated the contract to reflect the correct OCH Heroes collection address used in the production contracts.

**Implementation:**

```solidity
address public immutable COLLECTION = 0x7c47ea32fd27d1a74fc6e9f31ce8162e6ce070eb;  // Corrected OCH Heroes address
```

## [I-06] Misleading Accounting: "Sale Proceeds" Actually Tracks Burned ETH Amount

## Severity

Informational Risk

## Description

The metric `totalETHFromSales` is described as tracking ETH earned from selling NFTs, but it is incremented by the ETH amount passed into `burnProceedsETH()` rather than by actual marketplace sale proceeds. This conflates sale revenue with the amount routed into burns, which can diverge from real proceeds.

## Location of Affected Code

File: [NFTVault%20Final.sol#L95](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/NFTVault%20Final.sol#L95)

```solidity
uint256 public totalETHFromSales;   // Total ETH earned from selling OCH Heroes
```

File: [NFTVault%20Final.sol#L251-L253](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/NFTVault%20Final.sol#L251-L253)

```solidity
function burnProceedsETH(uint256 amountEth, uint256 minOut) external onlyController nonReentrant {
  // code
  // Update our stats
  totalETHFromSales += amountEth;
  totalHEROSTRBurned += herostrReceived;
  totalBurns++;

  emit HEROSTRBurned(amountEth, herostrReceived, totalBurns);
}
```

## Impact

Operational reporting and strategy evaluation can be skewed as "sale proceeds" may over/understate actual marketplace revenue

## Recommendation

- Rename `totalETHFromSales` to reflect its meaning (e.g., `totalETHBurned` or `totalETHRoutedToBurn`).
- If actual sale proceeds are required, increment a separate counter when sales are confirmed (e.g., upon receipt events or decoded Seaport receipts).

## Team Response

**Status: FIXED**

We have updated variable naming and documentation to accurately reflect what is being tracked. The variable has been renamed from `totalETHFromSales` to `totalETHBurned` to avoid confusion about its purpose.

**Implementation:**

```solidity
uint256 public totalETHBurned;  // Renamed from totalETHFromSales for clarity

function getStats() external view returns (
    uint256 ethBalance,
    uint256 ethSpent,
    uint256 nftsBought,
    uint256 ethBurned, // Updated return variable name
    uint256 herostrBurned,
    uint256 burnCount
) {
    return (
        address(this).balance,
        totalETHSpent,
        totalNFTsBought,
        totalETHBurned, // Updated variable reference
        totalHEROSTRBurned,
        totalBurns
    );
}
```

## [G-01] Router Allowance Checked on Every Swap Consumes Gas

## Severity

Gas Optimization

## Description

The contract checks the router allowance on every swap and approves only when the allowance is insufficient (e.g., the first swap or after an external reset). This imposes a per-swap SLOAD and occasional SSTORE. Since the router is immutable and approval is to `type(uint256).max`, setting the approval once in the constructor allows removing (or gating) the per-swap check to reduce gas in swap execution.

## Location of Affected Code

File: [HEROSTR.sol#L462-L465](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/HEROSTR.sol#L462-L465)

```solidity
function _swapBackExact(uint256 tokensToSwap) private returns (uint256 sold) {
  // code
  // Check if we need approval (more gas efficient)
  uint256 currentAllowance = allowance(address(this), address(router));
  if (currentAllowance < tokensToSwap) {
      _approve(address(this), address(router), type(uint256).max);
  }
  // code
}
```

## Impact

- Saves an SLOAD on every swap and avoids occasional SSTORE when allowance is topped up.
- Reduces per-swap gas, which compounds across frequent swapbacks.

## Recommendation

Consider applying the following changes:

- In the `constructor()`, set a one-time infinite approval:

```solidity
_approve(address(this), address(router), type(uint256).max);
```

- Remove the per-swap allowance check/approve in `_swapBackExact()`.
- Remove the extra `approveRouterMax()` function, with constructor-time approval and no per-swap checks, it becomes redundant.

## Team Response

**Status: FIXED**

We have implemented the suggested optimization by setting infinite approval in the constructor and removing per-swap allowance checks.

**Implementation:**

```solidity
// In constructor
_approve(address(this), address(router), type(uint256).max);

// Removed allowance check from _swapBackExact
```

## [G-02] Use Immutables/Constants for WETH and Distribution Shares

## Severity

Gas Optimization

## Description

- WETH address fetched via external call on demand. Caching the WETH address as `immutable` in the constructor avoids external calls in hot paths.
- Distribution shares (`vaultShare`, `accumulatorShare`, `teamShare`) are never mutated in this contract yet are read from storage on each distribution, marking them `constant` (or `immutable`) removes repeated SLOADs.

## Location of Affected Code

File: [HEROSTR.sol#L343-L345](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/HEROSTR.sol#L343-L345)

```solidity
function _WETH() private view returns (address) {
    return router.WETH();
}
```

File: [HEROSTR.sol#L107-L109](https://github.com/0xcaptainy/HEROSTR/blob/cafe69ed029aef74e874471b157afabfacb0d81c/HEROSTR.sol#L107-L109)

```solidity
// Distribution shares
uint256 public vaultShare = 80;
uint256 public accumulatorShare = 10;
uint256 public teamShare = 10;
```

## Impact

- Saves one or more external calls per swap/distribution and in `unwrapAllWETH()`.
- Removes SLOADs during distribution, reducing gas cost on every swapback.

## Recommendation

- Add `address public immutable WETH;` set in the constructor as `WETH = IUniswapV2Router02(_router).WETH();` and replace `_WETH()` usages with `WETH`.
- Declare shares as constants, e.g., `uint256 public constant VAULT_SHARE = 80;`, `ACCUMULATOR_SHARE = 10;`, `TEAM_SHARE = 10;`, and update computations to use these constants.

## Team Response

**Status: FIXED**

We have implemented both optimizations:

1. Cached WETH address as immutable in constructor
2. Converted distribution shares to constants

**Implementation:**

```solidity
address public immutable WETH;
uint256 public constant VAULT_SHARE = 80;
uint256 public constant ACCUMULATOR_SHARE = 10;
uint256 public constant TEAM_SHARE = 10;

// In constructor
WETH = IUniswapV2Router02(_router).WETH();
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Pudgystrategy |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PudgyStrategy-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`1/64 Rule`

