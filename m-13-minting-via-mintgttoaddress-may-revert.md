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
solodit_id: 41409
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
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

[M-13] Minting via mintGTToAddress may revert

### Overview


This bug report discusses an issue with minting ERC721 DAO tokens using the `mintGTToAddress()` function. The problem arises when the user tries to mint more tokens than the maximum limit allowed. The current code checks for this limit after each mint, causing the transaction to revert and the tokens not to be minted. The recommendation is to move the check outside of the loop to prevent this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When minting ERC721 DAO tokens via `mintGTToAddress()` a check is performed to validate that the user won't end up with more than the max limit:

```solidity
    uint256 length = _userAddress.length;
    for (uint256 i; i < length;) {
        for (uint256 j; j < _amountArray[i];) {
@>          if (balanceOf(_userAddress[i]) + _amountArray[i] > erc721DaoDetails.maxTokensPerUser) {
@>              revert MaxTokensMintedForUser(_userAddress[i]);
@>          }

            _tokenIdTracker += 1;
            _safeMint(_userAddress[i], _tokenIdTracker);
            _setTokenURI(_tokenIdTracker, _tokenURI[i]);
            unchecked {
                ++j;
            }
        }
    }
```

So, for example, if the user has 0 NFTs, the max limit is 10, and 10 tokens are minted it should succeed as `0 (balance) + 10 (amount) <= 10 (maxTokensPerUser)`.

The problem is that this check will be performed after each mint. So, on the next iteration the balance will be one, and `1 (balance) + 10 (amount) <= 10 (maxTokensPerUser)` will be false. This will make the transaction revert, and the tokens won't be minted.

## Recommendations

Consider moving the `if` check outside of the `j` loop:

```diff
    uint256 length = _userAddress.length;
    for (uint256 i; i < length;) {
+       if (balanceOf(_userAddress[i]) + _amountArray[i] > erc721DaoDetails.maxTokensPerUser) {
+           revert MaxTokensMintedForUser(_userAddress[i]);
+       }
        for (uint256 j; j < _amountArray[i];) {
-           if (balanceOf(_userAddress[i]) + _amountArray[i] > erc721DaoDetails.maxTokensPerUser) {
-               revert MaxTokensMintedForUser(_userAddress[i]);
-           }

            _tokenIdTracker += 1;
            _safeMint(_userAddress[i], _tokenIdTracker);
            _setTokenURI(_tokenIdTracker, _tokenURI[i]);
            unchecked {
                ++j;
            }
        }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

