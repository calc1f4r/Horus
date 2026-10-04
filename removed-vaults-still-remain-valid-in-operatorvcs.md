---
# Core Classification
protocol: Liquid Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43668
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp
source_link: none
github_link: https://github.com/Cyfrin/2024-09-stakelink

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
finders_count: 9
finders:
  - bladesec
  - KrisRenZo
  - slvDev
  - avoloder
  - Joseph
---

## Vulnerability Title

Removed vaults still remain valid in `OperatorVCS`

### Overview


The report discusses a bug in a contract called `OperatorVCS`. The bug allows removed vaults to continue interacting with the contract, even though they should not be able to. This is because the function responsible for removing the vaults does not update a mapping that keeps track of active vaults. This means that removed vaults can still withdraw rewards, which is a high-risk issue. The report provides details on the vulnerable code and suggests a fix, along with a test to verify the fix. The tools used for this report were VScode and manual review. The recommendation is to modify the `removeVault` function to update the vault's mapping and prevent removed vaults from being considered valid. 

### Original Finding Content

## Summary

`OperatorVCS::removeVault` doesn't  update the `vaultMapping` which allows removed vaults to continue interacting with the strategy which is not intended.

## Impact

The function fails to update the `vaultMapping`, which means that even after a vault is removed, its address would still return true when checked against the `vaultMapping` and  removed vaults could continue withdrawing operator rewards

## Vulnerability Details

`removeVault` function is responsible for removing a vault from the strategy. Albeit, while it removes the vault from the `vaults` array, it doesn't update the `vaultMapping`. As a result, removed vaults are still considered valid by the contract and can continue to call functions that should only be restricted to active vaults.

<https://github.com/Cyfrin/2024-09-stakelink/blob/f5824f9ad67058b24a2c08494e51ddd7efdbb90b/contracts/linkStaking/OperatorVCS.sol#L324-L331>

```solidity
304:     function removeVault(uint256 _queueIndex) public {
305:         address vault = vaultsToRemove[_queueIndex];
306: 
307:         vaultsToRemove[_queueIndex] = vaultsToRemove[vaultsToRemove.length - 1];
308:         vaultsToRemove.pop();
309: 
310:         _updateStrategyRewards();
311:         (uint256 principalWithdrawn, uint256 rewardsWithdrawn) = IOperatorVault(vault).exitVault();
312: 
313:         totalDeposits -= principalWithdrawn + rewardsWithdrawn;
314:         totalPrincipalDeposits -= principalWithdrawn;
315: 
316:         uint256 numVaults = vaults.length;
317:         uint256 index;
318:         for (uint256 i = 0; i < numVaults; ++i) {
319:             if (address(vaults[i]) == vault) {
320:                 index = i;
321:                 break;
322:             }
323:         }
324:         for (uint256 i = index; i < numVaults - 1; ++i) {
325:             vaults[i] = vaults[i + 1];
326:         }
327:         vaults.pop();
328:         vaultMapping[vault] = false;
329:         token.safeTransfer(address(stakingPool), token.balanceOf(address(this)));
330:     }

```

Add this test to `operator-vcs.test.ts`

```typescript
it('removeVault should update vaultMapping correctly', async () => {
    const { accounts, strategy, stakingPool, vaults, stakingController, fundFlowController } = await loadFixture(deployFixture)

    // Initial setup
    await stakingPool.deposit(accounts[0], toEther(1000), [encodeVaults([])])
    await fundFlowController.updateVaultGroups()
    await time.increase(claimPeriod)
    await fundFlowController.updateVaultGroups()

    // Remove an operator and queue the vault for removal
    await stakingController.removeOperator(vaults[5])
    await strategy.queueVaultRemoval(5)

    // Wait for the unbonding period
    await time.increase(unbondingPeriod)
    await fundFlowController.updateVaultGroups()

    // Remove the vault
    await strategy.removeVault(0)

    // We verify that the vault is no longer in the vaults array
    const remainingVaults = await strategy.getVaults()
    assert.isFalse(remainingVaults.includes(vaults[5]), "Vault should be removed from vaults array")

    //Let's check if the removed vault is still considered valid by the strategy
    const isVaultValid = await strategy.isVaultValid(vaults[5])

    // This should be false if the suggested fix in the recommendation is applied
    assert.isFalse(isVaultValid, "Removed vault should not be considered valid")

    // Attempt to withdraw operator rewards for the removed vault
    // This should now revert after the fix
    await expect(strategy.withdrawOperatorRewards(accounts[1], 1))
      .to.be.revertedWithCustomError(strategy, "SenderNotAuthorized")
})
```

* Firstly, add this function to the `OperatorVCS.sol` contract:

```solidity
function isVaultValid(address vault) public view returns (bool) {
    return vaultMapping[vault];
}
```

Then run the poc test with:

* `yarn test test/linkStaking/operator-vcs.test.ts`

The test should fail which means that removed vaults are still considered valid.

* Update the `removeVault` function in the OperatorVCS contract using the recommendation in the recommendations section below:
* Run the test again. itll pass which shows the issue has been mitigated( i.e removed vaults are not valid anymore)

## Tools Used

\-- Vscode
\-- Manual review

## Recommendations

Modify the `removeVault` function to set the vault's mapping to false:

```diff
 function removeVault(uint256 _queueIndex) public {
        address vault = vaultsToRemove[_queueIndex];

        vaultsToRemove[_queueIndex] = vaultsToRemove[vaultsToRemove.length - 1];
        vaultsToRemove.pop();

        _updateStrategyRewards();
        (uint256 principalWithdrawn, uint256 rewardsWithdrawn) = IOperatorVault(vault).exitVault();

        totalDeposits -= principalWithdrawn + rewardsWithdrawn;
        totalPrincipalDeposits -= principalWithdrawn;

        uint256 numVaults = vaults.length;
        uint256 index;
        for (uint256 i = 0; i < numVaults; ++i) {
            if (address(vaults[i]) == vault) {
                index = i;
                break;
            }
        }
        for (uint256 i = index; i < numVaults - 1; ++i) {
            vaults[i] = vaults[i + 1];
        }
        vaults.pop();
+        vaultMapping[vault] = false;

        token.safeTransfer(address(stakingPool), token.balanceOf(address(this)));
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Liquid Staking |
| Report Date | N/A |
| Finders | bladesec, KrisRenZo, slvDev, avoloder, Joseph, baz1ka, zubyoz, 1337web3, Rhaydden |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-09-stakelink
- **Contest**: https://codehawks.cyfrin.io/c/cm1el4vjp00019d2nzombxfzp

### Keywords for Search

`vulnerability`

