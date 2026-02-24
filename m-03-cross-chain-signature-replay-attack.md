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
solodit_id: 6449
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest
source_link: https://code4rena.com/reports/2023-01-biconomy
github_link: https://github.com/code-423n4/2023-01-biconomy-findings/issues/466

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
  - account_abstraction
  - cross_chain
  - replay_attack

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
  - V_B  taek
  - gogo
---

## Vulnerability Title

[M-03] Cross-Chain Signature Replay Attack

### Overview


A Cross-Chain Signature Replay Attack vulnerability has been identified in the lines of code provided in the report. This vulnerability can lead to users losing funds or any unexpected behaviour that transaction replay attacks usually lead to. The vulnerability is due to the fact that the chainId is missing from the calculation of the UserOperation hash in the specified code. This means that the same UserOperation can be replayed on a different chain for the same smart contract account if the verifyingSigner is the same. The recommended mitigation step is to add the chainId in the calculation of the UserOperation hash in the specified code. This will ensure that the same UserOperation cannot be replayed on a different chain for the same smart contract account.

### Original Finding Content


User operations can be replayed on smart accounts accross different chains. This can lead to user's losing funds or any unexpected behaviour that transaction replay attacks usually lead to.

### Proof of Concept

As specified by the [EIP4337](https://eips.ethereum.org/EIPS/eip-4337) standard `to prevent replay attacks ... the signature should depend on chainid`. In [VerifyingSingletonPaymaster.sol#getHash](https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/paymasters/verifying/singleton/VerifyingSingletonPaymaster.sol#L77-L90) the chainId is missing which means that the same UserOperation can be replayed on a different chain for the same smart contract account if the `verifyingSigner` is the same (and most likely this will be the case).

### Recommended Mitigation Steps

Add the chainId in the calculation of the UserOperation hash in [VerifyingSingletonPaymaster.sol#getHash](https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/paymasters/verifying/singleton/VerifyingSingletonPaymaster.sol#L77-L90)

        function getHash(UserOperation calldata userOp)
        public view returns (bytes32) { // @audit change to view
            //can't use userOp.hash(), since it contains also the paymasterAndData itself.
            return keccak256(abi.encode(
                    userOp.getSender(),
                    userOp.nonce,
                    keccak256(userOp.initCode),
                    keccak256(userOp.callData),
                    userOp.callGasLimit,
                    userOp.verificationGasLimit,
                    userOp.preVerificationGas,
                    userOp.maxFeePerGas,
                    userOp.maxPriorityFeePerGas
    		block.chainid // @audit add chain id
                ));
        }

**[livingrockrises (Biconomy) confirmed](https://github.com/code-423n4/2023-01-biconomy-findings/issues/466#issuecomment-1421110204)**

**[gzeon (judge) decreased severity to Medium](https://github.com/code-423n4/2023-01-biconomy-findings/issues/466#issuecomment-1425735635)**

**[vlad\_bochok (warden) commented](https://github.com/code-423n4/2023-01-biconomy-findings/issues/466#issuecomment-1426673710):**
 > @gzeon @livingrockrises 
> 
> > User operations can be replayed on smart accounts accross different chains
> 
> The author refers that the operation may be replayed on a different chain. That is not true. The "getHash" function derives the hash of UserOp specifically for the paymaster's internal usage. While the paymaster doesn't sign the chainId, the UserOp may not be relayed on a different chain. So, the only paymaster may get hurt. In all other respects, the bug is valid.
> 
> The real use case of this cross-chan replayability is described in issue [`#504`](https://github.com/code-423n4/2023-01-biconomy-findings/issues/504) (which, I believe, was mistakenly downgraded).

**[livingrockrises (Biconomy) commented](https://github.com/code-423n4/2023-01-biconomy-findings/issues/466#issuecomment-1426685496):**
 > True. Besides chainId , address(this) should be hashed and contract must maintain it's own nonces per wallet otherwise wallet can replay the signature and use paymaster to sponsor! We're also planning to hash paymasterId as add-on on top of our off-chain validation for it.  
> 
> I have't seen an issue which covers all above. Either cross chain replay or suggested paymaster nonce.



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
| Finders | V_B  taek, gogo |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-biconomy
- **GitHub**: https://github.com/code-423n4/2023-01-biconomy-findings/issues/466
- **Contest**: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest

### Keywords for Search

`Account Abstraction, Cross Chain, Replay Attack`

