---
# Core Classification
protocol: Yieldy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2892
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-yieldy-contest
source_link: https://code4rena.com/reports/2022-06-yieldy
github_link: https://github.com/code-423n4/2022-06-yieldy-findings/issues/49

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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

[M-17] Staking: rebase() does not rebase according to the status of the current epoch.

### Overview


A bug has been identified in the staking contract of the ‘2022-06-yieldy’ GitHub repository. The rebase function can only be called once per epoch, and the rewards of the current epoch are used in the next epoch, which can cause the rewards to be updated incorrectly and lead to incorrect distribution of user rewards. A proof of concept can be found in the code linked in the report.

The recommended mitigation step to rectify the bug is to put the IYieldy(YIELDY_TOKEN).rebase command after the epoch.distribute update, as demonstrated in the code provided. This will ensure that the rewards are updated correctly before the rebase command is executed.

### Original Finding Content

_Submitted by cccz_

In the staking contract, the rebase function can only be called once per epoch.

In the rebase function, the rewards of the current epoch are used in the next epoch, which can cause the rewards to be updated incorrectly and lead to incorrect distribution of user rewards.

        function rebase() public {
            // we know about the issues surrounding block.timestamp, using it here will not cause any problems
            if (epoch.endTime <= block.timestamp) {
                IYieldy(YIELDY_TOKEN).rebase(epoch.distribute, epoch.number); // 懒更新

                epoch.endTime = epoch.endTime + epoch.duration;
                epoch.timestamp = block.timestamp;
                epoch.number++;

                uint256 balance = contractBalance();
                uint256 staked = IYieldy(YIELDY_TOKEN).totalSupply();

                if (balance <= staked) {
                    epoch.distribute = 0;
                } else {
                    epoch.distribute = balance - staked;
                }
            }
        }

### Proof of Concept

<https://github.com/code-423n4/2022-06-yieldy/blob/524f3b83522125fb7d4677fa7a7e5ba5a2c0fe67/src/contracts/Staking.sol#L701-L719>

### Recommended Mitigation Steps

Put `IYieldy(YIELDY_TOKEN).rebase` after epoch.distribute update

        function rebase() public {
            // we know about the issues surrounding block.timestamp, using it here will not cause any problems
            if (epoch.endTime <= block.timestamp) {
                uint256 balance = contractBalance();
                uint256 staked = IYieldy(YIELDY_TOKEN).totalSupply();

                if (balance <= staked) {
                    epoch.distribute = 0;
                } else {
                    epoch.distribute = balance - staked;
                }
                IYieldy(YIELDY_TOKEN).rebase(epoch.distribute, epoch.number);

                epoch.endTime = epoch.endTime + epoch.duration;
                epoch.timestamp = block.timestamp;
                epoch.number++;
            }
        }

**[toshiSat (Yieldy) acknowledged and commented](https://github.com/code-423n4/2022-06-yieldy-findings/issues/49#issuecomment-1168884765):**
 > This is how the system is designed.

**[JasoonS (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-06-yieldy-findings/issues/49#issuecomment-1200168413):**
 > Changing to Medium. It makes sense that the rebase happens after rewards so that those who enter later don't affect the distribution of rewards before they joined.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yieldy |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-yieldy
- **GitHub**: https://github.com/code-423n4/2022-06-yieldy-findings/issues/49
- **Contest**: https://code4rena.com/contests/2022-06-yieldy-contest

### Keywords for Search

`vulnerability`

