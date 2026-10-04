---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42264
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-07-spartan
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/6

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
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-11] Block usage of `addCuratedPool`

### Overview


The function `curatedPoolCount()` in the `poolFactory.sol` contract has a bug that can cause it to run out of gas and revert, preventing the execution of `addCuratedPool()`. This happens when the array `arrayPools` becomes too large, which can happen if users repeatedly create and empty pools using `createPoolADD()` and `remove()` functions. The `curatedPoolCount()` function is used to keep track of the number of curated pools, but it does not update this count when pools are added or removed. To fix this issue, the report recommends creating a new variable `curatedPoolCount` and updating it in the `addCuratedPool()` and `removeCuratedPool()` functions.

### Original Finding Content

_Submitted by gpersoon, also found by hickuphh3, and cmichel_

The function `curatedPoolCount()` contains a for loop over the array `arrayPools`. If `arrayPools` would be too big then the loop would run out of gas and `curatedPoolCount()` would revert. This would mean that `addCuratedPool()` cannot be executed anymore (because it calls `curatedPoolCount()` )

The array `arrayPools` can be increased in size arbitrarily by repeatedly doing the following:
- create a pool with `createPoolADD()`  (which requires 10,000 SPARTA)
- empty the pool with `remove()` of Pool.sol, which gives back the SPARTA tokens
These actions will use gas to perform.


```solidity
// https://github.com/code-423n4/2021-07-spartan/blob/main/contracts/poolFactory.sol#L45
function createPoolADD(uint256 inputBase, uint256 inputToken, address token) external payable returns(address pool){
    require(getPool(token) == address(0)); // Must be a valid token
    require((inputToken > 0 && inputBase >= (10000*10**18)), "!min"); // User must add at least 10,000 SPARTA liquidity & ratio must be finite
    Pool newPool; address _token = token;
    if(token == address(0)){_token = WBNB;} // Handle BNB -> WBNB
    require(_token != BASE && iBEP20(_token).decimals() == 18); // Token must not be SPARTA & it's decimals must be 18
    newPool = new Pool(BASE, _token); // Deploy new pool
    pool = address(newPool); // Get address of new pool
    mapToken_Pool[_token] = pool; // Record the new pool address in PoolFactory
    _handleTransferIn(BASE, inputBase, pool); // Transfer SPARTA liquidity to new pool
    _handleTransferIn(token, inputToken, pool); // Transfer TOKEN liquidity to new pool
    arrayPools.push(pool); // Add pool address to the pool array
    ..

function curatedPoolCount() internal view returns (uint){
    uint cPoolCount;
    for(uint i = 0; i< arrayPools.length; i++){
        if(isCuratedPool[arrayPools[i]] == true){
            cPoolCount += 1;
        }
    }
    return cPoolCount;
}
```

```solidity
function addCuratedPool(address token) external onlyDAO {
    ...
    require(curatedPoolCount() < curatedPoolSize, "maxCurated"); // Must be room in the Curated list
```


```solidity
// https://github.com/code-423n4/2021-07-spartan/blob/main/contracts/Pool.sol#L187
function remove() external returns (uint outputBase, uint outputToken) {
    return removeForMember(msg.sender);
}

// Contract removes liquidity for the user
function removeForMember(address member) public returns (uint outputBase, uint outputToken) {
    uint256 _actualInputUnits = balanceOf(address(this)); // Get the received LP units amount
    outputBase = iUTILS(_DAO().UTILS()).calcLiquidityHoldings(_actualInputUnits, BASE, address(this)); // Get the SPARTA value of LP units
    outputToken = iUTILS(_DAO().UTILS()).calcLiquidityHoldings(_actualInputUnits, TOKEN, address(this)); // Get the TOKEN value of LP units
    _decrementPoolBalances(outputBase, outputToken); // Update recorded BASE and TOKEN amounts
    _burn(address(this), _actualInputUnits); // Burn the LP tokens
    iBEP20(BASE).transfer(member, outputBase); // Transfer the SPARTA to user
    iBEP20(TOKEN).transfer(member, outputToken); // Transfer the TOKENs to user
    emit RemoveLiquidity(member, outputBase, outputToken, _actualInputUnits);
    return (outputBase, outputToken);
}
```
Recommend creating a variable `curatedPoolCount` and increase it in `addCuratedPool` and decrease it in `removeCuratedPool`.

**[verifyfirst (Spartan) confirmed and disagreed with severity](https://github.com/code-423n4/2021-07-spartan-findings/issues/6#issuecomment-885424168):**
 > We agree with the issue, this could be more efficient.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/6
- **Contest**: https://code4rena.com/reports/2021-07-spartan

### Keywords for Search

`vulnerability`

