---
# Core Classification
protocol: Evterminal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34060
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/EVTerminal-security-review.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-09] Malicious liquidity provider can rug-pull users

### Overview


This bug report highlights potential vulnerabilities in a token's liquidity system that could allow malicious users to take all the funds from the contract. These vulnerabilities include being able to remove liquidity without previously adding it, setting a low time for unlocking liquidity, and not extending the time for unlocking liquidity. The report recommends implementing checks for liquidity being added, enforcing a minimum time for unlocking liquidity, and only allowing the liquidity provider to remove their initial provided liquidity. The report also mentions that other decentralized exchanges may have similar vulnerabilities and that some projects choose not to lock their liquidity for flexibility.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

There are a few ways for malicious liquidity to rug-pull users:

#### Calling `removeLiquidity` without previously calling `addLiquidity`

A token owner can call `enableTrading` to allow trading without liquidity.
After some time, when funds accumulated in the contract - a malicious liquidity provider can call `removeLiquidity` to send all the funds to himself.

#### Setting a low `timeTillUnlockLiquidity`

There is no restriction to a minimum `timeTillUnlockLiquidity`. Therefore a malicious liquidity provider can set `timeTillUnlockLiquidity` to a low value. The token would seem open for trading and already funded because `_opt.liquidityAdded == true` however the liquidity provider can call `removeLiquidity` to remove the funds.

#### Not extending `timeTillUnlockLiquidity`.

Consider a token that a liquidity provider has locked funds for a long time (24 months). After the 24 months are over - the liquidity provider can take **_ALL_** the funds of the contract and not just his supplied liquidity

**Recommendations**

1. When trading also check `_opt.liquidityAdded == true`
2. In `initialize` function add a minimum `timeTillUnlockLiquidity` value. This should be enforced in `addLiquidity`
3. Allow the liquidity provider to remove only his initial provided liquidity and not the entire ETH reserve of the contract.

**EV Terminal comment**

_Other dexes also have the same design, we want to give them the flexibility. Many projects out there don’t lock their liquidity and keep on multisig or just leave it unlocked in case of a potential migration._

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Evterminal |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/EVTerminal-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

