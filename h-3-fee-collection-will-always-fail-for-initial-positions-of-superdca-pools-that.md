---
# Core Classification
protocol: Super DCA Liquidity Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63421
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1171
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-super-dca-judging/issues/720

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
finders_count: 52
finders:
  - bughunter442
  - tobi0x18
  - natachi
  - Aamirusmani1552
  - 0x60scs
---

## Vulnerability Title

H-3: Fee collection will always fail for initial positions of SuperDCA pools that contain native tokens

### Overview


This bug report discusses an issue found by multiple users in the SuperDCA protocol, specifically related to the collection of trading fees from pools containing native tokens like ETH. The root cause of the problem is that the protocol treats all tokens as ERC20 tokens, including native tokens which are represented as `address(0)` in Uniswap v4. This causes the fee collection function to fail and the accumulated fees to become permanently locked in the pool. The impact of this bug is a significant loss of revenue for the protocol, especially for high-volume ETH-paired pools. The protocol team has already fixed the issue and implemented a solution in their code. 

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-super-dca-judging/issues/720 

## Found by 
0x60scs, 0xB4nkz, 0xBoraichoT, 0xleo, 0xzen, 4Nescient, Aamirusmani1552, Al-Qa-qa, BADROBINX, BengalCatBalu, Boy2000, Cryptor, DuoSec, Icon\_0x, IzuMan, JeRRy0422, JohnTPark24, JohnWeb3, Kirkeelee, Ollam, Orhukl, R, Razkky, SMB62, SuperDevFavour, alicrali33, bbl4de, bughunter442, deadmanwalking, drdee, farman1094, gneiss, holtzzx, jo13, kom, namx05, natachi, nonso72, oct0pwn, pindarev, shiazinho, shieldrey, silver\_eth, techOptimizor, tobi0x18, udo, vinica\_boy, vivekd, volleyking, wickie, y4y, yeahChibyke

## Summary
Uniswap v4 represents native tokens like ETH as `address(0)` internally ([ref](https://docs.uniswap.org/contracts/v4/reference/core/types/Currency?utm_source=chatgpt.com#address_zero) ). The protocol has stated that all uniswap v4 pools need to be supported, including ones that contain native ETH as SuperDCA counterparty. However, even though native token pools can be listed successfully, the fee collection logic for the initial locked LP position treats all tokens like ERC20s, making fee claims impossible for pools with native tokens.

### Root Cause
In `SuperDCAListing.sol:317-318` the fee collection logic assumes both pool currencies are ERC20 tokens and calls `IERC20(Currency.unwrap(token)).balanceOf()` to get the before and after balances to calculate fees, but Uniswap v4 represents native ETH as `address(0)` which will revert when treated as an ERC20. 

https://github.com/sherlock-audit/2025-09-super-dca/blob/main/super-dca-gauge/src/SuperDCAListing.sol#L304-L324

If either token0 or token1 is a native token like ETH, this will translate to  `IERC20(Currency.unwrap(address(0)).balanceOf(recipient);` which will fail, causing fees for the initial position to be permanently lost

### Internal Pre-conditions
1. Pool needs to be created and listed with native ETH paired with DCA token
2. Admin needs to attempt fee collection from ETH-paired position

### External Pre-conditions
1. None

### Attack Path
1. User creates DCA/ETH pool position and lists token through SuperDCAListing
2. Pool generates trading fees over time in both DCA tokens and ETH
3. Admin calls `collectFees()` to retrieve accumulated fees from position
4. Function attempts to call `IERC20(address(0)).balanceOf(recipient)` for ETH
5. Transaction reverts due to invalid function call on address(0)
6. Fees remain permanently locked in position, unable to be collected

### Impact
The protocol suffers permanent loss of accumulated trading fees for all ETH-paired pools, as the fee collection mechanism becomes completely non-functional for these positions.

ETH pairs are typically high-volume so the inability to collect fees from these positions represents a significant ongoing revenue loss for the protocol, especially if the initial position contains a large amount of liquidity.

### PoC
Skip

### Mitigation
Consider implementing native ETH detection and adjusting the before and after balance queries:
1. Check if `Currency.unwrap()` returns `address(0)` for ETH or native chain token
2. Use `recipient.balance` for ETH balance queries instead of ERC20 calls

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/Super-DCA-Tech/super-dca-gauge/pull/39






### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Super DCA Liquidity Network |
| Report Date | N/A |
| Finders | bughunter442, tobi0x18, natachi, Aamirusmani1552, 0x60scs, nonso72, SMB62, 0xzen, DuoSec, oct0pwn, silver\_eth, shieldrey, deadmanwalking, udo, wickie, 0xleo, namx05, gneiss, JohnWeb3, SuperDevFavour, Cryptor, jo13, kom, Orhukl, bbl4de, Boy2000, IzuMan, BengalCatBalu, alicrali33, vinica\_boy, Kirkeelee, y4y, vivekd, Ollam, BADROBINX, holtzzx, pindarev, JohnTPark24, farman1094, Al-Qa-qa, Icon\_0x, 0xB4nkz, 0xBoraichoT, volleyking, Razkky, shiazinho, drdee, 4Nescient, JeRRy0422, techOptimizor, yeahChibyke, R |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-super-dca-judging/issues/720
- **Contest**: https://app.sherlock.xyz/audits/contests/1171

### Keywords for Search

`vulnerability`

