---
# Core Classification
protocol: GTE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64867
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
source_link: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
github_link: https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-80

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
finders_count: 20
finders:
  - Legend
  - NexusAudits
  - hgrano
  - Kaysoft
  - udogodwin
---

## Vulnerability Title

[M-24] Launchpad slippage is not enforced properly during token graduation

### Overview


The bug report is about a contract called Launchpad.sol on GitHub. The contract allows users to buy tokens from a launchpad by specifying the number of base tokens they want to buy and the maximum amount of quote tokens they want to spend. However, there is a bug in the contract that makes the slippage protection mechanism ineffective when a purchase order exhausts the bonding curve's supply and triggers a "graduation" to a secondary market. This means that the contract only checks the slippage against the cost of tokens bought from the bonding curve, not the total intended purchase. This allows a transaction to succeed even if the user receives a fraction of their desired tokens at a high price. The recommended mitigation step is to calculate and check the price per token the user is willing to pay and the price per token bought.

### Original Finding Content



`launchpad/Launchpad.sol` [# L287](https://github.com/code-423n4/2025-08-gte-perps/blob/main/contracts/launchpad/Launchpad.sol# L287)

When a user wants to buy tokens from the launchpad, they specify the number of base tokens they want to buy and the max amount of quote tokens they want to spend as slippage. The contract then proceeds to buy the base tokens from the curve and checks whether the quote tokens paid is higher than the max amount of quote tokens specified by the user or not and reverts the transaction if so.
```

function buy(BuyData calldata buyData)
    external
    nonReentrant
    onlyBondingActive(buyData.token)
    onlySenderOrOperator(buyData.account, SpotOperatorRoles.LAUNCHPAD_FILL)
    returns (uint256 amountOutBaseActual, uint256 amountInQuote)
{
    IUniswapV2Pair pair = _assertValidRecipient(buyData.recipient, buyData.token);
    LaunchData memory data = _launches[buyData.token];

    (amountOutBaseActual, data.active) = _checkGraduation(buyData.token, data, buyData.amountOutBase);

    amountInQuote = data.curve.buy(buyData.token, amountOutBaseActual);

    if (data.active && amountInQuote == 0) revert DustAttackInvalid();
@>  if (amountInQuote > buyData.maxAmountInQuote) revert SlippageToleranceExceeded();

    buyData.token.safeTransfer(buyData.recipient, amountOutBaseActual);
    address(data.quote).safeTransferFrom(buyData.account, address(this), amountInQuote);

    _emitSwapEvent({
        account: buyData.account,
        token: buyData.token,
        baseAmount: amountOutBaseActual,
        quoteAmount: amountInQuote,
        isBuy: true,
        curve: data.curve
    });

    // If graduated, handle AMM setup and remaining swap
    if (!data.active) {
        (amountOutBaseActual, amountInQuote) = _graduate(buyData, pair, data, amountOutBaseActual, amountInQuote);
    }
}
```

This slippage protection mechanism is ineffective when a purchase order exhausts the bonding curve’s supply and triggers the “graduation” to a secondary market (AMM pair). The contract checks the slippage against the cost of tokens bought from the bonding curve only, not the total intended purchase. This allows a transaction to succeed even if the user receives a fraction of their desired tokens at an exorbitant effective price.

### Recommended mitigation steps

Consider calculating and checking the price per token the user is willing to pay and the price per token bought instead.

[View detailed Proof of Concept](https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-80)

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | GTE |
| Report Date | N/A |
| Finders | Legend, NexusAudits, hgrano, Kaysoft, udogodwin, taticuvostru, randomx, HighKingMargo, deividrobinson, Web3Vikings, 0rpse, bigbear1229, chaos304, nuthan2x, Ekene, la-arana-inteligente, r1ver, niffylord, VinciGearHead, jesjupyter |

### Source Links

- **Source**: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
- **GitHub**: https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-80
- **Contest**: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad

### Keywords for Search

`vulnerability`

