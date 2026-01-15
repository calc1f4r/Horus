---
# Core Classification
protocol: Interpol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42134
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Interpol-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] BGT and reward tokens can be withdrawn without paying fees

### Overview


The report describes a bug in the `HoneyLocker` contract that allows the contract owner to withdraw tokens without paying fees. This is possible by calling the `withdrawLPToken()` function with a past expiration value and a zero-amount value. The report recommends implementing additional checks to prevent non-LP tokens from being withdrawn using this method. 

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

Some tokens are expected to be held by the `HoneyLocker` contract and are expected to pay fees when withdrawn. Such is the case of the BGT token, and other reward tokens.

To do that, a fee is implemented on the `withdrawBERA()` and `withdrawERC20()` tokens.

The issue lies in that it is possible to withdraw those ERC20 tokens via the `withdrawLPToken()` function:

```solidity
function withdrawLPToken(address _LPToken, uint256 _amount) external onlyOwner {
    if (expirations[_LPToken] == 0) revert HasToBeLPToken();
    if (block.timestamp < expirations[_LPToken]) revert NotExpiredYet();

    ERC20(_LPToken).transfer(msg.sender, _amount);
}
```

The function implements a `expirations[_LPToken] == 0` check to prevent non-LP tokens from being withdrawn, but this expectation can be broken by calling `depositAndLock()` with the token, a zero-amount value, and a past expiration:

```solidity
function depositAndLock(address _LPToken, uint256 _amountOrId, uint256 _expiration) external onlyOwnerOrMigratingVault {
    if (!unlocked && expirations[_LPToken] != 0 && _expiration < expirations[_LPToken]) {
        revert ExpirationNotMatching();
    }
    expirations[_LPToken] = unlocked ? 1 : _expiration;

    ERC721(_LPToken).transferFrom(msg.sender, address(this), _amountOrId);
}
```

This way, the contract owner can set a non-zero past `expirations[_LPToken]` value. This will allow them to withdraw tokens without paying fees via `withdrawLPToken()`.

## Recommendations

The `expirations[_LPToken] == 0` check in `withdrawLPToken()` is not sufficient to prevent non-LP tokens from being withdrawn with it.

Checking that the token is not the BGT token, works for it. But another whitelist check would be needed to prevent withdrawing non-LP tokens, or effectively only allowing LP-tokens to be deposited via `depositAndLock()`. Any of those options should work.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Interpol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Interpol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

