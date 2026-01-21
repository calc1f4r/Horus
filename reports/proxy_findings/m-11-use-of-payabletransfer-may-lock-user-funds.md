---
# Core Classification
protocol: Fractional
chain: everychain
category: uncategorized
vulnerability_type: call_vs_transfer

# Attack Vector Details
attack_type: call_vs_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3012
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/504

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.40
financial_impact: medium

# Scoring
quality_score: 2
rarity_score: 1

# Context Tags
tags:
  - call_vs_transfer

protocol_categories:
  - dexes
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 33
finders:
  - codexploder
  - scaraven
  - xiaoming90
  - cryptphi
  - 0x29A
---

## Vulnerability Title

[M-11] Use of `payable.transfer()` may lock user funds

### Overview


This bug report is about a vulnerability in the code of a contract written in Solidity, which is a programming language used to write smart contracts on the Ethereum blockchain. The vulnerability is caused by the use of the `payable.transfer()` function, which can lead to the locking of funds. This is because the function requires that the recipient has a `payable` callback, and only provides 2300 gas for its operation. If the recipient does not have a `payable` callback, or the contract's `payable` callback spends more than 2300 gas, then the transfer will fail and the funds will be locked. This vulnerability has a medium severity, as it can lead to the loss of funds.

To mitigate this vulnerability, the bug reporter recommends using `address.call{value:x}()` instead of `payable.transfer()`. The bug reporter used code inspection to identify the vulnerability.

### Original Finding Content

_Submitted by IllIllI, also found by 0x1f8b, 0x29A, Amithuddar, Avci, bardamu, BowTiedWardens, c3phas, cccz, codexploder, cryptphi, hake, horsefacts, hyh, Kthere, Limbooo, MEP, oyc&#95;109, pashov, peritoflores, Ruhum, scaraven, simon135, slywaters, sseefried, StyxRave, tofunmi, TomJ, Treasure-Seeker, TrungOre, Tutturu, Waze, and xiaoming90_

<https://github.com/code-423n4/2022-07-fractional/blob/e2c5a962a94106f9495eb96769d7f60f7d5b14c9/src/modules/Migration.sol#L172>

<https://github.com/code-423n4/2022-07-fractional/blob/e2c5a962a94106f9495eb96769d7f60f7d5b14c9/src/modules/Migration.sol#L325>

### Impact

The use of `payable.transfer()` is heavily frowned upon because it can lead to the locking of funds. The `transfer()` call requires that the recipient has a `payable` callback, only provides 2300 gas for its operation. This means the following cases can cause the transfer to fail:

*   The contract does not have a `payable` callback
*   The contract's `payable` callback spends more than 2300 gas (which is only enough to emit something)
*   The contract is called through a proxy which itself uses up the 2300 gas

If a user falls into one of the above categories, they'll be unable to receive funds from the vault in a migration wrapper. Inaccessible funds means loss of funds, which is Medium severity.

### Proof of Concept

Both `leave()`:

```solidity
File: src/modules/Migration.sol   #1

159           uint256 ethAmount = userProposalEth[_proposalId][msg.sender];
160           proposal.totalEth -= ethAmount;
161           userProposalEth[_proposalId][msg.sender] = 0;
162   
163           // Withdraws fractions from contract back to caller
164           IFERC1155(token).safeTransferFrom(
165               address(this),
166               msg.sender,
167               id,
168               amount,
169               ""
170           );
171           // Withdraws ether from contract back to caller
172           payable(msg.sender).transfer(ethAmount);
```

<https://github.com/code-423n4/2022-07-fractional/blob/e2c5a962a94106f9495eb96769d7f60f7d5b14c9/src/modules/Migration.sol#L159-L172>

and `withdrawContribution()` use `payable.transfer()`

```solidity
File: src/modules/Migration.sol   #2

320           // Temporarily store user's eth for the transfer
321           uint256 userEth = userProposalEth[_proposalId][msg.sender];
322           // Udpates ether balance of caller
323           userProposalEth[_proposalId][msg.sender] = 0;
324           // Withdraws ether from contract back to caller
325           payable(msg.sender).transfer(userEth);
```

<https://github.com/code-423n4/2022-07-fractional/blob/e2c5a962a94106f9495eb96769d7f60f7d5b14c9/src/modules/Migration.sol#L320-L325>

While they both use `msg.sender`, the funds are tied to the address that deposited them (lines 159 and 321), and there is no mechanism to change the owner of the funds to an alternate address.

### Recommended Mitigation Steps

Use `address.call{value:x}()` instead.

**[stevennevins (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/504#issuecomment-1189580118)**

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-07-fractional-findings/issues/504#issuecomment-1198327281):**
 > After an unsuccessful migration, a multisig user (or other contract) may find their funds unrecoverable. Since a contract is able to enter a migration successfully and there is no way to specify an alternative send to address or migrate their escrowed funds to another account -- assets can be lost; as the warden points out here. I agree with Medium risk for this.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2/5 |
| Rarity Score | 1/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | codexploder, scaraven, xiaoming90, cryptphi, 0x29A, Avci, pashov, BowTiedWardens, TomJ, bardamu, peritoflores, c3phas, 0x1f8b, Amithuddar, tofunmi, Kthere, MEP, IllIllI, simon135, cccz, Waze, Ruhum, slywaters, oyc_109, Treasure-Seeker, StyxRave, horsefacts, sseefried, hake, TrungOre, Limbooo, Tutturu, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/504
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`call vs transfer`

