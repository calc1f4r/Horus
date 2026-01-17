---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26064
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/201

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

protocol_categories:
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - bin2chen
  - T1MOH
---

## Vulnerability Title

[H-30] Incorrect flow of adding liquidity in `UlyssesRouter.sol`

### Overview


A bug has been identified in the 0xLightt (Maia) codebase, specifically in the `addLiquidity()` function of the Ulysses AMM (Automatic Market Maker) router. This function is stateless, meaning it is not supposed to contain any tokens. The current implementation assumes that a user first transfers tokens to the router and then the router deposits them into the pool. However, this is not an atomic operation and requires two transactions. This means that another user can break in after the first transaction and deposit someone else's tokens.

To mitigate this issue, the router should call the deposit function with `safeTransferFrom()` to transfer tokens from the sender to the router.

This bug has been identified as an Access Control issue, and 0xLightt (Maia) has confirmed the audit's findings. However, they have commented that they will not be rectifying this bug as the codebase is being migrated to Balancer Stable Pools.

### Original Finding Content


Usually the router in `AMM` is stateless, i.e. it isn't supposed to contain any tokens, it is just a wrapper of low-level pool functions to perform user-friendly interactions. The current implementation of `addLiquidity()` assumes that a user firstly transfers tokens to the router and then the router performs the deposit to the pool. However, it is not atomic and requires two transactions. Another user can break in after the first transaction and deposit someone else's tokens.

### Proof of Concept

The router calls the deposit with `msg.sender` as a receiver of shares:

<https://github.com/code-423n4/2023-05-maia/blob/54a45beb1428d85999da3f721f923cbf36ee3d35/src/ulysses-amm/UlyssesRouter.sol#L49-L56>

```solidity
    function addLiquidity(uint256 amount, uint256 minOutput, uint256 poolId) external returns (uint256) {
        UlyssesPool ulysses = getUlyssesLP(poolId);

        amount = ulysses.deposit(amount, msg.sender);

        if (amount < minOutput) revert OutputTooLow();
        return amount;
    }
```

And in deposit pool transfer tokens from `msg.sender`, which is the router:

<https://github.com/code-423n4/2023-05-maia/blob/54a45beb1428d85999da3f721f923cbf36ee3d35/src/erc-4626/UlyssesERC4626.sol#L34-L45>

```solidity
    function deposit(uint256 assets, address receiver) public virtual nonReentrant returns (uint256 shares) {
        // Need to transfer before minting or ERC777s could reenter.
        asset.safeTransferFrom(msg.sender, address(this), assets);

        shares = beforeDeposit(assets);

        require(shares != 0, "ZERO_SHARES");

        _mint(receiver, shares);

        emit Deposit(msg.sender, receiver, assets, shares);
    }
```

First, a user will lose tokens sent to the router, if a malicious user calls `addLiquidity()` after it.

### Recommended Mitigation Steps

Transfer tokens to the router via `safeTransferFrom()`:

```solidity
    function addLiquidity(uint256 amount, uint256 minOutput, uint256 poolId) external returns (uint256) {
        UlyssesPool ulysses = getUlyssesLP(poolId);
        address(ulysses.asset()).safeTransferFrom(msg.sender, address(this), amount);

        amount = ulysses.deposit(amount, msg.sender);

        if (amount < minOutput) revert OutputTooLow();
        return amount;
    }
```

### Assessed type

Access Control

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/201#issuecomment-1631643366)**

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/201#issuecomment-1655655112):**
 > We recognize the audit's findings on Ulysses AMM. These will not be rectified due to the upcoming migration of this section to Balancer Stable Pools.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | bin2chen, T1MOH |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/201
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

