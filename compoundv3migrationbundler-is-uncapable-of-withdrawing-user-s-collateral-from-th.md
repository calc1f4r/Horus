---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54337
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xStalin
---

## Vulnerability Title

Compoundv3migrationbundler is uncapable of withdrawing user 's collateral from the com- pound's instances 

### Overview


The `CompoundV3MigrationBundler` function is not working properly when trying to withdraw assets from Compound to Morpho Blue. This is because the function `ICompoundV3(instance).userCollateral()` returns a struct instead of a uint. This causes a Type Error when trying to assign the value to the `balance` variable, resulting in the entire transaction being reverted. To fix this, the received struct needs to be decoded and the value of the `balance` variable needs to be assigned correctly.

### Original Finding Content

## Context

(No context files were provided by the reviewer)

When the `CompoundV3MigrationBundler.compoundV3WithdrawFrom()` function is called to attempt to withdraw the user's collateral, the entire execution of the multicall transaction will be reverted because a runtime compilation error will occur when the returned value from the `Compound.userCollateral()` function (a struct) is tried to be assigned to the `balance` variable (uint256). [See the Proof of Concept section for more details]

## Proof of Concept

- The `CompoundV3MigrationBundler` intends to allow users to migrate positions from CompoundV3 to Morpho Blue. One of the functions that users can use to manage their compound's position and move their assets to Morpho Blue is the `compoundV3WithdrawFrom()` function, which allows users to withdraw their assets from Compound. This function enables users to withdraw the user's collateral that was deposited in Compound. 

The problem is that the function `ICompoundV3(instance).userCollateral()` returns a struct instead of a uint. Because the returned value is a struct, when the value is attempted to be assigned to the `balance` variable, a Type Error will occur, reverting all the multicall execution. This failure will prevent users from migrating their assets from Compound to Morpho and will result in users wasting gas on a transaction that always reverts.

- Let's do a walkthrough of the contracts to spot the exact issue:

### CompoundV3MigrationBundler.sol

```solidity
function compoundV3WithdrawFrom(address instance, address asset, uint256 amount) external payable protected {
    address _initiator = initiator();
    uint256 balance = asset == ICompoundV3(instance).baseToken()
        //@audit-ok => Compound.balanceOf() returns a uint256
        ? ICompoundV3(instance).balanceOf(_initiator)
        //@audit-issue => Compound.userCollateral() returns a struct, not a uint.
        //@audit-issue => When trying to assign the returned value to the `balance` variable which is an uint256, it will throw an error about incompatible types
        : ICompoundV3(instance).userCollateral(_initiator, asset);
    
    amount = Math.min(amount, balance);
    require(amount != 0, ErrorsLib.ZERO_AMOUNT);
    ICompoundV3(instance).withdrawFrom(_initiator, address(this), asset, amount);
}
```

- By examining the code of the CompoundV3 Protocol, we find that the call to `userCollateral()` actually calls a public mapping defined in the `CometStorage.sol` (which is a contract that the main contract inherits from), and this mapping ends up returning a struct.

### CompoundV3 Protocol, CometStorage.sol

```solidity
contract CometStorage {
    // ...
    //@audit-info => This is the returned Struct when userCollateral() is called!
    struct UserCollateral {
        uint128 balance;
        uint128 _reserved;
    }
    // ...
    //@audit-info => This is the public mapping that is called from the CompoundV3MigrationBundler::compoundV3WithdrawFrom()
    mapping(address => mapping(address => UserCollateral)) public userCollateral;
}
```

- As we have just seen in the previous walkthrough, as a result of not decoding the received struct and merely trying to assign it directly to a variable of type uint256, the entire execution will fail. All changes will be reverted, causing users to lose all the gas spent on the failed execution.

## Recommendation

The mitigation for this issue is to ensure that the received struct is decoded and the value of the variable `balance` is assigned correctly.

### Updated Code Example

```solidity
function compoundV3WithdrawFrom(address instance, address asset, uint256 amount) external payable protected {
    address _initiator = initiator();
    uint256 balance;

    if(asset == ICompoundV3(instance).baseToken()) {
        balance = ICompoundV3(instance).balanceOf(_initiator);
    } else {
        //@audit-ok => Extract the value of the `balance` variable returned from the Compound Contract
        (uint128 _balance, ) = ICompoundV3(instance).userCollateral(_initiator, asset);
        balance = uint256(_balance);
    }
    
    amount = Math.min(amount, balance);
    require(amount != 0, ErrorsLib.ZERO_AMOUNT);
    ICompoundV3(instance).withdrawFrom(_initiator, address(this), asset, amount);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | 0xStalin |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad

### Keywords for Search

`vulnerability`

