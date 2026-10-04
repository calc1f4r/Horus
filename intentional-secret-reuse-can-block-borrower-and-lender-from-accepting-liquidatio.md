---
# Core Classification
protocol: Atomic Loans
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13999
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/09/atomic-loans/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Steve Marx

---

## Vulnerability Title

Intentional secret reuse can block borrower and lender from accepting liquidation payment ✓ Fixed

### Overview


This bug report is about a vulnerability in the Sales smart contract of the AtomicLoans platform. The vulnerability allows Dave, the liquidator, to exploit the contract and obtain the collateral for free. This is done by Dave choosing the same secret hash as either Alice, Bob, or Charlie (arbiter) and then Alice and Bob revealing their secrets A and B through the process of moving the collateral. Dave then uses that secret to obtain the collateral, and Alice and Bob are unable to provide Dave’s secret to the `Sales` smart contract due to the order of conditionals in `provideSecret()`. 

The resolution for this bug is fixed in [AtomicLoans/atomicloans-eth-contracts#65](https://github.com/AtomicLoans/atomicloans-eth-contracts/pull/65). The recommendation is either changing the way `provideSecret()` works to allow for duplicate secret hashes or rejecting duplicate hashes in `create()`. The mitigating factor for this bug is that Alice and Bob could notice that Dave chose a duplicate secret hash and refuse to proceed with the sale, however, this is not something they are likely to do.

### Original Finding Content

#### Resolution



This is fixed in [AtomicLoans/atomicloans-eth-contracts#65](https://github.com/AtomicLoans/atomicloans-eth-contracts/pull/65).


#### Description


For Dave (the liquidator) to claim the collateral he’s purchasing, he must reveal secret D. Once that secret is revealed, Alice and Bob (the borrower and lender) can claim the payment.


Secrets must be provided via the `Sales.provideSecret()` function:


**code/ethereum/contracts/Sales.sol:L193-L200**



```
	function provideSecret(bytes32 sale, bytes32 secret\_) external {
		require(sales[sale].set);
		if      (sha256(abi.encodePacked(secret\_)) == secretHashes[sale].secretHashA) { secretHashes[sale].secretA = secret\_; }
        else if (sha256(abi.encodePacked(secret\_)) == secretHashes[sale].secretHashB) { secretHashes[sale].secretB = secret\_; }
        else if (sha256(abi.encodePacked(secret\_)) == secretHashes[sale].secretHashC) { secretHashes[sale].secretC = secret\_; }
        else if (sha256(abi.encodePacked(secret\_)) == secretHashes[sale].secretHashD) { secretHashes[sale].secretD = secret\_; }
        else                                                                          { revert(); }
	}

```
Note that if Dave chooses the same secret hash as either Alice, Bob, or Charlie (arbiter), there is no way to set `secretHashes[sale].secretD` because one of the earlier conditionals will execute.


For Alice and Bob to later receive payment, they must be able to provide Dave’s secret:


**code/ethereum/contracts/Sales.sol:L218-L222**



```
	function accept(bytes32 sale) external {
        require(!accepted(sale));
        require(!off(sale));
		require(hasSecrets(sale));
		require(sha256(abi.encodePacked(secretHashes[sale].secretD)) == secretHashes[sale].secretHashD);

```
Dave can exploit this to obtain the collateral for free:


1. Dave looks at Alice’s secret hashes to see which will be used in the sale.
2. Dave begins the liquidation process, using the same secret hash.
3. Alice and Bob reveal their secrets A and B through the process of moving the collateral.
4. Dave now knows the preimage for the secret hash he provided. It was revealed by Alice already.
5. Dave uses that secret to obtain the collateral.
6. Alice and Bob now want to receive payment, but they’re unable to provide Dave’s secret to the `Sales` smart contract due to the order of conditionals in `provideSecret()`.
7. After an expiration, Dave can claim a refund.


#### Mitigating factors


Alice and Bob *could* notice that Dave chose a duplicate secret hash and refuse to proceed with the sale. This is not something they are likely to do.


#### Recommendation


Either change the way `provideSecret()` works to allow for duplicate secret hashes or reject duplicate hashes in `create()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Atomic Loans |
| Report Date | N/A |
| Finders | Steve Marx
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/09/atomic-loans/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

