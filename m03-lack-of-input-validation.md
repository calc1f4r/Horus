---
# Core Classification
protocol: Fei Protocol Audit – Phase 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10853
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fei-audit-2/
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M03] Lack of input validation

### Overview


This bug report is about the lack of input validation in the codebase of the Fei Protocol. Input validation is important as it helps to prevent errors caused by incorrect inputs from having far-reaching negative consequences. There are many functions and contracts that require input validation, such as the `setAllocation` function of the `BondingCurve` contract, the `PCVDripController` contract, and the constructor of the `PCVSwapperUniswap` contract. The `onlyGovernance` modifier functions also require input validation, such as the `setFeiOracle` function of the `TribeReserveStabilizer` contract and the `setDuration` function of the `UniswapPCVController` contract.

To address this issue, it is recommended that programmatic safeguards are implemented to validate input parameters and ensure all function calls and contract constructions would “fail early and loudly” on erroneous inputs. This is especially important for functions or contracts that are vetted by governance, as subtle bugs in the parameters can have far-reaching impacts on the system. Partially fixed in PR#75, the first 2 points outlined in this issue were not addressed, however the remaining issues were fixed.

### Original Finding Content

Throughout this codebase we found there to be an overall lack of input validation. The functions lacking input validation are either modified by the `onlyGovernance` modifier or are `constructor`s. However simple human error in entering these values, by perhaps entering too many or too few 0s, can have far reaching negative consequences.


Some points where a lapse in input validation could be particularly problematic include:


* There is no check in the callstack of the [`setAllocation` function](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/bondingcurve/BondingCurve.sol#L135) of the [`BondingCurve` contract](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/bondingcurve/BondingCurve.sol#L18) to ensure that the `token` featured in the `BondingCurve` is the `token` handled by the `PCVDeposit`. In the case this mismatch would occur, the `PCVController` would have to manually reallocate these stray tokens using the `withdrawERC20` function.
* The [`PCVDripController` contract](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/pcv/PCVDripController.sol#L11) drips tokens from one `PCVDeposit` contract to another, but it never validates that the token each of them handle are the same. This means it could drip a token into a deposit contract that handles a different token. This mismatch could affect the accounting dictating the logic of the [`drip` function](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/pcv/PCVDripController.sol#L51). In particular, the check of [`dripEligible`](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/pcv/PCVDripController.sol#L105) may wind up considering the balance of the wrong token.
* The [constructor of `PCVSwapperUniswap` contract](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/pcv/PCVSwapperUniswap.sol#L47) does not check that the two tokens in the [`pair`](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/pcv/PCVSwapperUniswap.sol#L62) are [`tokenSpent`](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/pcv/PCVSwapperUniswap.sol#L64) and [`tokenReceived`](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/pcv/PCVSwapperUniswap.sol#L65). This can affect the calculations of the inputs to the uniswap swap, leading to accounting errors in pcv.


Examples of `onlyGovernor` modified functions lacking input validation are:


* The [`setFeiOracle` function](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/stabilizer/TribeReserveStabilizer.sol#L66) of the `TribeReserveStabilizer` contract doesn’t check `newFeiOracle` is not the zero-address.
* The [`setDuration` function](https://github.com/fei-protocol/fei-protocol-core-internal/blob/f54d7bb07c55adb78e2e142e7044f60090bb7602/contracts/pcv/UniswapPCVController.sol#L96) of the `UniswapPCVController` contract does not validation the `_duration` is non-zero or within sensible bounds.


The functions that could benefit from input validation in this codebase are numerous and there are many more than are listed here.


Consider implementing programmatic safeguards validating input parameters to ensure all function calls and contract constructions would “fail early and loudly” on erroneous inputs. This is needed especially in the case of functions or contracts vetted by governance, where subtle bugs in parameters that pass the governance process can have far reaching impacts on a system.


***Update:** Partially fixed in [PR#75](https://github.com/fei-protocol/fei-protocol-core-internal/pull/75). The first 2 points outlined in this issue were not addressed, however the remaining issues were fixed.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Fei Protocol Audit – Phase 2 |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fei-audit-2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

