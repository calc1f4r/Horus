---
# Core Classification
protocol: Staking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51793
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/altcoinist/staking
source_link: https://www.halborn.com/audits/altcoinist/staking
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

WETH rewards conversion to ALTT rewards might not be possible in the staking vault

### Overview


The report describes a bug in the StakingVault contract that allows anyone to call the `initWethConversion()` function after the Token Generation Event (TGE) and convert all accumulated WETH into ALTT. This function includes a check to ensure that the WETH balance is greater than or equal to the total WETH staked before the TGE and that the total WETH staked is greater than 0. However, if all users withdraw their WETH before this function is called, the remaining WETH in the contract will be stuck, preventing it from being converted into ALTT and distributed as rewards. The report provides a proof of concept and a BVSS score for the bug and recommends removing the redundant `require` statement to mitigate the issue. The bug has been solved by the Altcoinist team and the remediation hash is provided for reference.

### Original Finding Content

##### Description

Anyone can call `StakingVault::initWethConversion()` after the Token Generation Event (TGE) to convert all accumulated WETH into ALTT by initiating a swap.

The function includes the following check:

```
require(wethBalance >= wethDepositSum && wethDepositSum > 0);
```

This ensures two conditions:

1. The actual WETH balance of the staking vault must be greater than or equal to the total WETH staked before the TGE.
2. The total WETH staked must be greater than 0.

However, if all users withdraw their WETH before this function is called, the remaining WETH in the contract will be stuck. This means it cannot be converted into ALTT to be distributed as rewards, effectively locking those funds in the contract.

##### Proof of Concept

Add the following test to provided PoC file:

```
    function test_no_WETH_conversion() public {
        console.log("[+] Alice buys Lifetime Sub and stakes 10,000 WETH before TGE");
        _subscribe(alice, carol, SubscribeRegistry.packages.LIFETIME, 1, 1000e18, address(0), true);

        test_init_TGE();
        console.log("[+] All the staked WETH is withdrawn after TGE");
        vm.prank(alice);
        IStakingVault(authorVault).withdrawWeth(10000e18);

        vm.expectRevert();
        IStakingVault(authorVault).initWethConversion();
    }
```

Run `forge test --mt "test_no_WETH_conversion" -vvvv`

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:M/A:L/D:N/Y:M/R:N/S:U (4.6)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:M/A:L/D:N/Y:M/R:N/S:U)

##### Recommendation

Remove the `require` statement as it is redundant. By removing this check, we ensure that WETH can be converted into ALTT and distributed as rewards even if all users have withdrawn their WETH before this function is called.

##### Remediation

**SOLVED**: The suggested mitigation was applied by the **Altcoinist team**.

##### Remediation Hash

<https://github.com/altcoinist-com/contracts/commit/d812e2eb63c4bacfbee39dbd35c3058f73800e2c>

##### References

[altcoinist-com/contracts/src/StakingVault.sol#L197](https://github.com/altcoinist-com/contracts/blob/master/src/StakingVault.sol#L197)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Staking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/altcoinist/staking
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/altcoinist/staking

### Keywords for Search

`vulnerability`

