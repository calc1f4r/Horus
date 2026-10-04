---
# Core Classification
protocol: EVM Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50166
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

ALLOWING ERC777-KIND TOKENS ON PROTOCOL LEADS RE-ENTRANCY

### Overview


This bug report discusses a vulnerability in the ERC777 standard, which is used for sending and receiving tokens in smart contracts. The issue arises when a smart contract receives tokens and then calls another transfer function, causing a re-entrancy vulnerability. This can lead to loss of funds. The vulnerability has been identified and solved by the Moonwell Team by implementing a Reentrancy Guard and better check-effect-interaction design in the Comptroller.sol contract. The code location and commit IDs are also provided for reference.

### Original Finding Content

##### Description

The ERC777 standard allows the token contract to notify senders and recipients when ERC777 tokens are sent or received from their accounts with function hooks. These hooks are called as callbacks. If the recipient of the token is a smart contract, the smart contract may cause to re-entrancy by calling another transfer function.

During the tests, it was seen that the protocol could be affected by this vulnerability if ERC777-kind tokens are planned to be used. This may cause loss of funds.

Code Location
-------------

#### MToken.sol

```
        /////////////////////////
        // EFFECTS & INTERACTIONS
        // (No safe failures beyond this point)

        /* We write previously calculated values into storage */
        totalSupply = vars.totalSupplyNew;
        accountTokens[redeemer] = vars.accountTokensNew;

        /* We emit a Transfer event, and a Redeem event */
        emit Transfer(redeemer, address(this), vars.redeemTokens);
        emit Redeem(redeemer, vars.redeemAmount, vars.redeemTokens);

        /* We call the defense hook */
        comptroller.redeemVerify(address(this), redeemer, vars.redeemAmount, vars.redeemTokens);

        /*
         * We invoke doTransferOut for the redeemer and the redeemAmount.
         *  Note: The mToken must handle variations between ERC-20 and GLMR underlying.
         *  On success, the mToken has redeemAmount less of cash.
         *  doTransferOut reverts if anything goes wrong, since we can't be sure if side effects occurred.
         */
        doTransferOut(redeemer, vars.redeemAmount);

        return uint(Error.NO_ERROR);

```

##### Score

Impact: 3  
Likelihood: 4

##### Recommendation

**SOLVED:** `Moonwell Team` solved this issue by implementing Reentrancy Guard and better check-effect-interaction design to `Comptroller.sol` contract.

`Commit ID:` **e23657c5fbeb12c7393fa49da6f350dc0bd5114e** && **762cdc4cd9a8d09f29765f9e143b25af0ebe9720**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | EVM Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

