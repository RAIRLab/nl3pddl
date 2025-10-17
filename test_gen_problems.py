#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

from nl3pddl.problem_generators import PROBLEM_GENERATORS
from nl3pddl.gen_problems import plan_file


class TestProblemGenerators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        cls.domains_dir = Path("data/domains")

        # Verify domain files exist
        if not cls.domains_dir.exists():
            raise FileNotFoundError(
                f"Domain directory {cls.domains_dir} not found. "
                "Please ensure domains are generated first."
            )

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    def test_blocks_generator(self):
        self._test_generator("blocks", problem_index=1)

    def test_checkers_generator(self):
        self._test_generator("checkers-jumping", problem_index=1)

    def test_elevators_generator(self):
        self._test_generator("miconic", problem_index=1)

    def test_flow_generator(self):
        self._test_generator("flow", problem_index=1)

    def test_bookseller_generator(self):
        self._test_generator("bookseller", problem_index=1)

    def _test_generator(self, domain_name: str, problem_index: int = 1, max_retries: int = 5):
        # Get the generator function
        generator = PROBLEM_GENERATORS.get(domain_name)
        self.assertIsNotNone(
            generator,
            f"Generator for domain '{domain_name}' not found"
        )

        # Get domain file path
        domain_file = self.domains_dir / domain_name / "ground.pddl"
        self.assertTrue(
            domain_file.exists(),
            f"Domain file {domain_file} does not exist. "
            f"Please ensure the domain is generated first."
        )

        # Try to generate a solvable problem, retrying if necessary
        plans = None
        problem_file = os.path.join(self.test_dir, f"{domain_name}_test.pddl")

        for attempt in range(max_retries):
            try:
                # Use different seed for each attempt
                generator(problem_index + attempt, problem_file)
            except Exception as e:
                self.fail(
                    f"Generator for '{domain_name}' failed to create problem: {e}"
                )

            # Verify problem file was created
            self.assertTrue(
                os.path.exists(problem_file),
                f"Problem file {problem_file} was not created"
            )

            # Verify problem file is not empty
            file_size = os.path.getsize(problem_file)
            self.assertGreater(
                file_size,
                0,
                f"Generated problem file {problem_file} is empty"
            )

            # Read and verify basic PDDL structure
            with open(problem_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn(
                    "(define (problem",
                    content,
                    f"Problem file {problem_file} missing PDDL problem definition"
                )
                self.assertIn(
                    "(:domain",
                    content,
                    f"Problem file {problem_file} missing domain reference"
                )
                self.assertIn(
                    "(:init",
                    content,
                    f"Problem file {problem_file} missing initial state"
                )
                self.assertIn(
                    "(:goal",
                    content,
                    f"Problem file {problem_file} missing goal state"
                )

            # Validate that the problem can be solved
            print(f"\nValidating {domain_name} problem with planner (attempt {attempt + 1}/{max_retries})...")
            plans = plan_file(str(domain_file), problem_file, k=1)

            if plans is not None:
                break  # Successfully generated a solvable problem
            else:
                print(f"  Retry: Problem was unsolvable, generating new problem...")

        self.assertIsNotNone(
            plans,
            f"Failed to generate solvable problem for {domain_name} after {max_retries} attempts. "
            "All generated problems were unsolvable or had errors."
        )

        self.assertIn(
            "plans",
            plans,
            f"Plan object for {domain_name} missing 'plans' key"
        )

        plan_list = plans["plans"]
        self.assertGreater(
            len(plan_list),
            0,
            f"No plans found for {domain_name}. Problem may be unsolvable."
        )

        # Verify the plan has actions
        first_plan = plan_list[0]
        self.assertIn(
            "actions",
            first_plan,
            f"Plan for {domain_name} missing 'actions' key"
        )

        actions = first_plan["actions"]
        self.assertIsInstance(
            actions,
            list,
            f"Actions in plan for {domain_name} should be a list"
        )

        print(f"✓ {domain_name}: Generated valid problem with {len(actions)} actions in plan")


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestProblemGenerators)

    # verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run_tests()
