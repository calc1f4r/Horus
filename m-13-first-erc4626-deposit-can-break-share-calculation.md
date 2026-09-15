---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3688
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/143

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - pashov
  - 0xNazgul
  - Jeiwan
  - joestakey
  - neila
---

## Vulnerability Title

M-13: First ERC4626 deposit can break share calculation

### Overview


This bug report is about the issue M-13, which was found by eight people and is related to ERC4626 vault. It states that the first depositor of an ERC4626 vault can maliciously manipulate the share price by depositing the lowest possible amount (1 wei) of liquidity and then artificially inflating ERC4626.totalAssets. This can lead to the share price becoming very high and, due to rounding down, the next depositor losing their deposited funds. The code snippet provided shows that the shares are calculated as follows: `return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());`. The tool used for this bug was Manual Review and the recommendation is to mint a fixed amount of shares for the first deposit, e.g. 10**decimals().

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/143 

## Found by 
pashov, ctf\_sec, neila, rvierdiiev, \_\_141345\_\_, ak1, 0xNazgul, Jeiwan, joestakey

## Summary
The first depositor of an ERC4626 vault can maliciously manipulate the share price by depositing the lowest possible amount (1 wei) of liquidity and then artificially inflating ERC4626.totalAssets.

This can inflate the base share price as high as 1:1e18 early on, which force all subsequence deposit to use this share price as a base and worst case, due to rounding down, if this malicious initial deposit front-run someone else depositing, this depositor will receive 0 shares and lost his deposited assets.

## Vulnerability Detail
Given a vault with DAI as the underlying asset:

Alice (attacker) deposits initial liquidity of 1 wei DAI via `deposit()`
Alice receives 1e18 (1 wei) vault shares
Alice transfers 1 ether of DAI via transfer() to the vault to artificially inflate the asset balance without minting new shares. The asset balance is now 1 ether + 1 wei DAI -> vault share price is now very high (= 1000000000000000000001 wei ~ 1000 * 1e18)
Bob (victim) deposits 100 ether DAI
Bob receives 0 shares
Bob receives 0 shares due to a precision issue. His deposited funds are lost.

The shares are calculated as following 
`return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());`
In case of a very high share price, due to totalAssets() > assets * supply, shares will be 0.
## Impact
`ERC4626` vault share price can be maliciously inflated on the initial deposit, leading to the next depositor losing assets due to precision issues.
## Code Snippet
https://github.com/sherlock-audit/2022-10-astaria/blob/main/lib/astaria-gpl/src/ERC4626-Cloned.sol#L392
## Tool used

Manual Review

## Recommendation
This is a well-known issue, Uniswap and other protocols had similar issues when supply == 0.

For the first deposit, mint a fixed amount of shares, e.g. 10**decimals()
```jsx
if (supply == 0) {
    return 10**decimals; 
} else {
    return assets.mulDivDown(supply, totalAssets());
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | pashov, 0xNazgul, Jeiwan, joestakey, neila, \_\_141345\_\_, ak1, rvierdiiev, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/143
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

