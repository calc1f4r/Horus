---
# Core Classification
protocol: Redacted Cartel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6060
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-redacted-cartel-contest
source_link: https://code4rena.com/reports/2022-11-redactedcartel
github_link: #l-11-lack-of-input-validation

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-11] Lack of Input Validation

### Overview

See description below for full details.

### Original Finding Content


For defence-in-depth purpose, it is recommended to perform additional validation against the amount that the user is attempting to deposit, mint, withdraw and redeem to ensure that the submitted amount is valid.

[OpenZeppelinTokenizedVault.sol#L9](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/7c75b8aa89073376fb67d78a40f6d69331092c94/contracts/token/ERC20/extensions/ERC20TokenizedVault.sol#L95)


```diff
src/PirexGmx.sol:
  429       */
  430:     function depositGmx(uint256 amount, address receiver)
  431:         external
  432:         whenNotPaused
  433:         nonReentrant
  434:         returns (
  435:             uint256,
  436:             uint256,
  437:             uint256
  438:         )
  439:     {
+	         require(amount <= maxDeposit(receiver), "deposit more than max");
```

```diff
src/vaults/PirexERC4626.sol:
  79  
  80:     function mint(uint256 shares, address receiver)
  81:         public
  82:         virtual
  83:         returns (uint256 assets)
  84:     {
+ 	       require(shares <= maxMint(receiver), "mint more than max");

```

```diff
src/vaults/AutoPxGlp.sol:
  438:     function withdraw(
  439:         uint256 assets,
  440:         address receiver,
  441:         address owner
  442:     ) public override returns (uint256 shares) {
+                require(assets <= maxWithdraw(owner), "withdraw more than max");

src/vaults/AutoPxGmx.sol:
  317:     function withdraw(
  318:         uint256 assets,
  319:         address receiver,
  320:         address owner
  321:     ) public override returns (uint256 shares) {
+               require(assets <= maxWithdraw(owner), "withdraw more than max");
```


```diff
src/vaults/AutoPxGlp.sol:
  450       */
  451:     function redeem(
  452:         uint256 shares,
  453:         address receiver,
  454:         address owner
  455:     ) public override returns (uint256 assets) {
+               require(shares <= maxRedeem(owner), "redeem more than max");

src/vaults/AutoPxGmx.sol:
  340  
  341:     function redeem(
  342:         uint256 shares,
  343:         address receiver,
  344:         address owner
  345:     ) public override returns (uint256 assets) {
+                require(shares <= maxRedeem(owner), "redeem more than max");
```

## Non-Critical Issues Summary
| Number |Issues Details|Context|
|:--:|:-------|:--:|
| [N-01] |Insufficient coverage|1|
| [N-02] |Not using the named return variables anywhere in the function is confusing  |1 |
| [N-03] |Same Constant redefined elsewhere| 4 |
| [N-04] |Omissions in Events| 8 | 
| [N-05] |Add parameter to Event-Emit | 1 |
| [N-06] |NatSpec is missing  | 1 |
| [N-07] |Use `require` instead of `assert` | 1 |
| [N-08] |Implement some type of version counter that will be incremented automatically for contract upgrades | 1 |
| [N-09] |Constant values such as a call to keccak256(), should used to immutable rather than constant | 2 |
| [N-10] |For functions, follow Solidity standard naming conventions | 4  |
| [N-11] |Mark visibility of initialize(...) functions as ``external``| 1 |
| [N-12] |No same value input control | 8 |
| [N-13] |Include ``return parameters`` in _NatSpec comments_ | All |
| [N-14] |`0 address` check for ` asset ` | 1 |
| [N-15] |Use a single file for all system-wide constants| 6 |
| [N-16] |`Function writing` that does not comply with the `Solidity Style Guide`| All |
| [N-17] |Missing Upgrade Path for `PirexRewards` Implementation| 1 |
| [N-18] | No need `assert` check in `_computeAssetAmounts()` | 1 |
| [N-19] | Lack of event emission after critical `initialize()` functions | 1 |
| [N-20] | Add a timelock to critical functions | 11 |

Total 19 issues




### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Redacted Cartel |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-redactedcartel
- **GitHub**: #l-11-lack-of-input-validation
- **Contest**: https://code4rena.com/contests/2022-11-redacted-cartel-contest

### Keywords for Search

`vulnerability`

