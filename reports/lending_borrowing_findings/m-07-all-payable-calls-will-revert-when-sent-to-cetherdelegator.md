---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31820
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
  - Zach Obront
---

## Vulnerability Title

[M-07] All payable calls will revert when sent to CEtherDelegator

### Overview


This bug report discusses an issue with the Delegator contracts, which are supposed to pass along calls to their corresponding implementations. However, there is a problem with the fallback function in the `CEtherDelegator.sol` contract, as it contains a check that does not apply to CEther. This means that any payable function calls will cause the contract to revert, making it impossible to perform certain actions such as minting, repaying, adding reserves, or withdrawing WETH. While there is a workaround using the `delegateToImplementation()` function, it is not ideal and could cause inconvenience for users. The report recommends either removing the option to use a proxy contract for CEther or ensuring that the inheritance is set up correctly and the fallback function allows for ETH to be received. The bug has been fixed by removing the proxy option for CEther in a recent code update.

### Original Finding Content

The Delegator contracts are intended to pass along any calls to their corresponding implementations.

Some delegators perform this logic by manually implementing each underlying function. Others (such as `CEtherDelegator.sol`) simply use a fallback function which is intended to capture all possible calls to the implementation.

However, the fallback function of this contract contains a check that was taken from the other markets but does not apply to CEther:
```solidity
fallback() external payable {
    if (msg.value > 0) {
        revert CannotReceiveValueGtZero();
    }

    ...
}
```
This will revert in the case that any payable function call are sent to the contract.

Looking at `CEther.sol`, minting, repaying, adding reserves, or WETH withdrawals all require the ability to receive ETH.

Fortunately, there is a payable `delegateToImplementation()` function on the delegator, so all calls from users will be possible by sending their calls to that function, with encoded abi data instead. While this is inconvenient, it is not a security risk.

WETH withdrawals, on the other hand, can only be accepted by a payable `fallback()` or `receive()` function. These will revert when sent to the delegator, and so all liquidations will revert when WETH is attempted to be withdrawn.

**Note on Specifics**

Currently, the CEtherDelegator inherits from CEther. This means it is not a delegator. It contains all functionality itself, as well as having an identical implementation that it can delegate call out to.

This inherited contract contains all of the CEther functionality, including the ability to accept payments, so this bug is not currently a problem. However, when the other issue is fixed (which would presumably happen by inherting an interface from CEther instead of the full functionality), this bug will become a problem.

**Recommendation**

The easiest fix would be to remove the option to do a proxy contract for CEther, and instead implement it as an immutable non-proxy contract, the same way Compound does.

If this is not preferable, then ensure that (a) the inheritance is such that the delegator is working as a proxy and (b) the fallback function allows for ETH to be received.

**Review**

Fixed by removing the proxy option for CEther in [cd578511b94985956325d8ea1d95d3c5a9925af4](https://github.com/fungify-dao/taki-contracts/pull/9/commits/cd578511b94985956325d8ea1d95d3c5a9925af4).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

