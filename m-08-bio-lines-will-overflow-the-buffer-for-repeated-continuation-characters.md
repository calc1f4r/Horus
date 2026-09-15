---
# Core Classification
protocol: Canto Identity Subprotocols
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16188
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-03-canto-identity-subprotocols-contest
source_link: https://code4rena.com/reports/2023-03-canto-identity
github_link: https://github.com/code-423n4/2023-03-canto-identity-findings/issues/122

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - adriro
---

## Vulnerability Title

[M-08] Bio lines will overflow the buffer for repeated "continuation" characters

### Overview


The bug report describes an issue with the Bio `tokenURI` function in the code-423n4/2023-03-canto-identity repository. This function splits biography text into lines and takes into account certain "continuation" characters to prevent splitting the line in the middle of these characters. However, if the unicode string is a sequence of these continuation characters, the line buffer will eventually overflow and will revert the transaction due to an index of out bounds exception. 

To prove the vulnerability, a test was created using a string with 21 U+1F3FE characters to overflow the line buffer and revert the query to `tokenURI`. The full test file can be found in a provided link.

The recommendation for this vulnerability is to change to a new line when the current line buffer is full.

### Original Finding Content


The Bio `tokenURI` function splits biography text into lines. The algorithm will take into account certain "continuation" characters to prevent splitting the line in the middle of these characters and keep accumulating those in the current line buffer (`bytesLines`):

<https://github.com/code-423n4/2023-03-canto-identity/blob/main/canto-bio-protocol/src/Bio.sol#L60-L95>

```solidity
if ((i > 0 && (i + 1) % 40 == 0) || prevByteWasContinuation || i == lengthInBytes - 1) {
    bytes1 nextCharacter;
    if (i != lengthInBytes - 1) {
        nextCharacter = bioTextBytes[i + 1];
    }
    if (nextCharacter & 0xC0 == 0x80) {
        // Unicode continuation byte, top two bits are 10
        prevByteWasContinuation = true;
    } else {
        // Do not split when the prev. or next character is a zero width joiner. Otherwise, 👨‍👧‍👦 could become 👨>‍👧‍👦
        // Furthermore, do not split when next character is skin tone modifier to avoid 🤦‍♂️\n🏻
        if (
            // Note that we do not need to check i < lengthInBytes - 4, because we assume that it's a valid UTF8 string and these prefixes imply that another byte follows
            (nextCharacter == 0xE2 && bioTextBytes[i + 2] == 0x80 && bioTextBytes[i + 3] == 0x8D) ||
            (nextCharacter == 0xF0 &&
                bioTextBytes[i + 2] == 0x9F &&
                bioTextBytes[i + 3] == 0x8F &&
                uint8(bioTextBytes[i + 4]) >= 187 &&
                uint8(bioTextBytes[i + 4]) <= 191) ||
            (i >= 2 &&
                bioTextBytes[i - 2] == 0xE2 &&
                bioTextBytes[i - 1] == 0x80 &&
                bioTextBytes[i] == 0x8D)
        ) {
            prevByteWasContinuation = true;
            continue;
        }
        assembly {
            mstore(bytesLines, bytesOffset)
        }
        strLines[insertedLines++] = string(bytesLines);
        bytesLines = new bytes(80);
        prevByteWasContinuation = false;
        bytesOffset = 0;
    }
}
```

However, if the unicode string is a sequence of these continuation characters (which is a valid UTF8 string) the line buffer (which is 80 bytes) will eventually overflow and will revert the transaction due to an index of out bounds exception.

### Proof of Concept

In the following test we use a string with 21 [U+1F3FE](https://unicodeplus.com/U+1F3FE) characters to overflow the line buffer and revert the query to `tokenURI`.

Note: the snippet shows only the relevant code for the test. Full test file can be found [here](https://gist.github.com/romeroadrian/5ca5fdfb2a1239cde80ea1c5a7f5eec9).

```solidity
function test_Bio_tokenURI_LineBufferOverflow() public {
    // This is a skin tone codepoint ("f09f8fbe") repeated 21 times
    string memory text = unicode"🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾🏾";
    bio.mint(string(text));
    vm.expectRevert();
    bio.tokenURI(1);
}
```

### Recommendation

Change to a new line when the current line buffer is full.

**[OpenCoreCH (Canto Identity) confirmed and commented](https://github.com/code-423n4/2023-03-canto-identity-findings/issues/122#issuecomment-1489305397):**
 > Extreme edge case with a string that's technically valid, but semantically meaningless. But it's technically true.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto Identity Subprotocols |
| Report Date | N/A |
| Finders | adriro |

### Source Links

- **Source**: https://code4rena.com/reports/2023-03-canto-identity
- **GitHub**: https://github.com/code-423n4/2023-03-canto-identity-findings/issues/122
- **Contest**: https://code4rena.com/contests/2023-03-canto-identity-subprotocols-contest

### Keywords for Search

`vulnerability`

