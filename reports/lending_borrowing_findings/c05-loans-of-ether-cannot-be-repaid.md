---
# Core Classification
protocol: Aave Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11596
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[C05] Loans of Ether cannot be repaid

### Overview


This bug report concerns the repayment of an Ether loan taken out from the Aave protocol. The caller of the [`repay` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L329) of the `LendingPool` contract is expected to send Ether along with the transaction, which should be split in two to first pay the origination fee and then to pay down the loan. However, the `LendingPool` contract [expects to receive the repayment component](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L375) in the second transfer, but typically there is insufficient Ether to complete the second transfer, which causes the entire transaction to revert.

The bug has since been fixed in [MR#48](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/48/diffs) with the `LendingPoolCore` contract now either returning the excess ether to the `LendingPool` contract in the [`transferToFeeCollectionAddres` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolCore.sol#661) or recognizing if Ether was sent with the `repay` function and forwarding the exact amounts in both transfers. However, an erroneous inline comment was introduced stating “sending the total msg.value if the transfer is ETH”. In this case, when the function executes an ETH transfer, only the amount `msg.value.sub(vars.originationFee)` is transferred.

### Original Finding Content

Any user that has taken out a loan in the Aave protocol should be able to repay it by calling the [`repay` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L329) of the `LendingPool` contract. However, a flaw in this function makes it (typically) impossible to repay an Ether loan.


During the process of repaying an Ether loan the caller is expected to send Ether along with the transaction. That Ether should be split in two, to first pay the origination fee and then to pay down the loan. These operations are executed in lines [375](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L375) and [412](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L412). Both transfers are sent to the `LendingPoolCore` contract, which forwards the fee to a “fee collection address” during the first transfer. Even though the `LendingPoolCore` contract is the destination in both cases, it [expects to receive the repayment component](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L375) in the second transfer. Consequently, the `LendingPool` contract will (typically) have insufficient Ether to complete the second transfer, which will cause the entire transaction to revert.


Consider either returning the excess ether to the `LendingPool` contract in the [`transferToFeeCollectionAddres` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolCore.sol#661) or recognizing if Ether was sent with the `repay` function and forwarding the exact amounts in both transfers.


**Update**: *Fixed in [MR#48](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/48/diffs). However, note that an [erroneous inline comment](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/48/diffs#f32d1b0823e1b657d11caa63b3c186b8912d8067_425_444) has been introduced stating “sending the total msg.value if the transfer is ETH”. In this case, when the function executes an ETH transfer, only the amount `msg.value.sub(vars.originationFee)` is transferred.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Aave Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/aave-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

