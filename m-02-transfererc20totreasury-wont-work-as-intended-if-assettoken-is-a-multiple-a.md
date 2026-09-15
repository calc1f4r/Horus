---
# Core Classification
protocol: Cadmos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20368
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-12-01-Cadmos.md
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
  - Pashov
---

## Vulnerability Title

[M-02] `transferERC20ToTreasury` won't work as intended if `assetToken` is a multiple-address token

### Overview


The bug report concerns ERC20 tokens that are deployed behind a proxy, where the admin is able to rug all depositors with the transferERC20ToTreasury method. The check for this method requires the token address not to be the same as the assetToken address, however, as the tokens have multiple addresses the admin can give another address and pass those checks. 

The likelihood of this bug is low, as it requires using a multiple-address token and a malicious/compromised admin. The impact, on the other hand, is high, as users can use 100% of their deposits.

The recommendation given is to check the balance of the transferred token before and after the transfer and to verify that it is the same. This would be a better approach than checking the address of the transferred token.

### Original Finding Content

**Likelihood:**
Low, because it requires using a multiple-address token and a malicious/compromised admin

**Impact:**
High, because users can use 100% of their deposits

**Description**

Some ERC20 tokens on the blockchain are deployed behind a proxy, so they have at least 2 entry points (the proxy and the implementation) for their functionality. Example is Synthetix’s `ProxyERC20` contract from where you can interact with `sUSD, sBTC etc). If such a token was used as the `assetToken`token in an InvestmentPool, then the admin will be able to rug all depositors with the`transferERC20ToTreasury` method, even though it has the following check

```solidity
require(tokenAddress != _assetTokenAddress, "IP: Asset transfer");
```

Since the tokens have multiple addresses the admin can give another address and pass those checks.

**Recommendations**

Instead of checking the address of the transferred token, it is a better approach to check the balance of it before and after the transfer and to verify it is the same.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Cadmos |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-12-01-Cadmos.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

