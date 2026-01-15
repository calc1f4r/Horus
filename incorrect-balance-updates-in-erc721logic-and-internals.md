---
# Core Classification
protocol: HUB v1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51878
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/concrete/hub-v1
source_link: https://www.halborn.com/audits/concrete/hub-v1
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
  - Halborn
---

## Vulnerability Title

Incorrect Balance Updates in ERC721Logic and Internals

### Overview


The `update` function in the `ERC721LogicContract` and `ERC721_Internals` contracts has a critical issue where token balances are not properly updated in storage. This can cause discrepancies in ownership and token balances, leading to potential issues in the protocol's token transfer system. A proof of concept has been provided to demonstrate this issue. To fix the problem, the `update` logic should be modified to update balances in storage, and the correct balance keys should be used for both the `from` and `to` addresses. The Concrete team has solved this issue by removing the `ERC721Logic` contract.

### Original Finding Content

##### Description

The `update` function in both `ERC721LogicContract` and `ERC721_Internals` contracts has a **critical issue** in the token balance update logic. Specifically, the balance is not properly updated in storage, as it only modifies in-memory variables without committing changes to storage using `_storage.setUint`. Additionally, the code incorrectly uses the balance key for the `from` address when attempting to update the `to` address balance, causing an inconsistency between ownership and token balances.

This issue results in token transfers that fail to properly decrement the `from` balance and increment the `to` balance, leading to a critical discrepancy in the contract’s accounting of token ownership and balances. This discrepancy could easily lead to incorrect states where users own tokens, but the balances remain inaccurate, potentially causing significant issues in the protocol's token accounting and transfer mechanisms.

##### Proof of Concept

```
    function test_invalid_balance_erc721() external {
        bytes32 tokenId = keccak256(abi.encodePacked("test"));
        ERC721Token erc721 = new ERC721Token(tokenId, address(concreteStorage));

        vm.prank(ADMIN);
        accessControlManager.grantRole(bytes4(keccak256("COMMON")), address(erc721));

        erc721.mint(USER1, 100);

        assertEq(erc721.ownerOf(100), USER1);
        // ERROR: This will revert as the balance is not updated
		// Reason 1 is due to using a memory variable instead of storage
		// Reason 2 is due to using `from` instead of `to` for the second storage.
        assertEq(erc721.balanceOf(USER1), 1);
    }
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:C/A:M/D:C/Y:C/R:N/S:C (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:C/A:M/D:C/Y:C/R:N/S:C)

##### Recommendation

To address this critical issue, the following changes should be made:

1. **Ensure storage updates**: Modify the `update` logic to call `_storage.setUint` to properly update balances in storage, not just in memory.
2. **Correct balance key usage**: When updating balances, ensure that the `from` address balance is decremented, and the `to` address balance is incremented by using the correct balance keys for both addresses. The current implementation mistakenly uses the `from` address balance key for both, which is incorrect.

##### Remediation

**SOLVED**: The **Concrete team** solved the issue by removing the `ERC721Logic` contract.

##### Remediation Hash

048a8300af178b5d745a08ebaae87ac9fb7cd381

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | HUB v1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/concrete/hub-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/concrete/hub-v1

### Keywords for Search

`vulnerability`

