---
# Core Classification
protocol: Footium
chain: everychain
category: uncategorized
vulnerability_type: erc721

# Attack Vector Details
attack_type: erc721
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18600
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/71
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-footium-judging/issues/289

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
  - erc721
  - erc20
  - approve

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - cergyk
  - Quantish
  - PokemonAuditSimulator
  - 0x52
  - J4de
---

## Vulnerability Title

H-1: Escrow approvals are not cleared when club is transferred allowing for abuse after transfer

### Overview


A bug was discovered in FootiumEscrow.sol that allows malicious club owners to abuse their club after it has been sold or transferred. The bug is that ERC20 and ERC721 token approval persist regardless of the owner of the club. This means that any approvals set by the original owner can be accessed after the club is sold or transferred. This allows the original owner to use the persistent approval to drain all players and tokens from the club after the sale.

This bug was discovered by 0x52, BenRai, Brenzee, CMierez, J4de, MiloTruck, PokemonAuditSimulator, Quantish, cergyk, ctf_sec, mstpr-brainbot, pengun, sashik_eth, shaka, shogoki, and toshii. The impact of this bug is that malicious approvals can be used to drain club after sale.

The code snippet that was used to find the bug can be found at FootiumEscrow.sol#L75-L81 and FootiumEscrow.sol#L90-L96. The bug was found using manual review. The recommendation is that the club escrow system needs to be redesigned.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-footium-judging/issues/289 

## Found by 
0x52, BenRai, Brenzee, CMierez, J4de, MiloTruck, PokemonAuditSimulator, Quantish, cergyk, ctf\_sec, mstpr-brainbot, pengun, sashik\_eth, shaka, shogoki, toshii
## Summary

Escrow approvals remain even across club token transfers. This allows a malicious club owners to sell their club then drain everything after sale due to previous approvals.

## Vulnerability Detail

ERC20 and ERC721 token approval persist regardless of the owner of the club. The result is that approvals set by one owner can be accessed after a token has been sold or transferred. This allows the following attack:

1) User A owns clubId = 1
2) User A sets approval to themselves
3) User A sells clubId = 1 to User B
4) User A uses persistent approval to drain all players and tokens

## Impact

Malicious approvals can be used to drain club after sale

## Code Snippet

[FootiumEscrow.sol#L75-L81](https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumEscrow.sol#L75-L81)

[FootiumEscrow.sol#L90-L96](https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumEscrow.sol#L90-L96)

## Tool used

Manual Review

## Recommendation

Club escrow system needs to be redesigned

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Footium |
| Report Date | N/A |
| Finders | cergyk, Quantish, PokemonAuditSimulator, 0x52, J4de, MiloTruck, sashik\_eth, CMierez, toshii, pengun, shogoki, shaka, Brenzee, mstpr-brainbot, BenRai, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-footium-judging/issues/289
- **Contest**: https://app.sherlock.xyz/audits/contests/71

### Keywords for Search

`ERC721, ERC20, Approve`

