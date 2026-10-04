---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: oracle
vulnerability_type: read-only_reentrancy

# Attack Vector Details
attack_type: read-only_reentrancy
affected_component: oracle

# Source Information
source: solodit
solodit_id: 18493
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/141

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
  - read-only_reentrancy
  - oracle
  - flash_loan

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cuthalion0x
---

## Vulnerability Title

H-13: `BalancerPairOracle` can be manipulated using read-only reentrancy

### Overview


This bug report is about the `BalancerPairOracle` contract, which is used to calculate the price of a Balancer Pool Token (BPT). The issue is that the `BalancerPairOracle.getPrice` function makes an external call to `BalancerVault.getPoolTokens` without checking the Balancer Vault's reentrancy guard. This means that the Oracle can be manipulated to liquidate user positions prematurely, as the price calculation is based on a combination of token balances and BPT supply.

The vulnerability was found by cuthalion0x and was initially disclosed by the Balancer team in February. It was later exploited in a hack of the Sentiment protocol.

The code snippet provided is from the `BalancerPairOracle.sol` file, line 70 to 92. The tool used was manual review.

The Balancer team recommends using their official library to safeguard queries such as `Vault.getPoolTokens`. However, this library makes a state-modifying call to the Balancer Vault, so it is not suitable for `view` functions such as `BalancerPairOracle.getPrice`. There are two possible solutions: 1. Invoke the library somewhere else, such as in critical system functions like `BlueBerryBank.liquidate`, or 2. Adapt a slightly different read-only solution that checks the Balancer Vault's reentrancy guard without actually entering.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/141 

## Found by 
cuthalion0x
## Summary

`BalancerPairOracle.getPrice` makes an external call to `BalancerVault.getPoolTokens` without checking the Balancer Vault's reentrancy guard. As a result, the oracle can be trivially manipulated to liquidate user positions prematurely.

## Vulnerability Detail

In February, the Balancer team disclosed a read-only reentrancy vulnerability in the Balancer Vault. The detailed disclosure can be found [here](https://forum.balancer.fi/t/reentrancy-vulnerability-scope-expanded/4345). In short, all Balancer pools are susceptible to manipulation of their external queries, and all integrations must now take an extra step of precaution when consuming data. Via reentrancy, an attacker can force token balances and BPT supply to be out of sync, creating very inaccurate BPT prices.

Some protocols, such as Sentiment, remained unaware of this issue for a few months and were later [hacked](https://twitter.com/spreekaway/status/1643313471180644360) as a result.

`BalancerPairOracle.getPrice` makes a price calculation of the form `f(balances) / pool.totalSupply()`, so it is clearly vulnerable to synchronization issues between the two data points. A rough outline of the attack might look like this:

```solidity
AttackerContract.flashLoan() ->
    // Borrow lots of tokens and trigger a callback.
    SomeProtocol.flashLoan() ->
        AttackerContract.exploit()

AttackerContract.exploit() ->
    // Join a Balancer Pool using the borrowed tokens and send some ETH along with the call.
    BalancerVault.joinPool() ->
        // The Vault will return the excess ETH to the sender, which will reenter this contract.
        // At this point in the execution, the BPT supply has been updated but the token balances have not.
        AttackerContract.receive()

AttackerContract.receive() ->
    // Liquidate a position using the same Balancer Pool as collateral.
    BlueBerryBank.liquidate() ->
        // Call to the oracle to check the price.
        BalancerPairOracle.getPrice() ->
            // Query the token balances. At this point in the execution, these have not been updated (see above).
            // So, the balances are still the same as before the start of the large pool join.
            BalancerVaul.getPoolTokens()

            // Query the BPT supply. At this point in the execution, the supply has already been updated (see above).
            // So, it includes the latest large pool join, and as such the BPT supply has grown by a large amount.
            BalancerPool.getTotalSupply()

            // Now the price is computed using both balances and supply, and the result is much smaller than it should be.
            price = f(balances) / pool.totalSupply()

        // The position is liquidated under false pretenses.
```

## Impact

Users choosing Balancer pool positions (such as Aura vaults) as collateral can be prematurely liquidated due to unreliable price data.

## Code Snippet

https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/oracle/BalancerPairOracle.sol#L70-L92

## Tool used

Manual Review

## Recommendation

The Balancer team recommends utilizing their [official library](https://github.com/balancer/balancer-v2-monorepo/blob/3ce5138abd8e336f9caf4d651184186fffcd2025/pkg/pool-utils/contracts/lib/VaultReentrancyLib.sol) to safeguard queries such as `Vault.getPoolTokens`. However, the library makes a state-modifying call to the Balancer Vault, so it is not suitable for `view` functions such as `BalancerPairOracle.getPrice`. There are then two options:
1. Invoke the library somewhere else. Perhaps insert a hook into critical system functions like `BlueBerryBank.liquidate`.
2. Adapt a slightly different read-only solution that checks the Balancer Vault's reentrancy guard without actually entering.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | cuthalion0x |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/141
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Read-only Reentrancy, Oracle, Flash Loan`

