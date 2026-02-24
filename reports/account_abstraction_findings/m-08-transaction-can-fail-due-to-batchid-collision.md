---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6454
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest
source_link: https://code4rena.com/reports/2023-01-biconomy
github_link: https://github.com/code-423n4/2023-01-biconomy-findings/issues/246

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - rom
  - 0xdeadbeef0x
---

## Vulnerability Title

[M-08] Transaction can fail due to batchId collision

### Overview


This bug report is about a vulnerability in the protocol that supports 2D nonces through a `batchId` mechanism. The bug can cause unexpected failing of transactions due to a collision between `batchIds` being used. This is caused by two main ways to execute transaction from the smart wallet: via EntryPoint or via `execTransaction`. The `SmartAccount` locks the `batchId` #0 to be used by the `EntryPoint`, and when an `EntryPoint` calls `validateUserOp` before execution, the hardcoded nonce of `batchId` #0 will be incremented and validated. Calls to `execTransaction` are more immediate and are likely to be executed before a `UserOp` through `EntryPoint`, but there is no limitation in `execTransaction` to use `batchId` #0. This can result in unexpected failing of transactions if there is a call to `execTransaction` with `batchId` set to `0`.

The recommended mitigation steps for this vulnerability is to add a requirement that `batchId` is not `0` in `execTransaction` using `require(batchId != 0, "batchId 0 is used only by EntryPoint")`.

### Original Finding Content


The protocol supports 2D nonces through a `batchId` mechanism.<br>
Due to different ways to execute transaction on the wallet there could be a collision between `batchIds` being used.

This can result in unexpected failing of transactions

### Proof of Concept

There are two main ways to execute transaction from the smart wallet

1.  Via EntryPoint - calls `execFromEntryPoint`/`execute`
2.  Via `execTransaction`

`SmartAccount` has locked the `batchId` #0  to be used by the `EntryPoint`.<br>
When an `EntryPoint` calls `validateUserOp` before execution, the hardcoded nonce of `batchId` #0 will be incremented and validated, [contracts/smart-contract-wallet/SmartAccount.sol#L501](https://github.com/code-423n4/2023-01-biconomy/blob/53c8c3823175aeb26dee5529eeefa81240a406ba/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L501)

        // @notice Nonce space is locked to 0 for AA transactions
        // userOp could have batchId as well
        function _validateAndUpdateNonce(UserOperation calldata userOp) internal override {
            require(nonces[0]++ == userOp.nonce, "account: invalid nonce");
        }

Calls to `execTransaction` are more immediate and are likely to be executed before a `UserOp` through `EntryPoint`.<br>
There is no limitation in `execTransaction` to use `batchId` #0 although it should be called only by `EntryPoint`.

If there is a call to `execTransaction` with `batchId` set to `0`. It will increment the nonce and `EntryPoint` transactions will revert.
[contracts/smart-contract-wallet/SmartAccount.sol#L216](https://github.com/code-423n4/2023-01-biconomy/blob/53c8c3823175aeb26dee5529eeefa81240a406ba/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L216)

        function execTransaction(
            Transaction memory _tx,
            uint256 batchId,
            FeeRefund memory refundInfo,
            bytes memory signatures
        ) public payable virtual override returns (bool success) {
    -------
                nonces[batchId]++;
    -------
            }
        }

### Tools Used

VS Code

### Recommended Mitigation Steps

Add a requirement that `batchId` is not `0` in `execTransaction`:

`require(batchId != 0, "batchId 0 is used only by EntryPoint")`

**[livingrockrises (Biconomy) confirmed](https://github.com/code-423n4/2023-01-biconomy-findings/issues/246#issuecomment-1397693932)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | rom, 0xdeadbeef0x |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-biconomy
- **GitHub**: https://github.com/code-423n4/2023-01-biconomy-findings/issues/246
- **Contest**: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest

### Keywords for Search

`vulnerability`

