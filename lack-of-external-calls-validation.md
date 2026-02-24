---
# Core Classification
protocol: Account Abstraction Schnorr Signatures SDK
chain: everychain
category: uncategorized
vulnerability_type: external_call

# Attack Vector Details
attack_type: external_call
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52575
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-signatures-sdk
source_link: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-signatures-sdk
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - external_call
  - from=to

protocol_categories:
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

LACK OF EXTERNAL CALLS VALIDATION

### Overview


This bug report discusses the issue of non-validated external calls in a code library. This means that the code is making calls to external contracts without properly verifying the return value or handling any potential errors. This can lead to security vulnerabilities and unexpected behavior in the application. The report provides examples of unvalidated calls and suggests implementing proper error handling and validation, as well as ensuring the external contract follows best practices for reentrancy protection. The report also includes a recommendation from the InFlux Technologies team to handle errors and validation on the client side, and a link to a pull request for remediation. It rates the impact as 5 out of 10 and the likelihood as 3 out of 10.

### Original Finding Content

##### Description

Non-validated external calls occur when a function invokes an external contract without verifying the return value or handling potential errors.

Several external calls were detected without proper validation.

### Impact

This can lead to reentrancy attacks or unexpected side effects if the external call fails or returns an unexpected result, directly causing a potential impact in the availability or integrity of the environment.

##### Proof of Concept

Listed below, there are some examples of unvalidated calls that may fail or cause an unconsistent or unexpected behavior of the application execution flow.

* `examples/account-address/account_address.ts`

```
async function getAddressAlchemyAASDK(combinedAddresses: Address[], salt: string) {
  const rpcUrl = process.env.ALCHEMY_RPC_URL
  const transport = http(rpcUrl)
  const multiSigSmartAccount = await createMultiSigSmartAccount({
    transport,
    chain: CHAIN,
    combinedAddress: combinedAddresses,
    salt: saltToHex(salt),
    entryPoint: getEntryPoint(CHAIN),
  })

  return multiSigSmartAccount.address
}


```

* `src/helpers/create2.ts`

```
export async function getAccountImplementationAddress(factoryAddress: string, ethersSignerOrProvider: Signer | Provider): Promise<string> {
  const smartAccountFactory = new ethers.Contract(factoryAddress, MultiSigSmartAccountFactory_abi, ethersSignerOrProvider)
  const accountImplementation = await smartAccountFactory.accountImplementation()
  return accountImplementation
}
```

* `src/helpers/factory-helpers.ts`

```
export async function predictAccountAddress(
  factoryAddress: Hex,
  signer: Signer,
  combinedPubKeys: string[],
  salt: string
): Promise<`0x${string}`> {
  const smartAccountFactory = new ethers.Contract(factoryAddress, MultiSigSmartAccountFactory_abi, signer)
  const saltHash = ethers.keccak256(ethers.toUtf8Bytes(salt))
  const predictedAccount = await smartAccountFactory.getAccountAddress(combinedPubKeys, saltHash)
  return predictedAccount as Hex
}
```

* `examples/account-deployment/user-operation-init-code-deployment.ts`

```
const factoryAddress = deployments[CHAIN.id]?.MultiSigSmartAccountFactory

  const smartAccountAdddress = await predictAccountAddrOnchain(factoryAddress, combinedAddresses, salt, provider)
  console.log("Smart Account Address:", smartAccountAdddress)

  const initTransactionCost = parseUnits("0.05", 18)
  const addBalanceToSmartAccountTransaction = await wallet.sendTransaction({ to: smartAccountAdddress, value: initTransactionCost })
  await addBalanceToSmartAccountTransaction.wait()

  const transport = http(process.env.ALCHEMY_RPC_URL)
  const multiSigSmartAccount = await createMultiSigSmartAccount({
    transport,
    chain: CHAIN,
    combinedAddress: combinedAddresses,
    salt: saltToHex(salt),
    entryPoint: getEntryPoint(CHAIN),
  })
```

##### Score

Impact: 5  
Likelihood: 3

##### Recommendation

* Implement proper error handling and validation for external calls.
* Use `try/catch` blocks to handle exceptions and log errors appropriately.
* Ensure the external contract being called follows best practices for reentrancy protection.

##### Remediation

**RISK ACCEPTED**: According to the **InFlux Technologies team**, they wanted the library to throw the exact error message. Handling of error and validation should happen on a client using the library.

##### Remediation Hash

<https://github.com/RunOnFlux/account-abstraction/pull/17>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Halborn |
| Protocol | Account Abstraction Schnorr Signatures SDK |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-signatures-sdk
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/influx-technologies/account-abstraction-schnorr-signatures-sdk

### Keywords for Search

`External Call, from=to`

