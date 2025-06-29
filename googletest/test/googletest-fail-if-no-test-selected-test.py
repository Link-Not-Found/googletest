#!/usr/bin/env python3  # pylint: disable=g-interpreter-mismatch
#
# Copyright 2025, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Tests for Google Test's --gtest_fail_if_no_test_selected flag."""

from googletest.test import gtest_test_utils


# The command line flag for enabling the fail-if-no-test-selected behavior.
FAIL_IF_NO_TEST_SELECTED_FLAG = "gtest_fail_if_no_test_selected"

# The environment variable for the test output warnings file.
TEST_WARNINGS_OUTPUT_FILE = "TEST_WARNINGS_OUTPUT_FILE"


class GTestFailIfNoTestSelectedTest(gtest_test_utils.TestCase):
  """Tests the --gtest_fail_if_no_test_selected flag."""

  def Run(self, program_name, flags=None, env=None):
    """Run the given program with the given flag.

    Args:
      program_name: Name of the program to run.
      flags: The command line flags to pass to the program, or None.
      env: Dictionary with environment to pass to the subprocess.

    Returns:
      True if the program exits with code 0, false otherwise.
    """

    exe_path = gtest_test_utils.GetTestExecutablePath(program_name)
    args = [exe_path]
    if flags is not None:
      args.extend(flags)
    process = gtest_test_utils.Subprocess(args, capture_stderr=False, env=env)
    return process.exited and process.exit_code == 0

  def testSucceedsWhenFlagIsNotSetAndOnlyDisabledTestsPresent(self):
    """Tests that no test selected results in success without the flag set."""
    self.assertTrue(
        self.Run("googletest-fail-if-no-test-linked-test-with-disabled-test_"),
    )

  def testFailsWhenFlagIsSetAndOnlyDisabledTestsPresent(self):
    """Tests that no test selected results in failure with the flag set."""
    self.assertFalse(
        self.Run(
            "googletest-fail-if-no-test-linked-test-with-disabled-test_",
            flags=[f"--{FAIL_IF_NO_TEST_SELECTED_FLAG}"],
        ),
    )

  def testSucceedsWhenFlagIsSetAndEnabledTestsPresent(self):
    """Tests that a test running still succeeds when the flag is set."""
    self.assertTrue(
        self.Run(
            "googletest-fail-if-no-test-linked-test-with-enabled-test_",
            flags=[f"--{FAIL_IF_NO_TEST_SELECTED_FLAG}"],
        ),
    )


if __name__ == "__main__":
  gtest_test_utils.Main()
