---
# Core Classification
protocol: Mass
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29679
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
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
finders_count: 5
finders:
  - Gustavo Grieco
  - Josselin Feist
  - Tarun Bansal
  - Kurt Willis
  - Richie Humphrey
---

## Vulnerability Title

DCA ownership transfers can be abused to steal tokens

### Overview


This bug report discusses a low difficulty issue related to data validation in the Nested Finance platform. The issue involves the transfer of ownership for DCA (Dollar Cost Averaging) contracts without the consent of the new owner. This can potentially be exploited to steal users' tokens. The report explains how the recipient of a DCA swap is stored in the swap parameter and how the tokens are transferred from the current owner to the recipient during an automated swap. The bug occurs when ownership of a DCA is transferred without checking for the new owner's consent, allowing an attacker to steal tokens from the new owner. The report recommends short-term solutions such as disallowing ownership transfers or implementing a two-step ownership transfer process, and long-term solutions such as creating documentation and conducting additional tests to prevent similar issues.

### Original Finding Content

## Vulnerability Report

**Difficulty:** Low  
**Type:** Data Validation  

## Description
DCA ownership is transferred without the consent of the new owner, which means that DCA ownership transfers can be abused to steal users’ tokens. The recipient of a DCA swap is stored in the swap parameter `ISwapRouter.ExactInputSingleParams.recipient`.

```solidity
struct Dca {
    uint120 lastExecuted;
    uint112 interval;
    uint16 swapSlippage;
    bool isGelatoWatching;
    uint16[] tokensOutAllocation;
    bytes32 taskId;
    ISwapRouter.ExactInputSingleParams[] swapsParams;
}
```
*Figure 21.1: The Dca struct in INestedDca.sol*

In most cases, the recipient of the swap will also be the creator of the DCA, stored in `ownerOf[dcaId]`. When an automated swap is performed, the tokens are transferred from the current owner of the given DCA to the recipient defined in the swap parameters.

```solidity
IERC20(swapParams.tokenIn).safeTransferFrom(
    ownerOf[dcaId], address(this), swapParams.amountIn
);
// Perform the DCA programmed swap
amountsOut[i] = _performDcaSwap(dcaId, i);
```
*Figure 21.2: The performDca function in NestedDca.sol*

When ownership of a DCA is transferred via the `transferDcaOwnership` function, the function sets the new owner without checking for the new owner’s consent. If ownership is transferred after the DCA has already been set up and started, then the tokens will be transferred from the new user instead. This issue can be abused to steal tokens from any user that has already given their token-spending approval to the NestedDca contract.

## Exploit Scenario
Bob sets up a DCA to convert his USDC tokens to ETH. For this purpose, he has given the NestedDca contract unlimited approval. He currently has $1 million worth of USDC in his wallet. Eve notices this and sets up a DCA that transfers $1 million of USDC (that she does not own) to ETH in a single swap. She then starts the DCA and immediately transfers the ownership of the DCA to Bob. Once Eve’s automated task is performed, Bob’s $1 million of USDC is transferred to Eve.

## Recommendations
- **Short term:** Either disallow transfers of DCA ownership or add a two-step ownership transfer process, in which the new owner must accept the ownership transfer.
- **Long term:** Create documentation/diagrams that highlight all of the transfers of assets and the token approvals. Add additional tests, and use Echidna to test system invariants targeting the assets and DCA transfers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Mass |
| Report Date | N/A |
| Finders | Gustavo Grieco, Josselin Feist, Tarun Bansal, Kurt Willis, Richie Humphrey |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf

### Keywords for Search

`vulnerability`

