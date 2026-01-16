---
# Core Classification
protocol: Sai
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17274
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/sai.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/sai.pdf
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
finders_count: 6
finders:
  - Josselin Feist
  - 2017: December 15
  - 2018: Initial report delivered
  - Mark Mossberg
  - Changelog October 24
---

## Vulnerability Title

Loss of decimal precision leads to free tokens

### Overview


This bug report is about Sai, a system that uses fixed point decimal representation to handle fractional values. This lack of precision when dealing with multiplication or division can be exploited by an attacker to receive tokens for free. The report provides four patterns of attack, each with a test case and a demonstration of severity. 

Pattern 1 and 3 are exploitable to generate free Sai tokens, while Pattern 2 and 4 can be used to generate free skr and gem tokens respectively. In each case, the attacker is able to exploit a certain token ratio condition.

To prevent the attacks, the report recommends adding certain requirements to SaiTub.draw, SaiTub.join, and SaiTap.bust. However, a solution to mitigate Pattern 4 could not be easily found. The report suggests using a tool based on formal methods, such as Manticore, to ensure that these issues are properly mitigated. 

The report also provides recommended references such as What causes floating point round errors? (as answered by Mark Booth) to help understand the problem better.

### Original Finding Content

## Type: Numerics
## Target: SaiTub, SaiTap, SaiTop

### Difficulty: Low

### Description
The Sai system uses the fixed point decimal representation to handle fractional values. Fixed point arithmetic is known to lack precision when dealing with multiplication or division. These operations are used to compute token prices. The resulting loss of precision allows an attacker to receive tokens for free.

Exploitation of these issues requires a specific state of the system (e.g., a specific value for chi). Appendix C contains test cases along with each required beginning state. Note that these test cases exercise the vulnerabilities but do not exploit them to the fullest. To demonstrate the severity of the problem, we provide a test case in Appendix D where an attacker is able to generate `0x28000000` free `skr` tokens.

### Pattern 1: Division Rounding to Zero
This pattern represents `draw`, and can be exploited to generate free Sai tokens (`15 wei` worth in our example in Appendix C):

```solidity
f(input):
    a += input / x
    b += input
```

If an attacker calls `f(user)` where the following condition is met, then `a` is not increased, while `b` is increased by `user`.

```
user / x == 0 (1)
```

### Pattern 2: Division Roundings
This pattern represents `draw/wipe` and can be exploited to generate free Sai tokens (`1 wei` worth in our example in Appendix C):

```solidity
f1(input):
    a += input / x
    b += input

f2(input):
    a -= input / x
    b -= input
```

If an attacker calls `f1(user1)` followed by `f2(user2)` where the following conditions are met, then `a` ends with its initial value, while `b` is increased by `y`.

```
user2 == user1 - y
user1 / x == user2 / x (1) (2)
```

### Pattern 3: Multiplication Rounding to Zero
This pattern represents `join` and can be exploited to generate free `skr` tokens (`1 wei` in our example in Appendix C):

```solidity
f(input):
    a += input * x
    b += input
```

If an attacker calls `f(user)` where the following condition is met, then `a` is not increased, while `b` is increased by `user`.

```
user * x == 0 (1)
```

`SaiTap.bust` may also be vulnerable to this issue. Appendix D shows an example where a user can generate `0x28000000` free `skr` tokens by abusing this pattern.

### Pattern 4: Multiplication Roundings
This pattern represents `join/exit` and can be exploited to steal `gem` tokens (`1 wei` in our example in Appendix C):

```solidity
f1(input):
    a += input * x
    b += input

f2(input):
    a -= input * x
    b -= input
```

If an attacker calls `f1(user1)` followed by `f2(user2_0), …, f2(user2_n)` where the following conditions are met, then `a` ends with its initial value, while `b` is increased by the difference in (2).

```
user1 = user2_0 + ... + user2_n
user1 * x < user2_0 * x + ... + user2_n * x (1) (2)
```

`SaiTap.bust/SaiTap.boom` may also be vulnerable to this issue.

### Exploit Scenario
Bob exploits certain token ratio conditions in Sai, using `join` to generate `0x28000000` free `skr` tokens. This allows Bob to do several things, including maliciously manipulate the `SKR/GEM` ratio, and effectively draw SAI without spending any GEM. Alice discovers the attack and announces it publicly. As a result, users lose trust in Sai.

### Recommendation
To prevent Pattern 1, add in `SaiTub.draw`:

```solidity
require(div(wad, chi()) > 0)
```

To prevent Pattern 3, add in `SaiTub.join` and `SaiTap.bust`:

```solidity
require(ask(wad) > 0)
```

A solution to prevent Pattern 2 could be to add in `SaiTub.draw`:

```solidity
wad = rmul(rdiv(wad, chi()), chi())
```

Note that all of these recommendations require additional, thorough testing to validate the work properly. Further, we could not easily find a solution to mitigate the fourth pattern. Fixed point computation is not well suited for multiplication and division and requires careful consideration of corner cases. Consider using a tool based on formal methods, such as `Manticore`, to ensure that these issues are properly mitigated.

### Recommended References
- What causes floating point round errors? (as answered by Mark Booth)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Sai |
| Report Date | N/A |
| Finders | Josselin Feist, 2017: December 15, 2018: Initial report delivered, Mark Mossberg, Changelog October 24, 2017: Added Appendix E with retest results Public release January 31 |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/sai.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/sai.pdf

### Keywords for Search

`vulnerability`

