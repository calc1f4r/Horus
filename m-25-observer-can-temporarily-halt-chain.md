---
# Core Classification
protocol: ZetaChain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36954
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-11-zetachain
source_link: https://code4rena.com/reports/2023-11-zetachain
github_link: https://github.com/code-423n4/2023-11-zetachain-findings/issues/336

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
  - ChristiansWhoHack
---

## Vulnerability Title

[M-25] Observer Can Temporarily Halt Chain

### Overview


This bug report discusses a potential issue with the process for changing the TSS address in the Zetachain code. This process involves several manual steps and has the potential for failure, which could result in significant downtime for the chain. The report suggests two potential solutions: removing the observer and continuing with the change, or automating the process to reduce the risk of human error. The team behind Zetachain has confirmed the issue and is working on a solution. 

### Original Finding Content


<https://github.com/code-423n4/2023-11-zetachain/blob/b237708ed5e86f12c4bddabddfd42f001e81941a/repos/node/x/observer/keeper/hooks.go#L92>

The process for changing the TSS address happens as follows:

1.  Observer is either added or **slashed**. This disables inbound calls and starts the kegen process.
2.  All TSS key holders vote on the TSS key. NOTE: this must be done by manually running a script or restarting the node.
3.  Each TSS key holders votes on the new public key to Zetachain.
4.  The admin calls `MigrateFSSFunds` to the new key. NOTE: this must be done MANUALLY by the admin.
5.  The TSS address must be updated on the connector and ERC20Custody contracts on all of the chains. NOTE: this must be done MANUALLY by the admin.
6.  Inbound transactions must be turned on again. NOTE: this must be done MANUALLY by the admin.

If a single observer gets slashed for any reason, the chain will be halted until steps 2-6 are manually done. Within the endblocker, we can see the code that will disable inbound CCTXs and restart the keygen process if the observer count is mismatched. This happens within the [BeginBlocker](https://github.com/code-423n4/2023-11-zetachain/blob/b237708ed5e86f12c4bddabddfd42f001e81941a/repos/node/x/observer/abci.go#L28) process of the observer module.

```golang

	if totalObserverCountCurrentBlock == int(lastBlockObserverCount.Count) {
		return
	}

           ... 

	k.DisableInboundOnly(ctx)
	k.SetKeygen(ctx, types.Keygen{BlockNumber: math.MaxInt64})
```

The count changes only when slashing occurs. The slashing happens automatically using the `StakingHooks`. Within the hook `BeforeValidatorSlashed()`, it checks to see if the user is underneath the specified threshold. If that's true, then they will be removed.

```golang

	for _, mapper := range mappers {
               ...
		if  sdk.NewDecFromInt(resultingTokens).LT(obsParams.MinObserverDelegation) {
			mapper.ObserverList = CleanAddressList(mapper.ObserverList, accAddress.String())
			k.SetObserverMapper(ctx, mapper)
		}
	}
```

From the code above, it is clear that an observer going off line from slashing will restart the keygen process and halt the chain. This may happen on accident, such as the server going down from a power outage, or on purpose from a malicious validator.

Considering this requires all TSS voters to perform operations (currently 11 on Ethereum) and the administrator, there are a lot of points of failure here. If this happens, I would guess it would take 12 hours to get everything back into a working state. For a fairly common occurrence, this is a large amount of downtime.

### Remediation

One strategy would to simply remove the observer and keep moving on until a pre-determined date. Since the threshold for all of the keys is 2 out of 3, everyone would keep functioning normally until the change was made.

An additional strategy would be to *automate* this entire process. However, many of these operations are super sensitive, such as migrating admin keys. So, this may be intentional.

**[lumtis (ZetaChain) confirmed](https://github.com/code-423n4/2023-11-zetachain-findings/issues/336#issuecomment-1885770508)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ZetaChain |
| Report Date | N/A |
| Finders | ChristiansWhoHack |

### Source Links

- **Source**: https://code4rena.com/reports/2023-11-zetachain
- **GitHub**: https://github.com/code-423n4/2023-11-zetachain-findings/issues/336
- **Contest**: https://code4rena.com/reports/2023-11-zetachain

### Keywords for Search

`vulnerability`

