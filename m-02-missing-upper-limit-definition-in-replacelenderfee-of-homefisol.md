---
# Core Classification
protocol: Rigor Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3106
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-rigor-protocol-contest
source_link: https://code4rena.com/reports/2022-08-rigor
github_link: https://github.com/code-423n4/2022-08-rigor-findings/issues/400

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
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - 8olidity
  - __141345__
  - 0x52
  - codexploder
  - MiloTruck
---

## Vulnerability Title

[M-02] Missing upper limit definition in `replaceLenderFee()` of `HomeFi.sol`

### Overview


This bug report is about a vulnerability in the `HomeFi` contract of a project called "2022-08-rigor". The vulnerability is that the admin of the `HomeFi` contract can set `lenderFee` to greater than 100%, which would force calls to `lendToProject()` to all projects created in the future to revert. This is because the calculation for `lenderFee` in `lendToProject()` will overflow when `lenderFee` is set to a large value.

The recommended mitigation step for this vulnerability is to consider adding a reasonable fee rate bounds check in the `replaceLenderFee()` function. This would prevent potential griefing and increase the trust of users in the contract.

### Original Finding Content

_Submitted by MiloTruck, also found by &#95;&#95;141345&#95;&#95;, 0x52, 8olidity, cccz, Ch&#95;301, codexploder, cryptonue, hansfriese, Ruhum, and sseefried_

[Community.sol#L392-L394](https://github.com/code-423n4/2022-08-rigor/blob/main/contracts/Community.sol#L392-L394)<br>
[HomeFi.sol#L184-L197](https://github.com/code-423n4/2022-08-rigor/blob/main/contracts/HomeFi.sol#L184-L197)<br>

The admin of the `HomeFi` contract can set `lenderFee` to greater than 100%, forcing calls to `lendToProject()` to all projects created in the future to revert.

### Proof of Concept

Using the function `replaceLenderFee()`, admins of the `HomeFi` contract can set `lenderFee` to any arbitrary `uint256` value:

```solidity
 185:        function replaceLenderFee(uint256 _newLenderFee)
 186:            external
 187:            override
 188:            onlyAdmin
 189:        {
 190:            // Revert if no change in lender fee
 191:            require(lenderFee != _newLenderFee, "HomeFi::!Change");
 192:    
 193:            // Reset variables
 194:            lenderFee = _newLenderFee;
 195:    
 196:            emit LenderFeeReplaced(_newLenderFee);
 197:        }
```

New projects that are created will then get its `lenderFee` from the `HomeFi` contract. When communities wish to lend to these projects, it calls `lendToProject()`, which has the following calculation:

```solidity
 392:        // Calculate lenderFee
 393:        uint256 _lenderFee = (_lendingAmount * _projectInstance.lenderFee()) /
 394:            (_projectInstance.lenderFee() + 1000);
```

If `lenderFee` a large value, such as `type(uint256).max`, the calculation shown above to overflow. This prevents any community from lending to any new projects.

### Recommended Mitigation Steps

Consider adding a reasonable fee rate bounds checks in the `replaceLenderFee()` function. This would prevent potential griefing and increase the trust of users in the contract.

**[zgorizzo69 (Rigor) confirmed](https://github.com/code-423n4/2022-08-rigor-findings/issues/400)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rigor Protocol |
| Report Date | N/A |
| Finders | 8olidity, __141345__, 0x52, codexploder, MiloTruck, cccz, Ruhum, cryptonue, hansfriese, Ch_301, sseefried |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-rigor
- **GitHub**: https://github.com/code-423n4/2022-08-rigor-findings/issues/400
- **Contest**: https://code4rena.com/contests/2022-08-rigor-protocol-contest

### Keywords for Search

`vulnerability`

