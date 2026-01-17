---
# Core Classification
protocol: AegisVault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41330
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AegisVault-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-01] Owner can sweep tokens in certain cases

### Overview

See description below for full details.

### Original Finding Content

The AegisVaultCore includes a `sweepExtraTokens()` function designed to recover non-vault tokens from the contract:

```solidity
    function sweepExtraTokens(address _token, address _recipient) external override {
        _onlyAdmin();
        require(
            _token != address(depositVault) && _token != address(targetVault) && _token != address(depositToken)
                && _token != address(targetToken),
            "WTK"
        );

        IERC20 token = IERC20(_token);
        uint256 tokenBalance = token.balanceOf(address(this));
        require(tokenBalance > 0, "ZBL");
        token.safeTransfer(_recipient, tokenBalance);

        emit SweepExtraTokens(msg.sender, _token, _recipient, tokenBalance);
    }
```

When the owner attempts to rescue a vault token, the function throws a "WTK" error. However, the owner can bypass this check if a token has multiple entry points. For example, this was the case with the TUSD token when its secondary entry point was still active. This vulnerability remains a risk as other tokens with multiple entry points may exist. While there is no direct fix for this issue, it is important to document that the owner can withdraw all tokens in cases where tokens have multiple entry points.

## Solo labs comments

_While the Aegis owner cannot recover deposit and target tokens when they are implemented as standard ERC20 tokens, recovery could potentially be possible if these tokens have multiple entry points. However, this scenario is highly unlikely, as such tokens are rare and not typically used in ICHI vaults. If the need for an Aegis contract that handles such tokens ever arises, it will be evaluated on a case-by-case basis._

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AegisVault |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AegisVault-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

