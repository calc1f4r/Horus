---
# Core Classification
protocol: Primitive
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18741
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Primitive-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Primitive-Spearbit-Security-Review.pdf
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
finders_count: 4
finders:
  - M4rio.eth
  - Christoph Michel
  - Kurt Barry
  - Sabnock
---

## Vulnerability Title

Tokens With Multiple Addresses Can Be Stolen Due to Reliance on balanceOf

### Overview


This bug report is about the risk of using multiple valid contract addresses for the same underlying storage in the FVM (PortfolioVirtual). This is a medium risk issue that can be exploited by an attacker to gain access to the entire balance of a double entrypoint token. The attacker can do this by atomically creating a second pool with the alternate address, allocating liquidity, and then deallocating it. 

The recommendation is to explicitly warn users not to create pools with tokens that have multiple valid addresses. Additionally, a blacklist could be added to prevent any address other than an "official" one from being used. An architectural solution would be to store tokens in dedicated, special-purpose contracts for each token address, but this would increase gas costs and complexity. The report has been marked as Acknowledged.

### Original Finding Content

## Security Advisory

## Severity: Medium Risk

### Context
`AccountLib.sol#L230`

### Description
Some ERC20 tokens have multiple valid contract addresses that serve as entrypoints for manipulating the same underlying storage (such as Synthetix tokens like SNX and sBTC and the TUSD stablecoin). Because the FVM holds all tokens for all pools in the same contract, it assumes that a contract address is a unique identifier for a token and relies on the return value of `balanceOf` for manipulated tokens to determine what transfers are needed during transaction settlement. Consequently, multiple entrypoint tokens are not safe to be used in pools.

For example, suppose there is a pool with non-zero liquidity where one token has a second valid address. An attacker can atomically create a second pool using the alternate address, allocate liquidity, and then immediately deallocate it. During the execution of the `_settlement` function, `getNetBalance` will return a positive net balance for the double entrypoint token, crediting the attacker and transferring them the entire balance of the double entrypoint token. This attack only costs gas, as the allocation and deallocation of non-double entrypoint tokens will cancel out.

### Recommendation
At a minimum, anyone interacting with contracts derived from `PortfolioVirtual` should be explicitly warned not to create pools containing tokens with multiple valid addresses. An explicit blacklist could be added to prevent any address other than an "official" one from being used to create pairs and pools for such tokens (potentially fixed at deployment time, as double entrypoint tokens are rare and now widely known to be dangerous).

Architecturally, tokens could be stored in dedicated, special-purpose contracts for each token address, although this would increase gas costs and complexity.

### Spearbit
Marked as Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Primitive |
| Report Date | N/A |
| Finders | M4rio.eth, Christoph Michel, Kurt Barry, Sabnock |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Primitive-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Primitive-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

