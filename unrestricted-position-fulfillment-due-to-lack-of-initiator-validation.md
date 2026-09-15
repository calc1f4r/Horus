---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37028
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
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
  - Zokyo
---

## Vulnerability Title

Unrestricted position fulfillment due to lack of initiator validation

### Overview


The VodkaVaultV2 contract has a critical vulnerability that allows attackers to bypass security measures and potentially steal funds. This is due to a lack of validation in the afterDepositExecution function, which can be exploited by crafting a malicious deposit request. The recommendation is to implement a check for all callbacks to ensure that the account parameter corresponds to the VodkaVaultV2 address. This vulnerability affects all flows that include a callback to the VodkaHandler contract. The bug has been resolved.

### Original Finding Content

**Severity**: Critical

**Status**:  Resolved

**Description**

The VodkaVaultV2 contract holds functions designed to initiate specific operations on the GMX system, essentially starting the whole relevant process. For instance, the user can call the requestOpenPosition function specifying the amount, leverage, and the asset they want to short. Then, this function creates a struct with required data and calls the createDeposit function on GMX's exchangeRouter, passing prepared parameters.

```solidity
       IExchangeRouter.CreateDepositParams memory params = IExchangeRouter.CreateDepositParams({
           receiver: address(this),
           callbackContract: strategyAddresses.VodkaHandler,
           uiFeeReceiver: msg.sender,
           market: gmp.marketToken,
           initialLongToken: gmp.longToken,
           initialShortToken: gmp.shortToken,
           longTokenSwapPath: new address[](0),
           shortTokenSwapPath: new address[](0),
           minMarketTokens: 0, 
           shouldUnwrapNativeToken: false,
           executionFee: gmxOpenCloseFees,
           callbackGasLimit: 2000000
       });


       bytes32 key = IExchangeRouter(gmxAddresses.exchangeRouter).createDeposit(params);
```
The `createDeposit` method caches the msg.sender address, which refers to the VodkaVaultV2 contract, and then invokes the createDeposit function on the depositHandler contract.
```solidity
   function createDeposit(
       DepositUtils.CreateDepositParams calldata params
   ) external payable nonReentrant returns (bytes32) {
       address account = msg.sender;


       return depositHandler.createDeposit(
           account,
           params
       );
   }
```
In the final step of the deposit creation routine, the sent parameters, along with the account address, are encoded into a Props struct within the DepositUtils contract.
```solidity
       Deposit.Props memory deposit = Deposit.Props(
           Deposit.Addresses(
               account,
               params.receiver,
               params.callbackContract,
               params.uiFeeReceiver,
               market.marketToken,
               params.initialLongToken,
               params.initialShortToken,
               params.longTokenSwapPath,
               params.shortTokenSwapPath
           ),
```
Privileged actors on the GMX platform review the request and decide whether to accept or revoke it by calling executeDeposit or cancelDeposit functions respectively. If the deposit request is accepted and executed, a callback is made to the callbackContract (set during the request phase) via the afterDepositExecution function, providing a related Props struct as an argument.
```solidity
   function afterDepositExecution(
       bytes32 key,
       Deposit.Props memory deposit,
       EventUtils.EventLogData memory eventData
   ) internal {
       if (!isValidCallbackContract(deposit.callbackContract())) { return; }


       try IDepositCallbackReceiver(deposit.callbackContract()).afterDepositExecution{ gas: deposit.callbackGasLimit() }(
           key,
           deposit,
           eventData
       ) {
       } catch {
           emit AfterDepositExecutionError(key, deposit);
       }
   }
```

On the Vaultka side, the afterDepositExecution function receives the callback, but without validation to ensure that VodkaVaultV2 was the initiator of the entire process, completely omitting the deposit parameter.
```solidity
   function afterDepositExecution(
       bytes32 key,
       Deposit.Props memory deposit,
       EventUtils.EventLogData memory eventData
   ) external {
       require(
           IRoleStore(RoleStore).hasRole(msg.sender, Role.CONTROLLER),
           "Not proper role"
       );
       IVodkaV2(strategyAddresses.VodkaV2).fulfillOpenPosition(
           key,
           eventData.uintItems.items[0].value
       );
   }
```
Since there’s no validation of the initiator in the afterDepositExecution function, an attacker can craft a malicious deposit request, with arbitrary data provided, and set the VodkaHandler contract’s address as a callbackContract, effectively bypassing the accounting step included in requestDeposit.

The deposit routine was provided as an example. However, the described vulnerability equally relates to every flow that includes a callback to a function in the VodkaHandler contract

**Recommendation**: 

Implement a check for all callbacks to ensure that the account parameter from the Props struct corresponds to the VodkaVaultV2 address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

