---
# Core Classification
protocol: Joyn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1772
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-joyn-contest
source_link: https://code4rena.com/reports/2022-03-joyn
github_link: https://github.com/code-423n4/2022-03-joyn-findings/issues/73

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - rayn
---

## Vulnerability Title

[M-12] `CoreCollection.setRoyaltyVault` doesn't check `royaltyVault.royaltyAsset` against `payableToken`, resulting in potential permanent lock of `payableTokens` in royaltyVault

### Overview


This bug report is about a vulnerability in the CoreCollection, ERC721Payable and RoyaltyVault contracts. The vulnerability can lead to minting fees being permanently stuck in the RoyaltyVault if the CoreProxy and RoyaltyVault are paired with an incompatible token. This is because the CoreProxy does not allow modifications of the pairing RoyaltyVault once assigned.

The Proof of Concept shows that if any other kind of tokens are sent to the RoyaltyVault, it would get stuck inside the vault forever. This is because the RoyaltyVault can only handle the `royaltyVault.royaltyAsset` token assigned upon creation.

The tools used to find this vulnerability were vim and ganache-cli.

The recommended mitigation step is to check if the `payableToken` is the same as `royaltyVault.royaltyAsset` when assigning vaults to CoreProxy. This can be done by adding a `require` statement in the `setRoyaltyVault` function.

### Original Finding Content

_Submitted by rayn_

<https://github.com/code-423n4/2022-03-joyn/blob/main/core-contracts/contracts/CoreCollection.sol#L185>

<https://github.com/code-423n4/2022-03-joyn/blob/main/core-contracts/contracts/ERC721Payable.sol#L50>

<https://github.com/code-423n4/2022-03-joyn/blob/main/royalty-vault/contracts/RoyaltyVault.sol#L31>

### Impact

Each CoreProxy is allowed to be associated with a RoyaltyVault, the latter which would be responsible for collecting minting fees and distributing to beneficiaries. Potential mismatch between token used in CoreProxy and RoyaltyVault might result in minting tokens being permanently stuck in RoyaltyVault.

### Proof of Concept

Each RoyaltyVault can only handle the `royaltyVault.royaltyAsset` token assigned upon creation, if any other kind of tokens are sent to the vault, it would get stuck inside the vault forever.

        function sendToSplitter() external override {
            ...
            require(
                IERC20(royaltyAsset).transfer(splitterProxy, splitterShare) == true,
                "Failed to transfer royalty Asset to splitter"
            );
            ...
            require(
                IERC20(royaltyAsset).transfer(
                    platformFeeRecipient,
                    platformShare
                ) == true,
                "Failed to transfer royalty Asset to platform fee recipient"
            );
            ...
        }

Considering that pairing of CoreProxy and RoyaltyVault is not necessarily handled automatically, and can sometimes be manually assigned, and further combined with the fact that once assigned, CoreProxy does not allow modifications of the pairing RoyaltyVault. We can easily conclude that if a CoreProxy is paired with an incompatible RoyaltyVault, the `payableToken` minting fees automatically transferred to RoyaltyVault by `_handlePayment` will get permanently stuck.

         function setRoyaltyVault(address _royaltyVault)
             external
             onlyVaultUninitialized
         {
             ...
             royaltyVault = _royaltyVault;
             ...
         }

         function _handlePayment(uint256 _amount) internal {
             address recipient = royaltyVaultInitialized()
                 ? royaltyVault
                 : address(this);
             payableToken.transferFrom(msg.sender, recipient, _amount);
             ...
         }

### Tools Used

vim, ganache-cli

### Recommended Mitigation Steps

While assigning vaults to CoreProxy, check if `payableToken` is the same as `royaltyVault.royaltyAsset`

         function setRoyaltyVault(address _royaltyVault)
             external
             onlyVaultUninitialized
         {
             require(
                 payableToken == _royaltyVault.royaltyAsset(),
                 "CoreCollection : payableToken must be same as royaltyAsset."
             );
             ...
             royaltyVault = _royaltyVault;
             ...
         }

**[sofianeOuafir (Joyn) confirmed](https://github.com/code-423n4/2022-03-joyn-findings/issues/73)** 

**[deluca-mike (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/73#issuecomment-1153010132):**
 > Downgraded to medium because, while a more automated and validated way of assigning a compatible royalty vault would prevent this issue, in the current framework you'd need to make a user error (albeit one that is not easy to spot), to lose funds.



***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Joyn |
| Report Date | N/A |
| Finders | rayn |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-joyn
- **GitHub**: https://github.com/code-423n4/2022-03-joyn-findings/issues/73
- **Contest**: https://code4rena.com/contests/2022-03-joyn-contest

### Keywords for Search

`vulnerability`

