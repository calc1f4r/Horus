---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19462
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Testing Findings And Suggestions

### Overview

See description below for full details.

### Original Finding Content

## Description

This section details findings relating to the test implementation, using the Brownie framework, which do not have direct security implications. Also refer to additions and modifications to the tests provided to the development team alongside this report.

## 1. Missed Edge Cases/Coverage

The following useful test cases were identified that are not currently covered:

- **Cases for EVMScriptPermissions**: With valid and invalid EVM Script inputs of different lengths. In particular, for `isValidPermissions` tests, a valid permissions list containing more than 1 permission, invalid permissions longer than 1 permission but shorter than 2, and permissions lists containing duplicate entries (to be explicit, duplicate entries should be treated as valid or not).
- **ContractProxy Tests**: The tests currently don’t exercise the `ContractProxy` by default. Arguably, the default tests and fixtures implemented in `conftest.py` should mimic the real-world deployment. While unit tests against the underlying `EasyTrack` contract are reasonable, the vast majority of tests interact directly with the `EasyTrack` contract, with only a few specific tests using the `ContractProxy`. An alternative option would be to have two different test directories, with the `conftest.py` for “unit” testing using mocks for contracts not in focus, and the “integration” `conftest.py` providing contract fixtures mimicking the intended deployment.

## 2. Test Isolation & EVM Snapshots

The tests fail to make use of the powerful and developer-friendly Brownie isolation fixtures, greatly limiting performance, and increasing the risk of tests affecting other tests’ results and validity.

In order to prevent tests from affecting each other, most fixtures in the current test implementation are “function scoped” (meaning they execute at the start of every test function), so new contracts are redeployed at the start of every test function. This greatly increases execution time, and it’s still prone to developer error (e.g. with account balances needing to be manually reset before each test).

The Brownie isolation fixtures provide a developer-friendly means to snapshot and rollback the underlying test EVM between test functions and modules. This makes it possible for slow contract deployments (and other setup) to only be done once per test module, and developers can be confident that tests are properly isolated from each other. Similarly, this makes it safe for tests to be run in parallel with `pytest-xdist`, allowing execution time to be greatly reduced.

The performance limitations can also encourage less exhaustive tests, sub-optimal test style (in which several independent checks are made in a single test), and can otherwise hinder the development workflow.

## 3. Opportunities to Use pytest Fixtures that Return Constants Instead of Global Variables

A detailed example at `./tests/sigp-easy-track/tests/isolation_example/` was provided to the development team alongside this report.

For example, in `test_evm_script_permissions.py`, the `VALID_PERMISSIONS` global variable can be replaced with a fixture that returns a valid permission. The more powerful fixtures can then be parameterized to return one of several values, immediately covering more edge cases wherever used, or overridden at different levels to modify initial test state without needing to redefine a whole hierarchy of fixtures.

## 4. Tests Making Multiple Checks That Should Be Separated

The testing team notes that it is preferred practice that test functions check only one conceptual “action”. While this check may involve multiple assert statements, they should all be about the same action (e.g. that both a transaction’s return value and emitted logs are as expected).

The current test functions will often make multiple independent asserts within a single test, which should preferably be split into separate test functions. For example, `test_is_valid_permissions()` makes three independent calls to `EVMScriptPermissions.isValidPermissions()` with different inputs. If the first assert fails, the later checks are not evaluated; so it is not clear from the test results whether 1 or 3 things are wrong with the `isValidPermissions()`.

It is likely that this was done for performance reasons (to avoid the slow setup between tests) but the EVM snapshots can avoid this problem. Test parameterization can make it easy to implement separate tests with various inputs without rewriting the code.

## 5. Tests Asserting the Order in Which Inputs Are Validated

Several tests were identified that, likely unintentionally, make assumptions about the order in which the contracts verify input. This can be an internal implementation detail that, if modified, would cause these tests to fail unnecessarily.

For example, in `test_add_evm_script_factory_called_without_permissions()`, there is more than one thing wrong with the input (empty permissions, and an invalid sender). The test then asserts that an error relating to the invalid sender is returned, when it could easily be one relating to the invalid permissions. Unless intentional and the order of these requirements is important, it is usually preferable to provide invalid input where only one thing is wrong with it.

## 6. Input Value Discrepancy in isValidPermissions

At `test_evm_script_permissions.py:62`, the input to `isValidPermissions()` is likely a different value than intended.

```python
assert not evm_script_permissions_wrapper.isValidPermissions(b"11223344556677889911")
```

When passed to the contract, the value `b"11223344556677889911"` is actually 20 bytes long and equivalent to the solidity bytes value `hex"3131323233333434353536363737383839393131"` (the ASCII/Unicode encoding of the numbers 112...), not the 10 byte hex `11223344556677889911`. It appears that the string value `"0x11223344556677889911"` is actually the intended input. In this case, the test is still okay because either the input is invalid, but this misunderstanding could lead to bugs elsewhere. Confirm whether this is intended and adjust accordingly.

## 7. Unnecessary Imports in conftest.py

The imports in the Brownie `conftest.py` at lines [5-21] are unnecessary, as all Brownie `ContractContainer` instances are available as pytest fixtures. Instead, these can be listed as fixture dependencies in any fixtures that require them.

## 8. Code Clarity Improvement in utils/evm_script.py

A nitpick at `utils/evm_script.py:21-22`. The current code works with `int256` because the input to `encode_single` is always positive:

```python
length = eth_abi.encode_single("int256", len(calldata_bytes) // 2).hex()
result += addr_bytes + length[56:] + calldata_bytes
```

but is more clearly written using `uint32`:

```python
length = eth_abi.encode_single("uint32", len(calldata_bytes) // 2).hex()
result += addr_bytes + length + calldata_bytes
```

This more clearly reflects the `CallsScript` encoding.

## 9. Brownie Report Exclusion Configuration

The Brownie report exclusion settings can be more easily and reliably configured in `brownie-config.yaml` via the `exclude_paths` field, rather than needing to manually add all test contract names to the `exclude_contracts` field.

```yaml
exclude_paths:
  - contracts/test/**/*
```

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

This has been addressed (primarily in PR #9) as follows:

1. 
   - ee5835d — More tests cases added.
   - 96479e8 — `ContractProxy` removed (see LET-01), so no need for tests.
2. adc4473 — Resolved, using isolation fixtures and improved fixture scoping.
3. Used where relevant and more convenient than global variables.
4. ee5835d — Tests split up and parameterization used.
5. ee5835d.
6. d7c0b24.
7. adc4473.
8. ee5835d.
9. ee5835d.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf

### Keywords for Search

`vulnerability`

