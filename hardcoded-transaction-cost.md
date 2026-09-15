---
# Core Classification
protocol: Account Abstraction Schnorr Signatures SDK
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52578
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-signatures-sdk
source_link: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-signatures-sdk
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
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

HARDCODED TRANSACTION COST

### Overview


The report highlights a bug in the source code examples where the `initTransactionCost` variable is hardcoded, making it unresponsive to real-time gas price fluctuations on the blockchain network. This can lead to incorrect transaction execution or unexpected failures. The severity of this issue was lowered from HIGH to MEDIUM as it was found in the `examples` folder, but it is still a bad practice that should be removed. The report provides proof of concept code and recommends replacing the hardcoded value with a dynamic calculation based on current gas prices. The team has agreed that this issue is not applicable and no remediation is needed.

### Original Finding Content

##### Description

The `initTransactionCost` variable was hardcoded in the source code examples, making it static and unresponsive to real-time gas price fluctuations on the blockchain network. This approach did not account for dynamic network conditions, potentially leading to incorrect transaction execution or unexpected failures due to insufficient gas provision.

### Impact

The major security concern about this issue was the use of a hardcoded transaction value (`initTransactionCost`), which could lead to incorrect execution or gas manipulation. This value must be calculated dynamically.

* **Economic Denial of Service (EDoS):** If gas prices surge unexpectedly, a hardcoded gas limit may lead to transaction failures or delays.
* **Manipulation Risk:** Attackers could deliberately increase network congestion, forcing the hardcoded value to be insufficient, causing critical operations to fail.
* **Reduced Flexibility:** The contract cannot adapt to real-time gas price changes, increasing operational risk.

This vulnerability severity was lowered from HIGH to MEDIUM because all the hardcoded values for the transaction cost were found in the `examples` folder of the project. However, this bad practice should be removed, according to the best security practices.

##### Proof of Concept

* `examples/account-deployment/user-operation-init-code-deployment.ts`

```
const smartAccountAdddress = await predictAccountAddrOnchain(factoryAddress, combinedAddresses, salt, provider)
  console.log("Smart Account Address:", smartAccountAdddress)

  const initTransactionCost = parseUnits("0.05", 18)
  const addBalanceToSmartAccountTransaction = await wallet.sendTransaction({ to: smartAccountAdddress, value: initTransactionCost })
  await addBalanceToSmartAccountTransaction.wait()
```

* `examples/account-deployment/user-operation-init-code-deployment.ts`

```
const smartAccountAdddress = await predictAccountAddrOnchain(factoryAddress, combinedAddresses, salt, provider)
  console.log("Smart Account Address:", smartAccountAdddress)

  const initTransactionCost = parseUnits("0.05", 18)
  const addBalanceToSmartAccountTransaction = await wallet.sendTransaction({ to: smartAccountAdddress, value: initTransactionCost })
  await addBalanceToSmartAccountTransaction.wait()
```

* `examples/sign_3_of_3/sign-3_of_3.ts`

```
/**
   * Prefund smart account
   */
  const initTransactionCost = parseUnits("0.05", 18)
  const addBalanceToSmartAccountTransaction = await wallet.sendTransaction({ to: multiSigSmartAccount.address, value: initTransactionCost })
  await addBalanceToSmartAccountTransaction.wait()
```

* `examples/user-operation/transfer-erc20/transfer-erc20.ts`

```
/**
  * Prefund smart account
  */
 const initTransactionCost = parseUnits("0.05", 18)
 const addBalanceToSmartAccountTransaction = await wallet.sendTransaction({ to: multiSigSmartAccount.address, value: initTransactionCost })
 await addBalanceToSmartAccountTransaction.wait()
```

* `examples/user-operation/transfer-native/transfer-native.ts`

```
/**
   * Prefund smart account
   */
  const initTransactionCost = parseUnits("0.06", 18)
  const addBalanceToSmartAccountTransaction = await wallet.sendTransaction({ to: multiSigSmartAccount.address, value: initTransactionCost })
  await addBalanceToSmartAccountTransaction.wait()
```

##### Score

Impact: 4  
Likelihood: 2

##### Recommendation

Similarly to other functions, consider relying on calls to specific contracts to determine the gas estimation. Alternatively, consider using APIs (e.g., blockchain node RPC endpoints or third-party services) as this is the more common approach for gas estimation.

* Replace the hardcoded `initTransactionCost` with a dynamic calculation based on the current gas price using on-chain data or a reliable oracle.
* Implement a buffer margin to account for sudden price spikes in congested conditions.
* Test the contract under varying gas price scenarios to ensure resilience.

##### Remediation

**NOT APPLICABLE**: Finally agreed with the **InFlux Technologies team** that this issue was not applicable.

##### Remediation Hash

<https://github.com/RunOnFlux/account-abstraction/pull/17>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Account Abstraction Schnorr Signatures SDK |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-signatures-sdk
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-signatures-sdk

### Keywords for Search

`vulnerability`

