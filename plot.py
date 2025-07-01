
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
    #df = df[df['total_evals'] > 0]

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

    df = df[df['total_evals'] > 0]
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

#plot pie charts subfigs for each model of how many experiments failed 
# via action_timeout and hde_timeout, plot a separate chart for each domain
df = pd.read_csv(results_file)
for m in df['model'].unique():
    df = pd.read_csv(results_file)
    # Filter by model
    df = df[df['model'] == m]

    # Rename hde_runs to hde_steps
    df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

    #filter out HDE_timeout and total_evals < 0
    # df = df[df['total_evals'] > 0 | (df['action_timeout'] == False) & (df['hde_timeout'] == False)]

    # Group by domain and count action_timeout and hde_timeout
    df['domain_path'] = df['domain_path'].apply(
        lambda x: x.split('/')[-1] if '/' in x else x)
    domains = df['domain_path'].unique()

    fig, axs = plt.subplots(1, len(domains), figsize=(3 * len(domains), 4))
    for ax, d in zip(axs, domains):
        subset = df[df['domain_path'] == d]

        action_timeout_count = subset['action_timeout'].sum()
        hde_timeout_count = subset['hde_timeout'].sum()
        successful_count = len(subset) - action_timeout_count - hde_timeout_count

        sizes = [successful_count, action_timeout_count, hde_timeout_count]
        labels = ['Successful', 'Action Timeout', 'HDE Timeout']
        colors = ['#66c2a5', '#fc8d62', '#8da0cb']

        ax.pie(sizes, labels=labels, autopct='%1.1f%%',
               startangle=90, colors=colors)
        ax.set_title(f'{m} - {d}')
    plt.tight_layout()
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=1)
    plt.savefig(f'figs/pie-{m}.png')


