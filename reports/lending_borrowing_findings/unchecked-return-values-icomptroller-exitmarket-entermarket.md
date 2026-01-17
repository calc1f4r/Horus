---
# Core Classification
protocol: Fuji Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16527
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
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
finders_count: 2
finders:
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

Unchecked Return Values - IComptroller exitMarket, enterMarket

### Overview


This bug report focuses on the `IComptroller.exitMarket()` and `IComptroller.enterMarkets()` functions and their unchecked return values. These functions are used by all Providers and may return a non-zero uint on error, but none of the Providers check for this error condition. This suggests that unchecked return values may be a systemic problem. The code for these functions is provided, and it is recommended that return values are required to be `ERROR.NO_ERROR` or `0`. This would ensure that any errors are properly handled and prevent any unexpected behavior in the system.

### Original Finding Content

#### Description


`IComptroller.exitMarket()`, `IComptroller.enterMarkets()` may return a non-zero uint on error but none of the Providers check for this error condition. Together with [issue 4.10](#aavegeist-interface-declaration-mismatch-and-unchecked-return-values), this might suggest that unchecked return values may be a systemic problem.


Here’s the upstream implementation:


**contracts/Comptroller.sol:L179-L187**



```
if (amountOwed != 0) {
 return fail(Error.NONZERO\_BORROW\_BALANCE, FailureInfo.EXIT\_MARKET\_BALANCE\_OWED);
}

/\* Fail if the sender is not permitted to redeem all of their tokens \*/
uint allowed = redeemAllowedInternal(cTokenAddress, msg.sender, tokensHeld);
if (allowed != 0) {
 return failOpaque(Error.REJECTION, FailureInfo.EXIT\_MARKET\_REJECTION, allowed);
}

```

```
 /\*\*
 \* @notice Removes asset from sender's account liquidity calculation
 \* @dev Sender must not have an outstanding borrow balance in the asset,
 \* or be providing necessary collateral for an outstanding borrow.
 \* @param cTokenAddress The address of the asset to be removed
 \* @return Whether or not the account successfully exited the market
 \*/
 function exitMarket(address cTokenAddress) external returns (uint) {
 CToken cToken = CToken(cTokenAddress);
 /\* Get sender tokensHeld and amountOwed underlying from the cToken \*/
 (uint oErr, uint tokensHeld, uint amountOwed, ) = cToken.getAccountSnapshot(msg.sender);
 require(oErr == 0, "exitMarket: getAccountSnapshot failed"); // semi-opaque error code

 /\* Fail if the sender has a borrow balance \*/
 if (amountOwed != 0) {
 return fail(Error.NONZERO\_BORROW\_BALANCE, FailureInfo.EXIT\_MARKET\_BALANCE\_OWED);
 }

 /\* Fail if the sender is not permitted to redeem all of their tokens \*/
 uint allowed = redeemAllowedInternal(cTokenAddress, msg.sender, tokensHeld);
 if (allowed != 0) {
 return failOpaque(Error.REJECTION, FailureInfo.EXIT\_MARKET\_REJECTION, allowed);
 }

```
#### Examples


* Unchecked return value `exitMarket`


All Providers exhibit the same issue, probably due to code reuse. (also see <https://github.com/ConsenSysDiligence/fuji-protocol-audit-2022-02/issues/19)>. Some examples:


**code/contracts/fantom/providers/ProviderCream.sol:L52-L57**



```
function \_exitCollatMarket(address \_cyTokenAddress) internal {
 // Create a reference to the corresponding network Comptroller
 IComptroller comptroller = IComptroller(\_getComptrollerAddress());

 comptroller.exitMarket(\_cyTokenAddress);
}

```
**code/contracts/fantom/providers/ProviderScream.sol:L52-L57**



```
function \_exitCollatMarket(address \_cyTokenAddress) internal {
 // Create a reference to the corresponding network Comptroller
 IComptroller comptroller = IComptroller(\_getComptrollerAddress());

 comptroller.exitMarket(\_cyTokenAddress);
}

```
**code/contracts/mainnet/providers/ProviderCompound.sol:L46-L51**



```
function \_exitCollatMarket(address \_cTokenAddress) internal {
 // Create a reference to the corresponding network Comptroller
 IComptroller comptroller = IComptroller(\_getComptrollerAddress());

 comptroller.exitMarket(\_cTokenAddress);
}

```
**code/contracts/mainnet/providers/ProviderIronBank.sol:L52-L57**



```
function \_exitCollatMarket(address \_cyTokenAddress) internal {
 // Create a reference to the corresponding network Comptroller
 IComptroller comptroller = IComptroller(\_getComptrollerAddress());

 comptroller.exitMarket(\_cyTokenAddress);
}

```
* Unchecked return value `enterMarkets` (Note that `IComptroller` returns `NO_ERROR` when already joined to `enterMarkets`.


All Providers exhibit the same issue, probably due to code reuse. (also see <https://github.com/ConsenSysDiligence/fuji-protocol-audit-2022-02/issues/19)>. For example:


**code/contracts/fantom/providers/ProviderCream.sol:L39-L46**



```
function \_enterCollatMarket(address \_cyTokenAddress) internal {
 // Create a reference to the corresponding network Comptroller
 IComptroller comptroller = IComptroller(\_getComptrollerAddress());

 address[] memory cyTokenMarkets = new address[](1);
 cyTokenMarkets[0] = \_cyTokenAddress;
 comptroller.enterMarkets(cyTokenMarkets);
}

```
#### Recommendation


Require that return value is `ERROR.NO_ERROR` or `0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fuji Protocol |
| Report Date | N/A |
| Finders | Dominik Muhs,  Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

