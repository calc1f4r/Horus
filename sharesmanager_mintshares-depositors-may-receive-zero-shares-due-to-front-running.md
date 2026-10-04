---
# Core Classification
protocol: Liquid Collective
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7029
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - share_inflation
  - front-running

protocol_categories:
  - staking_pool
  - liquid_staking
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Optimum
  - Matt Eccentricexit
  - Danyal Ellahi
  - Saw-mon and Natalie
  - Emanuele Ricci
---

## Vulnerability Title

SharesManager._mintShares - Depositors may receive zero shares due to front-running

### Overview


This bug report is about a potential attack vector in the SharesManager.1.sol#L202 contract. The attack vector is a front-running attack in which an attacker can spot a call to UserDepositManagerV1._deposit and front-run it with a transaction that sends wei to the contract. This will cause the victim to receive fewer shares than expected, as the number of shares minted to a depositor is determined by (_underlyingAssetValue * _total-Supply()) / oldTotalAssetBalance. The attacker does not necessarily have to be a whitelisted user, and the funds sent by the attacker cannot be directly claimed back. 

The most profitable attack vector is when the attacker is able to determine the share price, in which case they will need to send at least attackerShares * (_underlyingAssetValue - 1) + 1 to the contract. To fix this vulnerability, a validation check enforcing that sharesToMint > 0 should be added, and the fix presented in issue An attacker can freeze all incoming deposits and brick the oracle members' reporting system with only 1 wei should also be implemented.

### Original Finding Content

## Medium Risk Report

## Severity 
Medium Risk

## Context 
SharesManager.1.sol#L202

## Description 
The number of shares minted to a depositor is determined by 

\[
\text{shares} = \frac{\text{underlyingAssetValue} \times \text{totalSupply()}}{\text{oldTotalAssetBalance}}
\]

Potential attackers can spot a call to `UserDepositManagerV1._deposit` and front-run it with a transaction that sends wei to the contract (by self-destructing another contract and sending the funds to it), causing the victim to receive fewer shares than expected. 

More specifically, if `oldTotalAssetBalance()` is greater than `underlyingAssetValue * totalSupply()`, then the number of shares the depositor receives will be 0, although `underlyingAssetValue` will still be pulled from the depositor’s balance. 

An attacker with access to enough liquidity and the mempool data can spot a call to `UserDepositManagerV1._deposit` and front-run it by sending at least 

\[
\text{totalSupplyBefore} \times (\text{underlyingAssetValue} - 1) + 1 \text{ wei}
\]

to the contract. This way, the victim will get 0 shares, but `underlyingAssetValue` will still be pulled from their account balance. 

In this case, the attacker does not necessarily have to be a whitelisted user, and it is important to mention that the funds sent by them cannot be directly claimed back; rather, they will increase the price of the share.

The attack vector mentioned above is the general front-run case. The most profitable attack vector will be when the attacker can determine the share price (e.g., if the attacker mints the first share). In this scenario, the attacker will need to send at least 

\[
\text{attackerShares} \times (\text{underlyingAssetValue} - 1) + 1 
\]

to the contract (with `attackerShares` being completely controlled by the attacker, and thus can be set to 1). 

In our case, depositors are whitelisted, which makes this attack harder for a foreign attacker.

## Recommendation 
Consider adding a validation check enforcing that `sharesToMint > 0`.

## Spearbit 
The fix presented in the issue "An attacker can freeze all incoming deposits and brick the oracle members' reporting system with only 1 wei" also addresses this vulnerability.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Liquid Collective |
| Report Date | N/A |
| Finders | Optimum, Matt Eccentricexit, Danyal Ellahi, Saw-mon and Natalie, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LiquidCollective-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Share Inflation, Front-Running`

