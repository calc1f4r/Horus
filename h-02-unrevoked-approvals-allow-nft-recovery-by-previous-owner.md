---
# Core Classification
protocol: Superposition
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41513
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-superposition
source_link: https://code4rena.com/reports/2024-08-superposition
github_link: https://github.com/code-423n4/2024-08-superposition-findings/issues/160

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
finders_count: 10
finders:
  - ZanyBonzy
  - Nikki
  - oakcobalt
  - zhaojohnson
  - Testerbot
---

## Vulnerability Title

[H-02] Unrevoked approvals allow NFT recovery by previous owner

### Overview


The bug report describes a vulnerability in a smart contract that allows the previous owner of a token to reclaim it after it has been transferred to a new owner. This is because the approval status for the token is not revoked upon transfer, allowing the previous owner (or any approved address) to use the approval mechanism to re-transfer the token back to themselves. This can lead to potential exploitation, loss of assets, and decreased trust in the platform. To fix this, the contract should be updated to revoke approvals upon transfer. This issue has been confirmed by a third party and has been deemed high-risk.

### Original Finding Content


The vulnerability arises from the fact that after a token transfer, the approval status for the token is not revoked. Specifically, the `getApproved[_tokenId]` is not updated on transfer. This allows the previous owner (or any approved address) to reclaim the NFT by using the approval mechanism to re-transfer the token back to themselves. This is critical because the new owner of the NFT may lose their asset without realizing it, leading to potential exploitation, loss of assets, and decreased trust in the platform.

### Details

In the provided `approve` function, any user can approve themselves or another address for a specific token ID:

```solidity
/// @inheritdoc IERC721Metadata
function approve(address _approved, uint256 _tokenId) external payable {
    _requireAuthorised(msg.sender, _tokenId);
    getApproved[_tokenId] = _approved;
}
```

Since the approval is not revoked upon transfer, the previous owner retains the ability to re-transfer the NFT. The `_requireAuthorised` function is the only check on transfer permission:

```solidity
function _requireAuthorised(address _from, uint256 _tokenId) internal view {
    // revert if the sender is not authorised or the owner
    bool isAllowed =
        msg.sender == _from ||
        isApprovedForAll[_from][msg.sender] ||
        msg.sender == getApproved[_tokenId];

    require(isAllowed, "not allowed");
    require(ownerOf(_tokenId) == _from, "_from is not the owner!");
}
```

### Step-by-Step PoC:

1. **Initial Approval**: The owner of a token (`owner1`) approves an address (`addr2`) to transfer their token.
2. **Token Transfer**: The token is transferred from `owner1` to `newOwner`.
3. **Approval Not Revoked**: The approval for `addr2` is not revoked after the transfer.
4. **NFT Recovery**: `addr2` can still use their approval to transfer the NFT back to themselves, effectively recovering the NFT from `newOwner`.

There is no existing tests for this specific smart contract (because it is in solidity). A coded POC for this easy-to-understand vulnerability would involve to create all deployment logic.

### Recommended Mitigation Steps

To prevent this vulnerability, any existing approvals should be revoked when a token is transferred. This can be achieved by adding a line in the transfer function to clear the approval:

```solidity
getApproved[_tokenId] = address(0);
```

This line should be added to the token transfer function to ensure that any previously approved addresses cannot transfer the NFT after it has been sold or transferred to a new owner.

### Assessed type

Token-Transfer

**[af-afk (Superposition) confirmed via duplicate issue #56](https://github.com/code-423n4/2024-08-superposition-findings/issues/56#event-14300401337)** 

**[0xsomeone (judge) commented](https://github.com/code-423n4/2024-08-superposition-findings/issues/160#issuecomment-2369621226):**
 > The submission details how approvals are not cleared whenever an NFT transfer occurs, permitting the NFT to be recovered after it has been transferred which breaks a crucial invariant of NFTs and would affect any and all integrations of the NFT (i.e., staking systems, marketplaces, etc.). As such, I believe a high-risk severity rating is appropriate.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Superposition |
| Report Date | N/A |
| Finders | ZanyBonzy, Nikki, oakcobalt, zhaojohnson, Testerbot, SpicyMeatball, SBSecurity, IzuMan, Shubham, Japy69 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-superposition
- **GitHub**: https://github.com/code-423n4/2024-08-superposition-findings/issues/160
- **Contest**: https://code4rena.com/reports/2024-08-superposition

### Keywords for Search

`vulnerability`

