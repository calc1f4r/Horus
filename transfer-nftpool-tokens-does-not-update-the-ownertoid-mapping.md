---
# Core Classification
protocol: Gorples EVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51296
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/entangle-labs/gorples-evm
source_link: https://www.halborn.com/audits/entangle-labs/gorples-evm
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
  - Halborn
---

## Vulnerability Title

Transfer NFTPool Tokens Does Not Update the ownerToId Mapping

### Overview


The report describes a bug in the NFTPool contract where token holders are able to transfer NFTs to each other, but the mapping that keeps track of token ownership is not being updated. This means that token holders can have more than one token, even though this may not be intended. The bug was proven using a test and the recommendation is to either update the mapping upon transfers or disable the transferability of NFTPool tokens. The Entangle team has solved this issue by only allowing NFT transfers to the null address.

### Original Finding Content

##### Description

As indicated in the `Transfer NFTPool Tokens Allow Users To Have More Than One NFT` finding, the NFTPool contract allows token holders to transfer NFTs between each other. This does not only allow addresses to have more than one token, but it was observed that the mapping in charge of keeping track of token ownership (`ownerToId`) was not being updated upon transfers.

If NFTPool token transfers should be allowed, it would be necessary to override the OpenZeppelin's ERC721 library functions in charge of such transfers so they properly update the `ownerToId`.

##### Proof of Concept

The following `Foundry` test was used in order to prove the aforementioned issue:

```
// ownerToId should be updated after transferring a NFTPool token
// Fail: ownerToId IS NOT UPDATED
function testFailownerToIdTransferedNFT() public {
    // Needs to add the pool to the master borpa
    masterBorpa.add(address(nftPool), 100);

    mockERC20.approve(address(nftPool), 1);
    nftPool.createPosition(1, address(this));
    assertEq(nftPool.ownerToId(address(this)), 1);
    assertEq(nftPool.ownerToId(attacker), 0);

    nftPool.safeTransferFrom(address(this), attacker, 1);

    mockERC20.transfer(attacker, 1);

    assertEq(nftPool.ownerToId(address(this)), 0);
    assertEq(nftPool.ownerToId(attacker), 1);
}
```

To run it, just execute the following `forge` command:

```
forge test --mt testFailownerToIdTransferedNFT -vvvvvv
```

Observe that the test passes because the last two assertions fail. This is because after transferring the token ID 1, the `ownerToId` mapping is outdated and does not reflect the actual owner:

```
...
 [517713] NFTPoolTest::testFailownerToIdTransferedNFT()
...
    ├─ [0] VM::assertEq(1, 0) [staticcall]
    │   └─ ← [Revert] assertion failed: 1 != 0
    └─ ← [Revert] assertion failed: 1 != 0

Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 8.43ms (554.88µs CPU time)

Ran 1 test suite in 928.72ms (8.43ms CPU time): 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

To address this vulnerability and align with the expected behavior, it is recommended to implement additional logic within the NFTPool contract to update the `ownerToId` upon transfers or disable the transferability of NFTPool tokens altogether to prevent unintended token ownership changes.

### Remediation Plan

**SOLVED:** The **Entangle team** solved this issue by only allowing the NFT transfers to `address(0)`.

##### Remediation Hash

<https://github.com/Entangle-Protocol/borpa/commit/d2cbafadc671fdfdc9ad2229b7700591e171b185>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Gorples EVM |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/entangle-labs/gorples-evm
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/entangle-labs/gorples-evm

### Keywords for Search

`vulnerability`

