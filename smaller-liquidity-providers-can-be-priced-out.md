---
# Core Classification
protocol: Hifi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59630
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
source_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Zeeshan Meghji
  - Roman Rohleder
  - Souhail Mssassi
---

## Vulnerability Title

Smaller Liquidity Providers Can Be Priced Out

### Overview


The report discusses an issue with the HifiPool.sol file in the Hifi protocol. The problem is that an early liquidity provider can manipulate the share price by adding a small amount of liquidity and then transferring a large amount of the underlying token directly to the pool. This makes it difficult for other liquidity providers to add liquidity as they would need to provide a large amount of the underlying token for just one share. The Hifi team has decided not to fix this issue as it can be recreated by creating a new Hifi pool. However, they recommend implementing a solution similar to Uniswap V2, where a minimum amount of liquidity tokens are permanently locked to prevent this type of attack.

### Original Finding Content

**Update**
The Hifi team chose not to resolve the issue as ill-initialized pools can be recreated. From the Hifi team :

```
It makes sense to have this fix for a Uniswap V2 pool where the pool contract of tokens A and B could only be created once since it is created via CREATE2, but that is not the case for our protocol. In our protocol, you could always create a new Hifi pool to replace an ill-initialized Hifi pool.
```

**File(s) affected:**`packages/amm/contracts/HifiPool.sol`

**Description:** An early liquidity provider can manipulate a single share's price to raise it high enough such that only the largest providers can afford to add liquidity. The share price can be manipulated by first only adding a tiny amount of liquidity and then directly transferring a large amount of the underlying token to the pool.

**Exploit Scenario:**

1.   The first liquidity provider calls `HifiPool.mint(1)` with `1` Wei of underlying. The liquidity provider receives `1` liquidity token, which is currently the entire supply.
2.   The liquidity provider transfers `10**21` of the underlying token directly to the `HifiPool`. The liquidity token supply is still `1`, which means that `1` share is now worth `10**21 + 1` underlying tokens.
3.   If any liquidity provider wants to add liquidity, they will need to provide a minimum of `10**21` underlying tokens to obtain just `1` share.

**Recommendation:** Uniswap V2 solves a similar problem by defining a minimum amount of liquidity tokens (`10**3`) which are permanently locked. This raises the cost of the above attack by a factor of `10**3`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hifi Finance |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Roman Rohleder, Souhail Mssassi |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html

### Keywords for Search

`vulnerability`

