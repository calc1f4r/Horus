---
# Core Classification
protocol: Lucidly June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36395
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Lucidly-security-review-June.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] Certain stablecoins cannot be added to Pool

### Overview


This bug report discusses an issue with a protocol that is supposed to work with different types of tokens. However, there is a problem with the code that checks for the number of decimals in the tokens. This check only allows tokens with 18 decimals to be added to the pool, but popular stablecoins like USDC and USDT have only 6 decimals. This means that these tokens cannot be added to the pool. The recommendation is to remove the check for 18 decimals to allow for the addition of these popular stablecoins.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

The protocol aims to work with standard tokens, stablecoins, and LRTs, but in the constructor and the `addToken` function, there's a check ensuring that token decimals equal 18.

From constructor:

```solidity
            if (ERC20(tokens_[t]).decimals() != 18) {
                revert Pool__InvalidDecimals();
            }
```

From `addToken`:

```
        if (ERC20(token_).decimals() != 18) revert Pool__InvalidParams();
```

Most popular stablecoins like [USDC](https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48) and [USDT](https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7), do not have 18 decimals but 6, and as such cannot be added to the pool.

**Recommendations**

Recommend removing the check for decimals being 18.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Lucidly June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Lucidly-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

