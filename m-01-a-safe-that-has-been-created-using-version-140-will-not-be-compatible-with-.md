---
# Core Classification
protocol: Brahma
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27567
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-brahma
source_link: https://code4rena.com/reports/2023-10-brahma
github_link: https://github.com/code-423n4/2023-10-brahma-findings/issues/383

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
finders_count: 2
finders:
  - bronze\_pickaxe
  - imare
---

## Vulnerability Title

[M-01] A safe that has been created using version `1.40=<` will not be compatible with Brahma

### Overview


This bug report is about a problem with Safe's created outside of the Brahma ecosystem being unable to integrate into the Brahma system. This is due to a new requirement in the Safe contracts version 1.4.0 and up, which requires the guard contract to support the EIP-165 interface. This means that any Safe created with version 1.4.0 or up will not be able to use the guard contract provided by the Brahma ecosystem.

The recommended mitigation steps are to either add support for the EIP-165 interface or update the Safe contracts used in Brahma from 1.3.0 to the most recent version. This bug was assessed as a “Context” type by a judge and was confirmed and fixed by the Brahma team, who added the recommended IERC165 support.

### Original Finding Content


Safe's created outside of the Brahma ecosystem should be able to seamlessly integrate into the `Brahma`. This Safe should call `WalletRegistry.registerWallet` to register. After registration,
this safe will be a `consoleAccount` and should be able to use the same functionality that all the other `consoleAccounts` have.

However, Safe's that have been created using version `1.4.0=<` are not fully compatible with Brahma. This is because, in version 1.4.0, `IERC165` support has been [added](https://github.com/safe-global/safe-contracts/pull/310/files) to the `GuardManager.sol`, this is the code added:

```diff
+ if (guard != address(0)) {
+ require(Guard(guard).supportsInterface(type(Guard).interfaceId), "GS300");
+ }
```

This means that every Safe that has been created using Safe's contract version 1.40 and up, can only add guards that support the `EIP-165` interface, as read from the [CHANGELOG.md](https://github.com/safe-global/safe-contracts/blob/main/CHANGELOG.md?plain=1#L206)

### Proof of Concept

Consider the following:

- Alice has a safe setup.
- Alice wants to integrate their safe into the Brahma ecosystem.
- Alice calls `WalletRegistry.registerWallet` and this call succeeds.
- Alice decides they want to implement the guard contract provided by the Brahma ecosystem, `SafeModeratorOverridable.sol`
- Alice calls `GnosisSafe.setGuard(address(SafeModeratorOverridable))`.
- This will fail because of this new require statement in Safe contracts `v1.4.0=<`:

```
function setGuard(address guard) external authorized {
        if (guard != address(0)) {
            require(Guard(guard).supportsInterface(type(Guard).interfaceId), "GS300");
        }
```

Because the `SafeModeratorOverridable.sol` does not support the `EIP-165` interface:

```
source: contracts/src/core/SafeModeratorOverridable.sol

contract SafeModeratorOverridable is AddressProviderService, IGuard {
```

This means that every Safe created with version 1.4.0 or up, can not implement the guard contract, which is a fundamental part of the way the `ConsoleAccounts` function.

### Recommended Mitigation Steps

Add support for the `EIP-165` interface or update the Safe contracts used in Brahma from 1.3.0 to the most recent version.

### Assessed type

Context

**[0xsomeone (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-10-brahma-findings/issues/383#issuecomment-1783092407):**
 > This appears to be a contender for "best" as it clearly pinpoints the flaw (i.e. Gnosis Safe instances created externally rather than via the code) as well as versions (i.e. `>=1.4.0`) the bug is applicable to.

**[0xad1onchain (Brahma) confirmed](https://github.com/code-423n4/2023-10-brahma-findings/issues/383#issuecomment-1783607114)**

**[0xad1onchain (Brahma) commented](https://github.com/code-423n4/2023-10-brahma-findings/issues/383#issuecomment-1817756510):**
> Fixed, added the recommended IERC165 support.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Brahma |
| Report Date | N/A |
| Finders | bronze\_pickaxe, imare |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-brahma
- **GitHub**: https://github.com/code-423n4/2023-10-brahma-findings/issues/383
- **Contest**: https://code4rena.com/reports/2023-10-brahma

### Keywords for Search

`vulnerability`

