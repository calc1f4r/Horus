---
# Core Classification
protocol: Holograph
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5592
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/102

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - 0xA5DF
  - 0x52
  - ladboy233
  - Chom
  - adriro
---

## Vulnerability Title

[H-07] Failed job can't be recovered. NFT may be lost.

### Overview


This bug report is about a vulnerability in the code of the HolographOperator.sol contract on the github repository code-423n4/2022-10-holograph. The vulnerability can lead to a failed job not being recoverable and the NFT associated with that job being lost. The code in question is located at lines 329 and 419-429. 

The vulnerability occurs when the nonRevertingBridgeCall fails. The code will delete the _operatorJobs[hash] and set _failedJobs[hash] to true and emit the FailedOperatorJob event. This means that the job is not replayable and the NFT is lost forever.

The recommended mitigation steps for this vulnerability are to move the delete _operatorJobs[hash] to the end of the function executeJob, but this implementation is not safe. The selected operator may get slashed and additional checks may need to be added to allow retries for only the selected operator.

### Original Finding Content


[HolographOperator.sol#L329](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L329)<br>
[HolographOperator.sol#L419-L429](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L419-L429)<br>

```solidity
function executeJob(bytes calldata bridgeInRequestPayload) external payable {
...
delete _operatorJobs[hash];
...
    try
      HolographOperatorInterface(address(this)).nonRevertingBridgeCall{value: msg.value}(
        msg.sender,
        bridgeInRequestPayload
      )
    {
      /// @dev do nothing
    } catch {
      _failedJobs[hash] = true;
      emit FailedOperatorJob(hash);
    }
}
```

First, it will `delete _operatorJobs[hash];` to have it not replayable.

Next, assume `nonRevertingBridgeCall` failed. NFT won't be minted and the catch block is entered.

`_failedJobs[hash]` is set to true and event is emitted

Notice that `_operatorJobs[hash]` has been deleted, so this job is not replayable. This mean NFT is lost forever since we can't retry executeJob.

### Recommended Mitigation Steps

Move `delete _operatorJobs[hash];` to the end of function executeJob covered in `if (!_failedJobs[hash])`

```solidity
...
if (!_failedJobs[hash]) delete _operatorJobs[hash];
...
```

But this implementation is not safe. The selected operator may get slashed. Additionally, you may need to check `_failedJobs` flag to allow retry for only the selected operator.

**[gzeon (judge) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/102#issuecomment-1296298124):**
 > While the use of non-blocking call is good to unstuck operator, consider making the failed job still executable by anyone (so the user can e.g. use a higher gas limit) to avoid lost fund. Kinda like how Arbitrum retryable ticket works. Can be high risk due to asset lost.

**[Trust (warden) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/102#issuecomment-1296346691):**
 > I think it's a design choice to make it not replayable. Sponsor discussed having a refund mechanism at the source chain, if we were to leave it replayable the refunding could lead to double mint attack.

**[alexanderattar (Holograph) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/102#issuecomment-1307872286):**
 > This is a valid point and the desired code is planned but wasn't implemented in time for the audit. We will add logic to handle this case.

**[gzeon (judge) increased severity to High and commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/102#issuecomment-1320929853):**
 > Since asset can be lost, I think it is fair to judge this as High risk.

**[alexanderattar (Holograph) resolved and commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/102#issuecomment-1351772822):**
 > We have a fix for this: https://github.com/holographxyz/holograph-protocol/pull/98/files#diff-552f4c851fa3089f9c8efd33a2f10681bc27743917bb63000a5d19d5b41e0d3f



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Holograph |
| Report Date | N/A |
| Finders | 0xA5DF, 0x52, ladboy233, Chom, adriro |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/102
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`Business Logic`

