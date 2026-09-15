---
# Core Classification
protocol: Alchemy - Modular Account V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58888
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/alchemy-modular-account-v-2/b4818bd5-5cf2-43bb-8eed-46d8a761bc42/index.html
source_link: https://certificate.quantstamp.com/full/alchemy-modular-account-v-2/b4818bd5-5cf2-43bb-8eed-46d8a761bc42/index.html
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Nikita Belenkov
  - Ruben Koch
  - Hytham Farah
---

## Vulnerability Title

`NativeTokenLimitModule` Can Be Bypassed

### Overview


The client has fixed a bug in the `NativeTokenLimitModule` and `PaymasterGuardModule` files. The bug allowed an attacker to drain funds from an account by submitting a `UserOperation` with a `paymasterAndData` field of 52 bytes containing only zeroes. The bug was caused by a missing check for a non-zero length `bytes` array in the decoded address. To fix this, a check should be added in the modules' if-conditions to ensure that `paymasterAndData` is not equal to zero.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `37cd0f18422ece242612660c0f41eb9c4e4552cc` and `d83d463904fe35f6d369a44529e132d8e8640796`

**File(s) affected:**`NativeTokenLimitModule`, `PaymasterGuardModule`

**Description:** The `NativeTokenLimitModule` is intended to limit the native tokens some validation can access from the account. In case paymasters provided, the check is regularly skipped, as the paymaster is covering the gas costs, unless it is some special paymaster that has some existing ERC20 token allowance that withdraws e.g. ERC20 tokens equivalent to the gas consumed from the account.

However, the decoded address is missing a check that it is a non-zero length `bytes` array of just zeroes. This enables a bypass in the `paymasters` registry, as in this case `userOp.paymasterAndData.length != 0` as well as `specialPaymasters[address(0x0)][msg.sender]  == 0`, if `address(0x0)` is not specifically registered as a `specialPaymaster`, which does not seem intended.

EthInfinitism's EntryPoint internally treats a `paymasterAndData` field of zero length [the same way](https://github.com/eth-infinitism/account-abstraction/blob/6f02f5a28a20e804d0410b4b5b570dd4b076dcf9/contracts/core/EntryPoint.sol#L391) as `paymaster = address(0x0)`, `paymasterVerificationGasLimit = 0`and `paymasterPostOpGasLimit = 0`. The unpacking of the paymasterAndData variable [here](https://github.com/eth-infinitism/account-abstraction/blob/6f02f5a28a20e804d0410b4b5b570dd4b076dcf9/contracts/core/UserOperationLib.sol#L120) does not do any reverts on zero-values either.

This enables all UserOperation-validations installed on the account that have this validation hook installed to fully drain the underlying account by simply encoding a 52 byte long `paymasterAndData` field containing only zeroes.

Furthermore, in the `PaymasterGuardModule`, a similar check is performed. If this module were to be installed without the `onInstall()` callback or with an `installData` parameter encoding the zero address, native funds could be drained in the same way.

**Exploit Scenario:**

An attacker could submit a `UserOperation` with a `paymasterAndData` field of 52 bytes containing only zeroes, causing `payingPaymaster` to resolve to `address(0)`. If `entityId` validation was missed or misconfigured during module installation, the `paymasters[entityId][msg.sender]` mapping could also resolve to `address(0)`, passing the check without a valid registered paymaster. Combining this with the `NativeTokenLimitModule` increases the risk: the attacker could bypass transaction limits set for no-paymaster calls, allowing unrestricted withdrawals and potentially draining account funds.

**Recommendation:** Add a check in the if-conditions of the modules to check that `paymasterAndData != 0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Alchemy - Modular Account V2 |
| Report Date | N/A |
| Finders | Nikita Belenkov, Ruben Koch, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/alchemy-modular-account-v-2/b4818bd5-5cf2-43bb-8eed-46d8a761bc42/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/alchemy-modular-account-v-2/b4818bd5-5cf2-43bb-8eed-46d8a761bc42/index.html

### Keywords for Search

`vulnerability`

