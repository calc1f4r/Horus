---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42512
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-biconomy
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/72

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-15] `WhitelistPeriodManager`: Improper state handling of exclusion removals

### Overview


The bug report is about an issue in the `WhitelistPeriodManager.sol` smart contract, which is used in the Biconomy project. The issue was discovered by two users, hickuphh3 and throttle. The problem is that the `totalLiquidity` and `totalLiquidityByLp` mappings are not updated correctly when an address is removed from the `isExcludedAddress` mapping. This can cause problems with enforcing limits and with a function called `getMaxCommunityLpPosition()`, but the main concern is that it can prevent users from withdrawing their staked LP tokens from the liquidity farming contract. 

The bug was demonstrated with a code example, showing how a user named Bob would be unable to withdraw their tokens due to a subtraction overflow. The recommended solution is to prevent exclusion removals by adding a function that only allows addresses to be excluded, but not removed from the exclusion list. 

The Biconomy team has confirmed the bug and a judge has decreased its severity to Medium, as it requires an external condition (the owner stopping the exclusion) and can be mitigated by using a different function.

### Original Finding Content

_Submitted by hickuphh3, also found by throttle_

[WhitelistPeriodManager.sol#L178-L184](https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/WhitelistPeriodManager.sol#L178-L184)<br>
[WhitelistPeriodManager.sol#L115-L125](https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/WhitelistPeriodManager.sol#L115-L125)<br>

The `totalLiquidity` and `totalLiquidityByLp` mappings are not updated when an address is removed from the `isExcludedAddress` mapping. While this affects the enforcement of the cap limits and the `getMaxCommunityLpPositon()` function, the worst impact this has is that the address cannot have liquidity removed / transferred due to subtraction overflow.

In particular, users can be prevented from withdrawing their staked LP tokens from the liquidity farming contract should it become non-excluded.

### Proof of Concept

*   Assume liquidity farming address `0xA` is excluded
*   Bob stakes his LP token
*   Liquidity farming contract is no longer to be excluded: `setIsExcludedAddressStatus([0xA, false])`
*   Bob attempts to withdraw liquidity → reverts because `totalLiquidityByLp[USDC][0xA] = 0`, resulting in subtraction overflow.

```jsx
// insert test case in Withdraw test block of LiquidityFarming.tests.ts
it.only('will brick withdrawals by no longer excluding farming contract', async () => {
  await farmingContract.deposit(1, bob.address);
  await wlpm.setIsExcludedAddressStatus([farmingContract.address], [false]);
  await farmingContract.connect(bob).withdraw(1, bob.address);
});

// results in
// Error: VM Exception while processing transaction: reverted with panic code 0x11 (Arithmetic operation underflowed or overflowed outside of an unchecked block)
```

### Recommended Mitigation Steps

The simplest way is to prevent exclusion removals.

```jsx
function setIsExcludedAddresses(address[] memory _addresses) external onlyOwner {
  for (uint256 i = 0; i < _addresses.length; ++i) {
    isExcludedAddress[_addresses[i]] = true;
    // emit event
    emit AddressExcluded(_addresses[i]);
  }
}
```

**[ankurdubey521 (Biconomy) confirmed](https://github.com/code-423n4/2022-03-biconomy-findings/issues/72)**

**[pauliax (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/72#issuecomment-1114794396):**
 > Great find, but I think it should be of Medium severity because it requires an external condition, the owner should stop excluding the contract, and also in case that happens, function setIsExcludedAddresses can be used to exclude this address again so the funds are not stuck forever in this case.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/72
- **Contest**: https://code4rena.com/reports/2022-03-biconomy

### Keywords for Search

`vulnerability`

