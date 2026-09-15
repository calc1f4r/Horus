---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6320
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/23

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - csanuragjain
  - HollaDieWaldfee
  - sha256yan
  - kaliberpoziomka8552
  - cccz
---

## Vulnerability Title

[H-01] Lock.sol: assets deposited with Lock.extendLock function are lost

### Overview


This bug report is about the `Lock` contract in the code-423n4/2022-12-tigris repository which allows end-users to interact with bonds. There are two functions that allow to lock some amount of assets. The first function is `Lock.lock` which creates a new bond and the second function is `Lock.extendLock` which extends the lock for some `_period` and / or increases the locked amount by some `_amount`. 

The issue is that the `Lock.extendLock` function does not increase the value in `totalLocked[_asset]`. This however is necessary because `totalLocked[_asset]` is reduced when `Lock.release` is called. Therefore only the amount of assets deposited via `Lock.lock` can be released again. The amount of assets deposited using `Lock.extendLock` can never be released again because reducing `totalLocked[_asset]` will cause a revert due to underflow, causing the assets to be lost.

The recommended mitigation step is to add `totalLocked[_asset] += amount` to the `Lock.extendLock` function. This bug can be tested using the code provided in the report and running it with npx hardhat test --grep "release can cause underflow".

### Original Finding Content


<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/Lock.sol#L10> 

<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/Lock.sol#L61-L76> 

<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/Lock.sol#L84-L92> 

<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/Lock.sol#L98-L105>

### Impact

The `Lock` contract (<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/Lock.sol#L10>) allows end-users to interact with bonds.

There are two functions that allow to lock some amount of assets. The first function is `Lock.lock` (<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/Lock.sol#L61-L76>) which creates a new bond. The second function is `Lock.extendLock` (<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/Lock.sol#L84-L92>). This function extends the lock for some `_period` and / or increases the locked amount by some `_amount`.

The issue is that the `Lock.extendLock` function does not increase the value in `totalLocked[_asset]`. This however is necessary because `totalLocked[_asset]` is reduced when `Lock.release` (<https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/Lock.sol#L98-L105>) is called.

Therefore only the amount of assets deposited via `Lock.lock` can be released again. The amount of assets deposited using `Lock.extendLock` can never be released again because reducing `totalLocked[_asset]` will cause a revert due to underflow.

So the amount of assets deposited using `Lock.extendLock` is lost.

### Proof of Concept

1.  User A calls `Lock.lock` to lock a certain `_amount` (amount1) of `_asset` for a certain `_period`.
2.  User A calls then `Lock.extendLock` and increases the locked amount of the bond by some amount2
3.  User A waits until the bond has expired
4.  User A calls `Lock.release`. This function calculates `totalLocked[asset] -= lockAmount;`. Which will cause a revert because the value of `totalLocked[asset]` is only amount1

You can add the following test to the `Bonds` test in `Bonds.js`:

```javascript
describe("ReleaseUnderflow", function () {
    it("release can cause underflow", async function () {
        await stabletoken.connect(owner).mintFor(user.address, ethers.utils.parseEther("110"));
        // Lock 100 for 9 days
        await lock.connect(user).lock(StableToken.address, ethers.utils.parseEther("100"), 9);

        await bond.connect(owner).setManager(lock.address);

        await stabletoken.connect(user).approve(lock.address, ethers.utils.parseEther("10"));

        // Lock another 10
        await lock.connect(user).extendLock(1, ethers.utils.parseEther("10"), 0);

        await network.provider.send("evm_increaseTime", [864000]); // Skip 10 days
        await network.provider.send("evm_mine");

        // Try to release 110 after bond has expired -> Underflow
        await lock.connect(user).release(1);
    });
});
```

Run it with `npx hardhat test --grep "release can cause underflow"`.\
You can see that it fails because it causes an underflow.

### Tools Used

VS Code

### Recommended Mitigation Steps

Add `totalLocked[_asset] += amount` to the `Lock.extendLock` function.

**[TriHaz (Tigris Trade) confirmed](https://github.com/code-423n4/2022-12-tigris-findings/issues/23)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/23#issuecomment-1383078283):**
 > The warden has shown an issue with accounting that will cause principal deposits added via `extendLock` to be lost, for this reason I agree with High Severity.

**[GainsGoblin (Tigris Trade) resolved](https://github.com/code-423n4/2022-12-tigris-findings/issues/23#issuecomment-1407130352):**
 > Mitigation: https://github.com/code-423n4/2022-12-tigris/pull/2#issuecomment-1419172200



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | csanuragjain, HollaDieWaldfee, sha256yan, kaliberpoziomka8552, cccz, 0xbepresent, Ruhum, 0xsomeone, rvierdiiev, ali_shehab |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/23
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

