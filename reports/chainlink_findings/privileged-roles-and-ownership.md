---
# Core Classification
protocol: Venus Multichain Support
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60205
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
source_link: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
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
finders_count: 4
finders:
  - Shih-Hung Wang
  - Julio Aguilar
  - Ibrahim Abouzied
  - Cameron Biniamow
---

## Vulnerability Title

Privileged Roles and Ownership

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the Venus team. The Venus team provided the following explanation:

> The owner of the Venus contracts is Normal Timelock on the BNB chain. Initially, on Ethereum, it will be a multisig wallet, but later in phase 2, it will be the Normal Timelock too, and all actions will be carried out via VIP only.

**Description:** Smart contracts will often have `owner` variables to designate the person with special privileges to make modifications to the smart contract. In this protocol, access control is also granted on a per-function basis through `_checkAccessAllowed()`.

**VTreasuryV8**

The `VTreasuryV8.sol` contract contains the following privileged roles:

1.   An owner (`owner`, `onlyOwner` modifier) as initialized during the constructor execution to `msg.sender`:
    1.   Transfer any amount of any token to any address by calling `withdrawTreasuryToken()`.
    2.   Transfer any amount of the native token to any address by calling `withdrawTreasuryNative()`.

**XVS Bridge & XVS**

The `BaseXVSProxyOFT.sol` contract contains the following privileged roles:

1.   An owner (`owner`, `onlyOwner` modifier) as initialized during the constructor execution to `msg.sender`:
    1.   `setOracle()`: Set the address of the `ResilientOracle` contract.
    2.   `setMaxSingleTransactionLimit()`: Sets the limit of a single transaction amount.
    3.   `setMaxDailyLimit()`: Sets the limit of daily (24-hour) transactions amount.
    4.   `setMaxSingleReceiveTransactionLimit()`: Sets the maximum limit for a single receive transaction.
    5.   `setMaxDailyReceiveLimit()`: Sets the maximum daily limit for receiving transactions.
    6.   `setWhitelist()`: Sets the whitelist address to skip checks on transaction limit.
    7.   `pause()`: Pauses the bridge.
    8.   `unpause()`: Unpauses the bridge.

The `XVSBridgeAdmin.sol` contract contains the following privileged roles:

1.   An owner (`owner`, `onlyOwner` modifier) as initialized during the constructor execution to `msg.sender`:
    1.   Insert or modify the mapping between function signatures and names to allow specific roles to call the privileged functions on the bridges.

The `XVS.sol` contract contains the following privileged roles:

1.   An Access Control Manager (`accessControlManager_`), as initialized during the constructor execution to `accessControlManager_`:
    1.   Control who is allowed to mint tokens by indirectly affecting `_ensureAllowed("mint(address,uint256)")`.
    2.   Control who is allowed to burn tokens by indirectly affecting `_ensureAllowed("burn(address,uint256)")`.

The following functions in this contract are protected through `_ensureAllowed()`:

1.   `mint(address,uint256)`: Mints a capped `amount_` of tokens to a specified `account_`.
2.   `burn(address,uint256)`: Burns any `amount_` of tokens from a specified `account_`.

**XVS Vault**

The `XVSVault.sol` contract contains the following privileged roles:

1.   An administrator (`admin`, `onlyAdmin()` modifier), as initialized during the constructor execution to `msg.sender`:
    1.   Change the XVS store contract address (`xvsStore`) that controls reward token transfers by calling `setXvsStore()`.
    2.   Change the access control manager implementation address (and thereby indirectly all `_checkAccessAllowed()`-controlled access checks) by calling `setAccessControl()`.

The following functions in this contract are protected through `_checkAccessAllowed()` with their corresponding function signatures:

1.   `pause()`: Pause the contract (and thereby all calls to `deposit()`, `claim()`, `executeWithdrawal()`, `requestWithdrawal()`, `updatePool()`, `delegate()` and `delegateBySig()`) by calling `pause()`.
2.   `resume()`: Resume the contract from a paused state by calling `resume()`.
3.   `add(address,uint256,address,uint256,uint256)`: Add a new pool by calling `add()`.
    1.   Using an existing reward token, but a new pool token allows the caller to globally update the `rewardTokenAmountsPerBlock[]` variable for all pools using this reward token, **without explicitly calling `setRewardAmountPerBlock()`**. In extreme cases, this could either drain the reward token (by choosing a high reward value) or halt any future rewards (by choosing zero).
    2.   **Accidentally or with malicious intent the caller could add enough new pools to make calling `massUpdatePools()` prohibitively gas-expensive and thereby deny the service to the following functions**:
        1.   `add()`
        2.   `set()`
        3.   `setRewardAmountPerBlock()`

4.   `set(address,uint256,uint256)`: Update the accumulated rewards per share for all pools and change the allocation point of a pool by calling `set()`.
5.   `setRewardAmountPerBlock(address,uint256)`: Update the accumulated rewards per share for all pools and arbitrarily change the reward amount per block by calling `setRewardAmountPerBlock()`.
    1.   **By setting it to zero no additional rewards would be accumulated.**
    2.   **By setting it to an unusually high value the reward token could be drained.**

6.   `setWithdrawalLockingPeriod(address,uint256,uint256)`: Change the lockup period for withdrawing deposited funds by calling `setWithdrawalLockingPeriod()`.

The `XVSStore.sol` contract contains the following privileged roles:

1.   An administrator (`admin`, `onlyAdmin()` modifier), as initialized during the constructor execution to `msg.sender`:
    1.   Transfer the role to another address (which has to accept it by calling `acceptAdmin()`) by calling `setPendingAdmin()`.
    2.   Designate a new owner role by calling `setNewOwner()`.
    3.   Add/remove token addresses from the `rewardTokens[]` array by calling `setRewardToken()`.

2.   An owner (`owner`, `onlyOwner()` modifier), as set through `setNewOwner()` by `admin`:
    1.   Transfer an arbitrary amount of reward tokens by calling `safeRewardTransfer()`.
        1.   **A compromised owner could drain all funds from this contract by**:
            1.   Adding a to-be-drained token to the `rewardTokens[]` array, if not already a reward token.
            2.   Transfer an arbitrary amount by calling `safeRewardTransfer()`.

        2.   **A compromised admin could drain all funds from this contract by**:
            1.   Adding a to-be-drained token to the `rewardTokens[]` array, if not already a reward token.
            2.   Set themselves as an owner by calling `setNewOwner()`.
            3.   Transfer an arbitrary amount by calling `safeRewardTransfer()`.

    2.   The owner can drain this contract of any ERC-20 token held within it by calling `XVSVault.emergencyRewardWithdraw()`.

**Resilient and Chainlink Oracles**

The following functions in `ResilientOracle.sol` are protected through `_checkAccessAllowed()`:

1.   `pause()`: Pauses the oracle.
2.   `unpause()`: Unpauses the oracle.
3.   `setOracle(address,address,uint8)`: Sets the address for the main, pivot, or fallback oracle.
4.   `enableOracle(address,uint8,bool)`: Enables the main, pivot, or fallback oracle.
5.   `setTokenConfig(TokenConfig)`: Assigns an asset to an oracle.

The following functions in `ChainlinkOracle.sol` are protected through `_checkAccessAllowed()`:

1.   `setDirectPrice(address,uint256)`: Manually sets the price for an asset. **The manual price overrides any prices returned by the chainlink oracle, even if the oracle is functioning correctly.**
2.   `setTokenConfig(TokenConfig)`: Assigns an asset to a price feed and defines a maximum stale period.

**Protocol Share Reserves**

The `ProtocolShareReserves.sol` contract contains the following privileged roles:

1.   An owner (`owner`, `onlyOwner` modifier) as initialized during the constructor execution to `msg.sender`:
    1.   `setPrime()`: Setter for the prime contract.
    2.   `setPoolRegistry()`: Setter for the pool registry.

The following functions in this contract are protected through `_ensureAllowed()`:

1.   `addOrRemoveAssetFromPrime(address,bool)`: Updates local storage to reflect whether an asset is stored in the Prime contract.
2.   `addOrUpdateDistributionConfigs(DistributionConfig[])`: Adds/Updates the distribution between different distribution targets. **This can add beneficiaries when releasing funds.**
3.   `removeDistributionConfig(Schema,address)`: Removes a distribution target if it is already allocated 0 distributions.

**Recommendation:** Consider documenting the risk and impact a compromised privileged role can cause on the protocol and inform the users in detail. As the privileged roles can be the single point of failure of the protocol, consider using a multi-sig or a contract with a timelock feature to mitigate the risk of being compromised or exploited.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus Multichain Support |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Julio Aguilar, Ibrahim Abouzied, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-multichain-support/f163c791-6598-41b2-b626-b347ac0ee032/index.html

### Keywords for Search

`vulnerability`

