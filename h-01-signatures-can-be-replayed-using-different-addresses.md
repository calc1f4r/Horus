---
# Core Classification
protocol: Sofamon-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41365
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Sofamon-security-review-August.md
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

[H-01] Signatures can be replayed using different addresses

### Overview


This report describes a bug in the `commitToMint` function of a smart contract. This bug allows anyone to replay signatures using different addresses, potentially leading to a loss of funds. The severity of this bug is medium and the likelihood of it occurring is high. To fix this issue, it is recommended to include the address of the executor in the hash that is signed, preventing the signature from being valid for other addresses.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `commitToMint` function in the contract allows signatures signed by the `signer` to be replayed using different addresses. Anyone can see the signatures on-chain and then replay them with different accounts that have the same nonce. An attacker can start inputting previous signatures submitted by a user starting from a nonce of 0 until the current one.

```solidity
/// @param _collectionId The Id of the collection you wish to roll for
/// @param spins The amount of spins you wish to roll
/// @param signature A signature commit to the price, nonce, and minter from the authority address
///
/// @return ticketNonce The nonce to use to claim your mint
function commitToMint(uint256 _collectionId, uint256 spins, address minter, bytes memory signature) public payable returns (uint256 ticketNonce) {
    if (msg.sender != commitController) {
        uint256 nonce = userNonce[msg.sender];
        bytes32 hash = keccak256(abi.encodePacked(_collectionId, spins, nonce, msg.value, minter));
        bytes32 signedHash = hash.toEthSignedMessageHash();
        address approved = ECDSA.recover(signedHash, signature);

        if (approved != signer) {
            revert NotApproved();
        }
    }

    if (msg.value != 0) {
        payable(protocolFeeTo).transfer(msg.value);
    }

    ticketNonce = rng.rng();

    NonceData memory data = NonceData({ owner: minter, collectionId: uint128(_collectionId), spins: uint128(spins) });

    uint256 _userNonce = userNonce[msg.sender];
    userNonce[msg.sender] = _userNonce + 1;

    dataOf[ticketNonce] = data;

    emit MintCommited(msg.sender, minter, spins, msg.value, _userNonce + 1, ticketNonce);
}
```

## Recommendations

To mitigate this issue, it is recommended to either include the address of the executor in the hash that is signed. This ensures that the signature is bound to a specific address and cannot be replayed by others. Here is a possible modification:

```solidity
bytes32 hash = keccak256(abi.encodePacked(_collectionId, spins, nonce, msg.value, minter, msg.sender));
```

This addition ensures that the `msg.sender` address is included in the hash, preventing the signature from being valid for other addresses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sofamon-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Sofamon-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

