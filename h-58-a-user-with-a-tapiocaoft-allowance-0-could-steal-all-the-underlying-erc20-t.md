---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27548
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/219

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - carrotsmuggler
  - bin2chen
  - 0x73696d616f
  - dirk\_y
  - chaduke
---

## Vulnerability Title

[H-58] A user with a TapiocaOFT allowance >0 could steal all the underlying ERC20 tokens of the owner

### Overview


The `TapiocaOFT.sol` contract allows users to wrap ERC20 tokens into an OFTV2 type contract to allow for seamless cross-chain use. A bug has been discovered in the `_wrap` method of the contract, which allows a user with a non-zero allowance to keep using the same allowance to spend the owner's tokens. This means that if an owner had 100 tokens and gave an allowance of 10 to a spender, that spender would be able to spend all 100 tokens in 10 transactions. 

The bug occurs because the allowance of the user is checked, but this isn't checking the underlying ERC20 allowance, but the allowance of the current contract (the TapiocaOFT). When a user wants to wrap a non-native ERC20 token into a TapiocaOFT they call `wrap` which calls `_wrap` under the hood, and this is where the bug is. 

The recommended mitigation step for this bug is to require that the sender must be the owner of the ERC20 tokens being wrapped in order to use the contract. This would prevent users from being able to steal all of the owner's tokens, as they would not be able to approve the `TapiocaOFT` contract to spend their tokens. The code change suggested for this is to remove the allowance check and replace it with a requirement that the sender must be the owner. 

This bug has been confirmed by 0xRektora (Tapioca).

### Original Finding Content


The `TapiocaOFT.sol` contract allows users to wrap ERC20 tokens into an OFTV2 type contract to allow for seamless cross-chain use.

As with most ERC20 tokens, owners of tokens have the ability to give an allowance to another address to spend their tokens. This allowance should be decremented every time a user spends the owner's tokens. However the `TapiocaOFT.sol` `_wrap` method contains a bug that allows a user with a non-zero allowance to keep using the same allowance to spend the owner's tokens.

For example, if an owner had 100 tokens and gave an allowance of 10 to a spender, that spender would be able to spend all 100 tokens in 10 transactions.

### Proof of Concept

When a user wants to wrap a non-native ERC20 token into a TapiocaOFT they call `wrap` which calls `_wrap` under the hood:

        function _wrap(
            address _fromAddress,
            address _toAddress,
            uint256 _amount
        ) internal virtual {
            if (_fromAddress != msg.sender) {
                require(
                    allowance(_fromAddress, msg.sender) >= _amount,
                    "TOFT_allowed"
                );
            }
            IERC20(erc20).safeTransferFrom(_fromAddress, address(this), _amount);
            _mint(_toAddress, _amount);
        }

If the sender isn't the owner of the ERC20 tokens being wrapped, the allowance of the user is checked. However this isn't checking the underlying ERC20 allowance, but the allowance of the current contract (the TapiocaOFT).

Next, the underlying ERC20 token is transferred from the owner to this address. This decrements the allowance of the sender, however the sender isn't the original message sender, but this contract.

In order to use this contract as an owner (Alice) I would have to approve the `TapiocaOFT` contract to spend my ERC20 tokens, and it is common to approve this contract to spend all my tokens if I trust the contract. Now let's say I approved another user (Bob) to spend some (let's say 5) of my `TapiocaOFT` tokens. Bob can now call `wrap(aliceAddress, bobAddress, 5)` as many times as he wants to steal all of Alice's tokens.

### Recommended Mitigation Steps

In my opinion you shouldn't be able to wrap another user's ERC20 tokens into a different token, because this is a different action to spending. Also, there is no way to decrement the allowance of the user (of the TapiocaOFT token) in the same call as we aren't actually transferring any tokens; there is no function selector in the ERC20 spec to decrease an allowance from another contract.

Therefore I would suggest the following change:

    diff --git a/contracts/tOFT/BaseTOFT.sol b/contracts/tOFT/BaseTOFT.sol
    index 5658a0a..e8b7f63 100644
    --- a/contracts/tOFT/BaseTOFT.sol
    +++ b/contracts/tOFT/BaseTOFT.sol
    @@ -350,12 +350,7 @@ contract BaseTOFT is BaseTOFTStorage, ERC20Permit {
             address _toAddress,
             uint256 _amount
         ) internal virtual {
    -        if (_fromAddress != msg.sender) {
    -            require(
    -                allowance(_fromAddress, msg.sender) >= _amount,
    -                "TOFT_allowed"
    -            );
    -        }
    +        require (_fromAddress == msg.sender, "TOFT_allowed");
             IERC20(erc20).safeTransferFrom(_fromAddress, address(this), _amount);
             _mint(_toAddress, _amount);
         }

**[0xRektora (Tapioca) confirmed](https://github.com/code-423n4/2023-07-tapioca-findings/issues/219#issuecomment-1685311808)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | carrotsmuggler, bin2chen, 0x73696d616f, dirk\_y, chaduke |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/219
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

