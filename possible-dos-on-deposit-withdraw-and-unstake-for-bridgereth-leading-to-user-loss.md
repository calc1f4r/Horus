---
# Core Classification
protocol: DittoETH
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27448
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc
source_link: none
github_link: https://github.com/Cyfrin/2023-09-ditto

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
  - dos

protocol_categories:
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - Bauer
  - chainNue
  - T1MOH
  - ElHaj
  - t0x1c
---

## Vulnerability Title

Possible DOS on deposit(), withdraw() and unstake() for BridgeReth, leading to user loss of funds

### Overview


This bug report is about a possible denial-of-service attack on the BridgeReth mechanism that could lead to users losing funds. The vulnerability is caused by RocketPool rETH tokens having a deposit delay that prevents users who have recently deposited from transferring or burning tokens. If this delay is changed in the future, users staking actions could prevent other users from unstaking for a few hours, leading to their ETH becoming irretrievable. 

To prevent this issue, it is recommended that the Reth bridge is modified to obtain rETH only through the UniswapV3 pool. This would avoid any future issues with the deposit delay mechanism, although users may get less rETH due to the slippage.

### Original Finding Content

## Summary
Future changes on deposit delay on rETH tokens would prevent DittoETH users to use deposit(), withdraw() and unstake() for BridgeReth, which would make its transfering and burning impractical, leading to user funds losses.
## Vulnerability Details
RocketPool rETH tokens has a [deposit delay](https://github.com/rocket-pool/rocketpool/blob/967e4d3c32721a84694921751920af313d1467af/contracts/contract/token/RocketTokenRETH.sol#L157-L172) that prevents any user who has recently deposited to transfer or burn tokens. In the past this delay was set to 5760 blocks mined (aprox. 19h, considering one block per 12s). This delay can prevent DittoETH users from transfering if another user staked recently.

File: RocketTokenRETH.sol
``` solidity
  // This is called by the base ERC20 contract before all transfer, mint, and burns
    function _beforeTokenTransfer(address from, address, uint256) internal override {
        // Don't run check if this is a mint transaction
        if (from != address(0)) {
            // Check which block the user's last deposit was
            bytes32 key = keccak256(abi.encodePacked("user.deposit.block", from));
            uint256 lastDepositBlock = getUint(key);
            if (lastDepositBlock > 0) {
                // Ensure enough blocks have passed
                uint256 depositDelay = getUint(keccak256(abi.encodePacked(keccak256("dao.protocol.setting.network"), "network.reth.deposit.delay")));
                uint256 blocksPassed = block.number.sub(lastDepositBlock);
                require(blocksPassed > depositDelay, "Not enough time has passed since deposit");
                // Clear the state as it's no longer necessary to check this until another deposit is made
                deleteUint(key);
            }
        }
    }
```

Any future changes made to this delay by the admins could potentially lead to a denial-of-service attack on the `BridgeRouterFacet::deposit` and `BridgeRouterFacet::withdraw` mechanism for the rETH bridge.
## Impact
Currently, the delay is set to zero, but if RocketPool admins decide to change this value in the future, it could cause issues. Specifically, protocol users staking actions could prevent other users from unstaking for a few hours. Given that many users call the stake function throughout the day, the delay would constantly reset, making the unstaking mechanism unusable. It's important to note that this only occurs when stake() is used through the rocketDepositPool route. If rETH is obtained from the Uniswap pool, the delay is not affected.   
All the ETH swapped for rETH calling `BridgeReth::depositEth` would become irrecuperable, leading to a user bank run on DittoETH to not be perjudicated of this protocol externalization to all the users that have deposited.
## Tools Used
Manual review.
## Recommendations
Consider modifying Reth bridge to obtain rETH only through the UniswapV3 pool, on average users will get less rETH due to the slippage, but will avoid any future issues with the deposit delay mechanism.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | DittoETH |
| Report Date | N/A |
| Finders | Bauer, chainNue, T1MOH, ElHaj, t0x1c, 0xmuxyz, alra, Infect3d, Lalanda, rvierdiiev, nican0r |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-09-ditto
- **Contest**: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc

### Keywords for Search

`DOS`

