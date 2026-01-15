---
# Core Classification
protocol: Linea Spingame
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50056
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
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
finders_count: 4
finders:
  - Alex Roan
  - Giovanni Di Siena
  - Immeas
  - Farouk
---

## Vulnerability Title

Native token prizes cannot be funded due to missing `receive()` function

### Overview


This bug report is about a problem with SpinGame, which is a game that gives out prizes in different types of tokens. One of these types is native tokens, but there is an issue that is preventing users from successfully claiming these prizes. The problem is that the Spin contract does not have a way to receive native tokens, which means that the team responsible for maintaining the contract's token balance cannot fund it with these tokens. This makes it impossible for users to claim native token prizes. The bug has been fixed by adding a function to the contract that allows it to receive native tokens. This fix has been verified and is now available in the latest version of the contract.

### Original Finding Content

**Description:** SpinGame supports multiple prize types, including ERC721, ERC20, and native tokens, where native tokens are represented as `prize.tokenAddress = address(0)`.

To ensure that prizes can be successfully claimed, the protocol team is responsible for maintaining a sufficient token balance in the contract by transferring the necessary assets to the Spin contract.

However, there is an issue specifically with native token prizes: the Spin contract does not have a `receive()` or `fallback()` function, and none of its functions are `payable`. This means there is no way for the team to fund the contract with native tokens using a standard transfer, preventing users from successfully claiming native token prizes.

**Impact:** Native token prizes cannot be claimed because there is no mechanism to deposit native tokens into the contract. The only way to provide a native token balance would involve esoteric workarounds, such as self-destructing a contract that sends funds to the Spin contract.


**Proof of Concept:** Add the following test to `Spin.t.sol`:
```solidity
function testTransferNativeToken() public {
    vm.deal(admin,1e18);

    vm.prank(admin);
    (bool success, ) = address(spinGame).call{value: 1e18}("");

    // transfer failed as there is no `receive` or `fallback` function
    assertFalse(success);
}
```

**Recommended Mitigation:** Consider adding a `receive()` function to the contract to allow native token deposits:

```solidity
receive() external payable {}
```

**Linea:** Fixed in commit [`d1ab4bd`](https://github.com/Consensys/linea-hub/commit/d1ab4bdbaac3639a36d66440b9e6da95771e4b34)

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Linea Spingame |
| Report Date | N/A |
| Finders | Alex Roan, Giovanni Di Siena, Immeas, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

