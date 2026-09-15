---
# Core Classification
protocol: Harpie
chain: everychain
category: uncategorized
vulnerability_type: call_vs_transfer

# Attack Vector Details
attack_type: call_vs_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3376
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/3
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/007-M

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.40
financial_impact: medium

# Scoring
quality_score: 2.001075122243043
rarity_score: 1.0014334963240574

# Context Tags
tags:
  - call_vs_transfer

protocol_categories:
  - staking_pool
  - oracle

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - csanuragjain
  - IllIllI
  - pashov
  - gogo
  - yixxas
---

## Vulnerability Title

M-4: Usage of deprecated transfer() can result in revert.

### Overview


This bug report is about an issue found in the withdrawPayments() function of the Vault.sol contract. It was found by Lambda, cccz, yixxas, Waze, IEatBabyCarrots, pashov, 0xSmartContract, JohnSmith, Tomo, CodingNameKiki, sach1r0, IllIllI, csanuragjain, and gogo. The issue is that the function uses the deprecated transfer() which can result in a revert due to a fixed amount of gas. This can happen if the withdrawer smart contract does not implement a payable fallback function, or if it does but uses more than 2300 gas units, or if it needs less than 2300 gas units but is called through a proxy that raises the call’s gas usage above 2300. The impact of this bug is that funds may not be received by the fee recipient.

The bug was fixed by using call instead of transfer(). A code snippet was provided, as well as a link to a pull request with the fix. Lead Senior Watson confirmed the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/007-M 

## Found by 
Lambda, cccz, yixxas, Waze, IEatBabyCarrots, pashov, 0xSmartContract, JohnSmith, Tomo, CodingNameKiki, sach1r0, IllIllI, csanuragjain, gogo

## Summary
The function withdrawPayments() is used by the Owners to withdraw the fees.

## Vulnerability Detail
transfer() uses a fixed amount of gas, which was used to prevent reentrancy. However this limit your protocol to interact with others contracts that need more than that to process the transaction.

Specifically, the withdrawal will inevitably fail when:
1.The withdrawer smart contract does not implement a payable fallback function.
2.The withdrawer smart contract implements a payable fallback function which uses more than 2300 gas units.
3.The withdrawer smart contract implements a payable fallback function which needs less than 2300 gas units but is called through a proxy that raises the call’s gas usage above 2300.

## Impact
transfer() uses a fixed amount of gas, which can result in revert.
https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/

## Code Snippet
https://github.com/Harpieio/contracts/blob/97083d7ce8ae9d85e29a139b1e981464ff92b89e/contracts/Vault.sol#L159
https://github.com/Harpieio/contracts/blob/97083d7ce8ae9d85e29a139b1e981464ff92b89e/contracts/Vault.sol#L156-L160

## Tool used

Manual Review

## Recommendation
Use call instead of transfer(). Example:
(bool succeeded, ) = _to.call{value: _amount}("");
require(succeeded, "Transfer failed.");

## Lead Senior Watson

Fair considering recipient may be a contract with custom logic for `receive()`. But this is definitely recoverable if the fee recipient wasn't able to receive funds.

## Harpie Team

Moved to .call. Fix [here](https://github.com/Harpieio/contracts/pull/4/commits/655834654b5dc1225e9d2fcd2c07b00401aeac3b). 

## Lead Senior Watson

Confirmed fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2.001075122243043/5 |
| Rarity Score | 1.0014334963240574/5 |
| Audit Firm | Sherlock |
| Protocol | Harpie |
| Report Date | N/A |
| Finders | csanuragjain, IllIllI, pashov, gogo, yixxas, cccz, Waze, 0xSmartContract, CodingNameKiki, Lambda, JohnSmith, sach1r0, Tomo, IEatBabyCarrots |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/007-M
- **Contest**: https://app.sherlock.xyz/audits/contests/3

### Keywords for Search

`call vs transfer`

