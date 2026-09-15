---
# Core Classification
protocol: Metamask Delegationframework
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55603
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
github_link: none

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
finders_count: 2
finders:
  - 0kage
  - Al-qaqa
---

## Vulnerability Title

Gas griefing via duplicate entries in `Allowed` class of enforcers

### Overview


This bug report highlights an issue with two contracts, `AllowedMethodsEnforcer` and `AllowedTargetsEnforcer`, which do not properly check for duplicate entries in their terms data. This allows attackers to create delegations with excessive duplicates, leading to increased gas costs during validation. The impact of this bug is demonstrated in a test case, where including 100 duplicate method signatures resulted in a ~3x increase in gas consumption. The report recommends implementing a validation to prevent duplicates and using a binary search on a sorted array instead of a linear search. Metamask and Cyfrin have acknowledged the issue.

### Original Finding Content

**Description:** Multiple enforcer contracts (`AllowedMethodsEnforcer` and `AllowedTargetsEnforcer`) don't validate the uniqueness of entries in their terms data, allowing malicious users to intentionally create delegations with excessive duplicates, dramatically increasing gas costs during validation.

`AllowedMethodsEnforcer`: Allows duplicate method selectors (4 bytes each)
`AllowedTargetsEnforcer`: Allows duplicate target addresses (20 bytes each)

None of these contracts prevent or detect duplicates in their terms data. This allows an attacker to artificially inflate gas costs by including the same entries multiple times, resulting in expensive linear search operations during validation.


```solidity
function getTermsInfo(bytes calldata _terms) public pure returns (bytes4[] memory allowedMethods_) {
    uint256 j = 0;
    uint256 termsLength_ = _terms.length;
    require(termsLength_ % 4 == 0, "AllowedMethodsEnforcer:invalid-terms-length");
    allowedMethods_ = new bytes4[](termsLength_ / 4);
    for (uint256 i = 0; i < termsLength_; i += 4) {
        allowedMethods_[j] = bytes4(_terms[i:i + 4]);
        j++;
    }
}

// In beforeHook:
for (uint256 i = 0; i < allowedSignaturesLength_; ++i) {
    if (targetSig_ == allowedSignatures_[i]) { //@audit linear search can be expensive
        return;
    }
}
```

**Impact:** As demonstrated in the test case for `AllowedMethodsEnforcer`, including 100 duplicate method signatures increases gas consumption from 50,881 to 155,417 (a difference of 104,536 gas). This represents a ~3x increase in gas consumption with just 100 duplicates. A malicious actor can use this to make execution expensive for a delegator.

**Proof of Concept:** Run the following test

```solidity
 function test_AllowedMethods_DuplicateMethodsGriefing() public {
        // Create terms with a high number of duplicated methods to increase gas costs
        bytes memory terms = createDuplicateMethodsTerms(INCREMENT_SELECTOR, 100);

        // Create execution to increment counter
        Execution memory execution =
            Execution({ target: address(aliceCounter), value: 0, callData: abi.encodeWithSelector(INCREMENT_SELECTOR) });

        // Create delegation with allowed methods caveat
        Caveat[] memory caveats = new Caveat[](1);
        caveats[0] = Caveat({ enforcer: address(allowedMethodsEnforcer), terms: terms, args: "" });

        // Create and sign the delegation
        Delegation memory delegation = Delegation({
            delegate: address(users.bob.deleGator),
            delegator: address(users.alice.deleGator),
            authority: ROOT_AUTHORITY,
            caveats: caveats,
            salt: 0,
            signature: hex""
        });

        delegation = signDelegation(users.alice, delegation);

        // Measure gas usage with many duplicate methods
        Delegation[] memory delegations = new Delegation[](1);
        delegations[0] = delegation;

        uint256 gasUsed = uint256(
            bytes32(
                gasReporter.measureGas(
                    address(users.bob.deleGator),
                    address(delegationManager),
                    abi.encodeWithSelector(
                        delegationManager.redeemDelegations.selector,
                        createPermissionContexts(delegation),
                        createModes(),
                        createExecutionCallDatas(execution)
                    )
                )
            )
        );

        console.log("Gas used with 100 duplicate methods:", gasUsed);

        // Now compare to normal case with just one method
        terms = abi.encodePacked(INCREMENT_SELECTOR);
        caveats[0].terms = terms;

        delegation.caveats = caveats;
        delegation = signDelegation(users.alice, delegation);

        delegations[0] = delegation;

        uint256 gasUsedNormal = uint256(
            bytes32(
                gasReporter.measureGas(
                    address(users.bob.deleGator),
                    address(delegationManager),
                    abi.encodeWithSelector(
                        delegationManager.redeemDelegations.selector,
                        createPermissionContexts(delegation),
                        createModes(),
                        createExecutionCallDatas(execution)
                    )
                )
            )
        );

        console.log("Gas used with 1 method:", gasUsedNormal);
        console.log("Gas diff:", gasUsed - gasUsedNormal);

        assertGt(gasUsed, gasUsedNormal, "Griefing with duplicate methods should use more gas");
    }

    function createDuplicateMethodsTerms(bytes4 selector, uint256 count) internal pure returns (bytes memory) {
        bytes memory terms = new bytes(count * 4);
        for (uint256 i = 0; i < count; i++) {
            bytes4 methodSig = selector;
            for (uint256 j = 0; j < 4; j++) {
                terms[i * 4 + j] = methodSig[j];
            }
        }
        return terms;
    }

    function createPermissionContexts(Delegation memory del) internal pure returns (bytes[] memory) {
        Delegation[] memory delegations = new Delegation[](1);
        delegations[0] = del;

        bytes[] memory permissionContexts = new bytes[](1);
        permissionContexts[0] = abi.encode(delegations);

        return permissionContexts;
    }

    function createExecutionCallDatas(Execution memory execution) internal pure returns (bytes[] memory) {
        bytes[] memory executionCallDatas = new bytes[](1);
        executionCallDatas[0] = ExecutionLib.encodeSingle(execution.target, execution.value, execution.callData);
        return executionCallDatas;
    }

    function createModes() internal view returns (ModeCode[] memory) {
        ModeCode[] memory modes = new ModeCode[](1);
        modes[0] = mode;
        return modes;
    }
```
**Recommended Mitigation:** Consider enforcing that entries in terms are strictly increasing, which naturally prevents duplicates. A validation as shown below will prevent duplicates in this case. Also, consider implementing a binary search on a sorted array viz-a-viz linear search.

```solidity
function getTermsInfo(bytes calldata _terms) public pure returns (bytes4[] memory allowedMethods_) {
    uint256 termsLength_ = _terms.length;
    require(termsLength_ % 4 == 0, "AllowedMethodsEnforcer:invalid-terms-length");
    allowedMethods_ = new bytes4[](termsLength_ / 4);

    bytes4 previousSelector = bytes4(0);

    for (uint256 i = 0; i < termsLength_; i += 4) {
        bytes4 currentSelector = bytes4(_terms[i:i + 4]);

        // Ensure selectors are strictly increasing (prevents duplicates)
        require(uint32(currentSelector) > uint32(previousSelector),
                "AllowedMethodsEnforcer:selectors-must-be-strictly-increasing"); //@audit prevents duplicates

        allowedMethods_[i/4] = currentSelector;
        previousSelector = currentSelector;
    }
}
```

**Metamask:** Acknowledged. It is the responsibility of the redeemer to see the terms are setup in such a way to prevent griefing attacks.

**Cyfrin:** Acknowledged.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Cyfrin |
| Protocol | Metamask Delegationframework |
| Report Date | N/A |
| Finders | 0kage, Al-qaqa |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

