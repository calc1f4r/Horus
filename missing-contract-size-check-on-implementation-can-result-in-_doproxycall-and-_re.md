---
# Core Classification
protocol: Op Enclave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58272
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
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
  - Zigtur
  - 0xTylerholmes
  - 0xIcingdeath
  - CarrotSmuggler
---

## Vulnerability Title

Missing contract size check on implementation can result in _doProxyCall and _resolveImplemen-

### Overview

See description below for full details.

### Original Finding Content

## tation succeeding silently

**Severity:** Low Risk  
**Context:** ResolvingProxy.sol#L96-L99, ResolvingProxy.sol#L137-L143, ResolvingProxy.sol#L149-L152  

## Description
When using `delegatecall`, account existence must be checked prior to calling; otherwise, the outer call will succeed while the target implementation contract's code was never executed. The function used to retrieve the implementation is the following:

```solidity
function _getImplementation() internal view returns (address) {
    address impl;
    bytes32 proxyImplementation = IMPLEMENTATION_SLOT;
    assembly {
        impl := sload(proxyImplementation)
    }
    return impl;
}
```

Note from the Solidity documentation specifically:

> The low-level functions `call`, `delegatecall`, and `staticcall` return `true` as their first return value if the account called is non-existent, as part of the design of the EVM. Account existence must be checked prior to calling if needed.

For reference, check the Solidity docs on control structures. The `_resolveImplementation` function is also vulnerable to the following attack, regardless of whether wrapped in an assembly block or not. Thus, the admin address should also be checked to ensure that its code length is greater than zero.

## Exploit Scenario:
1. `deployProxy` is called with `proxy` and `salt`, where `proxy` is `address(0)`:
    ```solidity
    function deployProxy(address proxy, bytes32 salt) public returns (address) {
        return ResolvingProxyFactory.setupProxy(proxy, proxyAdmin, salt);
    }
    ```

2. Proxy will be created using `create2` which invokes the `ResolvingProxy` constructor, setting the `IMPLEMENTATION_SLOT` to the zero address:
    ```solidity
    function _setImplementation(address _implementation) internal {
        bytes32 proxyImplementation = IMPLEMENTATION_SLOT;
        assembly {
            sstore(proxyImplementation, _implementation)
        }
    }
    ```

3. When a user invokes a function on the `ResolvingProxy` either through the fallback or another way, the admin need not even be set up correctly – it will merely return the proxy from the slot above:
    ```solidity
    function _resolveImplementation() internal view returns (address) {
        address proxy = _getImplementation();
        bytes memory data = abi.encodeCall(IResolver.getProxyImplementation, (proxy));
        (bool success, bytes memory returndata) = _getAdmin().staticcall(data);
        if (success && returndata.length == 0x20) {
            return abi.decode(returndata, (address)); // return value of implementation.getproxy
        }
        return proxy; // otherwise return implementation contract
    }
    ```

4. The `_doProxyCall` will use this zero address to execute the `delegatecall`, which in the outermost transaction, will succeed. This is because developers are expected to check that the address being delegate-called on exists prior to calling any contracts on it.

## Recommendation
Add a check to ensure the `_implementation` and admin contract provided to the `ResolvingProxy` contract is non-zero. This can be done using OpenZeppelin's `isAddress` helper function or through checking `address.code.length > 0` or `extcodesize(addr) > 0` in Yul.

**Base:** Acknowledged. Given this proxy is aimed to match the implementation of Optimism's Proxy (Proxy.sol#L124), which doesn't check for codesize prior to a delegatecall, and also the fact that this only has impact from an erroneous deploy or upgrade, I'm inclined not to change this behavior. However, Optimism's Proxy does have a 0 address check, which we may add a check for.  

**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Op Enclave |
| Report Date | N/A |
| Finders | Zigtur, 0xTylerholmes, 0xIcingdeath, CarrotSmuggler |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

