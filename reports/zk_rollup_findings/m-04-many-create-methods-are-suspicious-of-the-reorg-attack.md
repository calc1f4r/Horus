---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: chain_reorganization_attack

# Attack Vector Details
attack_type: chain_reorganization_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26073
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/861

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
  - chain_reorganization_attack

protocol_categories:
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Breeje
---

## Vulnerability Title

[M-04] Many `create` methods are suspicious of the reorg attack

### Overview


A bug report was submitted about a possible reorg attack in the `createTalosV3Strategy` method of the `TalosStrategyStaked` contract. This bug is particularly concerning for chains like Arbitrum and Polygon, as a reorg attack can last a few minutes, allowing someone to create the `TalosStrategyStaked` contract and transfer funds to it using the `deposit` method. The same issue can affect factory contracts in Ulysses omnichain contracts as well, with more severe consequences.

The impact of this bug is the potential for fund exploits. The tools used to identify the bug were VS Code.

The recommended mitigation steps to prevent this bug from happening in the future are to deploy such contracts via `create2` with `salt`. This bug was addressed in the Maia-DAO/eco-c4-contest repository. The severity of the bug was determined to be low, as there is no loss of funds when a reorg attack happens.

### Original Finding Content


### Proof of Concept

There are many instances of this; but to understand things better, take the example of the `createTalosV3Strategy` method.

The `createTalosV3Strategy` function deploys a new `TalosStrategyStaked` contract using the `create` method, where the address derivation depends only on the arguments passed.

At the same time, some of the chains like Arbitrum and Polygon are suspicious of the reorg attack.

```solidity
File: TalosStrategyStaked.sol

  function createTalosV3Strategy(
        IUniswapV3Pool pool,
        ITalosOptimizer optimizer,
        BoostAggregator boostAggregator,
        address strategyManager,
        FlywheelCoreInstant flywheel,
        address owner
    ) public returns (TalosBaseStrategy) {
        return new TalosStrategyStaked( // @audit-issue Reorg Attack
                pool,
                optimizer,
                boostAggregator,
                strategyManager,
                flywheel,
                owner
            );
    }

```

[Link to Code](https://github.com/code-423n4/2023-05-maia/blob/main/src/talos/TalosStrategyStaked.sol#L28)

Even more, the reorg can be a couple of minutes long. So, it is quite enough to create the `TalosStrategyStaked` and transfer funds to that address using the `deposit` method; especially when someone uses a script and not doing it by hand.

Optimistic rollups (Optimism/Arbitrum) are also suspect to reorgs. If someone finds a fraud, the blocks will be reverted, even though the user receives a confirmation.

The same issue can affect factory contracts in Ulysses omnichain contracts as well, with more severe consequences.

You can refer to this issue previously reported, [here](https://code4rena.com/reports/2023-04-frankencoin#m-14-re-org-attack-in-factory), to have a better understanding of it.

### Impact

Exploits involving the stealing of funds.

### Tools Used

VS Code

### Recommended Mitigation Steps

Deploy such contracts via `create2` with `salt`.

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/861#issuecomment-1640083554)**

**[T1MOH (warden) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/861#issuecomment-1651485343):**
 > In my opinion, low severity is more appropriate as there is no loss of funds when reorg attack happens.
 >
> >So, it is quite enough to create the `TalosStrategyStaked` and transfer funds to that address using the `deposit` method; especially when someone uses a script and not doing it by hand.
> 
> But in the described scenario, there is no loss of funds of users, as they deposit to `TalosStrategyStaked` and receive shares in exchange. So they don't lose funds, because anytime they can exchange shares back. The report lacks severe impact and is more of an informational type.

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/861#issuecomment-1708800852):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/861)

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | Breeje |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/861
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`Chain Reorganization Attack`

