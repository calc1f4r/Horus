---
# Core Classification
protocol: Ethos Network Financial Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44327
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/675
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-ethos-network-ii-judging/issues/1

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
finders_count: 12
finders:
  - newspacexyz
  - volodya
  - 0xPhantom2
  - rmdanxyz
  - LeFy
---

## Vulnerability Title

M-1: authorProfileId can avoid being slashed

### Overview


This bug report is about an issue with the Ethos Network II project. The problem is that the authorProfileId can avoid being slashed, which means that someone can escape punishment for inaccurate claims or unethical behavior. This is because there is no lock on staking and withdrawals for the accused authorProfileId.

The root cause of this issue is that the code does not follow the documentation, which states that there should be a lock on staking and withdrawals for the accused. This allows anyone to unvouch at any time, even if they are accused of wrongdoing.

The attack path for this bug is that the accused profile can see that there are a lot of complaints against them and unvouch all their funds before they can be punished.

The impact of this bug is that the authorProfileId can avoid being slashed, which goes against the intended purpose of the project.

There is currently no proof of concept for this bug, but the report suggests a possible solution to mitigate the issue. This involves adding a new function to pause actions for a specific authorProfileId, which would prevent them from unvouching their funds before being punished.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-ethos-network-ii-judging/issues/1 

## Found by 
0xAnmol, 0xPhantom2, 0xbakeng, 0xc0ffEE, BengalCatBalu, Contest-Squad, LeFy, X12, farismaulana, newspacexyz, rmdanxyz, volodya
### Summary

there is not lock lock on lock on staking (and withdrawals) for the accused authorProfileId 

### Root Cause

According to [docs](https://whitepaper.ethos.network/ethos-mechanisms/slash) their should be lock
> Any Ethos participant may act as a "whistleblower" to accuse another participant of inaccurate claims or unethical behavior. This accusation triggers a 24h lock on staking (and withdrawals) for the accused. 
Currently anyone can unvouch at any time
```solidity
  function unvouch(uint256 vouchId) public whenNotPaused nonReentrant {
    Vouch storage v = vouches[vouchId];
    _vouchShouldExist(vouchId);
    _vouchShouldBePossibleUnvouch(vouchId);
    // because it's $$$, you can only withdraw/unvouch to the same address you used to vouch
    // however, we don't care about the status of the address's profile; funds are always attached
    // to an address, not a profile
    if (vouches[vouchId].authorAddress != msg.sender) {
      revert AddressNotVouchAuthor(vouchId, msg.sender, vouches[vouchId].authorAddress);
    }

    v.archived = true;
    // solhint-disable-next-line not-rely-on-time
    v.activityCheckpoints.unvouchedAt = block.timestamp;
    // remove the vouch from the tracking arrays and index mappings
    _removeVouchFromArrays(v);

    // apply fees and determine how much is left to send back to the author
    (uint256 toWithdraw, ) = applyFees(v.balance, false, v.subjectProfileId);
    // set the balance to 0 and save back to storage
    v.balance = 0;
    // send the funds to the author
    // note: it sends it to the same address that vouched; not the one that called unvouch
    (bool success, ) = payable(v.authorAddress).call{ value: toWithdraw }("");
    if (!success) {
      revert FeeTransferFailed("Failed to send ETH to author");
    }

    emit Unvouched(v.vouchId, v.authorProfileId, v.subjectProfileId);
  }
```
[contracts/contracts/EthosVouch.sol#L452](https://github.com/sherlock-audit/2024-11-ethos-network-ii/blob/main/ethos/packages/contracts/contracts/EthosVouch.sol#L452)
### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

Accused profile sees that a lot of complains going against him and unvouch all vouched funds before slashing

### Impact

authorProfileId can avoid being slashed

### PoC

_No response_

### Mitigation

```diff

+    function pauseActions(uint authorProfileId) external onlyOwner{
+        ...
+    }

  function unvouch(uint256 vouchId) public whenNotPaused nonReentrant  {
+      uint256 authorProfileId = IEthosProfile(
+          contractAddressManager.getContractAddressForName(ETHOS_PROFILE)
+      ).verifiedProfileIdForAddress(msg.sender);
+    require(!isActionsPaused(authorProfileId), "actions paused")
      Vouch storage v = vouches[vouchId];
    _vouchShouldExist(vouchId);
    _vouchShouldBePossibleUnvouch(vouchId);

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Ethos Network Financial Contracts |
| Report Date | N/A |
| Finders | newspacexyz, volodya, 0xPhantom2, rmdanxyz, LeFy, farismaulana, Contest-Squad, BengalCatBalu, 0xc0ffEE, 0xbakeng, 0xAnmol, X12 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-ethos-network-ii-judging/issues/1
- **Contest**: https://app.sherlock.xyz/audits/contests/675

### Keywords for Search

`vulnerability`

