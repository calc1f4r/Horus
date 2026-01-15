---
# Core Classification
protocol: Nume
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31636
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-03-05-Nume.md
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
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] NFT Withdrawal request is not deleted after successful withdrawal

### Overview


This bug report discusses an issue with the withdrawal process for NFTs (non-fungible tokens) on a platform. The severity of the bug is high as it can lead to attackers stealing users' NFTs. The likelihood of the bug occurring is medium, as it requires the user to re-deposit their NFT. 

The bug occurs because the withdrawal request for NFTs is not properly deleted after the withdrawal is performed. This means that a user can withdraw the same NFT multiple times, even after selling it to someone else. 

To fix this issue, the report recommends making a small change to the code. Instead of deleting the user's request from a memory array, it should be deleted from a storage array. This ensures that the withdrawal request is properly deleted and cannot be used again by the user. 

In summary, this bug report highlights the importance of properly deleting withdrawal requests to prevent attackers from stealing NFTs. It also provides a simple solution to fix the issue.

### Original Finding Content

**Severity**

**Impact:** High. Attacker can steal user's nfts.

**Likelihood:** Medium. It requires re-deposit of NFT

**Description**

Withdrawal backend nft request is incorrectly deleted after performing withdrawal.

Here you can see that delete is performed on memory array instead of storage:

```solidity
    function withdrawNFT(
        address _user,
        address _nftContractAddress,
        uint256 _tokenId,
        bool _mintedNft,
        uint256 _queueIndex,
        bool _isContractWithdrawal
    ) external nonReentrant {
        AppStorage.enforceExodusMode();

        AppStorage.NumeStorage storage ns = AppStorage.numeStorage();

        bytes32 queueItem = keccak256(
            abi.encodePacked(_user, _nftContractAddress, _tokenId, _mintedNft)
        );

        if (_isContractWithdrawal) {
            ...
        } else {
@>          bytes[] memory userBackendNftWithdrawalRequests = ns
                .userBackendNftWithdrawalRequests[_user];
            require(
                _queueIndex <= userBackendNftWithdrawalRequests.length,
                "NFTWithdrawalsFacet: Invalid queue index"
            );
            (
                address user,
                address nftContractAddress,
                uint256 tokenId,
                bool mintedNft
            ) = abi.decode(
                    userBackendNftWithdrawalRequests[_queueIndex - 1],
                    (address, address, uint256, bool)
                );
            PaymentUtils.payNft(user, nftContractAddress, tokenId, mintedNft);
@>          delete userBackendNftWithdrawalRequests[_queueIndex - 1];
        }

        emit NFTWithdrawn(_user, _nftContractAddress, _tokenId, _mintedNft);
    }
```

It means actually user's withdrawal request is not deleted after withdrawal. It allows user to withdraw the same nft multiple times.
Suppose following scenario:

1. User1 deposits NFT.
2. User1 withdraws NFT via `withdrawNFT()`. His request is still.
3. User1 sells NFT to User2.
4. User2 deposits NFT. But now User1 has ability withdraw it.

**Recommendations**

```diff
    function withdrawNFT(
        address _user,
        address _nftContractAddress,
        uint256 _tokenId,
        bool _mintedNft,
        uint256 _queueIndex,
        bool _isContractWithdrawal
    ) external nonReentrant {
        ...

        if (_isContractWithdrawal) {
            ...
        } else {
            bytes[] memory userBackendNftWithdrawalRequests = ns
                .userBackendNftWithdrawalRequests[_user];
            require(
                _queueIndex <= userBackendNftWithdrawalRequests.length,
                "NFTWithdrawalsFacet: Invalid queue index"
            );
            ...
            PaymentUtils.payNft(user, nftContractAddress, tokenId, mintedNft);
-           delete userBackendNftWithdrawalRequests[_queueIndex - 1];
+           delete ns.userBackendNftWithdrawalRequests[_user][_queueIndex - 1];
        }

        emit NFTWithdrawn(_user, _nftContractAddress, _tokenId, _mintedNft);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nume |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-03-05-Nume.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

