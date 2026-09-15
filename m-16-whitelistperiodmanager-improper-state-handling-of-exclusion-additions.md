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
solodit_id: 42513
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-biconomy
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/75

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

[M-16] `WhitelistPeriodManager`: Improper state handling of exclusion additions

### Overview


This bug report is about an issue with the `totalLiquidity` and `totalLiquidityByLp` mappings in the `WhitelistPeriodManager.sol` contract. These mappings are not being updated properly when an address is added to the `isExcludedAddress` mapping, causing problems with the cap limits and a function called `getMaxCommunityLpPositon()`. This function is supposed to return a value of 0 for an address that is excluded from the whitelist, but it is returning a value of 500 instead. This means that excluded addresses are still able to provide liquidity, which is not intended. A recommended solution is to check that an address has no liquidity before adding it to the `isExcludedAddress` mapping. The severity of this issue has been determined to be medium.

### Original Finding Content

_Submitted by hickuphh3_

[WhitelistPeriodManager.sol#L178-L184](https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/WhitelistPeriodManager.sol#L178-L184)<br>
[WhitelistPeriodManager.sol#L83-L99](https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/WhitelistPeriodManager.sol#L83-L99)<br>

The `totalLiquidity` and `totalLiquidityByLp` mappings are not updated when an address is added to the `isExcludedAddress` mapping. This affects the enforcement of the cap limits and the `getMaxCommunityLpPositon()` function, which implicitly assumes that whitelisted addresses will have 0 liquidity, for addresses with non-zero liquidity at the time of addition to the whitelist.

### Proof of Concept

*   Assume the following initial conditions:
    *   Alice’s address `0xA` is the sole USDC liquidity provider
        *   `totalLiquidity[USDC] = 500`
        *   `totalLiquidity[USDC][0xA] = 500`
    *   USDC total cap of `500`, ie. `perTokenTotalCap[USDC] = 500`
*   Exclude Alice’s address `0xA`: `setIsExcludedAddressStatus([0xA, true])`
    *   totalLiquidity mappings are unchanged
*   The following deviant behaviour is observed:
    *   `getMaxCommunityLpPositon()` returns `500` when it should return `0`
    *   All non-excluded addresses are unable to provide liquidity when they should have been able to, as Alice’s liquidity should have been excluded.
    ```jsx
    // insert test case in WhitelistPeriodManager.test.ts
    describe.only("Test whitelist addition", async () => {
      it('produces deviant behaviour if excluding address with existing liquidity', async () => {
        await wlpm.setCaps([token.address], [500], [500]);
        await liquidityProviders.connect(owner).addTokenLiquidity(token.address, 500);
        await wlpm.setIsExcludedAddressStatus([owner.address], [true]);
        // 1) returns 500 instead of 0
        console.log((await wlpm.getMaxCommunityLpPositon(token.address)).toString());
        // 2) bob (or other non-excluded addresses) will be unable to add liquidity
        await expect(liquidityProviders.connect(bob).addTokenLiquidity(token.address, 1)).to.be.revertedWith('ERR__LIQUIDITY_EXCEEDS_PTTC');
      });
    });
    ```

### Recommended Mitigation Steps

Check that the address to be excluded is not holding any LP token at the time of exclusion.

```jsx
// in setIsExcludedAddressStatus()
for (uint256 i = 0; i < _addresses.length; ++i) {
  if (_status[i]) {
    require(lpToken.balanceOf(_addresses[i]) == 0, 'address has existing liquidity');
  }
  ...
}
```

**[ankurdubey521 (Biconomy) confirmed](https://github.com/code-423n4/2022-03-biconomy-findings/issues/75)**

**[pauliax (judge) commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/75#issuecomment-1114843528):**
 > I think it is a different issue than M-15, based on the description it deserves a severity of Medium.



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
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/75
- **Contest**: https://code4rena.com/reports/2022-03-biconomy

### Keywords for Search

`vulnerability`

