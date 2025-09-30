### -r
python driver.py -r  390.36s user 49.27s system 13% cpu 53:32.81 total

### -g
Generated PDDL problem: data/gen_problems/feedback/blocks/problem-1.pddl
Generated data/gen_problems/feedback/blocks/problem-1.pddl
Unexpected Error occurred
ERROR:nl3pddl.logger:Failed to gen plans for data/gen_problems/feedback/blocks/problem-1.pddl, retrying...
Generated PDDL problem: data/gen_problems/feedback/blocks/problem-1.pddl
Generated data/gen_problems/feedback/blocks/problem-1.pddl
Unexpected Error occurred
ERROR:nl3pddl.logger:Failed to gen plans for data/gen_problems/feedback/blocks/problem-1.pddl, retrying...
Generated PDDL problem: data/gen_problems/feedback/blocks/problem-1.pddl
Generated data/gen_problems/feedback/blocks/problem-1.pddl
Unexpected Error occurred
ERROR:nl3pddl.logger:Failed to gen plans for data/gen_problems/feedback/blocks/problem-1.pddl, retrying...
Generated PDDL problem: data/gen_problems/feedback/blocks/problem-1.pddl
Generated data/gen_problems/feedback/blocks/problem-1.pddl
^CTraceback (most recent call last):
  File "/home/do/rair/nl3pddl/driver.py", line 42, in <module>
    n3p.generate_problems()
  File "/home/do/rair/nl3pddl/nl3pddl/gen_problems.py", line 130, in generate_problems
    plans = gen_problem_till_success(generator, i, problem_file, domain_file)
  File "/home/do/rair/nl3pddl/nl3pddl/gen_problems.py", line 101, in gen_problem_till_success
    plans = plan_file(
  File "/home/do/rair/nl3pddl/nl3pddl/gen_problems.py", line 57, in plan_file
    _ = subprocess.check_output(args, stderr=subprocess.DEVNULL)
  File "/usr/lib/python3.10/subprocess.py", line 421, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
  File "/usr/lib/python3.10/subprocess.py", line 505, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
  File "/usr/lib/python3.10/subprocess.py", line 1141, in communicate
    stdout = self.stdout.read()
KeyboardInterrupt

python driver.py -g  4162.67s user 2496.86s system 100% cpu 1:50:31.62 total
