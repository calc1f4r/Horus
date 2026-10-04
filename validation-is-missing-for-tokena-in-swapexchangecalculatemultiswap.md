---
# Core Classification
protocol: Swapexchange
chain: everychain
category: uncategorized
vulnerability_type: missing_check

# Attack Vector Details
attack_type: missing_check
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26175
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
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
  - missing_check

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Hans
  - 0kage
---

## Vulnerability Title

Validation is missing for tokenA in `SwapExchange::calculateMultiSwap()`

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Description:** The protocol supports claiming a chain of swaps and the function `SwapExchange::calculateMultiSwap()` is used to do some calculations including the amount of tokenA that can be received for a given amount of tokenB.
Looking at the implementation, the protocol does not validate that the tokenA of the last swap in the chain is actually the same as the tokenA of `multiClaimInput`.
Because this view function is supposed to be used by the frontend to 'preview' the result of a `MultiSwap`, this does not imply a direct security risk but can lead to unexpected results. (It is notable that the actual swap function `SwapExchange::_claimMultiSwap()` implemented a proper validation.)

```solidity
SwapExchange.sol
150:     function calculateMultiSwap(SwapUtils.MultiClaimInput calldata multiClaimInput) external view returns (SwapUtils.SwapCalculation memory) {
151:         uint256 swapIdCount = multiClaimInput.swapIds.length;
152:         if (swapIdCount == 0 || swapIdCount > _maxHops) revert Errors.InvalidMultiClaimSwapCount(_maxHops, swapIdCount);
153:         if (swapIdCount == 1) {
154:             SwapUtils.Swap memory swap = swaps[multiClaimInput.swapIds[0]];
155:             return SwapUtils._calculateSwapNetB(swap, multiClaimInput.amountB, _feeValue, _feeDenominator, _fixedFee);
156:         }
157:         uint256 matchAmount = multiClaimInput.amountB;
158:         address matchToken = multiClaimInput.tokenB;
159:         uint256 swapId;
160:         bool complete = true;
161:         for (uint256 i = 0; i < swapIdCount; i++) {
162:             swapId = multiClaimInput.swapIds[i];
163:             SwapUtils.Swap memory swap = swaps[swapId];
164:             if (swap.tokenB != matchToken) revert Errors.NonMatchingToken();
165:             if (swap.amountB < matchAmount) revert Errors.NonMatchingAmount();
166:             if (matchAmount < swap.amountB) {
167:                 if (!swap.isPartial) revert Errors.NotPartialSwap();
168:                 matchAmount = MathUtils._mulDiv(swap.amountA, matchAmount, swap.amountB);
169:                 complete = complete && false;
170:             }
171:             else {
172:                 matchAmount = swap.amountA;
173:             }
174:             matchToken = swap.tokenA;
175:         }
176:         (uint8 feeType,) = _calculateFeeType(multiClaimInput.tokenA, multiClaimInput.tokenB);//@audit-issue no validation matchToken == multiClaimInput.tokenA
177:         uint256 fee = FeeUtils._calculateFees(matchAmount, multiClaimInput.amountB, feeType, swapIdCount, _feeValue, _feeDenominator, _fixedFee);
178:         SwapUtils.SwapCalculation memory calculation;
179:         calculation.amountA = matchAmount;
180:         calculation.amountB = multiClaimInput.amountB;
181:         calculation.fee = fee;
182:         calculation.feeType = feeType;
183:         calculation.isTokenBNative = multiClaimInput.tokenB == Constants.NATIVE_ADDRESS;
184:         calculation.isComplete = complete;
185:         calculation.nativeSendAmount = SwapUtils._calculateNativeSendAmount(calculation.amountB, calculation.fee, calculation.feeType, calculation.isTokenBNative);
186:         return calculation;
187:     }
```

**Impact:** The function will return an incorrect swap calculation result if the last swap in the chain has a different tokenA than the tokenA of `multiClaimInput` and it can lead to unexpected results.

**Recommended Mitigation:** Add a validation that the tokenA of the last swap in the chain is the same as the tokenA of `multiClaimInput`.

**Protocol:** Fixed in commit [d3c758e](https://github.com/SwapExchangeio/Contracts/commit/d3c758e6c08f6be75bd420ffd8bf4de71a407897).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Swapexchange |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Missing Check`

