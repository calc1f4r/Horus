---
# Core Classification
protocol: Cega (Eth V2)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47650
audit_firm: OtterSec
contest_link: https://www.cega.fi/
source_link: https://www.cega.fi/
github_link: https://github.com/cega-fi/cega-eth-v2

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Invalid State Transition

### Overview


This bug report discusses a problem with the checks for vault and settlement status in a specific function called checkTradeExpiry. The issue is that these checks are not strict enough, allowing for unauthorized state transitions to occur. This can be exploited by an attacker to revive a settled and in-the-money vault, causing an unintended inflation of deposit assets. A proof of concept is provided, along with an evaluation of the severity of the issue and recommendations for remediation and a patch that has been implemented to fix the issue.

### Original Finding Content

## Vault Status and Settlement Status Checks in `checkTradeExpiry`

The checks for vault status and settlement status in `checkTradeExpiry` are too lenient, allowing for unauthorized state transitions. An exploitable scenario involves invoking `checkDCSTradeExpiry` on a vault that is already settled and in a Zombie state, thereby forcibly reviving the vault.

## DCSLogic.sol

```solidity
function checkTradeExpiry(
    CegaGlobalStorage storage cgs,
    IAddressManager addressManager,
    address vaultAddress
) internal onlyValidVault(cgs, vaultAddress) {
    Vault storage vault = cgs.vaults[vaultAddress];
    DCSVault storage dcsVault = cgs.dcsVaults[vaultAddress];
    DCSProduct storage dcsProduct = cgs.dcsProducts[vault.productId];
    require(
        dcsVault.settlementStatus != SettlementStatus.Defaulted,
        "Trade has defaulted already"
    );
    [...]
}
```

This ultimately results in an unintended inflation of the deposit assets during the execution of subsequent `settleDCSVault`, as a settled in-the-money vault would have its total assets denoted in units of swap assets.

## Proof of Concept

1. The attacker wins an auction and settles a vault, causing the vault to be in-the-money with a swap.
2. This changes `vault.totalAssets` to show swap assets instead of the deposit asset. Additionally, the vault’s status becomes Zombie.
3. The attacker executes `checkDCSTradeExpiry` on the vault, in the Zombie state. This changes the vault’s status to `TradeExpired` and `AwaitingSettlement`, effectively reviving it.
4. The attacker calls `settleDCSVault` on the revived vault.
5. This triggers an extra swap. However, it becomes an invalid operation since `totalAssets` are counted in swap assets, not deposit assets.
6. If the swap asset contains more decimal points or has a price larger than 1018, it may inflate the deposit assets and enable theft.

## Cega Audit 04 | Vulnerabilities

We evaluated the severity of this issue to be 'med' instead of 'high'. The consequences of a successful invalid state transition are identical to that of OS-CGA-ADV-00: repeated settlements on the same vault. However, it has a lower likelihood of success due to off-chain `traderAdmin` behavior. `traderAdmin` bots are programmed so that roll-overs occur after the default grace period, and thus calling `checkTradeExpiry` on a zombified vault will fail as its settlement state will be transitioned to `Defaulted` due to the intermediate invocation to `checkSettlementDefault`.

## Remediation

Implement proper checks in `checkDCSTradeExpiry` to ensure that the settlement status is either `InitialPremiumPaid` or `AwaitingSettlement` and the vault status is either `Traded` or `TradeExpired`.

## Patch

Fixed in ef85de1.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cega (Eth V2) |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: https://www.cega.fi/
- **GitHub**: https://github.com/cega-fi/cega-eth-v2
- **Contest**: https://www.cega.fi/

### Keywords for Search

`vulnerability`

