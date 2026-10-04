---
# Core Classification
protocol: Tangleswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44632
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-27-Tangleswap.md
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
  - Zokyo
---

## Vulnerability Title

Possibility of incorrect minting of liquidity via finalize()

### Overview


The bug report is about a potential issue with the TangleswapCallingParams.mintParams logic, which could result in incorrect values being passed to the finalize() function. This could lead to a smaller amount of liquidity being added to the liquidity pool, with the remaining amount being left in the contract. This could potentially allow a malicious admin to drain and remove all the remaining liquidity. The report recommends implementing an access control mechanism for the finalize() function to prevent this issue.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

Depending upon the logic of TangleswapCallingParams.mintParams(which is out of scope of this audit) if the parameters-
        uint160 sqrtPriceX96,
        int24 tickLower,
        int24 tickUpper
- to the finalize() function are provided incorrect values, which are not corresponding to the getTokenAmounts() values (i.e. lesser than the expected amount), it may lead to lesser liquidity getting minted or added in the liquidity pool. The rest of the liquidity would remain in the contract and which will require an admin to intervene by removing the remaining liquidity via withdrawDeposits(), and then add it manually to the Tangleswap pool, which introduces centralization risk of a malicious admin draining and removing all the remaining liquidity. 

**Recommendation**: 

Therefore, it is advised to check if the following scenarios can arise and introduce specific measures such as an access control mechanism to finalize function so that this issue is prevented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tangleswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-27-Tangleswap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

