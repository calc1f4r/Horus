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
solodit_id: 6440
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest
source_link: https://code4rena.com/reports/2023-01-biconomy
github_link: https://github.com/code-423n4/2023-01-biconomy-findings/issues/496

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - gogo
  - hihen
  - ro
  - Koolex
  - kankodu
---

## Vulnerability Title

[H-01] Destruction of the `SmartAccount` implementation

### Overview


This bug report is about an issue with the SmartAccount contract, which is part of the code-423n4/2023-01-biconomy project. If the SmartAccount implementation contract is not initialized, it can be destroyed using a single delegatecall to a contract that executes the selfdestruct opcode on any incoming call. This would result in the freezing of all functionality of the wallets that point to such an implementation, as well as making it impossible to change the implementation address. 

The issue is that the deploy script does not enforce the initialization of the SmartAccount contract implementation. To prevent this attack, either the deploy script should be changed to initialize the SmartAccount implementation, or the SmartAccount contract should be updated to add a constructor that will prevent the implementation contract from being initialized. 

The impact of this issue would be the complete freezing of all functionality of all wallets, including freezing of all funds.

### Original Finding Content


[contracts/smart-contract-wallet/SmartAccount.sol#L166](https://github.com/code-423n4/2023-01-biconomy/blob/53c8c3823175aeb26dee5529eeefa81240a406ba/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L166)<br>
[contracts/smart-contract-wallet/SmartAccount.sol#L192](https://github.com/code-423n4/2023-01-biconomy/blob/53c8c3823175aeb26dee5529eeefa81240a406ba/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L192)<br>
[contracts/smart-contract-wallet/SmartAccount.sol#L229](https://github.com/code-423n4/2023-01-biconomy/blob/53c8c3823175aeb26dee5529eeefa81240a406ba/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L229)<br>
[contracts/smart-contract-wallet/base/Executor.sol#L23](https://github.com/code-423n4/2023-01-biconomy/blob/53c8c3823175aeb26dee5529eeefa81240a406ba/scw-contracts/contracts/smart-contract-wallet/base/Executor.sol#L23)

If the `SmartAccount` implementation contract is not initialized, it can be destroyed using the following attack scenario:

*   Initialize the `SmartAccount` **implementation** contract using the `init` function.
*   Execute a transaction that contains a single `delegatecall` to a contract that executes the `selfdestruct` opcode on any incoming call, such as:

```solidity
contract Destructor {
    fallback() external {
        selfdestruct(payable(0));
    }
}
```

The destruction of the implementation contract would result in the freezing of all functionality of the wallets that point to such an implementation. It would also be impossible to change the implementation address, as the `Singleton` functionality and the entire contract would be destroyed, leaving only the functionality from the Proxy contract accessible.

In the deploy script there is the following logic:

```typescript
const SmartWallet = await ethers.getContractFactory("SmartAccount");
const baseImpl = await SmartWallet.deploy();
await baseImpl.deployed();
console.log("base wallet impl deployed at: ", baseImpl.address);
```

So, in the deploy script there is no enforce that the `SmartAccount` contract implementation was initialized.

The same situation in `scw-contracts/scripts/wallet-factory.deploy.ts` script.

Please note, that in case only the possibility of initialization of the `SmartAccount` implementation will be banned it will be possible to use this attack. This is so because in such a case `owner` variable will be equal to zero and it will be easy to pass a check inside of `checkSignatures` function using the fact that for incorrect input parameters `ecrecover` returns a zero address.

### Impact

Complete freezing of all functionality of all wallets (including complete funds freezing).

### Recommended Mitigation Steps

Add to the deploy script initialization of the `SmartAccount` implementation, or add to the `SmartAccount` contract the following constructor that will prevent implementation contract from the initialization:

```solidity
// Constructor ensures that this implementation contract can not be initialized
constructor() public {
    owner = address(1);
}
```

**[gzeon (judge) commented](https://github.com/code-423n4/2023-01-biconomy-findings/issues/496#issuecomment-1384930216):**
 > [`#14`](https://github.com/code-423n4/2023-01-biconomy-findings/issues/14) also notes that if owner is left to address(0) some validation can be bypassed.

**[livingrockrises (Biconomy) confirmed](https://github.com/code-423n4/2023-01-biconomy-findings/issues/496#issuecomment-1404324137)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | gogo, hihen, ro, Koolex, kankodu, Matin, HE1M, smit_rajput, 0xdeadbeef0x, chaduke, spacelord47, taek, adriro, V_B, jonatascm |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-biconomy
- **GitHub**: https://github.com/code-423n4/2023-01-biconomy-findings/issues/496
- **Contest**: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest

### Keywords for Search

`vulnerability`

