---
# Core Classification
protocol: Wonderland
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54121
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5295cf96-7a54-4150-9d94-396944b3604e
source_link: https://cdn.cantina.xyz/reports/cantina_wonderland_jul2024.pdf
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
finders_count: 4
finders:
  - shung
  - Optimum
  - 0xicingdeath
  - r0bert
---

## Vulnerability Title

Improvements on Fuzzing Suite 

### Overview

See description below for full details.

### Original Finding Content

## Recommendations for Improving Invariant Tests in Wonderland OpUSDC Codebase

## Context
(No context files were provided by the reviewer)

## Description
The Wonderland OpUSDC codebase has a significant number of invariant tests. The below provides recommendations on improvements and enhancements that can be made to increase coverage.

### 1. Add Relevant Assertions to All Empty Catch Clauses
Not checking anything within these clauses can result in missed corner cases. While it may be difficult to fully match all preconditions required for a successful call, start by documenting all the cases in which the attempted call may revert, such that implementing an assertion should not be too much effort.

For example, take id-14 – where the catch clause is empty:

```solidity
/// @custom:property-id 14
/// @custom:property Incoming successful messages should only come from the linked adapter's
function fuzz_l2LinkedAdapterIncommingMessages(uint8 _selectorIndex, uint256 _amount, address _address) public {
    _selectorIndex = _selectorIndex % 3;
    hevm.prank(l2Adapter.MESSENGER());
    
    if (_selectorIndex == 0) {
        try l2Adapter.receiveMessage(_address, _amount) {
            // Mint tokens to L1 adapter to keep the balance consistent
            hevm.prank(_usdcMinter);
            usdcMainnet.mint(address(l1Adapter), _amount);
            assert(mockMessenger.xDomainMessageSender() == address(l1Adapter));
        } catch {}
    }
}
```
From here, if we add an `assert(false)` into the catch statement, we can quickly see there is a failure of `InvalidSender` because the sender is not correct. This showcases why adding assertions to the catch statement is important, and the failure to do so can provide a false sense of security.

```
fuzz_l2LinkedAdapterIncommingMessages(uint8,uint256,address): failed!
Call sequence:
OpUsdcTest.fuzz_l2LinkedAdapterIncommingMessages(0,0,0x0)
Traces:
call 0x159932407dC2226A7EFAF9A9E7E224Be35537269::MESSENGER()
...
error Revert IOpUSDCBridgeAdapter_InvalidSender () 
```

### 2. Add Specific Invariant Functions to Test the Transition of Status
Id 18 tests that the status must either be one of the four message statuses which may work; however, it is a relatively basic check considering the enum only has four possible states. Instead, consider adding specific invariant checks that only check the adjustment and changing of state.

### 3. Ensure Invariants Reflect Realistic Behaviour
The invariants may provide a false sense of security, depending on how they are worded. Some examples can be found below:

- USDC proxy admin and token ownership rights **can only** be transferred during the migration to native flow (id-17) – this is not, precisely, what the fuzzing suite is checking. The fuzzing suite is checking that when the `transferUSDCRoles` function is called, the owner and the admin addresses are updated, but the fuzzer provides no guarantees that these addresses can only change while calling this function.

- Resume should be able to be set only by the owner and through the correct function (id-8) – similar to above, this provides no guarantee that this is the only way that the owner address can change. This test merely checks that through calling the `resumeMessaging` function, the output / post-condition state is correct.

- Incoming successful messages should only come from the linked adapter's (id-14) – this is also not exactly what the fuzzing test is currently testing. Regardless of `_selectorIndex`, different `receiveX` functions are being called and asserting that the `xDomainMessageSender` is equivalent to `l1Adapter`. As the catch clauses are empty (related to bullet point 1), this invariant test does not actually test the failure case.

- Set burn only if migrating (id-9) – the test itself doesn’t actually mention any form of migration or call any functions that are migration-related. The more accurate phrasing for this would be some variation of: "Set burnAmount on L1 if messengerStatus is UPGRADING."

- Can receive USDC even if the state is not active (id-12) – this property seemingly violates Circle's token standard expectations where it can "pause USDC bridging to create a lock on total supply".

### 4. Be Careful Using hevm.prank in the Fuzzing Suite
As highlighted in bullet point 1, issues can arise as only the subsequent call immediately after the prank call is to be pranked, which can result in calls looking like they were successful but actually failing. Care must be taken to ensure that all functions that are expected to run successfully have actually executed and did not revert with error messages similar to "InvalidSender" or variations thereof.

For example, the first hevm prank is not being applied to the `receiveMessage` call – it is applying to the call immediately after, the require statement, which doesn’t need any form of checking.

```solidity
/// @custom:property-id 14
/// @custom:property Incoming successful messages should only come from the linked adapter's
function fuzz_l1LinkedAdapterIncommingMessages(uint8 _selectorIndex, uint256 _amount, address _address) public {
    _selectorIndex = _selectorIndex % 2;
    
    if (_selectorIndex == 0) {
        hevm.prank(l1Adapter.MESSENGER());
        require(usdcMainnet.balanceOf(address(l1Adapter)) >= _amount);
        
        try l1Adapter.receiveMessage(_address, _amount) {
            // Mint tokens to L1 adapter to keep the balance consistent
            hevm.prank(_usdcMinter);
            usdcMainnet.mint(address(l1Adapter), _amount);
            assert(mockMessenger.xDomainMessageSender() == address(l2Adapter));
        } catch { assert(false); }
    }
}
```

### 5. Use the Coverage Reports Every Time You Run the Fuzzer
Manual analysis of the coverage report is needed to ensure your invariants are correct and your fuzzing suite is thoroughly investigating all branches you would expect it would.

- id-14 example
- id-12 example

### 6. Use Try-Catch Clauses and Nest Them if Needed
In id-11, the assumption is that the first call to `migrateToNative` is successful; therefore, the fuzzer should try to call the function a second time with the same arguments.

```solidity
/// @custom:property-id 11
/// @custom:property Upgrading state only via migrate to native, should be callable multiple times (msg fails)
function fuzz_migrateToNativeMultipleCall(address _burnCaller, address _roleCaller) public {
    // Precondition: ensure we haven’t started the migration or we only initiated/is pending in the bridge
    require(
        l1Adapter.messengerStatus() == IL1OpUSDCBridgeAdapter.Status.Active ||
        l1Adapter.messengerStatus() == IL1OpUSDCBridgeAdapter.Status.Upgrading
    );
    require(_burnCaller != address(0) && _roleCaller != address(0));
    
    // As the bridge would relay and execute the migration atomically, including deprecating l1adapter
    mockMessenger.pauseMessaging();
    
    // Action
    try l1Adapter.migrateToNative(_burnCaller, _roleCaller, 0, 0) {
        assert(l1Adapter.messengerStatus() == IL1OpUSDCBridgeAdapter.Status.Upgrading);
    } catch {}
    
    // Try calling a second time
    try l1Adapter.migrateToNative(_burnCaller, _roleCaller, 0, 0) {} catch {
        assert(false);
    }
}
```
This poses a few problems:
1. With no checks on the catch clause on the first call, it is unclear whether the first attempted `migrateToNative` was even successful.
2. Assuming that the first `migrateToNative` had failed, there is no point in trying to call the same function with the same arguments immediately afterward.
3. The empty try statement on the second `migrateToNative` only checks that the call is successful, and not whether the state had actually changed.

### 7. Be Decisive About What Functions Are Public and Private
Echidna by default will run any public or external function as part of its fuzzing suite. For this particular codebase, this is why functions under the "Expose target contract selectors" are being fuzzed as well. As there are no assertions in either of these functions, this would suggest the sole purpose is to generate valid inputs and/or valid helpers, in which case these functions should be either marked internal/private or added to the Echidna/Medusa filter list to not fuzz these directly.

This is the reason that you see the following assertion while running the test suite, which will not actually help generate more state(s) because there are no explicit assertions here:
```
generateCallAdapterL1(uint256,address,address,uint256,uint256,uint32,uint32): passing
```

## Recommendation
The files mentioned below contain recommendations for additional invariants that can be tested.

- `test/integration/Factories.t.sol.test_deployAllContracts`
- `test/invariants/fuzz/OpUSDC.t.sol.fuzz_testDeployments`

Consider adding the following checks, according to the Circle deployment checks:
- implementation is the address of the implementation contract.
- version is 2.
- totalSupply of token immediately after deployment is zero.
- initialized is true.

## Future Plans
Wonderland: Wonderland partially fixed some of the concerns mentioned above and will continue to make changes in future iterations.

Cantina Managed: Partially fixed in PR 136 and will continue to test as the codebase grows.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Wonderland |
| Report Date | N/A |
| Finders | shung, Optimum, 0xicingdeath, r0bert |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_wonderland_jul2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5295cf96-7a54-4150-9d94-396944b3604e

### Keywords for Search

`vulnerability`

