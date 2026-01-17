---
# Core Classification
protocol: Level Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60875
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
source_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
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
finders_count: 4
finders:
  - Jeffrey Kam
  - Mustafa Hasan
  - Rabib Islam
  - Guillermo Escobero
---

## Vulnerability Title

Short Positions Are Not Limited, Leading to Potential Protocol Break

### Overview


The bug report states that a maximum limit has been added for global short position sizes in the Pool.sol file. However, it is the responsibility of the client to correctly set these limits. The report explains that while the maximum global long position size for a token is limited by the total amount of holdings in the vault, the maximum global short position size is only limited by the amount of stablecoin that can be used as collateral for borrowing. This means that with enough stablecoins, it is possible to open large short positions that could result in a negative value for the total assets under management. This can cause issues when users try to add or remove liquidity. The recommendation is to limit the global short position size to ensure that the assets under management are always positive.

### Original Finding Content

**Update**
Fixed. Global short position sizes can now be limited. However, it is up to the client to correctly set these limits.

**File(s) affected:**`Pool.sol`

**Description:** Although the maximum global long position size of a token (i.e. the cumulative total size of all long positions on said token) is capped at the total amount of all holdings of the token in the vault, the maximum global short position size is in practice capped only by the amount of stablecoin that can be collateralized and borrowed in order to open short positions. However, the formula for calculating the total assets under management (in dollars) with respect to a given non-stablecoin token is defined by the formula

```
aum = SignedIntOps.wrap(_asset.poolAmount).sub(_asset.reservedAmount).mul(_price).add(_asset.guaranteedValue);
aum = aum.sub(shortPnl);
```

where `poolAmount` is the amount of tokens deposited by LPs plus long position collateral, `reservedAmount` is the amount of tokens borrowed plus long position collateral, `guaranteedValue` is the value of the amount of tokens borrowed in USD, and `shortPnL` is the sum of all profits and losses of open short positions on the token.

However, since the global short position size is not capped (except by the stablecoin reserves), with large enough amounts of stablecoins in the pools, it is in theory possible to open large enough short positions on a token such that, were the token to go down, the `shortPnL` value would exceed the amount of the tokens in the pool. This would cause the total assets under management to be a negative number, causing a reversion every time `_getTrancheValue()` is called. This is particularly concerning, as the function is called whenever a user decides to add or remove liquidity.

**Recommendation:** Limit the global short position size such that assets under management is positive in all circumstances.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Level Finance |
| Report Date | N/A |
| Finders | Jeffrey Kam, Mustafa Hasan, Rabib Islam, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html

### Keywords for Search

`vulnerability`

