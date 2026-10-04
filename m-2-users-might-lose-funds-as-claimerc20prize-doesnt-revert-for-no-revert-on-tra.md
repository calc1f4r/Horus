---
# Core Classification
protocol: Footium
chain: everychain
category: uncategorized
vulnerability_type: safetransfer

# Attack Vector Details
attack_type: safetransfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18603
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/71
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-footium-judging/issues/86

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
  - safetransfer
  - weird_erc20

# Audit Details
report_date: unknown
finders_count: 74
finders:
  - 0xStalin
  - Quantish
  - jprod15
  - josephdara
  - J4de
---

## Vulnerability Title

M-2: Users might lose funds as `claimERC20Prize()` doesn't revert for no-revert-on-transfer tokens

### Overview


This bug report is about an issue found in the FootiumPrizeDistributor contract. The `claimERC20Prize()` function allows whitelisted users to claim ERC20 tokens. However, if a no-revert-on-failure token is used, the function does not revert when the token transfer fails, causing a portion of the user's claimable tokens to become unclaimable and resulting in a loss of funds. This issue was found by a group of auditors using manual review. The recommended solution is to use `safeTransfer()` from Openzeppelin's SafeERC20 to transfer ERC20 tokens.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-footium-judging/issues/86 

## Found by 
0xAsen, 0xGoodess, 0xGusMcCrae, 0xPkhatri, 0xRobocop, 0xStalin, 0xeix, 0xmuxyz, 0xnirlin, 14si2o\_Flint, 8olidity, ACai7, AlexCzm, BAHOZ, Bauchibred, Bauer, Cryptor, DevABDee, Diana, GimelSec, J4de, Koolex, MiloTruck, PRAISE, PTolev, Phantasmagoria, Piyushshukla, PokemonAuditSimulator, Polaris\_tow, Proxy, Quantish, R-Nemes, SanketKogekar, Sulpiride, TheNaubit, Tricko, \_\_141345\_\_, abiih, alliums8520, ast3ros, berlin-101, cergyk, ctf\_sec, cuthalion0x, dacian, ddimitrov22, deadrxsezzz, djxploit, favelanky, georgits, holyhansss, innertia, jasonxiale, josephdara, jprod15, kiki\_dev, l3r0ux, lewisbroadhurst, nzm\_, oot2k, oualidpro, peanuts, ravikiran.web3, sach1r0, santipu\_, sashik\_eth, shaka, shame, thekmj, tibthecat, tsvetanovv, whoismatthewmc1, wzrdk3lly, yy
## Summary

Users can call `claimERC20Prize()` without actually receiving tokens if a no-revert-on-failure token is used, causing a portion of their claimable tokens to become unclaimable.

## Vulnerability Detail

In the `FootiumPrizeDistributor` contract, whitelisted users can call `claimERC20Prize()` to claim ERC20 tokens. The function adds the amount of tokens claimed to the user's total claim amount, and then transfers the tokens to the user:

[FootiumPrizeDistributor.sol#L128-L131](https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumPrizeDistributor.sol#L128-L131)

```solidity
if (value > 0) {
    totalERC20Claimed[_token][_to] += value;
    _token.transfer(_to, value);
}
```

As the the return value from `transfer()` is not checked, `claimERC20Prize()` does not revert even when the transfer of tokens to the user fails.

This could potentially cause users to lose assets when:
1. `_token` is a no-revert-on-failure token.
2. The user calls `claimERC20Prize()` with `value` higher than the contract's token balance.

As the contract has an insufficient balance, `transfer()` will revert and the user receives no tokens. However, as `claimERC20Prize()` succeeds, `totalERC20Claimed` is permanently increased for the user, thus the user cannot claim these tokens again.

## Impact

Users can call `claimERC20Prize()` without receiving the token amount specified. These tokens become permanently unclaimable for the user, leading to a loss of funds.

## Code Snippet

https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumPrizeDistributor.sol#L128-L131

## Tool used

Manual Review

## Recommendation

Use `safeTransfer()` from Openzeppelin's [SafeERC20](https://docs.openzeppelin.com/contracts/2.x/api/token/erc20#SafeERC20) to transfer ERC20 tokens. Note that [`transferERC20()`](https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumEscrow.sol#L105-L111) in `FootiumEscrow.sol` also uses `transfer()` and is susceptible to the same vulnerability.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Footium |
| Report Date | N/A |
| Finders | 0xStalin, Quantish, jprod15, josephdara, J4de, 0xGoodess, 0xnirlin, jasonxiale, innertia, ddimitrov22, sashik\_eth, 0xPkhatri, TheNaubit, santipu\_, alliums8520, 0xAsen, tsvetanovv, dacian, shame, shaka, kiki\_dev, 0xeix, djxploit, peanuts, oualidpro, Phantasmagoria, wzrdk3lly, favelanky, ctf\_sec, Cryptor, MiloTruck, nzm\_, abiih, R-Nemes, PRAISE, Sulpiride, 0xmuxyz, deadrxsezzz, tibthecat, ast3ros, georgits, Bauer, Koolex, Diana, Tricko, 0xRobocop, DevABDee, Bauchibred, cuthalion0x, cergyk, 8olidity, PokemonAuditSimulator, lewisbroadhurst, SanketKogekar, Proxy, PTolev, whoismatthewmc1, ACai7, berlin-101, BAHOZ, ravikiran.web3, 14si2o\_Flint, 0xGusMcCrae, holyhansss, l3r0ux, Piyushshukla, \_\_141345\_\_, thekmj, sach1r0, oot2k, AlexCzm, GimelSec, yy, Polaris\_tow |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-footium-judging/issues/86
- **Contest**: https://app.sherlock.xyz/audits/contests/71

### Keywords for Search

`SafeTransfer, Weird ERC20`

