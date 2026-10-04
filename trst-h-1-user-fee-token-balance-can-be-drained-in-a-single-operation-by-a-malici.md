---
# Core Classification
protocol: Brahma
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18807
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Brahma.md
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
  - Trust Security
---

## Vulnerability Title

TRST-H-1 User fee  token  balance  can  be  drained in  a  single  operation  by a  malicious bot

### Overview


This bug report is about the fee calculation for the BrahRouter in `_buildFeeExecutable()`. It uses tx. gas price to get the gas price specified by the bot. A malicious bot can manipulate tx.gasprice to be as high as they wish, which can lead to draining the user's fee token balance and these losses will go to the Brahma fund manager.

To mitigate this issue, it is recommended to use a gas oracle or a capped priority fee to ensure an inflated gas price does not harm the user. The team response is that there exist some scenarios where high gas may be required for quick block inclusion like liquidation protection. They use 3rd party bots like gelato which work in a decentralized fashion and operators stake GEL tokens which get slashed if they submit txns with high gas price. If a 3rd party bot still tries to abuse it, they can be kicked by the governance using BotManager.sol.

### Original Finding Content

**Description:**
In `_buildFeeExecutable()`,  BrahRouter  calculates  the  total  fee  charged  to  the  wallet.  It  uses tx. gas price to get the gas price specified by the bot.
 
```solidity 

  if (feeToken == ETH) 
   {uint256 totalFee = (gasUsed + GAS_OVERHEAD_NATIVE) * tx.gasprice;
     totalFee = _applyMultiplier(totalFee);
       return (totalFee, recipient, TokenTransfer._nativeTransferExec(recipient, totalFee));
            } else {uint256 totalFee = (gasUsed + GAS_OVERHEAD_ERC20) * tx.gasprice;
      // Convert fee amount value in fee tokenuint256 feeToCollect =PriceFeedManager(_addressProvider.priceFeedManager()).getTokenXPriceInY(totalFee, ETH, feeToken);
  feeToCollect = _applyMultiplier(feeToCollect);
 return (feeToCollect, recipient, TokenTransfer._erc20TransferExec(feeToken, recipient, feeToCollect));}
```

**Impact:**
The issue is that a malicious bot can manipulate tx.gasprice to be as high as they wish. This value is calculated post EIP1559 as the block base fee plus the sender's priority fee. A bot can offer an extremely high priority fee to drain the user's fee token balance. These losses will go to the Brahma fund manager. 

**Recommended Mitigation:**
Use a gas oracle or a capped priority fee to ensure an inflated gas price down not harm the user.


**Team response:**
There  exist  some  scenarios  where  high  gas  may  be  required  for  quick  block  inclusion  like liquidation protection. An additional check is not worth the added oracle gas cost for this.We  use  reputable  3rd  party  bots  like  gelato  which  work  in  a decentralizedfashion  for  bot operators.  operators  stake  GEL  tokens  which  get  slashed  if  they  submit  txns  with  high  gas price.  Even  if  they  do  so,  they  have  less  economic  incentive  to  do  so  as  the  gas  fee  will  be burned rather than being paid to the miner. If a 3rd party bot still tries to abuse it, they can be kicked by the governance usingBotManager.sol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Brahma |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Brahma.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

