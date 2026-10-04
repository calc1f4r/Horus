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
solodit_id: 16532
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
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
finders_count: 2
finders:
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

Aave/Geist Interface declaration mismatch and unchecked return values

### Overview


This bug report is about the two lending providers, Geist & Aave, which do not seem to be directly affiliated even though one is a fork of the other. The interface declaration used for both protocols might become problematic with future upgrades to either protocol. The interface declaration does not come from the original upstream project. The interface `IAaveLendingPool` does not declare any return values while some of the functions called in Geist or Aave return them. It was noted that the code was not verified for correctness and it was suggested that only official interface declarations from the upstream projects should be used and verified that all other interfaces match. 

The code for `ILendingPool` configured in `ProviderAave` and `IAaveLendingPool` was provided. It was noted that the methods `withdraw()`, `repay()` return `uint256` in the original implementation for Aave and Geist respectively. It was also noted that the actual amount withdrawn does not necessarily need to match the `amount` provided with the function argument. An excerpt of the upstream `LendingProvider.withdraw()` was also provided. It was noted that this will break the `withdrawAll` functionality of `LendingProvider` if token `isFTM`. 

The recommendation was to always use the original interface unless only a minimal subset of functions is used. It was suggested to use the original upstream interfaces of the corresponding project (link via the respective npm packages if available). It was also suggested to avoid omitting parts of the function declaration, especially when it comes to return values. Lastly, it was recommended to check return values and use the value returned from `withdraw()` AND `repay()`.

### Original Finding Content

#### Description


The two lending providers, Geist & Aave, do not seem to be directly affiliated even though one is a fork of the other. However, the interfaces may likely diverge in the future. Using the same interface declaration for both protocols might become problematic with future upgrades to either protocol.
The interface declaration does not seem to come from the original upstream project. The interface `IAaveLendingPool` does not declare any return values while some of the functions called in Geist or Aave return them.


**Note:** that we have not verified all interfaces for correctness. However, we urge the client to only use official interface declarations from the upstream projects and verify that all other interfaces match.


#### Examples


The `ILendingPool` configured in `ProviderAave` (`0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5` -> implementation: `0xc6845a5c768bf8d7681249f8927877efda425baf`)


**code/contracts/mainnet/providers/ProviderAave.sol:L19-L21**



```
function \_getAaveProvider() internal pure returns (IAaveLendingPoolProvider) {
 return IAaveLendingPoolProvider(0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5);
}

```
The `IAaveLendingPool` does not declare return values for any function, while upstream does.


**code/contracts/interfaces/aave/IAaveLendingPool.sol:L1-L46**



```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface IAaveLendingPool {
 function flashLoan(
 address receiverAddress,
 address[] calldata assets,
 uint256[] calldata amounts,
 uint256[] calldata modes,
 address onBehalfOf,
 bytes calldata params,
 uint16 referralCode
 ) external;

 function deposit(
 address \_asset,
 uint256 \_amount,
 address \_onBehalfOf,
 uint16 \_referralCode
 ) external;

 function withdraw(
 address \_asset,
 uint256 \_amount,
 address \_to
 ) external;

 function borrow(
 address \_asset,
 uint256 \_amount,
 uint256 \_interestRateMode,
 uint16 \_referralCode,
 address \_onBehalfOf
 ) external;

 function repay(
 address \_asset,
 uint256 \_amount,
 uint256 \_rateMode,
 address \_onBehalfOf
 ) external;

 function setUserUseReserveAsCollateral(address \_asset, bool \_useAsCollateral) external;
}

```
Methods: `withdraw()`, `repay()` return `uint256` in the original implementation for Aave, see:


<https://etherscan.io/address/0xc6845a5c768bf8d7681249f8927877efda425baf#code>


The `ILendingPool` configured for Geist:


Methods `withdraw()`, `repay()` return `uint256` in the original implementation for Geist, see:


<https://ftmscan.com/address/0x3104ad2aadb6fe9df166948a5e3a547004862f90#code>


**Note:** that the actual amount withdrawn does not necessarily need to match the `amount` provided with the function argument. Here’s an excerpt of the upstream `LendingProvider.withdraw()`:



```
...
 if (amount == type(uint256).max) {
 amountToWithdraw = userBalance;
 }
...
 return amountToWithdraw;

```
And here’s the code in Fuji that calls that method. This will break the `withdrawAll` functionality of `LendingProvider` if token `isFTM`.


**code/contracts/fantom/providers/ProviderGeist.sol:L151-L165**



```
function withdraw(address \_asset, uint256 \_amount) external payable override {
 IAaveLendingPool aave = IAaveLendingPool(\_getAaveProvider().getLendingPool());

 bool isFtm = \_asset == \_getFtmAddr();
 address \_tokenAddr = isFtm ? \_getWftmAddr() : \_asset;

 aave.withdraw(\_tokenAddr, \_amount, address(this));

 // convert WFTM to FTM
 if (isFtm) {
 address unwrapper = \_getUnwrapper();
 IERC20(\_tokenAddr).univTransfer(payable(unwrapper), \_amount);
 IUnwrapper(unwrapper).withdraw(\_amount);
 }
}

```
Similar for `repay()`, which returns the actual amount repaid.


#### Recommendation


* Always use the original interface unless only a minimal subset of functions is used.
* Use the original upstream interfaces of the corresponding project (link via the respective npm packages if available).
* Avoid omitting parts of the function declaration! Especially when it comes to return values.
* Check return values. Use the value returned from `withdraw()` AND `repay()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

