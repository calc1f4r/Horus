---
# Core Classification
protocol: Fractional
chain: everychain
category: uncategorized
vulnerability_type: supportsinterface

# Attack Vector Details
attack_type: supportsinterface
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3005
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/544

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - supportsinterface
  - erc2981
  - eip-2981

protocol_categories:
  - dexes
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x29A
---

## Vulnerability Title

[M-04] The `FERC1155.sol` don't respect the EIP2981

### Overview


This bug report is about an incomplete implementation of the EIP-2981: NFT Royalty Standard. The implementation is missing the implementation of `function supportsInterface(bytes4 interfaceID) external view returns (bool);` from the EIP-165: Standard Interface Detection. This means that a marketplace implemented royalties could check if the NFT have royalties, but if the `ERC2981` interface is not added to the `_registerInterface`, the marketplace will not be able to know if the NFT has royalties. The bug was identified manually and the recommended mitigation step is to add the `ERC2981` interfaceId on the `FERC1155` contract, like in the `solmate ERC1155.sol` from the Rari-Capital repository.

### Original Finding Content

_Submitted by 0x29A_

The [EIP-2981: NFT Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981) implementation is incomplete, missing the implementation of `function supportsInterface(bytes4 interfaceID) external view returns (bool);` from the [EIP-165: Standard Interface Detection](https://eips.ethereum.org/EIPS/eip-165).

### Proof of Concept

A marketplace that implemented royalties could check if the NFT has royalties, but if they don't, add the interface of `ERC2981` on the `_registerInterface`, the marketplace can't know if this NFT has royalties.

### Recommended Mitigation Steps

Like in [solmate ERC1155.sol](https://github.com/Rari-Capital/solmate/blob/03e425421b24c4f75e4a3209b019b367847b7708/src/tokens/ERC1155.sol#L137-L146) add the `ERC2981` interfaceId on the `FERC1155` contract

```solidity
    /*//////////////////////////////////////////////////////////////
                              ERC165 LOGIC
    //////////////////////////////////////////////////////////////*/

    function supportsInterface(bytes4 interfaceId) public view  override returns (bool) {
        return
            super.supportsInterface(interfaceId) ||
            interfaceId == 0x2a55205a; // ERC165 Interface ID for ERC2981
    }
```

**[aklatham (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/544)** 

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-07-fractional-findings/issues/544#issuecomment-1208112166):**
 > The contract implements the ERC2981 getter but does not register it as a 165 interface. Agree with the warden that this is a Medium risk issue. This is a function of the protocol and it may not work with many external marketplaces because it does not yet follow the standard as expected.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | 0x29A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/544
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`supportsInterface, ERC2981, EIP-2981`

