---
# Core Classification
protocol: Solo Margin Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11838
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/solo-margin-protocol-audit-30ac2aaf6b10/
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
  - OpenZeppelin
---

## Vulnerability Title

Contracts using the experimental ABIEncoderV2

### Overview


The Solo project uses the ABIEncoderV2 of Solidity, which is still experimental and may contain important bugs. This could be a risk for the project, so extra caution should be taken when testing it. The recent bug announcement suggests that most of the issues of the encoder will have an impact on the functionality of the contracts. This means that thorough testing should be done to mitigate any risks. However, even with great tests, there is always a chance to miss important issues that could affect the project. Therefore, more conservative options should be considered, like implementing upgrade, migration or pause functionalities, delaying the release until the ABIEncoderV2 is stable, or rewriting the project to use the current stable encoder. An update from the dYdX team states that the AbiEncoderV2 has been used in production for months without incident by other high-profile protocols, and that they have upgraded the compiler version to v0.5.7 since beginning the audit.

### Original Finding Content

The Solo project uses features from the ABIEncoderV2 of Solidity. This new version of the encoder is still experimental. Since the release of Solidity v0.5.4 (the one used by the Solo project), two new versions of Solidity have been released fixing important issues in this encoder.


Because the ABIEncoderV2 is experimental, it would be risky to release the project using it. Moreover, the recent findings show that it is likely that other important bugs are yet to be found.


As mentioned in the recent [bug announcement](https://blog.ethereum.org/2019/03/26/solidity-optimizer-and-abiencoderv2-bug/), most of the issues of the encoder will have impact on the functionality of the contracts. So the risk can be mitigated by being extra thorough on the testing process of the project at all levels.


However, even with great tests there is always a chance to miss important issues that will affect the project. Consider also more conservative options, like implementing upgrade, migration or pause functionalities, delaying the release until the ABIEncoderV2 is stable, or rewriting the project to use the current stable encoder.


***Update:*** *Statement from the dYdX team about this issue: “The AbiEncoderV2 has been used in production for months without incident by other high-profile protocols such as 0x Version 2. We do not see its use as a larger security risk than using the Solidity compiler in general. We have also upgraded the compiler version to v0.5.7 since beginning the Audit (which fixes the aforementioned bugs).”*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Solo Margin Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/solo-margin-protocol-audit-30ac2aaf6b10/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

