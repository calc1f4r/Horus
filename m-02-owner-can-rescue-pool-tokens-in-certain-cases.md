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
solodit_id: 36390
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

[M-02] Owner can `rescue()` pool tokens in certain cases

### Overview


This bug report discusses a high severity issue in a pool contract that allows the owner to recover non-pool tokens from the contract. The `rescue()` function, designed for this purpose, has a vulnerability that allows the owner to bypass a check and withdraw pool tokens. This is a risk for tokens with multiple entry points, such as TUSD. There is currently no direct fix for this issue, but it is recommended to document this vulnerability and be cautious when using tokens with multiple entry points.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

The pool contract includes a `rescue()` function designed to recover non-pool tokens from the contract:

```solidity
    function rescue(address token_, address receiver_) external onlyOwner {
        uint256 _numTokens = numTokens;
        for (uint256 t = 0; t < MAX_NUM_TOKENS; t++) {
            if (t == _numTokens) break;
            if (!(token_ != tokens[t])) revert Pool__CannotRescuePoolToken();
        }
        uint256 _amount = ERC20(token_).balanceOf(address(this));
        ERC20(token_).transfer(receiver_, _amount);
    }
```

When the owner attempts to rescue a pool token, the function throws a `Pool__CannotRescuePoolToken()` error. However, the owner can bypass this check if a token has multiple entry points. For example, this was the case with the TUSD token when its secondary entry point was still active. This vulnerability remains a risk as other tokens with multiple entry points may exist.

**Recommendations**

While there is no direct fix for this issue, it is important to document that the owner can withdraw all tokens in cases where tokens have multiple entry points.

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

