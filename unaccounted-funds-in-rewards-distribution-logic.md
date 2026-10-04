---
# Core Classification
protocol: BTC Hardfork - Enhancement / Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50856
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/coredao/btc-hardfork-enhancement-update
source_link: https://www.halborn.com/audits/coredao/btc-hardfork-enhancement-update
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Unaccounted funds in rewards distribution logic

### Overview


The `receiveRewards` function in the **SystemReward** contract is not working properly. When a transfer to a whitelist member fails, the `remain` value is still reduced by the intended transfer amount, even though the funds were not successfully sent. This can result in unallocated funds being unfairly distributed or lost. The issue has been fixed by the **CoreDAO team** in a recent commit.

### Original Finding Content

##### Description

The `receiveRewards` function in the **SystemReward** contract processes excess funds by distributing them to members of the `whiteListSet` based on their assigned percentage. However, when a transfer to a whitelist member fails, the `remain` value is still reduced by the intended transfer amount, regardless of whether the funds were successfully sent.

  

The mentioned scenario can result in unallocated funds being disproportionately redirected to other whitelist members, burned, or sent to the foundation. For example, if a transfer fails for one member, their share is effectively lost, and the remaining distribution does not account for this failure, potentially creating an imbalance in the intended allocation.

  

Code Location
-------------

```
  /// Receive funds from system, burn the portion which exceeds cap
  function receiveRewards() external payable override onlyInit {
    if (msg.value != 0) {
      if (address(this).balance > incentiveBalanceCap) {
        uint256 value = address(this).balance - incentiveBalanceCap;
        uint256 remain = value;
        for (uint256 i = 0; i < whiteListSet.length; i++) {
          uint256 toWhiteListValue = value * whiteListSet[i].percentage / SatoshiPlusHelper.DENOMINATOR;
          if (remain >= toWhiteListValue) {
            remain -= toWhiteListValue;
            bool success = payable(whiteListSet[i].member).send(toWhiteListValue);
            if (success) {
              emit whitelistTransferSuccess(whiteListSet[i].member, toWhiteListValue);
            } else {
              emit whitelistTransferFailed(whiteListSet[i].member, toWhiteListValue);
            }
          }
        }
        if (remain != 0) {
          if (isBurn) {
            IBurn(BURN_ADDR).burn{ value: remain }();
          } else {
            payable(FOUNDATION_ADDR).transfer(remain);
          }
        }
      }
      emit receiveDeposit(msg.sender, msg.value);
    }
  }
```

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:N/Y:H (7.5)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:N/Y:H)

##### Recommendation

The `receiveRewards` function should adjust the `remain` value only after confirming that a transfer was successful. For failed transfers, the function should log the amount and leave it in remain to ensure it is not inadvertently redirected or lost.

##### Remediation

**SOLVED**: The **CoreDAO team** solved the issue in the specified commit id.

##### Remediation Hash

<https://github.com/coredao-org/core-genesis-contract/commit/340eca9db07a93024501b5fe116bacada8ba0220>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | BTC Hardfork - Enhancement / Update |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/coredao/btc-hardfork-enhancement-update
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/coredao/btc-hardfork-enhancement-update

### Keywords for Search

`vulnerability`

