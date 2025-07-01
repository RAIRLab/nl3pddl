
"""
This script generates all the plots from the results.csv file.

TODO: Overhaul this entire file, it is slop.
"""

import math
import pandas as pd
import matplotlib.pyplot as plt

if __name__ != "__main__":
    raise RuntimeError("This script is intended to be run"
                       " directly, not imported.")

results_file = "results/results-2025-07-01_01-06-56.csv"

df = pd.read_csv(results_file)
for model in df['model'].unique():
    df = pd.read_csv(results_file)
    # Filter by model
    df = df[df['model'] == model]

    # Rename hde_runs to hde_steps
    df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

    # if action_runs == 5, then mark as timeout and set hde_steps to 25
    #df.loc[df['action_runs'] == 5, 'hde_steps'] = 25
    df = df[df['action_timeout'] == False]
    df = df[df['hde_timeout'] == False]

    # map domain paths to domain names
    df['domain_path'] = df['domain_path'].apply(
        lambda x: x.split('/')[-1] if '/' in x else x)

    stats = df.groupby(['domain_path', 'desc_class'])['hde_steps'].agg(["mean", "count", "std"])

    ci95_hi = []
    ci95_lo = []
    ms = []
    for i in stats.index:
        m, c, s = stats.loc[i]
        ci95_hi.append(m + 1.96*s/math.sqrt(c))
        ci95_lo.append(max(m - 1.96*s/math.sqrt(c), 0))
        ms.append(m)

    grouped = df.groupby(['domain_path', 'desc_class'])[
        'hde_steps'].mean().unstack()
    # Grouped boxplot with error bars as 95% confidence intervals
    ax = grouped.plot.bar()

    #generate error bars based on ci_hi and ci_lo
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        if height == 0:
            continue
        #TODO: this works but needs to be fixed, if we ever have identical heights we cant get the index.
        ind = ms.index(height)
        ci_hi = ci95_hi[ind]
        ci_lo = ci95_lo[ind]
        plt.vlines(p.get_x() + p.get_width()/2, ci_lo, ci_hi, color='k')

    plt.title(f'Average HDE Steps by Domain and Description Class: {model}')
    plt.suptitle('')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'figs/avgHDEbM-D-{model}.png')

# Plot the average tests passed by the model and description class
df = pd.read_csv(results_file)
for model in df['model'].unique():
    df = pd.read_csv(results_file)
    # Filter by model
    df = df[df['model'] == model]

    # Rename hde_runs to hde_steps
    df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

    # if action_runs == 5, then mark as timeout and set hde_steps to 25
    #df.loc[df['action_runs'] == 5, 'hde_steps'] = 25
    #df = df[df['action_timeout'] == False]
    #df = df[df['hde_timeout'] == False]

    # map domain paths to domain names
    df['domain_path'] = df['domain_path'].apply(
        lambda x: x.split('/')[-1] if '/' in x else x)

    stats = df.groupby(['domain_path', 'desc_class'])['evals_passed'].agg(["mean", "count", "std"])

    ci95_hi = []
    ci95_lo = []
    ms = []
    for i in stats.index:
        m, c, s = stats.loc[i]
        ci95_hi.append(m + 1.96*s/math.sqrt(c))
        ci95_lo.append(max(m - 1.96*s/math.sqrt(c), 0))
        ms.append(m)

    grouped = df.groupby(['domain_path', 'desc_class'])[
        'evals_passed'].mean().unstack()
    # Grouped boxplot with error bars as 95% confidence intervals
    ax = grouped.plot.bar()

    #generate error bars based on ci_hi and ci_lo
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        if height == 0:
            continue
        #TODO: this works but needs to be fixed, if we ever have identical heights we cant get the index.
        ind = ms.index(height)
        ci_hi = ci95_hi[ind]
        ci_lo = ci95_lo[ind]
        plt.vlines(p.get_x() + p.get_width()/2, ci_lo, ci_hi, color='k')

    plt.title(f'Evaluation Problems Passed by Domain and Description Class: {model}')
    plt.suptitle('')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'figs/avgEval-{model}.png')
