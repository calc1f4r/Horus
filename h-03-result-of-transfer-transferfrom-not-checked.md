---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: safetransfer

# Attack Vector Details
attack_type: safetransfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 488
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/8

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - safetransfer
  - erc20

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - gpersoon
  - zer0dot
  - heiho1  maplesyrup.
  - JMukesh
  - jonah1005
---

## Vulnerability Title

[H-03] Result of transfer / transferFrom not checked

### Overview


This bug report discusses a vulnerability that impacts the ability to transfer tokens from one address to another. The bug is that when insufficient tokens are present, no revert occurs, and a result of "false" is returned. This means that tokens can be minted without having received sufficient tokens to do so, resulting in a potential loss of funds. It is a best practice to always check the result of transferFrom and transfer. The report provides examples of where the result isn't checked, as well as examples of where it is checked. The tool used to analyze the code was grep. The recommended mitigation step is to always check the result of transferFrom and transfer.

### Original Finding Content

## Handle

gpersoon


## Vulnerability details

## Impact
A call to transferFrom or transfer is frequently done without checking the results.
For certain ERC20 tokens, if insufficient tokens are present, no revert occurs but a result of "false" is returned.
So its important to check this. If you don't you could mint tokens without have received sufficient tokens to do so. So you could loose funds.

Its also a best practice to check this.
See below for example where the result isn't checked.

Note, in some occasions the result is checked (see below for examples).

## Proof of Concept
Highest risk:
.\Dao.sol:                iBEP20(_token).transferFrom(msg.sender, address(this), _amount); // Transfer user's assets to Dao contract
.\Pool.sol:               iBEP20(TOKEN).transfer(member, outputToken); // Transfer the TOKENs to user
.\Pool.sol:               iBEP20(token).transfer(member, outputAmount); // Transfer the swap output to the selected user
.\poolFactory.sol:   iBEP20(_token).transferFrom(msg.sender, _pool, _amount);
.\Router.sol:           iBEP20(_fromToken).transfer(fromPool, iBEP20(_fromToken).balanceOf(address(this))); // Transfer TOKENs from ROUTER to fromPool
.\Router.sol:           iBEP20(_token).transfer(_pool, iBEP20(_token).balanceOf(address(this))); // Transfer TOKEN to pool
.\Router.sol:           iBEP20(_token).transferFrom(msg.sender, _pool, _amount); // Transfer TOKEN to pool
.\Router.sol:           iBEP20(_token).transfer(_recipient, _amount); // Transfer TOKEN to recipient
.\Synth.sol:             iBEP20(_token).transferFrom(msg.sender, address(this), _amount); // Transfer tokens in

less risky
.\Router.sol:           iBEP20(fromPool).transferFrom(_member, fromPool, unitsInput); // Transfer LPs from user to the pool
.\BondVault.sol:     iBEP20(_pool).transfer(member, _claimable); // Send claim amount to user
.\Router.sol:           iBEP20(_pool).transferFrom(_member, _pool, units); // Transfer LPs to the pool
.\Router.sol:           iBEP20(_pool).transferFrom(_member, _pool, units); // Transfer LPs to pool
.\Router.sol:           iBEP20(fromSynth).transferFrom(msg.sender, _poolIN, inputAmount); // Transfer synth from user to pool
.\Pool.sol:               iBEP20(synthIN).transfer(synthIN, _actualInputSynth); // Transfer SYNTH to relevant synth contract
.\Router.sol:           iBEP20(WBNB).transfer(_pool, _amount); // Transfer WBNB from ROUTER to pool
.\Dao.sol:               iBEP20(BASE).transfer(newDAO, baseBal);
.\Pool.sol:               iBEP20(BASE).transfer(member, outputBase); // Transfer the SPARTA to user
.\Pool.sol:               iBEP20(BASE).transfer(member, outputBase); // Transfer SPARTA to user
.\Router.sol:           iBEP20(BASE).transfer(toPool, iBEP20(BASE).balanceOf(address(this))); // Transfer SPARTA from ROUTER to toPool
.\Router.sol:           iBEP20(BASE).transfer(_pool, iBEP20(BASE).balanceOf(address(this))); // Transfer SPARTA to pool
.\Router.sol:           iBEP20(BASE).transfer(_pool, iBEP20(BASE).balanceOf(address(this))); // Transfer SPARTA from ROUTER to pool
.\Router.sol:           iBEP20(BASE).transferFrom(msg.sender, _pool, inputAmount); // Transfer SPARTA from ROUTER to pool

Sometimes the result is checked:
.\Dao.sol:              require(iBEP20(pool).transferFrom(msg.sender, address(_DAOVAULT), amount), "!funds"); // Send user's deposit to the DAOVault
.\Dao.sol:              require(iBEP20(BASE).transferFrom(msg.sender, address(_RESERVE), _amount), '!fee'); // User pays the new proposal fee
.\DaoVault.sol:      require(iBEP20(pool).transfer(member, _balance), "!transfer"); // Transfer user's balance to their wallet
.\synthVault.sol:    require(iBEP20(synth).transferFrom(msg.sender, address(this), amount)); // Must successfuly transfer in
.\synthVault.sol:    require(iBEP20(synth).transfer(msg.sender, redeemedAmount)); // Transfer from SynthVault to user

## Tools Used
grep

## Recommended Mitigation Steps
Always check the result of transferFrom and transfer

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | gpersoon, zer0dot, heiho1  maplesyrup., JMukesh, jonah1005, cmichel, k, 7811, 0xRajeev, shw |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/8
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`SafeTransfer, ERC20`

