---
# Core Classification
protocol: NFTMirror_2024-12-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50036
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/NFTMirror-security-review_2024-12-30.md
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

[C-01] Anyone can re-mint a token that was burned by the owner

### Overview


This bug report talks about an issue with token minting on the Beacon contract. It is considered a high severity bug with a high likelihood of occurring. The problem is that tokens can be burned by the owner and then minted again, even though they are supposed to be locked. This is because the code does not lock the tokens after they are burned. The report suggests a solution to add a line of code to lock the tokens after they are burned.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

The minting of tokens is restricted to the beacon contract by enforcing in the `_beforeTokenTransfer` hook that only the beacon can transfer locked tokens. As the default status of a token is locked, non-existing tokens are expected to be locked.

```solidity
    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal view override {
        if (msg.sender != BEACON_CONTRACT_ADDRESS) {
@>          if (tokenIsLocked(tokenId)) revert CallerNotBeacon();
        }
```

However, it has not been taken into account that tokens can be burned by the owner when they are not locked, and after they are burned, they are kept unlocked. This allows anyone to mint them again.

```solidity
    function burn(uint256 tokenId) external {
        if (tokenIsLocked(tokenId)) {
            _burn(tokenId);
        } else {
@>          _burn(msg.sender, tokenId);
        }
    }
```

#### Proof of concept

```solidity
function testBurnAndMint() public {
    testUnlockTokens_ShadowCollection();

    vm.prank(baycShadow.ownerOf(tokenId));
    baycShadow.burn(tokenId);

    assertEq(baycShadow.tokenIsLocked(tokenId), false);
    baycShadow.mint(recipient, tokenId);
}
```

## Recommendations

Lock tokens after they are burned by the owner.

```diff
    function burn(uint256 tokenId) external {
        if (tokenIsLocked(tokenId)) {
            _burn(tokenId);
        } else {
            _burn(msg.sender, tokenId);
+           _setExtraData(tokenId, LOCKED);
        }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | NFTMirror_2024-12-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/NFTMirror-security-review_2024-12-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

