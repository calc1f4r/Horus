---
# Core Classification
protocol: Liquid Collective Lceth
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59327
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/liquid-collective-lceth/727416a8-3cf6-46fb-a103-701d5c94649e/index.html
source_link: https://certificate.quantstamp.com/full/liquid-collective-lceth/727416a8-3cf6-46fb-a103-701d5c94649e/index.html
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
finders_count: 3
finders:
  - Andy Lin
  - Jeffrey Kam
  - Gelei Deng
---

## Vulnerability Title

Potential Denial of Service in Report Generation Due to Underflow

### Overview


The team has fixed an issue in the `oracle/report.go` file by adding a helper function and a check to avoid underflow. The problem was caused by a calculation in the `generateReport()` function, which could potentially result in a large value for `validatorsSkimmedBalance`. This could cause a denial of service on the oracles when submitting a report to the smart contract. The recommendation is to modify the calculation to fix the underflow issue.

### Original Finding Content

**Update**
The team fixed the issue by adding a helper function `getValidatorSkimmedBalance()` that includes the check `if wAmount <= beaconcommon.Gwei(32_000_000_000)` to avoid underflow. Addressed in: `d5ddf93`.

**File(s) affected:**`oracle/report.go`

**Description:** In `oracle/report.go:generateReport()`, there is a snippet of code that calculates the skimmed balance:

```
case withdrawalEpoch >= withdrawableEpoch:
    // All amounts below 32 ETH are considered exited
    validatorsExitedBalance += MinGwei(
        withdrawal.Amount,
        beaconcommon.Gwei(32_000_000_000),
    )
    // All amounts above 32 ETH are considered skimmed
    validatorsSkimmedBalance += MaxGwei(
        0,
        withdrawal.Amount - beaconcommon.Gwei(32_000_000_000),
    )
```

However, the calculation of `validatorsSkimmedBalance` can potentially underflow when `withdrawal.Amount` is less than 32 ETH. Since the underlying type of `withdrawal.Amount` is simply `uint64`, underflowing will result in setting `validatorsSkimmedBalance` to a value larger than `2^64 - 1 - 32_000_000_000 = 1.8446744e+19 GWEI`, approximately 150 times the current ETH supply. When a validator is slashed, they are forced to exit the validator set, with the `withdrawableEpoch` set to 36 days after the slashing event. This means the underflow illustrated above can occur around 36 days after a slashing event since the withdrawable amount of a slashed validator is lower than 32 ETH.

Consequently, the report submission to the smart contract side will likely revert at `OracleManager.1.sol::setConsensusLayerData() -> River.1.sol::_pullCLFunds()` because `collectedCLFunds` will not be equivalent to `_skimmedEthAmount + _exitedEthAmount`, given that `_skimmedEthAmount` will be a significantly large amount.

```
function _pullCLFunds(uint256 _skimmedEthAmount, uint256 _exitedEthAmount) internal override {
    ...
        IWithdrawV1(WithdrawalCredentials.getAddress()).pullEth(totalAmountToPull);
        uint256 collectedCLFunds = address(this).balance - currentBalance;
        if (collectedCLFunds != _skimmedEthAmount + _exitedEthAmount) {
            revert InvalidPulledClFundsAmount(_skimmedEthAmount + _exitedEthAmount, collectedCLFunds);
        }
    ...
}
```

This could have an impact as it might cause a denial of service on the oracles since no one will be able to submit a consensus layer report to the smart contract; it will revert due to the underflow issue described.

**Recommendation:** Modify the calculation in the `generateReport()` function to fix the underflow issue described above, for example, by adding an if condition to first check whether `withdrawal.Amount` is less than 32 ETH before performing the subtraction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Liquid Collective Lceth |
| Report Date | N/A |
| Finders | Andy Lin, Jeffrey Kam, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/liquid-collective-lceth/727416a8-3cf6-46fb-a103-701d5c94649e/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/liquid-collective-lceth/727416a8-3cf6-46fb-a103-701d5c94649e/index.html

### Keywords for Search

`vulnerability`

