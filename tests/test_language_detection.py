#!/usr/bin/env python3
"""Tests for grep_prune language auto-detection across supported languages."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from grep_prune import LANGUAGE_PATTERNS, detect_language  # noqa: E402


class TestDetectLanguage(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def _make(self, relpath, content="// stub\n"):
        path = os.path.join(self.tmp.name, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def _detect(self):
        return detect_language(self.tmp.name)

    def test_solidity(self):
        self._make("src/A.sol")
        self._make("src/B.sol")
        self.assertEqual(self._detect(), ["*.sol"])

    def test_rust(self):
        self._make("src/lib.rs")
        self._make("src/main.rs")
        self.assertEqual(self._detect(), ["*.rs"])

    def test_go(self):
        self._make("keeper/keeper.go")
        self._make("types/types.go")
        self.assertEqual(self._detect(), ["*.go"])

    def test_cpp(self):
        self._make("node/validator.cpp")
        self._make("node/net.cpp")
        self.assertEqual(self._detect(), ["*.cpp"])

    def test_cpp_header_heavy_project(self):
        self._make("include/state.hpp")
        self._make("include/net.hpp")
        self.assertEqual(self._detect(), ["*.hpp"])

    def test_mixed_rust_cpp_rust_dominant(self):
        for i in range(3):
            self._make(f"src/mod{i}.rs")
        self._make("bridge/bridge.cpp")
        detected = self._detect()
        self.assertEqual(detected[0], "*.rs")

    def test_empty_target_returns_all_supported(self):
        detected = self._detect()
        self.assertIn("*.cpp", detected)
        self.assertIn("*.rs", detected)
        self.assertIn("*.go", detected)

    def test_language_patterns_include_cpp_family(self):
        for ext in ("cpp", "cc", "cxx", "h", "hpp"):
            self.assertIn(ext, LANGUAGE_PATTERNS)


if __name__ == "__main__":
    unittest.main()
