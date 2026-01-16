---
# Core Classification
protocol: stETH by EaseDeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64085
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1203
source_link: none
github_link: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/212

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
finders_count: 25
finders:
  - HeckerTrieuTien
  - slcoder
  - OxSath404
  - axelot
  - Vesko210
---

## Vulnerability Title

M-2: Missing Tranche Tracking After `extendDeposit()` Causes Temporary Asset Underreporting

### Overview


This bug report discusses a vulnerability found in the `extendDeposit()` function of the stNXM contract. This function allows users to move their staking position from one tranche to another in the Nexus Mutual pool. However, the function fails to update the `tokenIdToTranches` mapping, which tracks the tranches that a staking position is in. As a result, when the `stakedNxm()` function is called, it only queries the old tranche (which now has 0 deposits) and misses the extended position in the new tranche. This causes the `totalAssets()` function to underreport the vault assets until the `resetTranches()` function is called, resulting in a temporary but real accounting discrepancy.

The vulnerable code is located in the `stNXM.sol` file and can be found on lines 366-380. This code is missing a line that tracks the new tranche in the `tokenIdToTranches` mapping. The correct pattern for this can be found in the `_stakeNxm()` function on lines 366-380. This function correctly tracks the new tranche when a staking position is created.

The impact of this bug is an accounting error. After using the `extendDeposit()` function, the new tranche is not tracked in the `tokenIdToTranches` mapping. As a result, when the `stakedNxm()` function is called, it only queries the old tranche and misses the extended position in the new tranche. This results in the `totalAssets()` function underreporting the vault assets until the `resetTranches()` function is called. This can be exploited by an attacker who can deposit more funds and receive an artificially high number of shares due to the incorrect share price. However, this error is temporary and self-corrects within 91 days. The severity of this bug is considered medium, as it requires specific conditions to be exploited and can be quickly corrected through the permissionless `resetTranches()` function.

A proof of concept (POC) is provided in the report to demonstrate the impact of this bug. It shows how an attacker can exploit the accounting error to receive more value than they deposited. The report also includes a recommendation to fix this bug, which involves immediately tracking the new tranche in the `tokenIdToTranches` mapping after extending the deposit.

The protocol team has already fixed this issue in the following PRs/commits: https://github

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/212 

## Found by 
0x73696d616f, 0x97, 0xDLG, 0xgh0stcybers3c, 0xsai, AestheticBhai, Drynooo, HeckerTrieuTien, IzuMan, Orhukl, OxSath404, Solea, Vesko210, Ziusz, asui, axelot, blockace, edger, ivxylo, oxwhite, slcoder, theboiledcorn, thimthor, werulez99, zaida

## Summary

The `extendDeposit()` function moves a staking position from one tranche to another in the Nexus Mutual pool but fails to update the `tokenIdToTranches` mapping. When `stakedNxm()` is subsequently called, it only queries the old tranche (which now has 0 deposits) and misses the extended position in the new tranche. This causes `totalAssets()` to underreport vault assets until `resetTranches()` is called, creating a temporary but real accounting discrepancy.

**Location:** [stNXM.sol](https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi/blob/main/stNXM-Contracts/contracts/core/stNXM.sol#L366-L380)

**Vulnerable Code:**
```solidity
function extendDeposit(uint256 _tokenId, uint256 _initialTrancheId, uint256 _newTrancheId, uint256 _topUpAmount)
    external
    onlyOwner
    update
{
    address stakingPool = tokenIdToPool[_tokenId];

    if (_topUpAmount > 0) {
        wNxm.unwrap(_topUpAmount);
        nxm.approve(nxmMaster.getLatestAddress("TC"), _topUpAmount);
    }

    IStakingPool(stakingPool).extendDeposit(_tokenId, _initialTrancheId, _newTrancheId, _topUpAmount);
    // ❌ Missing: tokenIdToTranches[_tokenId].push(_newTrancheId);
}
```

**Correct Pattern (from `_stakeNxm()`):**
```solidity
function _stakeNxm(uint256 _amount, address _poolAddress, uint256 _trancheId, uint256 _requestTokenId) internal {
    // ... approval logic ...
    uint256 tokenId = pool.depositTo(_amount, _trancheId, _requestTokenId, address(this));
    tokenIdToTranches[tokenId].push(_trancheId); // ✅ Correctly tracks new tranche
    // ...
}
```

## Impact

**Accounting Error:**
- After `extendDeposit()`, the new tranche is NOT tracked in `tokenIdToTranches`
- `stakedNxm()` loops through tracked tranches and queries Nexus: `getDeposit(tokenId, tranche)`
- For the new tranche: `getDeposit(tokenId, newTranche)` returns the extended funds but is never queried
- Result: `totalAssets()` underreports by the amount of the extended stake

**Exploitation Scenario:**
```bash
1. Initial state: 10,000 wNXM staked in tranche T1
   - totalAssets = 10,000
   - totalSupply = 10,000 shares
   - Share price = 1.0

2. Owner calls: extendDeposit(tokenId, T1, T2, 5000)
   - T2 now has 10,000 + 5000 = 15,000 wNXM
   - But tokenIdToTranches still = [T1]

3. stakedNxm() calculation:
   - Queries getDeposit(tokenId, T1) → 0 (was moved)
   - Never queries T2 (not tracked)
   - Returns 0

4. totalAssets now reports: 0 (artificially low!)
   - Share price drops to 0

5. Attacker deposits 5,000 wNXM:
   - Gets 5,000 / 0 = very high number of shares
   - Extreme share inflation

6. Someone calls resetTranches():
   - Discovers T2 has deposits
   - Updates tokenIdToTranches = [T2]
   - totalAssets corrects back to 15,000

7. Attacker redeems shares at corrected price
   - Extracts significantly more value than deposited
```

**Severity Justification:**
- Temporary accounting error that self-corrects within 91 days
- Requires specific conditions (owner using `extendDeposit`)
- Exploitable but correction is permissionless and quick
- Financial impact: Medium (temporary share inflation/deflation)

## POC

```solidity
function testExtendDepositAccountingError() public {
    // Setup: Initial staking position
    uint256 initialStake = 10000 ether;
    depositWNXM(initialStake, wnxmWhale);
    
    uint256 currentTranche = block.timestamp / 91 days;
    stakeNxm(initialStake, riskPools[0], currentTranche, tokenIds[0]);

    // Record initial state
    uint256 initialAssets = stNxm.totalAssets();
    uint256 initialSupply = stNxm.totalSupply();
    
    console.log("Before extend:");
    console.log("  totalAssets:", initialAssets);
    console.log("  totalSupply:", initialSupply);
    console.log("  tracked tranches:", stNxm.tokenIdToTranches(tokenIds[0]).length);

    // Owner extends deposit to new tranche
    uint256 extensionAmount = 5000 ether;
    uint256 newTranche = currentTranche + 4;

    vm.startPrank(multisig);
    stNxm.extendDeposit(tokenIds[0], currentTranche, newTranche, extensionAmount);
    vm.stopPrank();

    // Check accounting after extension (BEFORE resetTranches)
    uint256 assetsAfterExtend = stNxm.totalAssets();
    uint256[] memory tranchesAfter = stNxm.tokenIdToTranches(tokenIds[0]);

    console.log("\nAfter extend (before resetTranches):");
    console.log("  totalAssets:", assetsAfterExtend);
    console.log("  tracked tranches length:", tranchesAfter.length);
    
    // BUG: totalAssets doesn't increase
    // Extended funds exist in Nexus but aren't counted
    uint256 expectedIncrease = extensionAmount; // Should increase by at least this
    require(assetsAfterExtend < initialAssets + expectedIncrease, "Assets should have increased more");

    // Verify funds actually exist in Nexus pool
    IStakingPool pool = IStakingPool(riskPools[0]);
    (,, uint256 sharesInNewTranche,) = pool.getDeposit(tokenIds[0], newTranche);
    require(sharesInNewTranche > 0, "Deposit exists in new tranche");

    // Now call resetTranches - this fixes the accounting
    stNxm.resetTranches();

    uint256 assetsAfterReset = stNxm.totalAssets();
    uint256[] memory tranchesAfterReset = stNxm.tokenIdToTranches(tokenIds[0]);

    console.log("\nAfter resetTranches:");
    console.log("  totalAssets:", assetsAfterReset);
    console.log("  tracked tranches length:", tranchesAfterReset.length);

    // NOW assets are correct
    require(assetsAfterReset >= initialAssets + (extensionAmount / 2), "Assets corrected after reset");
    require(tranchesAfterReset.length >= 2, "New tranche now tracked");
}
```

## Recommendation

Add tranche tracking immediately after extending the deposit:

```solidity
function extendDeposit(uint256 _tokenId, uint256 _initialTrancheId, uint256 _newTrancheId, uint256 _topUpAmount)
    external
    onlyOwner
    update
{
    address stakingPool = tokenIdToPool[_tokenId];

    if (_topUpAmount > 0) {
        wNxm.unwrap(_topUpAmount);
        nxm.approve(nxmMaster.getLatestAddress("TC"), _topUpAmount);
    }

    IStakingPool(stakingPool).extendDeposit(_tokenId, _initialTrancheId, _newTrancheId, _topUpAmount);

    // Fix: Track the new tranche immediately
    tokenIdToTranches[_tokenId].push(_newTrancheId);

    // Optional: Consider removing _initialTrancheId if fully moved
    // This prevents querying a tranche with 0 deposits
}
```


## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/EaseDeFi/stNXM-Contracts/commit/40630a0d88fdd663803afb73dfb9437ae01707ed






### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | stETH by EaseDeFi |
| Report Date | N/A |
| Finders | HeckerTrieuTien, slcoder, OxSath404, axelot, Vesko210, oxwhite, Solea, zaida, 0x97, Orhukl, blockace, IzuMan, Drynooo, thimthor, edger, 0x73696d616f, AestheticBhai, theboiledcorn, 0xDLG, ivxylo, asui, werulez99, 0xsai, 0xgh0stcybers3c, Ziusz |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-11-stnxm-by-easedefi-judging/issues/212
- **Contest**: https://app.sherlock.xyz/audits/contests/1203

### Keywords for Search

`vulnerability`

