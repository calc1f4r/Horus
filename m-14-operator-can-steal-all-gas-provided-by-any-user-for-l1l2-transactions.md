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
solodit_id: 30293
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-zksync
source_link: https://code4rena.com/reports/2023-10-zksync
github_link: https://github.com/code-423n4/2023-10-zksync-findings/issues/255

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
  - bin2chen
  - erebus
  - anon
---

## Vulnerability Title

[M-14] Operator can steal all gas provided by ANY user for `L1→L2` transactions

### Overview


The report discusses a bug found in the bootloader function processL1Tx in the zkSync system contracts. The bug allows a malicious operator to steal all the gas provided by any user who requests an L1⇒L2 transaction by returning an overinflated refundGas value. This can happen because there are no checks for overflows in the assembly code. The recommended mitigation step is to use safeAdd instead of add to prevent this issue. The bug has been confirmed by the zkSync team and a fix has been suggested. 

### Original Finding Content


In [bootloader, function processL1Tx](https://github.com/code-423n4/2023-10-zksync/blob/1fb4649b612fac7b4ee613df6f6b7d921ddd6b0d/code/system-contracts/bootloader/bootloader.yul#L921C1-L921C57), it is possible for a malicious operator to steal all the gas provided by **ANY** user who requests an `L1⇒L2` transaction simply by returning an overinflated `refundGas` for the transaction execution.

### Proof of concept

The `refundGas` the user will receive is the sum of:

*Note: please see scenario in warden's [original submission](https://github.com/code-423n4/2023-10-zksync-findings/issues/255).*

With `reservedGas` being the excess of gas between what the user provided and what the operator is willing to use, and `refundGas` (not the final one) is the remaining gas left after preparing and executing the requested transaction.

As both quantities are added via the opcode `add`:

[bootloader, line 921](https://github.com/code-423n4/2023-10-zksync/blob/1fb4649b612fac7b4ee613df6f6b7d921ddd6b0d/code/system-contracts/bootloader/bootloader.yul#L921C1-L921C57)

```solidity
                refundGas := add(refundGas, reservedGas)
```

The operator can return an over-inflated value so that it gets picked by the `max()` function and is added to `reservedGas`; overflowing the result as there are no checks for overflows in assembly:

[bootloader, lines 921-927](https://github.com/code-423n4/2023-10-zksync/blob/1fb4649b612fac7b4ee613df6f6b7d921ddd6b0d/code/system-contracts/bootloader/bootloader.yul#L921C1-L927C100)

```solidity
                refundGas := add(refundGas, reservedGas) // overflow, refundGas = 0 while gasLimit != 0

                if gt(refundGas, gasLimit) { // correct, 0 < x for all x iff x != 0
                    assertionError("L1: refundGas > gasLimit")
                }

                // gasPrice * (gasLimit - refundGas) == gasPrice * (gasLimit - 0) == gasPrice * gasLimit
                let payToOperator := safeMul(gasPrice, safeSub(gasLimit, refundGas, "lpah"), "mnk")
```

As anyone will be able to be an operator once zkSync Era becomes decentralized, this issue becomes critical as it would be possible for **ANY** operator to *"farm"* the gas provided by **ANY** user.

### Recommended Mitigation Steps

Just use `safeAdd`:

[bootloader, line 921](https://github.com/code-423n4/2023-10-zksync/blob/1fb4649b612fac7b4ee613df6f6b7d921ddd6b0d/code/system-contracts/bootloader/bootloader.yul#L921C1-L921C57)

```diff
-               refundGas := add(refundGas, reservedGas)
+               refundGas := safeAdd(refundGas, reservedGas, "The operator is being an asshole")
```

**[miladpiri (zkSync) confirmed via duplicate issue #187](https://github.com/code-423n4/2023-10-zksync-findings/issues/187#issuecomment-1795021187)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2023-10-zksync-findings/issues/255#issuecomment-1826401662):**
 > Best because of formula, clearest and shows the fix.

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
| Finders | bin2chen, erebus, anon |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-zksync
- **GitHub**: https://github.com/code-423n4/2023-10-zksync-findings/issues/255
- **Contest**: https://code4rena.com/reports/2023-10-zksync

### Keywords for Search

`vulnerability`

