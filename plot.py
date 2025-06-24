
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

results_file = "results/results-2025-06-24_07-48-48.csv"

# # ================================================================
# # Average HDE Steps by Model and Description Class

# df = pd.read_csv(results_file)

# # Filter out rows where action_runs == 5
# df = df[df['action_runs'] != 5]

# # Rename hde_runs to hde_steps
# df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

# # Compute average HDE Steps by model and description class
# grouped = df.groupby(['model', 'desc_class'])['hde_steps'].mean().unstack()

# # Plot grouped bar chart
# ax = grouped.plot(kind='bar', figsize=(8, 5))
# ax.set_xlabel('Model')
# ax.set_ylabel('Average HDE Steps')
# ax.set_title('Average HDE Steps by Model and Description Class')
# plt.xticks(rotation=0)
# plt.legend(title='Description Class')
# plt.tight_layout()

# plt.savefig('figs/avgHDEbM.png')

# # ==============================================================================
# # Average HDE Steps by Domain and Description Class

# df = pd.read_csv(results_file)

# # Filter out rows where action_runs == 5
# df = df[df['action_runs'] != 5]

# # Rename hde_runs to hde_steps
# df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

# # map domain paths to domain names
# df['domain_path'] = df['domain_path'].apply(
#     lambda x: x.split('/')[-1] if '/' in x else x)

# # Compute average HDE Steps by domain and description class
# grouped = df.groupby(['domain_path', 'desc_class'])[
#     'hde_steps'].mean().unstack()

# # Plot grouped bar chart
# ax = grouped.plot(kind='bar', figsize=(10, 6))
# ax.set_xlabel('Domain')
# ax.set_ylabel('Average HDE Steps')
# ax.set_title('Average HDE Steps by Domain and Description Class')
# plt.xticks(rotation=0)
# plt.legend(title='Description Class')
# plt.tight_layout()
# plt.savefig('figs/avgHDEbD.png')


# # ==============================================================================

# df = pd.read_csv(results_file)

# # Prepare counts
# models = df['model'].unique()
# data = []
# for m in models:
#     subset = df[df['model'] == m]
#     failed = (subset['action_runs'] == 5).sum()
#     successful = (subset['action_runs'] != 5).sum()
#     data.append({'model': m, 'successful': successful, 'failed': failed})

# summary = pd.DataFrame(data)

# # Plot
# plt.figure()
# plt.bar(summary['model'], summary['successful'], label='Successful')
# plt.bar(summary['model'], summary['failed'],
#         bottom=summary['successful'], label='Failed')
# plt.xlabel('Model')
# plt.ylabel('Count of Runs')
# plt.title('Successful vs Failed Runs by Model')
# plt.legend()
# plt.xticks(rotation=0)
# plt.tight_layout()

# plt.savefig('figs/SvFbM.png')

# # ==============================================================================
# df = pd.read_csv(results_file)
# for model in df['model'].unique():
#     df = pd.read_csv(results_file)

#     # Extract simple domain name
#     df['domain'] = df['domain_path'].apply(lambda x: x.split('/')[-1])

#     # Only look at model runs
#     df = df[df['model'] == model]

#     # Count failed and successful runs by domain
#     domains = df['domain'].unique()
#     data = []
#     for d in domains:
#         subset = df[df['domain'] == d]
#         failed = (subset['action_runs'] == 5).sum()
#         successful = (subset['action_runs'] != 5).sum()
#         data.append({'domain': d, 'successful': successful, 'failed': failed})

#     summary = pd.DataFrame(data).set_index('domain')

#     # Plot stacked bar chart
#     summary.plot(kind='bar', stacked=True)
#     plt.xlabel('Domain')
#     plt.ylabel('Count of Runs')
#     plt.title(f'Successful vs Failed Runs by Domain {model}')
#     plt.tight_layout()

#     plt.savefig(f'figs/SvFbD-{model}.png')

#     df = pd.read_csv("results.csv")

#     # Filter by model
#     df = df[df['model'] == model]

#     # Filter out rows where action_runs == 5
#     df = df[df['action_runs'] != 5]

#     # Rename hde_runs to hde_steps
#     df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

#     # map domain paths to domain names
#     df['domain_path'] = df['domain_path'].apply(
#         lambda x: x.split('/')[-1] if '/' in x else x)

#     # Compute average HDE Steps by domain and description class
#     grouped = df.groupby(['domain_path', 'desc_class'])[
#         'hde_steps'].mean().unstack()

#     # Plot grouped bar chart
#     ax = grouped.plot(kind='bar', figsize=(10, 6))
#     ax.set_xlabel('Domain')
#     ax.set_ylabel('Average HDE Steps')
#     ax.set_title(f'Average HDE Steps by Domain and Description Class: {model}')
#     plt.xticks(rotation=0)
#     plt.legend(title='Description Class')
#     plt.tight_layout()
#     plt.savefig(f'figs/avgHDEbD-{model}.png')


# ==============================================================================
# Average HDE Steps by Model and Domain Boxplot

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
