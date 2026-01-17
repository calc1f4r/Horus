---
# Core Classification
protocol: Phi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41106
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-phi
source_link: https://code4rena.com/reports/2024-08-phi
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] Missing receiver address validation during `artId` creation in `_initializePhiArt()` could DOS future claiming

### Overview

See description below for full details.

### Original Finding Content


When an `artId` is being created, the `_initializeArt()` function is called as part of the process. In this function the receiver address is stored in the PhiArt struct. The issue is that this address is not validated to not be `address(0)`.

```solidity
File: PhiFactory.sol
642:     function _initializePhiArt(PhiArt storage art, ERC1155Data memory createData_) private {
643:         (
644:             uint256 credId,
645:             address credCreator,
646:             string memory verificationType,
647:             uint256 credChainId,
648:             bytes32 merkleRootHash
649:         ) = abi.decode(createData_.credData, (uint256, address, string, uint256, bytes32));
650: 
651:         ...
658:         art.receiver = createData_.receiver;
659:         ...
```

Due to this, during merkle or signature claiming from factory, the call would revert. This is because the `handleRewardsAndGetValueSent()` function calls the `depositRewards()` function that expects the receiver address of the artist to be non-zero as seen [here](https://github.com/code-423n4/2024-08-phi/blob/8c0985f7a10b231f916a51af5d506dd6b0c54120/src/reward/PhiRewards.sol#L93).

```solidity
  function claimFromFactory(
        uint256 artId_,
        address minter_,
        address ref_,
        address verifier_,
        uint256 quantity_,
        bytes32 data_,
        string calldata imageURI_
    )
        external
        payable
        whenNotPaused
        onlyPhiFactory
    {
        ...

        IPhiRewards(payable(phiFactoryContract.phiRewardsAddress())).handleRewardsAndGetValueSent{ value: msg.value }(
            artId_, credId, quantity_, mintFee(tokenId_), addressesData_, credChainId == block.chainid
        );
    }
```

### Solution

Add the zero address check during `artId` creation, i.e., in `_initializePhiArt()` function.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Phi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-phi
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-08-phi

### Keywords for Search

`vulnerability`

