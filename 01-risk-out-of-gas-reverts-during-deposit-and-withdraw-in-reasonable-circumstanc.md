---
# Core Classification
protocol: Liquid Ron
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50054
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-01-liquid-ron
source_link: https://code4rena.com/reports/2025-01-liquid-ron
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
finders_count: 0
finders:
---

## Vulnerability Title

[01] Risk `Out-Of-Gas` reverts during deposit and withdraw in reasonable circumstances

### Overview

See description below for full details.

### Original Finding Content


The `totalAssets()` function in `LiquidRon.sol` iterates over all staking proxies and consensus addresses to calculate the total assets controlled by the contract. This function is called during critical operations such as deposits and withdrawals. However, if the number of staking proxies or consensus addresses is large, the function can consume excessive gas, potentially exceeding the Ethereum block gas limit (30M gas). This can lead to out-of-gas (OOG) reverts, rendering the contract unusable for deposits and withdrawals in high-scale scenarios.

The most reasonable numbers I could come across are 60 validator and 100 staking proxy deployed:

* While this seems large:

  + The nature of staking protocols usually involve more than 100 validators.
  + If the TVL of the LiquidRonin is increasing and multiple user interactions are happening daily, they will need to deploy more proxies.
* The above two points make the bug more likely to rise.

### Impact

* **Denial of Service (DoS)**: If `totalAssets()` reverts due to OOG, users will be unable to deposit or withdraw funds, effectively freezing the contract temporarily till the operator claim and undelegate from number of operators to delete some them to decrease the iteration numbers on consensus adresses.
* **Scalability issues**: The contract cannot handle a large number of staking proxies or consensus addresses, limiting its scalability.
* **User funds at risk**: If withdrawals are blocked due to OOG reverts, users may be unable to access their funds. (same as first point).

### Proof of Concept

Paste this in `LiquidRon.t.sol`:
```

    function test_totalAssets_OOG() public {
    // Deploy multiple staking proxies
    uint256 proxyCount = 100; // Adjust this number to test different scenarios
    for (uint256 i = 0; i < proxyCount; i++) {
        liquidRon.deployStakingProxy();
    }

    // Add a large number of consensus addresses
    uint256 consensusCount = 60; // Adjust this number to test different scenarios
    address[] memory consensusAddrs = new address[](consensusCount);
    for (uint256 i = 0; i < consensusCount; i++) {
        consensusAddrs[i] = address(uint160(i + 1)); // Generate unique addresses
    }

    // Deposit some RON to initialize the system
    uint256 depositAmount = 1000000000000000000000000000000 ether;

    deal(address(this), depositAmount * 10);

    liquidRon.deposit{value: depositAmount * 10}();

    // Delegate amounts to consensus addresses
    uint256[] memory amounts = new uint256[](consensusCount);
    for (uint256 i = 0; i < consensusCount; i++) {
        amounts[i] = 1;
    }
    for (uint256 i = 0; i < proxyCount; i++) {
        liquidRon.delegateAmount(i, amounts, consensusAddrs);
    }

    // Call totalAssets() and check for OOG reverts
    uint256 blockGasLimit = 30_000_000;
    uint256 totalAssets;
    // passing the block gas limit as a parameter to simulate a real environment block limit
    try liquidRon.totalAssets{gas: blockGasLimit}() returns (uint256 _totalAssets) {
        totalAssets = _totalAssets;
    } catch {
        revert("OOG in totalAssets()");
    }

    // Assert that totalAssets is greater than 0
    assertTrue(totalAssets > 0, "totalAssets should be greater than 0");
}
```

The test fails with an `OutOfGas` error, demonstrating that `totalAssets()` consumes excessive gas and reverts when the number of staking proxies and consensus addresses is large.

### Recommended Mitigation Steps

1. **Optimize `totalAssets()` function**:
2. **Cache results**: Cache the results of expensive operations (e.g., staked amounts and rewards) to avoid recalculating them on every call.
3. **Batch processing**: Process staking proxies and consensus addresses in batches to reduce gas consumption per transaction.
4. **Off-chain calculation**: Use an off-chain service to calculate total assets and provide the result to the contract via a trusted oracle.
5. **Limit the number of proxies and consensus addresses**:
6. **Enforce limits**: Set a maximum limit on the number of staking proxies and consensus addresses that can be added to the contract.
7. **Prune inactive addresses**: Regularly prune inactive consensus addresses to reduce the number of iterations in `totalAssets()`.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Liquid Ron |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-01-liquid-ron
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-01-liquid-ron

### Keywords for Search

`vulnerability`

