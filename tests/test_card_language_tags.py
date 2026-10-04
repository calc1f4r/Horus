#!/usr/bin/env python3
"""Tests for hunt-card language/ecosystem informational tags."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.huntcards import derive_card_languages  # noqa: E402


class TestDeriveCardLanguages(unittest.TestCase):

    def test_solana_chain(self):
        self.assertEqual(derive_card_languages("solana", "transfer("), (["rust"], ["solana"]))

    def test_move_chains(self):
        for chain in ("sui", "aptos, movement"):
            languages, ecosystem = derive_card_languages(chain, "coin<")
            self.assertEqual(languages, ["move"])
            self.assertIn("sui", ecosystem)

    def test_cosmos_chain(self):
        self.assertEqual(derive_card_languages("cosmos", "keeper"), (["go", "rust"], ["cosmos"]))

    def test_evm_chain(self):
        self.assertEqual(derive_card_languages("ethereum", "x"), (["solidity"], ["evm"]))
        self.assertEqual(derive_card_languages("ethereum, bsc", "x"), (["solidity"], ["evm"]))

    def test_everychain_stays_any_without_evm_tokens(self):
        self.assertEqual(derive_card_languages("everychain", "rounding"), (["any"], ["any"]))

    def test_everychain_capped_to_evm_when_grep_is_solidity_shaped(self):
        for token in ("msg.sender", "require(", "keccak", "assembly"):
            self.assertEqual(
                derive_card_languages("everychain", f"foo {token} bar"),
                (["solidity"], ["evm"]),
                token,
            )

    def test_specific_chain_not_capped_by_evm_tokens(self):
        # A solana-documented card keeps solana even if its grep mentions solidity-ish text
        self.assertEqual(
            derive_card_languages("solana", "require("),
            (["rust"], ["solana"]),
        )

    def test_unknown_chain_falls_back_to_any(self):
        self.assertEqual(derive_card_languages("near", "x"), (["any"], ["any"]))
        self.assertEqual(derive_card_languages("", "x"), (["any"], ["any"]))


class TestGeneratedCardsTagged(unittest.TestCase):

    def test_all_cards_carry_tags(self):
        import json
        from pathlib import Path

        repo_root = Path(__file__).resolve().parents[1]
        cards = json.loads(
            (repo_root / "DB" / "manifests" / "huntcards" / "all-huntcards.json").read_text()
        )["cards"]
        self.assertTrue(cards, "no hunt cards generated")
        for card in cards:
            self.assertIn("languages", card, card["id"])
            self.assertIn("ecosystem", card, card["id"])
            self.assertTrue(card["languages"], card["id"])
            self.assertTrue(card["ecosystem"], card["id"])


if __name__ == "__main__":
    unittest.main()
