"""
Test suite for validating PDDL problem generators.

This module provides functionality to test problem generators by:
1. Generating PDDL problem files
2. Validating syntax with VAL Parser
3. Finding plans using k* planner
4. Validating plans with VAL Validate

Can be called with specific generators/sizes or run a full test suite.
"""

import os
import sys
import tempfile
import io
import contextlib
from kstar_planner import planners
import traceback
import subprocess
from pathlib import Path

from nl3pddl.problem_generators import PROBLEM_GENERATORS

VAL_PARSER = "submodules/VAL/build/bin/Parser"
VAL_VALIDATE = "submodules/VAL/build/bin/Validate"
DOMAINS_DIR = "data/domains"

GENERATORS = {}
for domain_name, generator_func in PROBLEM_GENERATORS.items():
    GENERATORS[domain_name] = {
        'generator': generator_func,
        'domain': domain_name,
        'domain_file': f'{DOMAINS_DIR}/{domain_name}/ground.pddl'
    }


def run_parser(domain_path, problem_path):
    """Run VAL Parser to check PDDL syntax."""
    print(f"\n{'='*60}")
    print("STEP 1: Syntax Check")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [VAL_PARSER, str(domain_path), str(problem_path)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("PASS: Syntax is valid")
            return True
        else:
            print("FAIL: Syntax check failed")
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def run_planner(domain_path, problem_path):
    """Run k* planner to find a plan."""
    print(f"\n{'='*60}")
    print("STEP 2: Finding a Plan")
    print(f"{'='*60}")

    try:
        plan_result = planners.plan_topk(
            domain_file=Path(domain_path),
            problem_file=Path(problem_path),
            number_of_plans_bound=1,
            timeout=30
        )

        if plan_result is None:
            print("FAIL: Planner returned None")
            return None

        if plan_result.get("unsolvable"):
            print("FAIL: Problem is UNSOLVABLE")
            return None

        if not plan_result.get("plans") or len(plan_result["plans"]) == 0:
            print("FAIL: No plans found")
            return None

        plan = plan_result["plans"][0]
        actions = plan.get("actions", [])

        print(f"PASS: Found a plan with {len(actions)} actions")
        print("\nPlan:")
        for i, action in enumerate(actions, 1):
            print(f"  {i}. {action}")

        return actions

    except Exception as e:
        print(f"FAIL: Planning failed: {e}")
        traceback.print_exc()
        return None


def run_validator(domain_path, problem_path, plan_actions):
    """Run VAL Validate to verify a plan."""
    print(f"\n{'='*60}")
    print("STEP 3: Validating Plan")
    print(f"{'='*60}")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.plan', delete=False) as f:
        for action in plan_actions:
            f.write(f"({action})\n")
        plan_file = f.name

    try:
        result = subprocess.run(
            [VAL_VALIDATE, "-v", str(domain_path), str(problem_path), plan_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("PASS: Plan is VALID")
            return True
        else:
            print("FAIL: Plan validation FAILED")
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return False

    except Exception as e:
        print(f"ERROR: Validation error: {e}")
        return False
    finally:
        os.unlink(plan_file)


def test_single_generator(generator_name, problem_size, verbose=False):
    """
    Test a single generator with a specific problem size.

    Args:
        generator_name: Name of the generator to test
        problem_size: Size parameter for problem generation
        verbose: If True, print detailed output

    Returns:
        Dict with test results (syntax, plan_found, plan_valid, plan_length)
    """
    gen_info = GENERATORS[generator_name]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.pddl', delete=False) as f:
        problem_file = f.name

    try:
        gen_info['generator'](problem_size, problem_file)
    except TypeError:
        try:
            gen_info['generator'](problem_size, problem_file, seed=None)
        except:
            os.unlink(problem_file)
            return {'syntax': False, 'plan_found': False, 'plan_valid': False, 'error': 'Generation failed'}

    domain_file = gen_info['domain_file']

    if not Path(domain_file).exists():
        os.unlink(problem_file)
        return {'syntax': False, 'plan_found': False, 'plan_valid': False, 'error': 'Domain not found'}

    if not verbose:
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            syntax_valid = run_parser(domain_file, problem_file)
            plan = run_planner(domain_file, problem_file) if syntax_valid else None
            plan_valid = run_validator(domain_file, problem_file, plan) if plan else False
    else:
        syntax_valid = run_parser(domain_file, problem_file)
        plan = run_planner(domain_file, problem_file) if syntax_valid else None
        plan_valid = run_validator(domain_file, problem_file, plan) if plan else False

    os.unlink(problem_file)

    return {
        'syntax': syntax_valid,
        'plan_found': plan is not None,
        'plan_valid': plan_valid,
        'plan_length': len(plan) if plan else 0
    }


def run_test_suite():
    """Run the full test suite for all problem generators."""
    print(f"\n{'='*60}")
    print("RUNNING TEST SUITE FOR ALL PROBLEM GENERATORS")
    print(f"{'='*60}\n")

    test_sizes = [x for x in range(1, 11)]
    results = {}

    for gen_name in GENERATORS.keys():
        print(f"\n{'='*60}")
        print(f"Testing: {gen_name}")
        print(f"{'='*60}")

        results[gen_name] = {}

        for size in test_sizes:
            print(f"  Size {size}...", end=" ", flush=True)
            result = test_single_generator(gen_name, size, verbose=False)
            results[gen_name][size] = result

            if result.get('syntax') and result.get('plan_found') and result.get('plan_valid'):
                print(f"PASS (plan length: {result['plan_length']})")
            elif result.get('syntax') and result.get('plan_found'):
                print(f"FAIL (plan invalid)")
            elif result.get('syntax'):
                print(f"FAIL (no plan found)")
            else:
                print(f"FAIL (syntax error)")

    print(f"\n{'='*60}")
    print("TEST SUITE SUMMARY")
    print(f"{'='*60}\n")

    total_tests = 0
    passed_tests = 0

    for gen_name, size_results in results.items():
        print(f"{gen_name}:")
        for size, result in size_results.items():
            total_tests += 1
            status = "PASS" if (result.get('syntax') and result.get('plan_found') and result.get('plan_valid')) else "FAIL"
            if status == "PASS":
                passed_tests += 1
            print(f"  Size {size}: {status}")

    print(f"\n{'='*60}")
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed ({100*passed_tests//total_tests}%)")
    print(f"{'='*60}\n")


def test_generators(generator_name=None, problem_size=5):
    """
    Main entry point for testing generators.

    Args:
        generator_name: Name of generator to test, or None for all generators
        problem_size: Size parameter for single generator test (default: 5)
    """
    if generator_name is None:
        run_test_suite()
        return

    if generator_name not in GENERATORS:
        print(f"ERROR: Unknown generator: {generator_name}")
        print(f"Available: {', '.join(GENERATORS.keys())}")
        return

    gen_info = GENERATORS[generator_name]

    print(f"\n{'='*60}")
    print(f"Testing Problem Generator: {generator_name}")
    print(f"{'='*60}")
    print(f"Problem size: {problem_size}")
    print(f"Domain: {gen_info['domain']}")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.pddl', delete=False) as f:
        problem_file = f.name

    print(f"\nGenerating problem to: {problem_file}")

    try:
        gen_info['generator'](problem_size, problem_file)
    except TypeError:
        gen_info['generator'](problem_size, problem_file, seed=None)

    domain_file = gen_info['domain_file']

    if not Path(domain_file).exists():
        print(f"ERROR: Domain file not found: {domain_file}")
        os.unlink(problem_file)
        return

    syntax_valid = run_parser(domain_file, problem_file)
    if not syntax_valid:
        print("\nFAILED: Syntax check failed")
        os.unlink(problem_file)
        return

    plan = run_planner(domain_file, problem_file)
    if plan is None:
        print("\nFAILED: Could not find a plan")
        os.unlink(problem_file)
        return

    plan_valid = run_validator(domain_file, problem_file, plan)

    os.unlink(problem_file)

    print(f"\n{'='*60}")
    print("FINAL RESULT")
    print(f"{'='*60}")
    if syntax_valid and plan is not None and plan_valid:
        print("SUCCESS: Problem is valid and solvable")
    else:
        print("FAILED: Problem has issues")
    print(f"  Syntax Valid:  {'PASS' if syntax_valid else 'FAIL'}")
    print(f"  Plan Found:    {'PASS' if plan is not None else 'FAIL'}")
    print(f"  Plan Valid:    {'PASS' if plan_valid else 'FAIL'}")
    print(f"{'='*60}\n")
