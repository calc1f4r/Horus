---
# Core Classification
protocol: Bridge Mutual
chain: everychain
category: reentrancy
vulnerability_type: reentrancy

# Attack Vector Details
attack_type: reentrancy
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13488
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/03/bridge-mutual/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - reentrancy
  - erc1155

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Daniel Luca
  - Sergii Kravchenko
---

## Vulnerability Title

Re-entrancy issue for ERC1155 ✓ Fixed

### Overview


This bug report is about an issue with ERC1155 tokens and their callback functions. When `safeTransferFrom` is used in the `LiquidityMining` contract, multiple transfers are done for each user and any receiver of the tokens can revert the transfer. This results in nobody being able to receive their tokens. To resolve this issue, the code was changed to move the `isNFTDistributed = true;` before the token transfers and only transferring tokens to the message sender. To prevent this issue from occurring in the future, it is recommended to add a reentrancy guard and to avoid transferring tokens for different receivers in a single transaction.

### Original Finding Content

#### Resolution



Addressed by moving `isNFTDistributed = true;` before the token transfers and only transferring tokens to the message sender.


#### Description


ERC1155 tokens have callback functions on some of the transfers, like `safeTransferFrom`, `safeBatchTransferFrom`. During these transfers, the `IERC1155ReceiverUpgradeable(to).onERC1155Received` function is called in the `to` address.


For example, `safeTransferFrom` is used in the `LiquidityMining` contract:


**code/contracts/LiquidityMining.sol:L204-L224**



```
function distributeAllNFT() external {
    require(block.timestamp > getEndLMTime(),
        "2 weeks after liquidity mining time has not expired");
    require(!isNFTDistributed, "NFT is already distributed");

    for (uint256 i = 0; i < leaderboard.length; i++) {
        address[] memory \_groupLeaders = groupsLeaders[leaderboard[i]];

        for (uint256 j = 0; j < \_groupLeaders.length; j++) {
            \_sendNFT(j, \_groupLeaders[j]);
        }
    }

    for (uint256 i = 0; i < topUsers.length; i++) {
        address \_currentAddress = topUsers[i];
        LMNFT.safeTransferFrom(address(this), \_currentAddress, 1, 1, "");
        emit NFTSent(\_currentAddress, 1);
    }

    isNFTDistributed = true;
}

```
During that transfer, the `distributeAllNFT`  function can be called again and again. So multiple transfers will be done for each user.


In addition to that, any receiver of the tokens can revert the transfer. If that happens, nobody will be able to receive their tokens.


#### Recommendation


* Add a reentrancy guard.
* Avoid transferring tokens for different receivers in a single transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | ConsenSys |
| Protocol | Bridge Mutual |
| Report Date | N/A |
| Finders | Daniel Luca, Sergii Kravchenko |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/03/bridge-mutual/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Reentrancy, ERC1155`

