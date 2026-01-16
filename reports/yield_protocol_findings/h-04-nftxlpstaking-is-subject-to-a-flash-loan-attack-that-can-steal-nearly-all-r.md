---
# Core Classification
protocol: NFTX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42183
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-05-nftx
source_link: https://code4rena.com/reports/2021-05-nftx
github_link: https://github.com/code-423n4/2021-05-nftx-findings/issues/88

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
  - dexes
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-04] `NFTXLPStaking` Is Subject To A Flash Loan Attack That Can Steal Nearly All Rewards/Fees That Have Accrued For A Particular Vault

### Overview


The LPStaking contract allows users to stake their tokens and claim rewards, but it does not require staked tokens to be locked for a period of time. This means that an attacker can stake, claim rewards, and unstake all in one transaction, leaving little rewards for legitimate stakers. This can be made easier by using a flash loan, which can be obtained through the NFTXVaultUpgradeable contract. This allows the attacker to stake a large amount of tokens and claim most of the rewards, leaving little for others. To fix this, it is recommended to require staked tokens to be locked for a certain period of time before they can be removed, or to only allow rewards to be claimed for tokens that have been staked for a certain period of time.

### Original Finding Content


The LPStaking contract does not require that a stake be locked for any period of time. The LPStaking contract also does not track how long your stake has been locked. So an attacker Alice can stake, claim rewards, and unstake, all in one transaction. If Alice utilizes a flash loan, then she can claim nearly all of the rewards for herself, leaving very little left for the legitimate stakers.

The fact that the `NFTXVaultUpgradeable` contract contains a native `flashLoan` function makes this attack that much easier, although it would still be possible even without that due to flashloans on Uniswap, or wherever else the nftX token is found.

Since a flash loan will easily dwarf all of the legitimate stakers' size of stake, the contract will erroneously award nearly all of the rewards to Alice.

1.  Wait until an NFTX vault has accrued any significant amount of fees/rewards
2.  `FlashLoanBorrow` a lot of ETH using any generic flash loan provider
3.  `FlashLoanBorrow` a lot of nftx-vault-token using `NFTXVaultUpgradeable.flashLoan()`
4.  Deposit the ETH and nftx-vault-token's into Uniswap for Uniswap LP tokens by calling `Uniswap.addLiquidity()`
5.  Stake the Uniswap LP tokens in `NFTXLPStaking` by calling `NFTXLPStaking.deposit()`
6.  Claim nearly all of the rewards that have accrued for this vault due to how large the flashLoaned deposit is relative to all of the legitimate stakes by calling `NFTXLPStaking.claimRewards()`
7.  Remove LP tokens from `NFTXLPStaking` by calling `NFTXLPStaking.exit()`;
8.  Withdraw ETH and nftx-vault-token's by calling `Uniswap.removeLiquidity()`;
9.  Pay back nftx-vault-token flash loan
10. Pay back ETH flash loan

See [GitHub issue page](https://github.com/code-423n4/2021-05-nftx-findings/issues/88) for an in-depth  example.

Recommend requiring that staked LP tokens be staked for a particular period of time before they can be removed. Although a very short time frame (a few blocks) would avoid flash loan attacks, this attack could still be performed over the course of a few blocks less efficiently. Ideally, you would want the rewards to reflect the product of the amount staked and the duration that they've been staked, as well as having a minimum time staked.

Alternatively, if you really want to allow people to have the ability to remove their stake immediately, then only allow rewards to be claimed for stakes that have been staked for a certain period of time. Users would still be able to remove their LP tokens, but they could no longer siphon off rewards immediately.

**[0xKiwi (NFTX) disputed](https://github.com/code-423n4/2021-05-nftx-findings/issues/88#issuecomment-845695223):**
 > After looking at the code, this is not possible. The dividend token code takes into consideration the current unclaimed rewards and when a deposit is made that value is deducted.

**[cemozer (Judge) commented](https://github.com/code-423n4/2021-05-nftx-findings/issues/88#issuecomment-848325710):**
 > @0xKiwi do you mind showing where in code that occurs?



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-nftx
- **GitHub**: https://github.com/code-423n4/2021-05-nftx-findings/issues/88
- **Contest**: https://code4rena.com/reports/2021-05-nftx

### Keywords for Search

`vulnerability`

