---
# Core Classification
protocol: Dyad
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18762
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-02-12-Dyad.md
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
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zach Obront
---

## Vulnerability Title

[H-02] Can steal all dNFTs and funds from contract by flash loaning deposits & liquidations

### Overview


This bug report describes an exploit in the liquidation process of a dNFT. When liquidate() is called, it requires that the current shares of the dNFT ID must be less than 0.1% of the total shares in the pool and the shares after liquidator’s funds are deposited must be greater than 0.1% of the total shares in the pool. This can be exploited to steal any dNFT by depositing sufficient ETH to move the pool to greater than 1000x a given depositor, liquidating them and adding a small balance to push them over 0.1% of the pool, and withdrawing the initial deposit. The exploit is demonstrated with a proof of concept code.

The recommendation is to rethink the logic of the liquidation process. This attack can be prevented by only liquidating if withdrawals exceed the collateralization ratio. This has been implemented in the fix for H-02.

### Original Finding Content

When liquidate() is called for a given dNFT ID, there are two requirements:

- The current shares of that ID must be less than 0.1% of the total shares in the pool
- The shares after the liquidator's funds are deposited must by greater than 0.1% of the total shares in the pool

This can be exploited to steal any dNFT by depositing sufficient ETH to move the pool to greater than 1000x a given depositor, liquidating them and adding a small balance to push them over 0.1% of the pool, and withdrawing the initial deposit.

By sorting all dNFTs from lowest balance to highest, an attacker could perform this attack in such a way as to liquidate every dNFT, assuming sufficient funds (which would be easy to secure via Flash Loans).

Because internal balances are held by the dNFT rather than the user, this would also have the effect of moving the entire value of the vault to the attacker.

**Proof of Concept**

```solidity
function test_CanLiquidateAnyone() public {
address attacker = makeAddr("attacker");
vm.deal(attacker, 6000 ether);
address victim = makeAddr("victim");
vm.deal(victim, 1000 ether);

vm.prank(attacker);
uint id1 = dNft.mint{value: 5 ether}(attacker);

vm.prank(victim);
uint id2 = dNft.mint{value: 5 ether}(victim);

vm.startPrank(attacker);
dNft.deposit{value: 5000 ether}(id1);
dNft.liquidate{value: 1 ether}(id2, attacker);
dNft.redeemDeposit(id1, attacker, 5000 ether);

assertEq(dNft.ownerOf(id2), attacker);
}
```

**Recommendation**
The logic of the liquidation process needs to be rethought. Besides this possible attack, it seems that liquidating users when their shares fall below 0.1% of the total is likely to lead to unexpected dynamics and doesn't accomplish the goal of keeping the protocol solvent.

**Review**

The new liquidation mechanism (see fix for H-02) only liquidates if withdrawals exceed collateralization ratio, so this attack is no longer possible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Dyad |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-02-12-Dyad.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

