---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35036
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#4-erc-4337-call-to-_payprefund-may-lead-to-the-validator-stake-being-split
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

ERC-4337 call to `_payPrefund` may lead to the validator stake being split

### Overview


There is a problem with the code at lines 114 and 103 in the `ContractWcFeeDistributor` and `Erc4337Account` files. If a user chooses to stop staking, the `ContractWcFeeDistributor` will receive a 32 ETH stake. However, if the user has withdrawn all previous rewards from the contract or the rewards are low, using the `withdraw()` function through the `ERC-4337` account may result in the transaction fee being paid with the stake funds. This can cause the user's stake to be split between the `referrer` and `service` instead of being returned in full. This is considered a high severity issue as it results in the user receiving less ETH than they initially deposited. To fix this, it is recommended to replace the call to `_payPrefund()` in the `Erc4337Account` file to prevent contract funds from being used for transaction fees.

### Original Finding Content

##### Description
There is an issue at line https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/ContractWcFeeDistributor.sol#L114 and https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/Erc4337Account.sol#L103.
If a user voluntarily exits staking, then `ContractWcFeeDistributor` will receive a 32 ETH stake (in case if there were no slashings). If all previous rewards were withdrawn from the contract (or they are quite low), then a call to the `withdraw()` function via `ERC-4337` account abstraction logic may lead to paying for the transaction fee using that stake funds (in case if there were no deposit or paymaster is not used). Then this `balance >= COLLATERAL` check will not pass and the users' stake would get split also to `referrer` and `service`.
The HIGH severity level was assigned to that issue since a user receives less ETH than they initially deposited. Their stake is split also to `referrer` and `service` what shouldn't happen in a normal case.

##### Recommendation
We recommend replacing the call to `_payPrefund()` here https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/Erc4337Account.sol#L52. This replacement will prevent contract funds from being used to pay for transaction gas.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#4-erc-4337-call-to-_payprefund-may-lead-to-the-validator-stake-being-split
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

