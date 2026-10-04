---
# Core Classification
protocol: Wonderland
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40344
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5295cf96-7a54-4150-9d94-396944b3604e
source_link: https://cdn.cantina.xyz/reports/cantina_wonderland_jul2024.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - shung
  - Optimum
  - 0xicingdeath
  - r0bert
---

## Vulnerability Title

BurnAmount sent from L2 to L1 may not be accurate as it does not account for pending failing messages 

### Overview


The L2OpUSDCBridgeAdapter contract has a function called receiveMigrateToNative() which is used to migrate bridged USDC to native USDC according to Circle's Bridged USDC standard. However, the function is not fully compliant with the standard as it does not accurately calculate the amount of USDC that needs to be burned. This is because it does not take into account any pending failed messages in the L2Messenger contract. This bug has a medium impact and a high likelihood of occurring. The recommendation is to record any amounts received after the migration and burn them separately. The bug has been fixed in commit eb625f95. Any funds sent from the L2 adapter after the migration will either be sent directly to the user or registered for a future claim in case of a failure.

### Original Finding Content

## L2OpUSDCBridgeAdapter Analysis

## Context
L2OpUSDCBridgeAdapter.sol#L81

## Description
In order to follow Circle's Bridged USDC standard, the L2OpUSDCBridgeAdapter contract implements the function `receiveMigrateToNative()`:

```solidity
/**
 * @notice Initiates the process to migrate the bridged USDC to native USDC
 * @dev Full migration can't finish until L1 receives the message for setting the burn amount
 * @param _roleCaller The address that will be allowed to transfer the USDC roles
 * @param _setBurnAmountMinGasLimit Minimum gas limit that the setBurnAmount message can be executed on L1
 */
function receiveMigrateToNative(address _roleCaller, uint32 _setBurnAmountMinGasLimit) external onlyLinkedAdapter {
    isMessagingDisabled = true;
    roleCaller = _roleCaller;
    uint256 _burnAmount = IUSDC(USDC).totalSupply();
    ICrossDomainMessenger(MESSENGER).sendMessage(
        LINKED_ADAPTER, abi.encodeWithSignature('setBurnAmount(uint256)', _burnAmount), _setBurnAmountMinGasLimit
    );
    emit MigratingToNative(MESSENGER, _roleCaller);
}
```

This function sends as the `_burnAmount` the current L2 USDC total supply. However, this is not totally compliant with the Bridged USDC Standard as this property would not be respected:

- The `setBurnAmount()` function must burn the amount of USDC held by the bridge that corresponds precisely to the circulating total supply of bridged USDC established by the supply lock.

This amount is not accurate as the total supply does not account for pending failed messages that are present at the time of the call in the L2Messenger contract. These messages could be called to mint new bridged USDC tokens as the `L2OpUSDCBridgeAdapter.receiveMessage()` function will still be working after the `L2OpUSDCBridgeAdapter.receiveMigrateToNative()` was triggered:

```solidity
/**
 * @notice Receive the message from the other chain and mint the bridged representation for the user
 * @dev This function should only be called when receiving a message to mint the bridged representation
 * @param _user The user to mint the bridged representation for
 * @param _amount The amount of tokens to mint
 */
function receiveMessage(address _user, uint256 _amount) external override onlyLinkedAdapter {
    // Mint the tokens to the user
    IUSDC(USDC).mint(_user, _amount);
    emit MessageReceived(_user, _amount, MESSENGER);
}
```

## Impact
**Medium**: The Circle's Bridged USDC standard is not fully respected and the `_burnAmount` is not accurate.

## Likelihood
**High**: A single failed message stuck in the L2Messenger by the time of the `receiveMigrateToNative()` will trigger this issue.

## Recommendation
Record any `L2OpUSDCBridgeAdapter.receiveMessage()` amounts after the `receiveMigrateToNative()` has been triggered. Then, this extra amount could be burned at any time with a separate function in `L2OpUSDCBridgeAdapter`, which would call the corresponding function in `L1OpUSDCBridgeAdapter` with the extra amount.

## Wonderland
Fixed in commit `eb625f95`.

## Cantina Managed
Fix verified. The fix implemented consists of sending a message back to L1 to withdraw to the original spender. This was achieved with the try/catch block added in the L1 adapter to the `receiveMessage()` function and through the addition of the `receiveWithdrawBlacklistedFundsPostMigration()` function.

Any funds that will be sent from the L2 adapter after a migration (L2 adapter status = Deprecated) will either be sent directly to the user in the L1 adapter or registered in the `blacklistedFundsDetails` mapping for a future claim in case of a failure.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Wonderland |
| Report Date | N/A |
| Finders | shung, Optimum, 0xicingdeath, r0bert |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_wonderland_jul2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5295cf96-7a54-4150-9d94-396944b3604e

### Keywords for Search

`vulnerability`

