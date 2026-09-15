---
# Core Classification
protocol: Numa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45280
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/554
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/41

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - juaan
---

## Vulnerability Title

M-3: CF minimum can be bypassed when minting nuAssets

### Overview


The report describes a bug found in the code for minting nuAssets. The bug allows users to bypass the minimum collateral factor (CF) requirement, which can lead to assets being minted even when the CF is below the critical level of 110%. This goes against the intended behavior stated in the README. The bug is caused by the CF being checked before the minting of nuAssets, rather than after. This allows users to mint a large number of nuAssets, effectively bypassing the warning CF. The impact of this bug is not specified, but a proof of concept (PoC) is provided to demonstrate its existence. To fix the bug, the modifier responsible for checking the CF should be updated to ensure that it is checked after the minting of nuAssets. The discussion among the team members suggests that this bug may not be considered valid, but further investigation is needed.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/41 

## Found by 
juaan

### Summary

CF is checked before minting nuAssets (instead of after), allowing CF to be massively decreased past the warning. This allows assets to be minted even past the critical CF of 110%, breaking the invariant stated in the README. 

[`NumaPrinter.mintNuAsset()`](https://github.com/sherlock-audit/2024-12-numa-audit/blob/ae1d7781efb4cb2c3a40c642887ddadeecabb97d/Numa/contracts/NumaProtocol/NumaPrinter.sol#L179) has the `notInWarningCF` modifier

```solidity
modifier notInWarningCF() {
	  uint currentCF = vaultManager.getGlobalCF();
	  require(currentCF > vaultManager.getWarningCF(), "minting forbidden");
	  _;
}
```

Invariant stated in the README is bypassed:

> New synthetics cannot be minted when CFTHEORETICAL < 110%, where CFTHEORETICAL = rETH_accountingBalance / synthetic_rETHdebt.


### Root Cause

The modifier checks the CF before the minting of the nuAssets.

This means that a user can mint a large number of nuAssets to effectively minting past the warning CF.

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

_No response_

### PoC

The PoC shows that the CF goes from `1e5` to  `1.0527e4` during the mint, while the warning CF is `9.9999e4`, so the warning CF has been bypassed, and assets have effectively been minted past the warning CF which should not be allowed. 

Add the test to `Printer.t.sol`
```solidity
function test_mintPastCF() public {
    uint numaAmount = 1000001e18;

    vm.startPrank(deployer);
    numa.transfer(userA, numaAmount);
    vm.stopPrank();
    
    vm.startPrank(userA);

    // compare getNbOfNuAssetFromNuma
    (uint256 nuUSDAmount, uint fee) = moneyPrinter.getNbOfNuAssetFromNuma(
        address(nuUSD),
        numaAmount
    );
    numa.approve(address(moneyPrinter), numaAmount);

    // warning cf test block mint
    uint globalCFBefore = vaultManager.getGlobalCF();


    // put back warning cf
    vm.startPrank(deployer);
    vaultManager.setScalingParameters(
        vaultManager.cf_critical(),
        globalCFBefore - 1,
        vaultManager.cf_severe(),
        vaultManager.debaseValue(),
        vaultManager.rebaseValue(),
        1 hours,
        2 hours,
        vaultManager.minimumScale(),
        vaultManager.criticalDebaseMult()
    );

    console.log("globalCFBefore: %e", globalCFBefore);
    console.log("warningCF: %e", vaultManager.getWarningCF());

    vm.startPrank(userA);

    // slippage ok
    moneyPrinter.mintAssetFromNumaInput(
        address(nuUSD),
        numaAmount,
        nuUSDAmount,
        userA
    );

    uint globalCFAfter = vaultManager.getGlobalCF();
    uint warningCF = vaultManager.getWarningCF();

    console.log("globalCFAfter: %e", globalCFAfter);
    console.log("warningCF: %e", warningCF);

    assertGt(globalCFBefore, warningCF);
    assertLt(globalCFAfter, warningCF);
}
```

### Mitigation

Update the modifier in the following way:

```diff
modifier notInWarningCF() {
+	  _;
	  uint currentCF = vaultManager.getGlobalCF();
	  require(currentCF > vaultManager.getWarningCF(), "minting forbidden");
-	  _;
}
```

This ensures that the CF is checked after minting the nuAssets, so it can't be bypassed.

## Discussion

**tibthecat**

Not sure about that one. Needs to check with team. The goal is to block minting when CF has already reached WarningCF, not to prevent from reaching this warningCF. 
Will check with team, but my current opinion is that it's invalid.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Numa |
| Report Date | N/A |
| Finders | juaan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/41
- **Contest**: https://app.sherlock.xyz/audits/contests/554

### Keywords for Search

`vulnerability`

