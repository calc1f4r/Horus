---
# Core Classification
protocol: Cally
chain: everychain
category: uncategorized
vulnerability_type: weird_erc20

# Attack Vector Details
attack_type: weird_erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2297
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-cally-contest
source_link: https://code4rena.com/reports/2022-05-cally
github_link: https://github.com/code-423n4/2022-05-cally-findings/issues/61

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
  - weird_erc20
  - fee_on_transfer

protocol_categories:
  - dexes
  - services
  - synthetics
  - liquidity_manager
  - options_vault

# Audit Details
report_date: unknown
finders_count: 25
finders:
  - 0x52
  - berndartmueller
  - hubble
  - smilingheretic
  - MiloTruck
---

## Vulnerability Title

[M-08] Vault is Not Compatible with Fee Tokens and Vaults with Such Tokens Could Be Exploited

### Overview


This bug report concerns the "Cally" contract, which is a part of a GitHub repository. It explains how the contract can be exploited if ERC20 tokens that charge a transaction fee are used in the "createVault()" function. The exploit allows an attacker to use the contract as a conduit to generate fee income, resulting in a loss of user funds and a loss of value from the contract. 

To exploit this vulnerability, an attacker would observe when a vault is created that contains such fee tokens, then create a new vault that contains the same token and withdraw the same amount. This causes the contract to pay the transfer fee for the attacker.

The recommended mitigation steps are to disallow fee tokens from being used in the vault. This can be done by adding a "require()" statement to check that the amount increase of the token balance in the "Cally" contract is equal to the amount being sent by the caller of the "createVault()" function.

### Original Finding Content

_Submitted by 0x1337, also found by 0x52, 0xDjango, 0xsanson, berndartmueller, BondiPestControl, BowTiedWardens, cccz, dipp, GimelSec, hake, hickuphh3, horsefacts, hubble, IllIllI, MaratCerby, MiloTruck, minhquanym, PPrieditis, reassor, shenwilly, smiling_heretic, TrungOre, VAD37, and WatchPug_

<https://github.com/code-423n4/2022-05-cally/blob/1849f9ee12434038aa80753266ce6a2f2b082c59/contracts/src/Cally.sol#L198-L200>

<https://github.com/code-423n4/2022-05-cally/blob/1849f9ee12434038aa80753266ce6a2f2b082c59/contracts/src/Cally.sol#L294-L296>

<https://github.com/code-423n4/2022-05-cally/blob/1849f9ee12434038aa80753266ce6a2f2b082c59/contracts/src/Cally.sol#L343-L345>

### Impact

Some ERC20 tokens charge a transaction fee for every transfer (used to encourage staking, add to liquidity pool, pay a fee to contract owner, etc.). If any such token is used in the `createVault()` function, either the token cannot be withdrawn from the contract (due to insufficient token balance), or it could be exploited by other such token holders and the `Cally` contract would lose economic value and some users would be unable to withdraw the underlying asset.

### Proof of Concept

Plenty of ERC20 tokens charge a fee for every transfer (e.g. Safemoon and its forks), in which the amount of token received is less than the amount being sent. When a fee token is used as the `token` in the `createVault()` function, the amount received by the contract would be less than the amount being sent. To be more precise, the increase in the `cally` contract token balance would be less than `vault.tokenIdOrAmount` for such ERC20 token because of the fee.

            vault.tokenType == TokenType.ERC721
                ? ERC721(vault.token).transferFrom(msg.sender, address(this), vault.tokenIdOrAmount)
                : ERC20(vault.token).safeTransferFrom(msg.sender, address(this), vault.tokenIdOrAmount);

The implication is that both the `exercise()` function and the `withdraw()` function are guaranteed to revert if there's no other vault in the contract that contains the same fee tokens, due to insufficient token balance in the `Cally` contract.

When an attacker observes that a vault is being created that contains such fee tokens, the attacker could create a new vault himself that contains the same token, and then withdraw the same amount. Essentially the `Cally` contract would be paying the transfer fee for the attacker because of how the token amount is recorded. This causes loss of user fund and loss of value from the `Cally` contract. It would make economic sense for the attacker when the fee charged by the token accrue to the attacker. The attacker would essentially use the `Cally` contract as a conduit to generate fee income.

### Recommended Mitigation Steps

Recommend disallowing fee tokens from being used in the vault. This can be done by adding a `require()` statement to check that the amount increase of the `token` balance in the `Cally` contract is equal to the amount being sent by the caller of the `createVault()` function.


**[outdoteth (Cally) confirmed and commented](https://github.com/code-423n4/2022-05-cally-findings/issues/61#issuecomment-1126980897):**
 > reference issue: https://github.com/code-423n4/2022-05-cally-findings/issues/39

**[HardlyDifficult (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-cally-findings/issues/61#issuecomment-1135276611):**
 > This is a good description of the potential issue when a fee on transfer token is used.
> 
> Lowing to 2 (Medium). See https://github.com/code-423n4/org/issues/3 for some discussion on how to consider the severity for these types of issues.
> 
> The attack described does leak value, but the vault could be recovered by transferring in the delta balance so that the contract has more than enough funds in order to exercise or withdraw. That plus these types of tokens are relatively rare is why I don't think this warrants a High severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Cally |
| Report Date | N/A |
| Finders | 0x52, berndartmueller, hubble, smilingheretic, MiloTruck, BowTiedWardens, minhquanym, 0xDjango, BondiPestControl, PPrieditis, VAD37, IllIllI, reassor, 0xsanson, cccz, hickuphh3, 0x1337, horsefacts, hake, TrungOre, WatchPug_, MaratCerby, shenwilly, dipp, GimelSec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-cally
- **GitHub**: https://github.com/code-423n4/2022-05-cally-findings/issues/61
- **Contest**: https://code4rena.com/contests/2022-05-cally-contest

### Keywords for Search

`Weird ERC20, Fee On Transfer`

