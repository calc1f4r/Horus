---
# Core Classification
protocol: Solflare MetaMask Snaps - Solflare, Sui, Aptos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25904
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/08/solflare-metamask-snaps-solflare-sui-aptos/
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
  - Martin Ortner

---

## Vulnerability Title

Dapp May Force a Sign Approval Dialog Without Showing the Message to Be Signed

### Overview


This bug report is about the `request.params.displayMessage` parameter in requests to `signTransaction` and `signAllTransactions` in the MetaMask trust module. This parameter allows the dapp to control if the data to be signed is displayed to the user or not, which can be dangerous as the dapp may silently ask for a signature to sign data the user did not intend to sign. This has potential to undermine security controls and procedures implemented by MetaMask which generally enforce clarity of what data the user is requested to sign. Examples of the bug are given in the report, and the recommendation is to remove the `displayMessage` toggle and consistently enforce the message to be signed to be displayed. This way, the user can verify that they are signing the correct data/transaction.

### Original Finding Content

#### Description


With the `request.params.displayMessage` parameter in requests to `signTransaction` and `signAllTransactions` the dapp controls if the message to be signed is displayed to the user or not. Allowing the dapp to control if the data to be signed is displayed to the user is dangerous as the dapp may silently ask for a signature to sign data the user did not intend to sign. This has potential to undermine security controls and procedures implemented by MetaMask which generally enforce clarity of what data the user is requested to sign.


Note that the snap as an extension to the MetaMask trust module should not have to trust the dapp that is requesting signature.


#### Examples


Affects all snaps under review.


##### Solflare Snap


**../aptos-snap/src/index.js:L39-L51**



```
const { derivationPath, message, simulationResult = [], displayMessage = true } = request.params || {};

assertInput(derivationPath);
assertIsString(derivationPath);
assertInput(message);
assertIsString(message);
assertIsArray(simulationResult);
assertAllStrings(simulationResult);
assertIsBoolean(displayMessage);

const accepted = await renderSignTransaction(dappHost, message, simulationResult, displayMessage);
assertConfirmation(accepted);

```
**../aptos-snap/src/ui.js:L28-L33**



```
 text(host),
 ...(simulationResultItems.length > 0 || displayMessage ? [divider()] : []),
 ...simulationResultItems,
 ...(displayMessage ? [copyable(message)] : [])
 ])
}

```
#### Recommendation


In accordance with how MetaMask signing works, it is highly recommended to remove the `displayMessage` toggle and **consistently** enforce the message to be signed to be displayed. Else, there is no way for the user to verify if they are signing the correct data/transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Solflare MetaMask Snaps - Solflare, Sui, Aptos |
| Report Date | N/A |
| Finders | Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/08/solflare-metamask-snaps-solflare-sui-aptos/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

