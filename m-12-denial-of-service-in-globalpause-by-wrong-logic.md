---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24841
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-08-frax
source_link: https://code4rena.com/reports/2022-08-frax
github_link: https://github.com/code-423n4/2022-08-frax-findings/issues/76

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-12] Denial of service in globalPause by wrong logic

### Overview


A bug was reported in the method `globalPause` of the FraxlendPairDeployer.sol#L405 source code. The bug is that the method returns an array (`_updatedAddresses`) and has never been initialized, so when you want to set its value, it fails. This results in a transaction FAULT when `globalPause` is called with any valid address.

It was recommended to initialize the `_updatedAddresses` array as shown in the code snippet. DrakeEvans (Frax) confirmed the bug, but disagreed with the severity and commented that it is a convenience function and no user funds are at risk. GititGoro (judge) decreased the severity to Medium, given the existence of per pair pausing.

### Original Finding Content

_Submitted by 0x1f8b_

The method `globalPause` is not tested and it doesn't work as expected.

### Proof of Concept

Because the method returns an array (`_updatedAddresses`) and has never been initialized, when you want to set its value, it fails.

Recipe:

*   Call `globalPause` with any valid address.
*   The transaction will FAULT.

#### Affected source code

*   [FraxlendPairDeployer.sol#L405](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairDeployer.sol#L405)

### Recommended Mitigation Steps

Initialize the `_updatedAddresses` array like shown below:

```diff
    function globalPause(address[] memory _addresses) external returns (address[] memory _updatedAddresses) {
        require(msg.sender == CIRCUIT_BREAKER_ADDRESS, "Circuit Breaker only");
        address _pairAddress;
        uint256 _lengthOfArray = _addresses.length;
+       _updatedAddresses = new address[](_lengthOfArray);
        for (uint256 i = 0; i < _lengthOfArray; ) {
            _pairAddress = _addresses[i];
            try IFraxlendPair(_pairAddress).pause() {
                _updatedAddresses[i] = _addresses[i];
            } catch {}
            unchecked {
                i = i + 1;
            }
        }
    }
```

**[DrakeEvans (Frax) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2022-08-frax-findings/issues/76#issuecomment-1238100769):**
 > Valid, disagree with severity.  This is a convenience function.  Pause can still be called on the pairs themselves individually.  No user funds at risk, and no users can even touch this function, additionally no loss of functionality in the pairs themselves.  Only result is admin having to revert and spin up tx individually.

**[gititGoro (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-08-frax-findings/issues/76#issuecomment-1266162395):**
 > Well caught! But definitely a Medium severity, given the existence of per pair pausing.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-frax
- **GitHub**: https://github.com/code-423n4/2022-08-frax-findings/issues/76
- **Contest**: https://code4rena.com/reports/2022-08-frax

### Keywords for Search

`vulnerability`

