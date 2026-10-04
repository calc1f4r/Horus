---
# Core Classification
protocol: GrowthDeFi WHEAT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13367
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/06/growthdefi-wheat/
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
  - dexes
  - cdp
  - yield
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sergii Kravchenko
  - David Oz Kashi
  -  Dominik Muhs
---

## Vulnerability Title

Future-proofness of the onlyEOAorWhitelist modifier

### Overview


This bug report focuses on the `onlyEOAorWhitelist` modifier, which is used to ensure that the message sender is equal to the transaction origin and that the calling party is not a smart contract. The modifier may become ineffective if Ethereum implements EIP-3074, which includes AUTH and AUTHCALL opcodes. This could open up additional attack vectors such as flash loans. The modifier can be disabled in the deployment script for testing purposes, and the attack can be split into multiple transactions, allowing miners to execute it without taking any additional risk. It is recommended to monitor the progress of EIP-3074 and update the contract system if it gets enabled, and to write code that can be called by external smart contracts without compromising security.

### Original Finding Content

#### Resolution



The client communicated this issue was addressed in commit 34c6b355795027d27ae6add7360e61eb6b01b91b.
 

#### Description


The `onlyEOAorWhitelist` modifier is used in various locations throughout the code. It performs a check that asserts the message sender being equal to the transaction origin to assert the calling party is not a smart contract.


This approach may stop working if [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074#allowing-txorigin-as-signer-1) and its AUTH and AUTHCALL opcodes get deployed.


While the OpenZeppelin reentrancy guard does not depend on `tx.origin`, the EOA check does. Its evasion can result in additional attack vectors such as flash loans opening up. It is noteworthy that preventing smart contract interaction with the protocol may limit its opportunities as smart contracts cannot integrate with it in the same way that GrowthDeFi integrates with its third-party service providers.


The `onlyEOAorWhitelist` modifier may give a false sense of security because it won’t allow making a flash loan attack by most of the users. But the same attack can still be made by some people or with more risk:


* The owner and the whitelisted contracts are not affected by the modifier.
* The modifier can be disabled:



```
**wheat-v1-core-audit/contracts/WhitelistGuard.sol:L21-L28**
```solidity
modifier onlyEOAorWhitelist()
{
  if (enabled) {
      address _from = _msgSender();
      require(tx.origin == _from || whitelist.contains(_from), "access denied");
  }
  _;
}
```

```

And in the deployment script, this modifier is disabled for testing purposes, and it’s important not to forget to turn it in on the production:


**wheat-v1-core-audit/migrations/02\_deploy\_contracts.js:L50**



```
await pancakeSwapFeeCollector.setWhitelistEnabled(false); // allows testing

```
* The attack can usually be split into multiple transactions. Miners can put these transactions closely together and don’t take any additional risk. Regular users can take a risk, take the loan, and execute the attack in multiple transactions or even blocks.


#### Recommendation


It is strongly recommended to monitor the progress of this EIP and its potential implementation on the Binance Smart Chain. If this functionality gets enabled, the development team should update the contract system to use the new opcodes.
We also strongly recommend relying less on the fact that only EOA will call the functions. It is better to write the code that can be called by the external smart contracts without compromising its security.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | GrowthDeFi WHEAT |
| Report Date | N/A |
| Finders | Sergii Kravchenko, David Oz Kashi,  Dominik Muhs |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/06/growthdefi-wheat/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

