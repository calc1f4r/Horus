---
# Core Classification
protocol: zkSync
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30296
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-zksync
source_link: https://code4rena.com/reports/2023-10-zksync
github_link: https://github.com/code-423n4/2023-10-zksync-findings/issues/175

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
  - cdp
  - yield
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - zkrunner
  - anon
---

## Vulnerability Title

[M-17] Discrepancy in ECRECOVER Precompile when Using `Delegatecall`

### Overview


This bug report discusses an inconsistency in the behavior of the ECRECOVER precompile contract in zkSync Era. When accessed through `delegatecall`, the contract behaves differently than expected, potentially compromising data integrity and user funds. This behavior is not seen in the standard Ethereum Virtual Machine (EVM). The report provides a proof of concept and recommends a revised code to mitigate the issue. The severity of the bug is considered medium due to its potential impact on the EVM compatibility of zkSync. The report is verified through testing and reviewing code. 

### Original Finding Content


The discrepancy in `delegatecall` behavior with the ECRECOVER precompile contract in zkSync Era can have significant impact leading to incorrect signature validation, potentially compromising data integrity and user funds.

### Proof of Concept

In the context of zkSync Era, there exists a noticeable inconsistency in how the ECRECOVER precompile contract (located at address 0x01) behaves when accessed via `delegatecall`. This behavior differs from the standard Ethereum Virtual Machine (EVM) behavior, where the outcomes remain uniform across `call`, `staticcall`, and `delegatecall`.

<https://github.com/code-423n4/2023-10-zksync/blob/1fb4649b612fac7b4ee613df6f6b7d921ddd6b0d/code/system-contracts/contracts/precompiles/Ecrecover.yul#L7>

In zkSync Era, when the ECRECOVER precompile contract is invoked using `delegatecall`, it diverges from the usual behavior by delegating the call to the contract itself and executing its code within the caller's context. This results in a returned value that does not align with the anticipated outcome of a `precompileCall`. Instead, it yields `bytes32(0)`.

To illustrate, in the following example, when executing the provided code in the EVM, the returned `bytes32` value consistently appears as `0x000000000000000000000000759389e8e5c1aa1f511e9ea98b6caedd262bff0b` for all three scenarios: `ecrecoverStaticcall`, `ecrecoverCall`, and `ecrecoverDelegatecall`. However, in the zkSync Era, while `ecrecoverStaticcall` and `ecrecoverCall` maintain the same results as in the EVM, `ecrecoverDelegatecall` produces an incorrect outcome:

    // SPDX-License-Identifier: MIT

    pragma solidity >=0.8.20;

    contract PoC {
        bytes32 h = keccak256("");
        uint8 v = 27;
        bytes32 r = bytes32(uint256(1));
        bytes32 s = bytes32(uint256(2));

        function ecrecoverStaticcall() public returns (bytes32) {
            bytes memory data = abi.encode(h, v, r, s);
            assembly {
                pop(staticcall(gas(), 0x01, add(data, 0x20), mload(data), 0, 0x20))
                return(0, 0x20)
            }
        }

        function ecrecoverCall() public returns (bytes32) {
            bytes memory data = abi.encode(h, v, r, s);
            assembly {
                pop(call(gas(), 0x01, 0x00, add(data, 0x20), mload(data), 0, 0x20))
                return(0, 0x20)
            }
        }

        function ecrecoverDelegatecall() public returns (bytes32) {
            bytes memory data = abi.encode(h, v, r, s);
            assembly {
                pop(
                    delegatecall(gas(), 0x01, add(data, 0x20), mload(data), 0, 0x20)
                )
                return(0, 0x20)
            }
        }
    }

This discrepancy is critical in its impact because it introduces a divergence from the expected EVM response. While the likelihood of encountering this issue is not high, as precompile contracts are typically invoked through `staticcall` rather than `delegatecall`.

### Recommended Mitigation Steps

The following revised code is recommended:

    function delegateCall(
            uint256 _gas,
            address _address,
            bytes calldata _data
        ) internal returns (bytes memory returnData) {
            bool success;
            if(_address == address(0x01){
                success = rawStaticCall(_gas, _address, _data);
            } else {
                success = rawDelegateCall(_gas, _address, _data);
            }
            returnData = _verifyCallResult(success);
        }

<https://github.com/code-423n4/2023-10-zksync/blob/1fb4649b612fac7b4ee613df6f6b7d921ddd6b0d/code/system-contracts/contracts/libraries/EfficientCall.sol#L88>

### Assessed type

Context

**[miladpiri (zkSync) confirmed and commented](https://github.com/code-423n4/2023-10-zksync-findings/issues/175#issuecomment-1794968351):**
 > It has high impact (we do not know in which context it will be used, so its wrong result can have critical impact), but low probability. So, medium is fair.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2023-10-zksync-findings/issues/175#issuecomment-1826878542):**
 > The Warden has shown an inconsistency in the behaviour of ecrecover when using `delegatecall`. Because the goal of the zkSync EVM is to be the EVM compatible, Medium Severity seems appropriate.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2023-10-zksync-findings/issues/175#issuecomment-1849019163):**
 > I have verified my statement through testing via the zksync-foundry code repo as well as reviewing both the Precompile as well as the Rust code.
>
>*Note: to view the provided image, please see the original comment [here](https://github.com/code-423n4/2023-10-zksync-findings/issues/175#issuecomment-1849019163).*

*Note: for full discussion, see [here](https://github.com/code-423n4/2023-10-zksync-findings/issues/175).*

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | zkSync |
| Report Date | N/A |
| Finders | zkrunner, anon |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-zksync
- **GitHub**: https://github.com/code-423n4/2023-10-zksync-findings/issues/175
- **Contest**: https://code4rena.com/reports/2023-10-zksync

### Keywords for Search

`vulnerability`

