---
# Core Classification
protocol: Florence Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20565
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-04-01-Florence Finance.md
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
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[H-01] Stakers/vault depositors can be front-run and lose their funds

### Overview


This bug report is about a potential vulnerability in the `FlorinStaking` contract. The vulnerability works when an attacker front-runs a user's transaction, depositing a small amount of tokens and then transferring a large amount of tokens to the contract. This causes the user's transaction to be calculated to mint 0 shares, allowing the attacker to withdraw the user's deposit plus their own deposit. This vulnerability has been fixed in the UniswapV2 protocol by minting the first 1000 shares to the zero-address and requiring that the minted shares are not 0. Implementing these two protections will resolve the vulnerability. This bug has a high impact as it can result in a theft of user assets, and a medium likelihood as it only works if the attacker is the first staker.

### Original Finding Content

**Impact:**
High, as it results in a theft of user assets

**Likelihood:**
Medium, as it works only if the attacker is the first staker

**Description**

Let's look at the following example:

1. The `FlorinStaking` contract has been deployed, unpaused and has 0 staked $FLR in it
2. Alice sends a transaction calling the `stake` method with `florinTokens == 10e18`
3. Bob is a malicious user/bot and sees the transaction in the mempool and front-runs it by depositing 1 wei of $FLR, receiving 1 wei of shares
4. Bob also front-runs Alice's transaction with a direct `ERC20::transfer` of 10e18 $FLR to the `FlorinStaking` contract
5. Now in Alice's transaction, the code calculates Alice's shares as `shares = florinTokens.mulDiv(totalShares_, getTotalStakedFlorinTokens(), MathUpgradeable.Rounding.Down);`, where `getTotalStakedFlorinTokens` returns `florinToken.balanceOf(address(this))`, so now `shares` rounds down to 0
6. Alice gets minted 0 shares, even though she deposited 10e18 worth of $FLR
7. Now Bob back-runs Alice's transaction with a call to `unstake` where `requestedFlorinTokens` is the contract's balance of $FLR, allowing him to burn his 1 share and withdraw his deposit + Alice's whole deposit

This can be replayed multiple times until the depositors notice the problem.

**Note:** This absolute same problem is present with the ERC4626 logic in `LoanVault`, as it is a common vulnerability related to vault shares calculations. OpenZeppelin has introduced a way for mitigation in version 4.8.0 which is the used version by this protocol.

**Recommendations**

UniswapV2 fixed this with two types of protection:

[First](https://github.com/Uniswap/v2-core/blob/master/contracts/UniswapV2Pair.sol#L119-L121), on the first `mint` it actually mints the first 1000 shares to the zero-address

[Second](https://github.com/Uniswap/v2-core/blob/ee547b17853e71ed4e0101ccfd52e70d5acded58/contracts/UniswapV2Pair.sol#L125), it requires that the minted shares are not 0

Implementing them both will resolve this vulnerability.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Florence Finance |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-04-01-Florence Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

