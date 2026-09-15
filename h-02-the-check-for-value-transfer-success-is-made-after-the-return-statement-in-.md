---
# Core Classification
protocol: Sturdy
chain: everychain
category: uncategorized
vulnerability_type: transfer_result_check

# Attack Vector Details
attack_type: transfer_result_check
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2333
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-sturdy-contest
source_link: https://code4rena.com/reports/2022-05-sturdy
github_link: https://github.com/code-423n4/2022-05-sturdy-findings/issues/157

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - transfer_result_check
  - weird_erc20

protocol_categories:
  - liquid_staking
  - lending
  - bridge
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 32
finders:
  - 0x52
  - 0xf15ers
  - mtz
  - fatherOfBlocks
  - berndartmueller
---

## Vulnerability Title

[H-02] The check for value transfer success is made after the return statement in `_withdrawFromYieldPool` of `LidoVault`

### Overview


This bug report is about a vulnerability in a smart contract code on the Ethereum blockchain. The code is located at https://github.com/code-423n4/2022-05-sturdy/blob/78f51a7a74ebe8adfd055bdbaedfddc05632566f/smart-contracts/LidoVault.sol#L142. The impact of this vulnerability is that users can lose their funds. The proof of concept is that the code checks the success of a transaction after returning the transfer value and finishing execution. If the call fails, the transaction won't revert, leaving users with no funds. The recommended mitigation step is to return the function after the success check.

### Original Finding Content


Users can lose their funds

### Proof of Concept

[LidoVault.sol#L142](https://github.com/code-423n4/2022-05-sturdy/blob/78f51a7a74ebe8adfd055bdbaedfddc05632566f/smart-contracts/LidoVault.sol#L142)<br>

The code checks transaction success after returning the transfer value and finishing execution. If the call fails the transaction won't revert since  require(sent, Errors.VT_COLLATERAL_WITHDRAW_INVALID); won't execute.

Users will have withdrawn without getting their funds back.

### Recommended Mitigation Steps

Return the function after the success check

**[sforman2000 (Sturdy) confirmed](https://github.com/code-423n4/2022-05-sturdy-findings/issues/157)**

**[iris112 (Sturdy) commented](https://github.com/code-423n4/2022-05-sturdy-findings/issues/157):**
 > [Fix the issue of return before require sturdyfi/code4rena-may-2022#9](https://github.com/sturdyfi/code4rena-may-2022/pull/9)

**[hickuphh3 (judge) commented](https://github.com/code-423n4/2022-05-sturdy-findings/issues/157#issuecomment-1145546283):**
 > Issue is rather clear-cut.



***
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Sturdy |
| Report Date | N/A |
| Finders | 0x52, 0xf15ers, mtz, fatherOfBlocks, berndartmueller, saian, peritoflores, tabish, z3s, p4st13r4, 0x4non, IllIllI, simon135, cccz, rotcivegaf, sorrynotsorry, hickuphh3, WatchPug, pedroais, oyc_109, isamjay, 0xliumin, sseefried, hake, TerrierLover, StErMi, CertoraInc, MaratCerby, Dravee, dipp, hyh, GimelSec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-sturdy
- **GitHub**: https://github.com/code-423n4/2022-05-sturdy-findings/issues/157
- **Contest**: https://code4rena.com/contests/2022-05-sturdy-contest

### Keywords for Search

`Transfer Result Check, Weird ERC20`

