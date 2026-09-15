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
solodit_id: 26112
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/75

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
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - T1MOH
---

## Vulnerability Title

[M-43] Deploy flow of `Talos` is broken

### Overview


A bug has been identified in the `Talos` protocol, preventing it from being deployed correctly. The `TalosBaseStrategy` needs `TalosManager` to be passed in the constructor, but the `TalosManager` needs `Strategy` to be passed into the constructor. This bug has been assessed as a Denial of Service (DoS) vulnerability. 

To mitigate this issue, it is recommended to add setters for complete deploy or initializing function. This has been addressed by 0xLightt (Maia) in the GitHub repository [here](https://github.com/Maia-DAO/eco-c4-contest/tree/75).

### Original Finding Content


The `Talos` protocol can't be deployed in a right way.

### Proof of Concept

`TalosBaseStrategy` needs `TalosManager` to be passed in the constructor:

<https://github.com/code-423n4/2023-05-maia/blob/54a45beb1428d85999da3f721f923cbf36ee3d35/src/talos/base/TalosBaseStrategy.sol#L79-L95>

```solidity
    constructor(
        IUniswapV3Pool _pool,
        ITalosOptimizer _optimizer,
        INonfungiblePositionManager _nonfungiblePositionManager,
        address _strategyManager,
        address _owner
    ) ERC20("TALOS LP", "TLP", 18) {
        ...

        strategyManager = _strategyManager;
        
        ...
    }
```

But `TalosManager` needs `Strategy` to be passed into the constructor:

<https://github.com/code-423n4/2023-05-maia/blob/54a45beb1428d85999da3f721f923cbf36ee3d35/src/talos/TalosManager.sol#L44-L56>

```solidity
   constructor(
        address _strategy,
        int24 _ticksFromLowerRebalance,
        int24 _ticksFromUpperRebalance,
        int24 _ticksFromLowerRerange,
        int24 _ticksFromUpperRerange
    ) {
        strategy = ITalosBaseStrategy(_strategy);
        
        ...
    }
```

### Recommended Mitigation Steps

Add setters for complete deploy or initializing function.

### Assessed type

DoS

**[0xLightt (Maia) confirmed](https://github.com/code-423n4/2023-05-maia-findings/issues/75#issuecomment-1631475531)**

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/75#issuecomment-1709185337):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/75).

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
| Finders | T1MOH |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/75
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

