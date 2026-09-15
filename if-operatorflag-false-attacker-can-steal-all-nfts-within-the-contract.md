---
# Core Classification
protocol: Mellow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40578
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10
source_link: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
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
finders_count: 4
finders:
  - Kaden
  - Saw-mon and Natalie
  - deadrosesxyz
  - Akshay Srivastav
---

## Vulnerability Title

If operatorFlag == false , attacker can steal all NFTs within the contract. 

### Overview


This bug report describes a vulnerability in the Core.sol contract, where an attacker can manipulate the rebalancing process to steal a victim's position. The attacker first creates a custom token and a pool with it, then deposits both in the Core.sol contract. By manipulating the order of rebalancing and using a callback function, the attacker is able to accrue fees and steal the victim's position. The recommendation is to add security measures and prevent empty callback parameters. This bug has been fixed in the latest commit. The risk level is high.

### Original Finding Content

## Attack Overview on ERC777-like Token

### Context:
Core.sol#L169

### Description:
For the attack, the attacker will need to first deploy an ERC777-like custom token and then a Velodrome pool with it. Let's say the victim's position is in WETH/USDC and the victim's position id is 1.

1. **Attacker creates an NFT** for their own ERC777/WETH token pool (id 2) and also a dust position in the USDC/WETH pool (id 3).
2. **Attacker deposits both NFTs** in Core.sol.
3. **Attacker rebalances the 3 positions**, inputting them in the following order: Victim's USDC/WETH (id 1), ERC777/WETH (id 2), Attacker's USDC/WETH (id 3).
4. **Upon callback completion**, the user makes a swap within their own ERC777/WETH pool, allowing some fees to be accrued.
5. **User increases the liquidity** of id 3 enough so that there’s sufficient liquidity to bypass the minLiquidity check of id 1.
6. **The first position is the victim's**. The returned id to be rebalanced with will be id 3 (the attacker's USDC/WETH position).
7. **Then the position in the ERC777/WETH pool will be rebalanced**. Upon transferring it, any accrued fees will be sent to the callback. It is important to note that some fees were purposefully accrued, allowing the attacker to 'steal' the transaction in their ERC777 hook.
8. **Having stolen the transaction**, the attacker calls withdraw on their position (id 3). The rebalancing process has not yet finished, and it believes id 3 still belongs to the attacker.
9. **Rebalancing continues**.
10. **The attacker deposits a dust position** to rebalance their USDC/WETH position.

In the end, the attacker has stolen the victim's position, which is tied to an NFT that is not within the contract or within the Gauge.

### Recommendation:
Keep the operator flag up, add the `nonReentrant` modifier to the withdraw function, and do not allow for empty callbackParams.

### Mellow:
Fixed in commit `736eef90`.

### Cantina:
Fixed in commit `736eef90`. The contract now has `nonReentrant` modifiers and does not allow for empty callback parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Mellow |
| Report Date | N/A |
| Finders | Kaden, Saw-mon and Natalie, deadrosesxyz, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_mellow_apr2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/72dfcce6-8b1b-4f5d-b5a7-657a40507b10

### Keywords for Search

`vulnerability`

