---
# Core Classification
protocol: Union Finance Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6390
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/44
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-union-judging/issues/24

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hyh
---

## Vulnerability Title

M-3: Market adapter removal corrupts withdraw sequence

### Overview


This bug report is about an issue found in the AssetManager contract of the Union protocol. The issue is that the withdraw sequence entry is being deleted in the removeAdapter() function using an incorrect index, causing the sequence array to become corrupted and withdrawals to become unavailable. 

The incorrect index is determined for the moneyMarkets array, but applied to withdrawSeq as well, while in there indices do differ. As withdrawals logic are based on withdraw sequence array, the withdrawals can end up unavailable. For example, if 95% of the funds are held in a market, whose entry corresponded to the index removed, withdrawals will be frozen for an arbitrary time for the whole protocol until withdrawSeq be manually restored. 

The bug was found manually and the recommendation is to consider repeating the entry finding logic for withdrawSeq, for example by repeating the for loop for adapterAddress in withdrawSeq.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-union-judging/issues/24 

## Found by 
hyh

## Summary

Withdraw sequence entry is being deleted in AssetManager's removeAdapter() using incorrect index, so the sequence array becomes corrupted and withdrawals can end up unavailable.

## Vulnerability Detail

`index` used for adapter removal is determined for `moneyMarkets` array, but applied to `withdrawSeq` as well, while in there indices do differ.

## Impact

As withdrawals logic are based on withdraw sequence array, the withdrawals can end up unavailable. For example, if 95% of the funds are held in a market, whose entry corresponded to the `index` removed, withdrawals will be frozen for an arbitrary time for the whole protocol until `withdrawSeq` be manually restored. 

## Code Snippet

removeAdapter() determines the `index` for `moneyMarkets` array:

https://github.com/sherlock-audit/2023-02-union/blob/main/union-v2-contracts/contracts/asset/AssetManager.sol#L435-L463

```solidity
    /**
     *  @dev Remove a adapter for the underlying lending protocol
     *  @param adapterAddress adapter address
     */
    function removeAdapter(address adapterAddress) external override onlyAdmin {
        bool isExist = false;
        uint256 index = 0;
        uint256 moneyMarketsLength = moneyMarkets.length;
        for (uint256 i = 0; i < moneyMarketsLength; i++) {
            if (adapterAddress == address(moneyMarkets[i])) {
                isExist = true;
                index = i;
                break;
            }
        }

        if (isExist) {
            for (uint256 i = 0; i < supportedTokensList.length; i++) {
                if (moneyMarkets[index].getSupply(supportedTokensList[i]) >= 10000) revert RemainingFunds(); //ignore the dust
            }
            moneyMarkets[index] = moneyMarkets[moneyMarketsLength - 1];
            moneyMarkets.pop();

            withdrawSeq[index] = withdrawSeq[withdrawSeq.length - 1];
            withdrawSeq.pop();

            _removeTokenApprovals(adapterAddress);
        }
    }
```

But `withdrawSeq` is a permutation of `moneyMarkets`, so their indices are independent and do not correspond to each other:

https://github.com/sherlock-audit/2023-02-union/blob/main/union-v2-contracts/contracts/asset/AssetManager.sol#L136-L143

```solidity
    /**
     *  @dev Set withdraw sequence
     *  @param newSeq priority sequence of money market indices to be used while withdrawing
     */
    function setWithdrawSequence(uint256[] calldata newSeq) external override onlyAdmin {
        if (newSeq.length != moneyMarkets.length) revert NotParity();
        withdrawSeq = newSeq;
    }
```

So `index` in `withdrawSeq` being deleted do not generally correspond to the adapter, i.e. some other market end up being removed:

https://github.com/unioncredit/union-v2-contracts/blob/49d1a7261a7be20fe77b91a8a73e3cba8bc5bda5/contracts/asset/AssetManager.sol#L464-L465

```solidity
            withdrawSeq[index] = withdrawSeq[withdrawSeq.length - 1];
            withdrawSeq.pop();
```

## Tool used

Manual Review

## Recommendation

Consider repeating the entry finding logic for `withdrawSeq`, for example:

https://github.com/sherlock-audit/2023-02-union/blob/main/union-v2-contracts/contracts/asset/AssetManager.sol#L435-L463

```solidity
    /**
     *  @dev Remove a adapter for the underlying lending protocol
     *  @param adapterAddress adapter address
     */
    function removeAdapter(address adapterAddress) external override onlyAdmin {
        bool isExist = false;
        uint256 index = 0;
+       uint256 indexSeq = 0;
        uint256 moneyMarketsLength = moneyMarkets.length;
        for (uint256 i = 0; i < moneyMarketsLength; i++) {
            if (adapterAddress == address(moneyMarkets[i])) {
                isExist = true;
                index = i;
                break;
            }
        }

        if (isExist) {
+           for (uint256 i = 0; i < moneyMarketsLength; i++) {
+               if (adapterAddress == address(withdrawSeq[i])) {
+                   indexSeq = i;
+                   break;
+               }
+           }

            for (uint256 i = 0; i < supportedTokensList.length; i++) {
                if (moneyMarkets[index].getSupply(supportedTokensList[i]) >= 10000) revert RemainingFunds(); //ignore the dust
            }
            moneyMarkets[index] = moneyMarkets[moneyMarketsLength - 1];
            moneyMarkets.pop();

-           withdrawSeq[index] = withdrawSeq[withdrawSeq.length - 1];
+           withdrawSeq[indexSeq] = withdrawSeq[withdrawSeq.length - 1];
            withdrawSeq.pop();

            _removeTokenApprovals(adapterAddress);
        }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance Update |
| Report Date | N/A |
| Finders | hyh |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-union-judging/issues/24
- **Contest**: https://app.sherlock.xyz/audits/contests/44

### Keywords for Search

`vulnerability`

