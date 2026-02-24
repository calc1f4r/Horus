---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: account_abstraction

# Attack Vector Details
attack_type: account_abstraction
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6444
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest
source_link: https://code4rena.com/reports/2023-01-biconomy
github_link: https://github.com/code-423n4/2023-01-biconomy-findings/issues/151

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
  - account_abstraction

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - taek
---

## Vulnerability Title

[H-05] Paymaster ETH can be drained with malicious sender

### Overview


This bug report is about a vulnerability in the VerifyingSingletonPaymaster.sol contract. The vulnerability can be exploited to replay the Paymaster's signature and drain their deposits. A Proof of Concept was provided in the form of an Upgrader.sol, MaliciousAccount.sol, and a test file. The vulnerability was tested using Hardhat and verified with Livingrock.

The recommended mitigation step is to add a simple boolean data for mapping if the hash is used or not. This can be done by adding the following code to the validatePaymasterUserOp function:

```
mapping(bytes32 => boolean) public usedHash

function validatePaymasterUserOp(UserOperation calldata userOp, bytes32 /*userOpHash*/, uint256 requiredPreFund)
external override returns (bytes memory context, uint256 deadline) {
    (requiredPreFund);
    bytes32 hash = getHash(userOp);
    require(!usedHash[hash], "used hash");
    usedHash[hash] = true;
```

This code will check if the hash has already been used, and if it has, the code will not allow the transaction to go through. This will prevent the Paymaster's signature from being replayed and their deposits from being drained.

### Original Finding Content


[contracts/smart-contract-wallet/paymasters/verifying/singleton/VerifyingSingletonPaymaster.sol#L97-L111](https://github.com/code-423n4/2023-01-biconomy/blob/53c8c3823175aeb26dee5529eeefa81240a406ba/scw-contracts/contracts/smart-contract-wallet/paymasters/verifying/singleton/VerifyingSingletonPaymaster.sol#L97-L111)

Paymaster's signature can be replayed to drain their deposits.

### Proof of Concept

Scenario :

*   user A is happy with biconomy and behaves well biconomy gives some sponsored tx using verifyingPaymaster -- let's say paymaster's signature as sig X
*   user A becomes not happy with biconomy for some reason and A wants to attack biconomy
*   user A delegate calls to Upgrader and upgrade it's sender contract to MaliciousAccount.sol
*   MaliciousAccount.sol does not check any nonce and everything else is same to SmartAccount(but they can also add some other details to amplify the attack, but let's just stick it this way)
*   user A uses sig X(the one that used before) to initiate the same tx over and over
*   user A earnes nearly nothing but paymaster will get their deposits drained

files : Upgrader.sol, MaliciousAccount.sol, test file <br><https://gist.github.com/leekt/d8fb59f448e10aeceafbd2306aceaab2>

### Tools Used

hardhat test, verified with livingrock

### Recommended Mitigation Steps

Since `validatePaymasterUserOp` function is not limited to view function in erc4337 spec, add simple boolean data for mapping if hash is used or not

    mapping(bytes32 => boolean) public usedHash

        function validatePaymasterUserOp(UserOperation calldata userOp, bytes32 /*userOpHash*/, uint256 requiredPreFund)
        external override returns (bytes memory context, uint256 deadline) {
            (requiredPreFund);
            bytes32 hash = getHash(userOp);
            require(!usedHash[hash], "used hash");
            usedHash[hash] = true;

**[livingrockrises (Biconomy) confirmed, but commented](https://github.com/code-423n4/2023-01-biconomy-findings/issues/151#issuecomment-1423007244):**
 > Unhappy with the recommendation.



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
| Finders | taek |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-biconomy
- **GitHub**: https://github.com/code-423n4/2023-01-biconomy-findings/issues/151
- **Contest**: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest

### Keywords for Search

`Account Abstraction`

