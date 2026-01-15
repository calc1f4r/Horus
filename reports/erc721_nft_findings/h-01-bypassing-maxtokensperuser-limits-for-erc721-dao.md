---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41385
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
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

[H-01] Bypassing `maxTokensPerUser` limits for ERC721 DAO

### Overview


The bug report is about a medium severity bug that has a high likelihood of happening. The issue occurs when users call a specific code, which performs checks and then calls another function. The problem is that there is no protection against reentrancy, which allows users to bypass the checks and buy more tokens than they are supposed to. This is especially problematic for DAOs that have whitelists, as one user can buy more tokens than allowed. The report suggests using a reentrancy guard or a different coding pattern to prevent this issue from happening.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

When users call `buyGovernanceTokenERC721DAO()` code performs max cap checks and then calls `mintToken()`. The issue is that there's no reentrancy guard and when code wants to mint tokens one by one by using `_safeMint()` user can reenter the Factory contract again in ERC721's hook function and call `buyGovernanceTokenERC721DAO()` and buy more while bypassing the checks because `_tokenIdTracker` and `balanceOf(_to) ` are still not updated fully. The impact is more severe in DAOs that have whitelists because one user can buy more than what he is supposed to.

```solidity
    function mintToken(address _to, string calldata _tokenURI, uint256 _amount) public onlyFactory(factoryAddress) {
        if (balanceOf(_to) + _amount > erc721DaoDetails.maxTokensPerUser) {
            revert MaxTokensMintedForUser(_to);
        }

        if (!erc721DaoDetails.isNftTotalSupplyUnlimited) {
            require(
                Factory(factoryAddress).getDAOdetails(address(this)).distributionAmount >= _tokenIdTracker + _amount, "Max supply reached" );
        }
        for (uint256 i; i < _amount;) {
            _tokenIdTracker += 1;
            _safeMint(_to, _tokenIdTracker);
```

This is POC:

1. User1 would call `buyGovernanceTokenERC721DAO()` to buy 10 tokens while max token for each user is 15.
2. When code wants to mint the first token for user and calls `_safeMint()` and User1's address would be called by hook function.
3. User1 would call `buyGovernanceTokenERC721DAO()` again to buy 10 more tokens and this times because the previous buy amounts has not been added to the `balanceOf(_to)` so the checks would pass.
4. As result User1 would buy 20 tokens while the max limit for each user was 15.

## Recommendations

Use reentrancy guard or use check-effect-interact pattern.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

