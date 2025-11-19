import os
import glob
import re
import sys
import tempfile
import io
import contextlib
from kstar_planner import planners
import traceback
import subprocess
from pathlib import Path

from nl3pddl.problem_generators import PROBLEM_GENERATORS
from nl3pddl.config import NUM_EVAL_PROBLEMS, NUM_FEEDBACK_PROBLEMS, PLANS_PER_PROBLEM
from nl3pddl.gen_problems import generate_problems
from nl3pddl.gen_landmarks import generate_landmarks
from nl3pddl.config import (
    FEEDBACK_PROBLEMS_DIR,
    EVAL_PROBLEMS_DIR,
)
import pddl

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
    """Run the full test suite for all problem generators and dataset outputs."""
    print(f"\n{'='*60}")
    print("RUNNING TEST SUITE FOR ALL PROBLEM GENERATORS")
    print(f"{'='*60}\n")

    # First, generate the full problem sets and landmarks
    print("Generating problems per config (feedback/evaluation)...")
    generate_problems()
    print("Generating landmarks for feedback problems...")
    generate_landmarks()

    # Validate dataset layout and counts
    _validate_generated_sets()

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


def _validate_generated_sets():
    """Validate generated feedback/evaluation problems and landmarks per config.

    Checks:
    - Exactly NUM_FEEDBACK_PROBLEMS and NUM_EVAL_PROBLEMS for each domain
    - Exactly PLANS_PER_PROBLEM plan files per problem
    - VAL Parser succeeds for each generated problem
    - Landmark JSON exists for each feedback problem
    """
    def get_pddl_domain_name(folder_name: str) -> str:
        dom_file = Path(DOMAINS_DIR) / folder_name / "ground.pddl"
        try:
            dom = pddl.parse_domain(str(dom_file))
            return dom.name
        except Exception:
            return folder_name

    def problem_path(base_dir: str, pddl_domain_name: str, idx: int) -> Path:
        return Path(base_dir) / pddl_domain_name / f"problem-{idx}.pddl"

    def plan_glob(base_dir: str, pddl_domain_name: str, idx: int) -> list[Path]:
        patt = Path(base_dir) / pddl_domain_name / f"plan-{idx}-*.txt"
        return [Path(p) for p in sorted(glob.glob(str(patt)))]

    def landmark_path(domain: str, idx: int) -> Path:
        return Path("data/gen_landmarks") / domain / f"problem-{idx}.json"

    def domain_file(domain: str) -> Path:
        return Path(DOMAINS_DIR) / domain / "ground.pddl"

    failures = []

    targets = [
        (FEEDBACK_PROBLEMS_DIR, NUM_FEEDBACK_PROBLEMS, "feedback"),
        (EVAL_PROBLEMS_DIR, NUM_EVAL_PROBLEMS, "evaluation"),
    ]

    for base, expected_n, label in targets:
        for folder_name in PROBLEM_GENERATORS.keys():
            pddl_name = get_pddl_domain_name(folder_name)
            base_domain_dir = Path(base) / pddl_name
            if not base_domain_dir.exists():
                failures.append(f"Missing directory: {base_domain_dir}")
                continue

            # Check exact indices 1..expected_n
            for i in range(1, expected_n + 1):
                p_path = problem_path(base, pddl_name, i)
                if not p_path.exists():
                    failures.append(f"Missing {label} problem: {p_path}")
                    continue

                # Syntax check
                syntax_ok = run_parser(domain_file(folder_name), p_path)
                if not syntax_ok:
                    failures.append(f"VAL Parser failed for {label}:{pddl_name} problem-{i}")

                # Plans per problem
                plans = plan_glob(base, pddl_name, i)
                if len(plans) != PLANS_PER_PROBLEM:
                    failures.append(
                        f"{label}:{pddl_name} problem-{i} expected {PLANS_PER_PROBLEM} plans, found {len(plans)}"
                    )
                # Validate first plan if present and syntax is ok
                if syntax_ok and plans:
                    # Convert text plan to actions list for run_validator()
                    try:
                        actions = []
                        with open(plans[0], 'r', encoding='utf-8') as pf:
                            for line in pf:
                                line = line.strip()
                                if not line:
                                    continue
                                if line.startswith('(') and line.endswith(')'):
                                    actions.append(line[1:-1])
                        if not actions or not run_validator(domain_file(folder_name), p_path, actions):
                            failures.append(f"VAL Validate failed for {label}:{pddl_name} problem-{i} using {plans[0].name}")
                    except Exception as e:
                        failures.append(f"Error reading/validating plan for {label}:{pddl_name} problem-{i}: {e}")

            # Ensure no extras beyond expected_n
            existing = sorted(glob.glob(str(base_domain_dir / "problem-*.pddl")))
            for path in existing:
                name = os.path.basename(path)
                m = re.match(r"problem-(\d+)\.pddl$", name)
                if m and int(m.group(1)) > expected_n:
                    failures.append(f"{label}:{pddl_name} has extra problem file: {name}")

    # Landmarks for feedback problems
    for folder_name in PROBLEM_GENERATORS.keys():
        pddl_name = get_pddl_domain_name(folder_name)
        for i in range(1, NUM_FEEDBACK_PROBLEMS + 1):
            lmp = landmark_path(pddl_name, i)
            if not lmp.exists():
                failures.append(f"Missing landmark file: {lmp}")

    if failures:
        print(f"\n{'-'*60}")
        print("DATASET VALIDATION FAILURES")
        print(f"{'-'*60}")
        for f in failures:
            print(f"- {f}")
        print(f"{'-'*60}\n")
        # Do not raise to allow per-generator tests to continue, but signal clearly
    else:
        print("Dataset validation passed: counts, plans, syntax, and landmarks look good.\n")


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
