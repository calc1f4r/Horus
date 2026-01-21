---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25700
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-11-canto
source_link: https://code4rena.com/reports/2022-11-canto
github_link: https://github.com/code-423n4/2022-11-canto-findings/issues/48

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - ronnyx2017
  - hihen
  - Ruhum
---

## Vulnerability Title

[H-01] User can redirect fees by using a proxy contract

### Overview


This bug report is about a security vulnerability related to the Turnstile contract and the Canto x/csr/keeper/evm_hooks.go. It allows anyone to register an address using the Turnstile contract, creating a proxy contract with which they can execute other smart contracts. This could lead to fees being sent to the user's own contract instead of the actual application they are using, or even to a proxy contract for high-usage contracts that send a percentage of the refund back to the caller. This incentivizes users to take the fees for themselves instead of giving them to the application, and is considered a HIGH risk.

Recommended mitigation steps include distributing fees according to each contract's gas usage, or making the feature permissioned so only select contracts are allowed to participate. This issue was discussed during the design of CSR.

### Original Finding Content


<https://github.com/code-423n4/2022-11-canto/blob/main/CIP-001/src/Turnstile.sol#L86-L101>

<https://github.com/code-423n4/2022-11-canto/blob/main/Canto/x/csr/keeper/evm_hooks.go#L51>

### Impact

For any given tx, the fees are sent to its recipient (`To`). Anybody can register an address using the Turnstile contract. Thus, a user is able to create a proxy contract with which they execute other smart contracts. That way, the fees are sent to their own contract instead of the actual application they are using. People who use smart contract wallets don't even have to bother with setting up a proxy structure. They just add their own wallet to the Turnstile contract.

Also, there might be a possibility of someone setting up a proxy for high-usage contracts where the fees are sent back to the caller. So for contract $X$, we create $X'$ which calls $X$ for the caller. Since $X'$ is the recipient of the tx, it gets the gas refund. To incentivize the user to use $X'$ instead of $X$, $X'$ sends a percentage of the refund to the caller. The feasibility both technically and economically depends on the contract that is attacked. But, theoretically, it's possible.

The incentive to take it for yourself instead of giving it to the app is pretty high. Since this causes a loss of funds for the app I rate it as HIGH.

### Proof of Concept

Registering an address is permissionless:

```sol
    function register(address _recipient) public onlyUnregistered returns (uint256 tokenId) {
        address smartContract = msg.sender;

        if (_recipient == address(0)) revert InvalidRecipient();

        tokenId = _tokenIdTracker.current();
        _mint(_recipient, tokenId);
        _tokenIdTracker.increment();

        emit Register(smartContract, _recipient, tokenId);

        feeRecipient[smartContract] = NftData({
            tokenId: tokenId,
            registered: true
        });
    }
```

Fees are sent to the recipient of the tx:

```sol
func (h Hooks) PostTxProcessing(ctx sdk.Context, msg core.Message, receipt *ethtypes.Receipt) error {
	// Check if the csr module has been enabled
	params := h.k.GetParams(ctx)
	if !params.EnableCsr {
		return nil
	}

	// Check and process turnstile events if applicable
	h.processEvents(ctx, receipt)

	contract := msg.To()
	if contract == nil {
		return nil
	}

        // ...
```

### Recommended Mitigation Steps

It's pretty difficult to fix this properly. The ideal solution is to distribute fees according to each contract's gas usage. That will be a little more complicated to implement. Also, you have to keep an eye on whether it incentivizes developers to make their contracts less efficient. Another solution is to make this feature permissioned so that only select contracts are allowed to participate. For example, you could say that an address has to be triggered $X$ amount of times before it is eligible for gas refunds.

**[tkkwon1998 (Canto) acknowledged and commented](https://github.com/code-423n4/2022-11-canto-findings/issues/48#issuecomment-1356331310):**
 > We acknowledge this as true, but it's a drawback that was discussed during the design of CSR.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | ronnyx2017, hihen, Ruhum |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-canto
- **GitHub**: https://github.com/code-423n4/2022-11-canto-findings/issues/48
- **Contest**: https://code4rena.com/reports/2022-11-canto

### Keywords for Search

`vulnerability`

