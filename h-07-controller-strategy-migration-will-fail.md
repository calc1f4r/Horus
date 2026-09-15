---
# Core Classification
protocol: JPEG'd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1913
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-jpegd-contest
source_link: https://code4rena.com/reports/2022-04-jpegd
github_link: https://github.com/code-423n4/2022-04-jpegd-findings/issues/57

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
  - lending
  - dexes
  - cdp
  - services
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - rayn
  - hickuphh3
---

## Vulnerability Title

[H-07] Controller: Strategy migration will fail

### Overview


This bug report concerns a vulnerability in the contracts of the code-423n4/2022-04-jpegd repository. Specifically, the controller calls the `withdraw()` method to withdraw JPEGs from the contract, but the strategy might blacklist the JPEG asset, which is what the PUSDConvex strategy has done. This would cause the migration to revert. In order to prove the concept, the tester inserted a test into the StrategyPUSDConvex.ts file, which demonstrated the issue. The recommended mitigation step is to replace `_current.withdraw(address(jpeg));` with `_current.withdrawJPEG(vaults[_token])`.

### Original Finding Content

_Submitted by hickuphh3, also found by rayn_

[Controller.sol#L95](https://github.com/code-423n4/2022-04-jpegd/blob/main/contracts/vaults/yVault/Controller.sol#L95)<br>
[StrategyPUSDConvex.sol#L266](https://github.com/code-423n4/2022-04-jpegd/blob/main/contracts/vaults/yVault/strategies/StrategyPUSDConvex.sol#L266)<br>

The controller calls the `withdraw()` method to withdraw JPEGs from the contract, but the strategy might blacklist the JPEG asset, which is what the PUSDConvex strategy has done.

The migration would therefore revert.

### Proof of Concept

Insert this test into [`StrategyPUSDConvex.ts`](https://github.com/code-423n4/2022-04-jpegd/blob/main/tests/StrategyPUSDConvex.ts).

```jsx
it.only("will revert when attempting to migrate strategy", async () => {
  await controller.setVault(want.address, yVault.address);
  await expect(controller.setStrategy(want.address, strategy.address)).to.be.revertedWith("jpeg");
});
```

### Recommended Mitigation Steps

Replace `_current.withdraw(address(jpeg));` with `_current.withdrawJPEG(vaults[_token])`.

**[spaghettieth (JPEG'd) confirmed and commented](https://github.com/code-423n4/2022-04-jpegd-findings/issues/57#issuecomment-1096633358):**
 > The proposed migration steps would modify the intended behaviour, which is to withdraw JPEG to the controller and not the vault. A correct solution would be replacing `_current.withdraw(address(jpeg))` with `_current.withdrawJPEG(address(this))`.

**[spaghettieth (JPEG'd) resolved and commented](https://github.com/code-423n4/2022-04-jpegd-findings/issues/57#issuecomment-1099242526):**
 > Fixed in [jpegd/core#6](https://github.com/jpegd/core/pull/6).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | JPEG'd |
| Report Date | N/A |
| Finders | rayn, hickuphh3 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-jpegd
- **GitHub**: https://github.com/code-423n4/2022-04-jpegd-findings/issues/57
- **Contest**: https://code4rena.com/contests/2022-04-jpegd-contest

### Keywords for Search

`vulnerability`

