---
# Core Classification
protocol: Urbit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19763
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/urbit/stardust/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/urbit/stardust/review.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

ERC-777 Related Reentrancy Considerations

### Overview

See description below for full details.

### Original Finding Content

## Description

The StarToken contract implements the ERC777 token standard using the related OpenZeppelin library. One of the most distinguishable features of the ERC777 standard compared to ERC20 is that if the token receiver is a contract, then the contract can implement the `ERC777Recipient` interface which defines the function `tokensReceived()`. This function is a hook that will be triggered every time the contract receives a token. To enable the hook trigger, the receiving contract must register itself to the ERC1820 contract registry.

This unique ERC777 feature can be weaponized to trigger a reentrancy condition. To be successful, this attack would require the victim contract to be affected by a security flaw as the result of not abiding by the recommended Checks-Effects-Interactions pattern.

This reentrancy condition can allow attackers to use two stars to switch for any other star in the list (see this relevant issue). Say we have `assets = [a, b, c]` and we have a balance of `2e18 StarTokens`. The standard `redeem()` workflow would normally only allow us to redeem the Star `c`. However, consider the following:

1. **redeem() (1)**:
   - `pop(c) -> assets = [a, b]`
   - `ownerBurn(1e18)` - reenter on `tokensToSend()` before we’ve burnt our balance of `2e18`
   
2. **redeem() (2)**:
   - `pop(b) -> assets = [a]`
   - `ownerBurn(1e18)` - reenter on `tokensToSend()` before we’ve burnt our balance of `2e18`
   
3. **redeem() (3)**:
   - `pop(a) -> assets = []`
   - `ownerBurn(1e18) -> balance = 1e18`
   - `transferPoint(a, attacker)`
   
4. **continue redeem(2)**:
   - `ownerBurn(1e18) -> balance = 0`
   - `transferPoint(b, attacker)`
   
5. **deposit(b)**:
   - `transferPoint(b, treasury)`
   - `push(b) -> assets =[b]`
   - `mint(1e18, attacker) -> balance = 1e18`
   
6. **continue redeem(3)**:
   - `ownerBurn(1e18) -> balance = 0`
   - `transferPoint(c, attacker)`
   
7. **deposit(c)**:
   - `transferPoint(c, treasury)`
   - `push(c) -> assets = [b, c]`
   - `mint(1e18, attacker) -> balance = 1e18`

The attacker managed to own star `a` and only spend `1e18` for it, bypassing the LIFO ("Last In First Out") queue. The testing team could not identify an exploitable attack vector for reentrancy on the Treasury contract. However, the testing team notes that the ERC777 and ERC1820 contracts were not included in the scope of this review. As a result, the testing team cannot express any opinions related to the security posture of these contracts.

## Recommendations

ERC777 token contracts do significantly increase the attack surface available to malicious users, compared to simpler ERC20 token contracts. Consider whether the added complexity is worth the extra features provided.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Urbit |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/urbit/stardust/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/urbit/stardust/review.pdf

### Keywords for Search

`vulnerability`

