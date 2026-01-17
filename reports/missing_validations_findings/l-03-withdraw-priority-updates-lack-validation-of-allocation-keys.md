---
# Core Classification
protocol: Prime Vaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64021
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Prime-Vaults-Security-Review.md
github_link: none

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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-03] Withdraw Priority Updates Lack Validation of Allocation Keys

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The `StrategyManager.setWithdrawPriority()` function updates the withdrawal queue without validating that the provided keys correspond to existing allocations. Although the function is restricted to the manager, the absence of on-chain checks increases the risk of misconfiguration, such as adding non-existent keys or accidentally omitting active strategies.

## Location of Affected Code

File: [contracts/StrategyManager.sol#L298-L306](https://github.com/prime-vaults/prime-vaults-strategy/blob/b722f446d14f0ff4fd600dab80a16ac8b11b413d/contracts/StrategyManager.sol#L298-L306)

```solidity
function setWithdrawPriority(WithdrawPriority[] calldata queue) external onlyManager {
    delete withdrawPriority;
    for (uint256 i; i < queue.length; ) {
        withdrawPriority.push(queue[i]);
        unchecked {
            ++i;
        }
    }
}
```

## Impact

If the manager inadvertently uploads a priority list with invalid keys or an empty list while relying on strategies for liquidity, user withdrawals could revert with `VAULT__INSUFFICIENT_FUNDS` until the configuration is corrected. This is an operational risk rather than a direct vulnerability.

## Recommendation

It is recommended to add basic sanity checks to `setWithdrawPriority()` to ensure that every key in the provided queue corresponds to a valid, existing allocation.

```solidity
function setWithdrawPriority(WithdrawPriority[] calldata queue) external onlyManager {
    delete withdrawPriority;
    for (uint256 i; i < queue.length; ) {
        // Validation: Ensure the allocation actually exists
        if (queue[i].kind == StrategyKind.SingleAsset) {
            if (!singleAllocs[queue[i].allocKey].exists) revert VAULT__ALLOCATION_NOT_FOUND();
        } else {
            if (!pairAllocs[queue[i].allocKey].exists) revert VAULT__ALLOCATION_NOT_FOUND();
        }

        withdrawPriority.push(queue[i]);
        unchecked {
            ++i;
        }
    }
}
```

## Team Response

Fixed.

## [I-01] Missing Zero Amount Validation in Deposit and Withdraw Functions

## Severity

Informational Risk

## Description

The `deposit()` and `withdraw()` functions in `PrimeStrategy.sol` do not validate that the `amount` parameter is greater than zero. This allows users to execute transactions with zero amounts, consuming gas unnecessarily, emitting misleading events, and potentially confusing off-chain systems.

## Location of Affected Code

File: [contracts/PrimeStrategy.sol](https://github.com/prime-vaults/prime-vaults-strategy/blob/b722f446d14f0ff4fd600dab80a16ac8b11b413d/contracts/PrimeStrategy.sol#L52-L100)

```solidity
function deposit(address token, uint256 amount) external nonReentrant {
    // @audit missing zero amount validation
    IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
    // code
}

function withdraw(address token, uint256 amount) external nonReentrant {
    // @audit missing zero amount validation
    // code
}
```

## Impact

Users pay gas fees for zero-amount transactions that have no effect.

## Proof of Concept

Call `deposit(USDC, 0)` or `withdraw(USDC, 0)`. The transaction succeeds, consumes gas, and emits events with zero amounts, providing no meaningful effect.

## Recommendation

Add zero amount validation: `require(amount > 0, "Amount must be greater than zero");` at the beginning of both functions.

## Team Response

Fixed.

## [I-02] Missing Event Emissions for Administrative Parameter Updates

## Severity

Informational Risk

## Description

Administrative functions in `StrategyManager` (like `setWithdrawPriority()`, `setTreasury()`) and the `executeAllocSingle()` function do not emit events upon execution. This lack of event emission prevents off-chain monitoring tools and users from tracking important configuration changes and fund movements in real-time.

## Location of Affected Code

File: [contracts/StrategyManager.sol](https://github.com/prime-vaults/prime-vaults-strategy/blob/b722f446d14f0ff4fd600dab80a16ac8b11b413d/contracts/StrategyManager.sol)

## Impact

Users and off-chain tools (like indexers or graphs) can't track the history of the vault correctly. If the manager changes the treasury address or reorders the withdrawal queue, nobody knows until they inspect the contract state manually.

## Recommendation

Define and emit events for all state-changing functions. This makes it easy to track what the Manager is doing.

Add these events to `StrategyManager.sol` (or an interface):

```solidity
event TreasurySet(address indexed newTreasury);
event WithdrawPrioritySet(WithdrawPriority[] priority);
event SingleAllocationSet(bytes32 indexed key, address indexed strategy, uint256 cap);
event PairAllocationSet(bytes32 indexed key, address indexed strategy, uint256 capA, uint256 capB);
event SingleAllocationExecuted(bytes32 indexed key, uint256 allocated);
```

And update the functions to emit them:

```solidity
function setTreasury(address _treasury) external onlyAdmin {
    treasury = _treasury;
    emit TreasurySet(_treasury);
}

function executeAllocSingle(bytes32 key) external onlyManager nonReentrant {
    // ... execution logic ...
    emit SingleAllocationExecuted(key, alloc.allocated);
}
```

## Team Response

Fixed.

## [I-03] Missing Zero Address Checks

## Severity

Informational Risk

## Description

The contracts `StrategyManager.sol`, `PrimeStrategy.sol`, and `StrategyRegistry.sol` accept address parameters without verifying they are not the zero address (`address(0)`). Missing these checks can lead to misconfiguration, loss of privileges, or loss of funds.

## Location of Affected Code

File: [`contracts/StrategyManager.sol](https://github.com/prime-vaults/prime-vaults-strategy/blob/b722f446d14f0ff4fd600dab80a16ac8b11b413d/contracts/StrategyManager.sol)

```solidity
constructor(address _strategyRegistry, address _manager, address _treasury, address _admin) {
    // ...
}

function addSingleAllocation(address token, uint256 cap, address stra) external onlyManager {
    // ...
}

function addPairAllocation(address tokenA, address tokenB, uint256 capA, uint256 capB, address stra) external onlyManager {
    // code
}

function updateRole(address user, bytes32 role, bool grant) external onlyAdmin {
    // code
}

function setTreasury(address _treasury) external onlyAdmin {
    // code
}

function topUpIL(address token, uint256 amount) external onlyManager {
    // code
}

function swap(SwapParams calldata params) external onlyManager nonReentrant {
    // params.tokenIn, params.tokenOut, params.to checks missing
    // code
}
```

File: [contracts/PrimeStrategy.sol](https://github.com/prime-vaults/prime-vaults-strategy/blob/b722f446d14f0ff4fd600dab80a16ac8b11b413d/contracts/PrimeStrategy.sol)

```solidity
constructor(address _manager, address _vaultRegistry, address _treasury)
    StrategyManager(_vaultRegistry, _manager, _treasury, msg.sender)
{}

function deposit(address token, uint256 amount) external nonReentrant {
    // code
}

function withdraw(address token, uint256 amount) external nonReentrant {
    // code
}
```

File: [contracts/StrategyRegistry.sol#L53-L76](https://github.com/prime-vaults/prime-vaults-strategy/blob/b722f446d14f0ff4fd600dab80a16ac8b11b413d/contracts/StrategyRegistry.sol#L53-L76)

```solidity
function addStrategy(address stra, address expectedVault) external onlyOwner {
  // code
}
```

## Impact

Missing zero address checks can lead to severe consequences. Deploying contracts with zero addresses as initial parameters forces a costly redeployment. Setting critical roles like admin or manager to the zero address permanently locks privileges, making the contract unmanageable. Furthermore, configuring the treasury to the zero address results in irreversible loss of funds (burning), while allocating zero address tokens or strategies causes operational failures, reverts, and potential asset loss.

## Recommendation

Add checks to ensure that critical address parameters are not zero.

```solidity
require(_address != address(0), "Invalid Address");
```

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Prime Vaults |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Prime-Vaults-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

