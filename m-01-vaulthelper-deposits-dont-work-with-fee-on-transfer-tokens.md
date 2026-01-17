---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42285
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-yaxis
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/127

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
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] `VaultHelper` deposits don't work with fee-on transfer tokens

### Overview


The report discusses a bug found in ERC20 tokens that have certain customizations to their contracts. These tokens include deflationary tokens that charge a fee for transfers and rebasing tokens that increase in value over time. The bug affects the `VaultHelper`'s `depositVault()` and `depositMultipleVault` functions, which may transfer less than the intended amount to the contract due to fees. This can lead to a failed transaction when attempting to deposit the full amount into the vault. The recommended mitigation steps include measuring the asset change before and after the transfer, and avoiding the use of rebasing or fee-charging tokens. The bug could potentially cause the protocol to fail, but can be avoided by not using the affected tokens. 

### Original Finding Content

_Submitted by cmichel, also found by 0xsanson_

There are ERC20 tokens that may make certain customizations to their ERC20 contracts.
One type of these tokens is deflationary tokens that charge a certain fee for every `transfer()` or `transferFrom()`.
Others are rebasing tokens that increase in value over time like Aave's aTokens (`balanceOf` changes over time).

#### Impact
The `VaultHelper`'s `depositVault()` and `depositMultipleVault` functions transfer `_amount` to `this` contract using `IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount);`.
This could have a fee, and less than `_amount` ends up in the contract.
The next actual vault deposit using `IVault(_vault).deposit(_token, _amount);` will then try to transfer more than the `this` contract actually has and will revert the transaction.

#### Recommended Mitigation Steps
One possible mitigation is to measure the asset change right before and after the asset-transferring routines.
This is already done correctly in the `Vault.deposit` function.

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/127#issuecomment-941740332):**
 > Agree with finding, checking actual balance of contract would mitigate vulnerability
> Additionally ensuring the protocol never uses rebasing or tokens with `feeOnTransfer` can be enough to mitigate
>
> The vulnerability can brick the protocol
> However it can be sidestepped by simply not using `feeOnTransfer` tokens
> Downgrading to medium



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/127
- **Contest**: https://code4rena.com/reports/2021-09-yaxis

### Keywords for Search

`vulnerability`

