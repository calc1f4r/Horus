---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24714
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-paladin
source_link: https://code4rena.com/reports/2022-03-paladin
github_link: https://github.com/code-423n4/2022-03-paladin-findings/issues/77

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-02] System could be wrapped and made useless without contract whitelisting

### Overview


This bug report was submitted by Picodes and it involves three lines of code from the HolyPaladinToken.sol file. It is possible to create a contract or a contract factory, known as a PAL Locker, which allows users to deposit PAL tokens and lock them. This would make the tokens liquid and transferrable again, which would go against the idea of locking tokens to make them non-liquid and to receive a boosted voting power and reward rate. This behavior has been seen in the past with veToken models. 

To make locked hPAL liquid, Alice could create a contact C. Then, she can deposit hPAL through the contract, lock them and delegate voting power to herself. She can then sell or tokenize the ownership of the contract C.

To prevent this behavior, it is recommended that Paladin implements a whitelisting/blacklisting system for contracts, similar to the veCRV & veANGLE. The checker should only block for Locking, allowing smart contracts to stake and use the basic version of hPAL without locking. Kogaroshi (Paladin) confirmed, resolved, and commented that changes were made to use a Whitelist and the changes can be found in the PaladinFinance/Paladin-Tokenomics#12 pull request.

### Original Finding Content

_Submitted by Picodes_

[HolyPaladinToken.sol#L253](https://github.com/code-423n4/2022-03-paladin/blob/9c26ec8556298fb1dc3cf71f471aadad3a5c74a0/contracts/HolyPaladinToken.sol#L253)<br>
[HolyPaladinToken.sol#L284](https://github.com/code-423n4/2022-03-paladin/blob/9c26ec8556298fb1dc3cf71f471aadad3a5c74a0/contracts/HolyPaladinToken.sol#L284)<br>
[HolyPaladinToken.sol#L268](https://github.com/code-423n4/2022-03-paladin/blob/9c26ec8556298fb1dc3cf71f471aadad3a5c74a0/contracts/HolyPaladinToken.sol#L268)<br>

Anyone could create a contract or a contract factory "PAL Locker" with a fonction to deposit PAL tokens through a contract, lock them and delegate the voting power to the contract owner. Then, the ownership of this contract could be sold. By doing so, locked hPAL would be made liquid and transferrable again. This would eventually break the overall system of hPAL, where the idea is that you have to lock them to make them non liquid to get a boosted voting power and reward rate.

Paladin should expect this behavior to happen as we've seen it happening with veToken models and model implying locking features (see <https://lockers.stakedao.org/> and <https://www.convexfinance.com/>).

This behavior could eventually be beneficial to the original DAO (ex. <https://www.convexfinance.com/> for Curve and Frax), but the original DAO needs to at least be able to blacklist / whitelist such contracts and actors to ensure their interests are aligned with the protocol.

### Proof of Concept

To make locked hPAL liquid, Alice could create a contact C. Then, she can deposit hPAL through the contract, lock them and delegate voting power to herself. She can then sell or tokenize the ownership of the contract C.

### Recommended Mitigation Steps

Depending on if Paladin wants to be optimistic or pessimistic, implement a whitelisting / blacklisting system for contracts.

See:
[Curve-Dao-Contracts/VotingEscrow.vy#L185](https://github.com/curvefi/curve-dao-contracts/blob/4e428823c8ae9c0f8a669d796006fade11edb141/contracts/VotingEscrow.vy#L185)<br>

[FraxFinance/veFXS_Solidity.sol.old#L370](https://github.com/FraxFinance/frax-solidity/blob/7375949a73042c1e6dd14848fc4ea1ba62e36fb5/src/hardhat/contracts/FXS/veFXS_Solidity.sol.old#L370)<br>

**[Kogaroshi (Paladin) confirmed, resolved, and commented](https://github.com/code-423n4/2022-03-paladin-findings/issues/77#issuecomment-1087503108):**
 > Changes were made to use a Whitelist similar to the veCRV & veANGLE (changes in this PR: [PaladinFinance/Paladin-Tokenomics#12](https://github.com/PaladinFinance/Paladin-Tokenomics/pull/12)).<br>
> The checker will only block for Locking, allowing smart contracts to stake and use the basic version of hPAL without locking.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-paladin
- **GitHub**: https://github.com/code-423n4/2022-03-paladin-findings/issues/77
- **Contest**: https://code4rena.com/reports/2022-03-paladin

### Keywords for Search

`vulnerability`

