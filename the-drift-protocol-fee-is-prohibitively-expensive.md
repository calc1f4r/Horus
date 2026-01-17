---
# Core Classification
protocol: Datachain - App for Liquidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58921
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/datachain-app-for-liquidity/b8c4b08a-4456-4ab9-a381-d738d1ba3f0b/index.html
source_link: https://certificate.quantstamp.com/full/datachain-app-for-liquidity/b8c4b08a-4456-4ab9-a381-d738d1ba3f0b/index.html
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
finders_count: 3
finders:
  - Hamed Mohammadi
  - Ibrahim Abouzied
  - Danny Aksenov
---

## Vulnerability Title

The Drift protocol fee is prohibitively expensive

### Overview


The client has marked a bug as "Fixed" in the code `617b92257ede7a3c039bd76be7c7cd0ec1864798`. The bug is located in the file `src/replaceable/TransferPoolFeeCalculator.sol` and affects the calculation of the protocol drift fee. The expected value of arbitraging a price drift between two pegged assets is not being accurately calculated, resulting in an overcharge of the protocol drift fee. This can be exploited in a scenario where a transfer is made for a stablecoin at a specific price point, leaving the user with only $1 after the fee is charged. The recommendation is to correct the fee calculation to only remove the expected value of the arbitrage.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `617b92257ede7a3c039bd76be7c7cd0ec1864798`.

**File(s) affected:**`src/replaceable/TransferPoolFeeCalculator.sol`

**Description:** The expected value of arbitraging a price drift between two pegged assets is equal to:

```
expectedValue = (dstPrice - srcPrice) * amountGD
```

The protocol drift fee is equal to:

```
(amountGd * srcPrice) / dstPrice
```

The current calculation far overcharges the protocol drift fee.

**Exploit Scenario:**

1.   The drift required to charge the fee is 10 basis points.
2.   If the transfer is for a stablecoin, the dift protocol fee will be charged when the source token price is $0.9990 and the destination price is $1.0000.
3.   For a transfer of $1000 USD, the drift protocol fee will be equal to `($1000 * $0.9990) / $1.0000 == $999`
4.   The user will only be left with $1 for their transfer.

**Recommendation:** Correct the fee to only remove the expected value of the arbitrage.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Datachain - App for Liquidity |
| Report Date | N/A |
| Finders | Hamed Mohammadi, Ibrahim Abouzied, Danny Aksenov |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/datachain-app-for-liquidity/b8c4b08a-4456-4ab9-a381-d738d1ba3f0b/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/datachain-app-for-liquidity/b8c4b08a-4456-4ab9-a381-d738d1ba3f0b/index.html

### Keywords for Search

`vulnerability`

