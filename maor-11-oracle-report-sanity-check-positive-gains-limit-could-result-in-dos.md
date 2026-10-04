---
# Core Classification
protocol: Mantle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53488
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-02-Mantle.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[MAOR-11] Oracle report sanity check positive gains limit could result in DoS

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** src/Oracle.sol:sanityCheckUpdate#L362-484

**Description:**

Once the oracle client has generated a report, it submits this report on-chain to the `Oracle.sol` contract. The Oracle contract will pass the report through a sanity check using `sanityCheckUpdate` and it will reject the report if it does not pass.

The sanity check contains checks on the change in the total balance of all Mantle validators on the consensus layer. Both lower and upper bounds are used.

The upper bound check is done using `maxConsensusLayerGainPerBlockPPT` and defined per block as 10 times the expected APR of 5%:

```
// 7200 slots per day * 365 days per year = 2628000 slots per year
// assuming 5% yield per year
// 5% / 2628000 = 1.9025e-8
// 1.9025e-8 per slot = 19025 PPT
maxConsensusLayerGainPerBlockPPT = 190250; // 10x approximate rate
```
Using the old (baseline) consensus layer balance, the upper bound is calculated using the report size in blocks and the maximum gain per block as defined above:
```
uint256 upperBound = baselineGrossCLBalance
    + Math.mulDiv(maxConsensusLayerGainPerBlockPPT * reportSize, baselineGrossCLBalance, _PPT_DENOMINATOR);
if (newGrossCLBalance > upperBound) {
    return ("Consensus layer change above max gain", newGrossCLBalance, upperBound);
}
```
If the new consensus layer balance crosses this upper bound, the report is rejected.

The issue here is that this upper bound check is quite conservative and does not account for any balance manipulation that could be performed by anyone. Any user can deposit ETH into validators owned by Mantle, increasing their balance on the consensus layer and consequently the consensus layer balance that is used in the oracle report.

For example, with a report size of a 2400 slots and a total validator balance of 50,000 ETH (86.5m$) the upper bound would be calculated as a maximum increase of 22.83 ETH. The actual rewards would be about 2.283 ETH, so the attacker would have to supply 20.55 ETH.

The cost of this attack is quite high but it might still become an attack vector for large competitors that want to disrupt Mantle’s protocol.

```
    function sanityCheckUpdate(OracleRecord memory prevRecord, OracleRecord calldata newRecord)
        public
        view
        returns (string memory, uint256, uint256)
    {
        uint64 reportSize = newRecord.updateEndBlock - newRecord.updateStartBlock + 1;
        [..]
        {
            //
            // Consensus layer balance change from the previous period.
            //
            // Checks that the change in the consensus layer balance is within the bounds given by the maximum loss and
            // minimum gain parameters. For example, a major slashing event will cause an out of bounds loss in the
            // consensus layer.

            // The baselineGrossCLBalance represents the expected growth of our validators balance in the new period
            // given no slashings, no rewards, etc. It's used as the baseline in our upper (growth) and lower (loss)
            // bounds calculations.
            uint256 baselineGrossCLBalance = prevRecord.currentTotalValidatorBalance
                + (newRecord.cumulativeProcessedDepositAmount - prevRecord.cumulativeProcessedDepositAmount);

            // The newGrossCLBalance is the actual amount of ETH we have recorded in the consensus layer for the new
            // record period.
            uint256 newGrossCLBalance = newRecord.currentTotalValidatorBalance
                + newRecord.windowWithdrawnPrincipalAmount + newRecord.windowWithdrawnRewardAmount;

            {
                // Relative lower bound on the net decrease of ETH on the consensus layer.
                // Depending on the parameters the loss term might completely dominate over the minGain one.
                //
                // Using a minConsensusLayerGainPerBlockPPT greater than 0, the lower bound becomes an upward slope.
                // Setting minConsensusLayerGainPerBlockPPT, the lower bound becomes a constant.
                uint256 lowerBound = baselineGrossCLBalance
                    - Math.mulDiv(maxConsensusLayerLossPPM, baselineGrossCLBalance, _PPM_DENOMINATOR)
                    + Math.mulDiv(minConsensusLayerGainPerBlockPPT * reportSize, baselineGrossCLBalance, _PPT_DENOMINATOR);

                if (newGrossCLBalance < lowerBound) {
                    return ("Consensus layer change below min gain or max loss", newGrossCLBalance, lowerBound);
                }
            }
            {
                // Upper bound on the rewards generated by validators scaled linearly with time and number of active
                // validators.
                uint256 upperBound = baselineGrossCLBalance
                    + Math.mulDiv(maxConsensusLayerGainPerBlockPPT * reportSize, baselineGrossCLBalance, _PPT_DENOMINATOR);

                if (newGrossCLBalance > upperBound) {
                    return ("Consensus layer change above max gain", newGrossCLBalance, upperBound);
                }
            }
        }

        return ("", 0, 0);
    }
```


**Remediation:**  We would recommend to either remove the upper bound on the absolute value or increase the maximum gain to increase the cost for an attacker.

Instead, we want to recommend to implement sanity checks on changes in the share rate of mETH, which is where a potential attack is more likely to manifest. For example, if a malicious oracle report greatly increases the consensus layer balance, they would only profit if the share rate also greatly increases. However, this check should also not be too conservative, or the original issue would reappear.

**Status:**   Acknowledged


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Mantle |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-02-Mantle.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

