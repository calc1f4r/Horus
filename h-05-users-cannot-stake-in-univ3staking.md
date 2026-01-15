---
# Core Classification
protocol: Dyad
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41692
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Dyad-security-review.md
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

protocol_categories:
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-05] Users cannot stake in `UniV3Staking`

### Overview


This bug report discusses an issue with the `UniswapV3Staking.stake()` function, which is used to pull NFTs from users. The problem is that the function calls a non-existent function, `onERC721Received()`, which causes the transfer to fail and the execution of `stake()` to revert. To fix this issue, the report recommends implementing the `onERC721Received()` function in the contract.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

`UniswapV3Staking.stake()` pulls NFTs from the user in the following way:

```solidity
        positionManager.safeTransferFrom(msg.sender, address(this), tokenId);
```

However, this will end up calling the `onERC721Received()` function on the `UniswapV3Staking` contract, and expect a return value. However since that function is not implemented in this contract, the ERC721 transfer will fail, reverting the execution of `stake()`.

## Recommendations

Implement the following function to ensure that ERC721's can be received via `safeTransferFrom()`:

```solidity
function onERC721Received(address, address, uint256, bytes calldata) public pure returns (bytes4) {
        return msg.sig;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Dyad |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Dyad-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

