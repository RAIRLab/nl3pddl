
"""
This script generates all the plots from the results.csv file.
"""

import shutil
import os
import math
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

pd.options.mode.copy_on_write = True

def plt_average_feedback_steps(ndf, model, pipeline):
    # Only that made it to the evaluation stage
    ndf = ndf[ndf['action_timeout'] == False]
    #ndf = ndf[ndf['hde_timeout'] == False]

    # map domain paths to domain names
    ndf['domain_path'] = ndf['domain_path'].apply(
        lambda x: x.split('/')[-1] if '/' in x else x)

    stats = ndf.groupby(['domain_path', 'desc_class'])['hde_steps'].agg(["mean", "count", "std"])

    ci95_hi = []
    ci95_lo = []
    ms = []
    for i in stats.index:
        m, c, s = stats.loc[i]
        ci95_hi.append(m + 1.96*s/math.sqrt(c))
        ci95_lo.append(max(m - 1.96*s/math.sqrt(c), 0))
        ms.append(m)

    grouped = ndf.groupby(['domain_path', 'desc_class'])[
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

    plt.title(f'Average Domain Feedback Steps: {model} - {pipeline}')
    plt.suptitle('')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'figs/avgHDEbM-D-{model}-{pipeline}.png')

def plt_average_eval(ndf, model, pipeline):
    # Only that made it to the evaluation stage
    # ndf = ndf[ndf['total_evals'] > 0]

    # map domain paths to domain names
    ndf['domain_path'] = ndf['domain_path'].apply(
        lambda x: x.split('/')[-1] if '/' in x else x)

    stats = ndf.groupby(['domain_path', 'desc_class'])['evals_passed'].agg(["mean", "count", "std"])

    ci95_hi = []
    ci95_lo = []
    ms = []
    for i in stats.index:
        m, c, s = stats.loc[i]
        ci95_hi.append(m + 1.96*s/math.sqrt(c))
        ci95_lo.append(max(m - 1.96*s/math.sqrt(c), 0))
        ms.append(m)

    grouped = ndf.groupby(['domain_path', 'desc_class'])[
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

    plt.title(f'Evaluations Passed: {model} - {pipeline}')
    plt.suptitle('')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'figs/avgEval-{model}-{pipeline}.png')

def plt_domain_failure_mode(ndf, model, pipeline):
    # Group by domain and count action_timeout and hde_timeout
    ndf['domain_path'] = ndf['domain_path'].apply(
        lambda x: x.split('/')[-1] if '/' in x else x)
    domains = ndf['domain_path'].unique()

    fig, axs = plt.subplots(1, len(domains), figsize=(3 * len(domains), 4))
    for ax, d in zip(axs, domains):
        subset = ndf[ndf['domain_path'] == d]

        action_timeout_count = subset['action_timeout'].sum()
        hde_timeout_count = subset['hde_timeout'].sum()
        successful_count = len(subset) - action_timeout_count - hde_timeout_count

        sizes = [successful_count, action_timeout_count, hde_timeout_count]
        colors = ['#66c2a5', '#fc8d62', '#8da0cb']

        ax.pie(sizes, labels=None, autopct='%1.1f%%',
               startangle=90, colors=colors)
        ax.set_title(f'{model} - {d}')
    plt.tight_layout()
    labels = ['No Feedback Left', 'Action Timeout', 'Feedback Timeout']
    #plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=1, labels=labels)
    plt.legend(labels=labels, loc='lower center')
    plt.savefig(f'figs/pie-{model}-{pipeline}.png')


def get_latest_results_file():
    import glob
    import os
    files = glob.glob("results/results-*.csv")
    if not files:
        raise FileNotFoundError("No results files found.")
    latest_file = max(files, key=os.path.getctime)
    return latest_file

# Save all figs in the fig director as a tar to the old_figs dir and clear the fig directory
def save_previous_figs_and_clear():
    fig_dir = "figs"
    old_figs_dir = "old_figs"

    # Create figs directory if it doesn't exist
    os.makedirs(fig_dir, exist_ok=True)

        # return early if the figs directory is empty
    if not os.listdir("figs"):
        return

    # Create old_figs directory if it doesn't exist
    os.makedirs(old_figs_dir, exist_ok=True)

    # Create a tarball of everything in figs, named with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.make_archive(f"{old_figs_dir}/figs-{timestamp}", 'tar', fig_dir)

    # Clear the figs directory
    for file in os.listdir(fig_dir):
        file_path = os.path.join(fig_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def plot_all_figures(results_file = None):
    if results_file is None:
        results_file = get_latest_results_file()

    save_previous_figs_and_clear()

    df = pd.read_csv(results_file)
    for model in df['model'].unique():
        for pipeline in df['feedback_pipeline'].unique():
            ndf = \
              df[(df['model'] == model) & (df['feedback_pipeline'] == pipeline)]
            ndf.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)
            plt_average_feedback_steps(ndf.copy(deep=True), model, pipeline)
            plt_average_eval(ndf.copy(deep=True), model, pipeline)
            plt_domain_failure_mode(ndf.copy(deep=True), model, pipeline)