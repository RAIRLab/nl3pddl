
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

# def plt_average_feedback_steps(ndf, model, pipeline):
#     # Only that made it to the evaluation stage
#     ndf = ndf[ndf['action_timeout'] == False]
#     #ndf = ndf[ndf['hde_timeout'] == False]

#     # map domain paths to domain names
#     ndf['domain_path'] = ndf['domain_path'].apply(
#         lambda x: x.split('/')[-1] if '/' in x else x)

#     stats = ndf.groupby(['domain_path', 'desc_class'])['hde_steps'].agg(["mean", "count", "std"])
#     ci95_hi = []
#     ci95_lo = []
#     ms = []
#     for i in stats.index:
#         m, c, s = stats.loc[i]
#         ci95_hi.append(m + 1.96*s/math.sqrt(c))
#         ci95_lo.append(max(m - 1.96*s/math.sqrt(c), 0))
#         ms.append(m)

#     grouped = ndf.groupby(['domain_path', 'desc_class'])[
#         'hde_steps'].mean().unstack()
#     # Grouped boxplot with error bars as 95% confidence intervals
#     ax = grouped.plot.bar()

#     #generate error bars based on ci_hi and ci_lo
#     for i, p in enumerate(ax.patches):
#         height = p.get_height()
#         if height == 0:
#             continue
#         #TODO: this works but needs to be fixed, if we ever have identical heights we cant get the index.
#         ind = ms.index(height)
#         ci_hi = ci95_hi[ind]
#         ci_lo = ci95_lo[ind]
#         plt.vlines(p.get_x() + p.get_width()/2, ci_lo, ci_hi, color='k')

#     plt.title(f'Average Domain Feedback Steps: {model} - {pipeline}')
#     plt.suptitle('')
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(f'figs/avgHDEbM-D-{model}-{pipeline}.png')

def plt_average_eval_all_domains(ndf, title=""):
    """ Y-axis: HDE score, X-axis: model, bars are summed over all domains, no error bars"""
    
    # Only that made it to the evaluation stage
    ndf = ndf[ndf['action_timeout'] == False]
    #ndf = ndf[ndf['hde_timeout'] == False]
    
    ndf['feedback_pipeline'] = ndf['feedback_pipeline'].replace({
        'none': 'No Feedback',
        'landmark-random-single': 'Landmark feedback',
        'landmark-search': 'Landmark feedback with search',
        'validate-random-single': 'Plan feedback',
        'validate-search': 'Plan feedback with search',
        'landmark-validate-random-single': 'Landmark + Plan feedback',
        'landmark - validate-search': 'Landmark + Plan feedback with search'
    })

    stats = ndf.groupby(['model', "feedback_pipeline"])['evals_passed'].agg(["mean", "count", "std"])

    ci95_hi = []
    ci95_lo = []
    ms = []
    for i in stats.index:
        m, c, s = stats.loc[i]
        ci95_hi.append(m + 1.96*s/math.sqrt(c))
        ci95_lo.append(max(m - 1.96*s/math.sqrt(c), 0))
        ms.append(m)

    grouped = ndf.groupby(['model', "feedback_pipeline"])['evals_passed'].mean().unstack()
    # Grouped boxplot with error bars as 95% confidence intervals
    ax = grouped.plot.bar(figsize=(12, 5))

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

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylim(top=10)
    plt.title(f'Average HDE Evaluation Score {title}')
    plt.suptitle('')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'figs/{title}.png')
    plt.cla()


# def plt_domain_failure_mode(ndf, model, pipeline):
#     # Group by domain and count action_timeout and hde_timeout
#     ndf['domain_path'] = ndf['domain_path'].apply(
#         lambda x: x.split('/')[-1] if '/' in x else x)
#     domains = ndf['domain_path'].unique()

#     fig, axs = plt.subplots(1, len(domains), figsize=(3 * len(domains), 4))
#     for ax, d in zip(axs, domains):
#         subset = ndf[ndf['domain_path'] == d]

#         action_timeout_count = subset['action_timeout'].sum()
#         hde_timeout_count = subset['hde_timeout'].sum()
#         successful_count = len(subset) - action_timeout_count - hde_timeout_count

#         sizes = [successful_count, action_timeout_count, hde_timeout_count]
#         colors = ['#66c2a5', '#fc8d62', '#8da0cb']

#         ax.pie(sizes, labels=None, autopct='%1.1f%%',
#                startangle=90, colors=colors)
#         ax.set_title(f'{model} - {d}')
#     plt.tight_layout()
#     labels = ['No Feedback Left', 'Action Timeout', 'Feedback Timeout']
#     #plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=1, labels=labels)
#     plt.legend(labels=labels, loc='lower center')
#     plt.savefig(f'figs/pie-{model}-{pipeline}.png')

# def plt_h_score_vs_true_score_progression(ndf, model, pipeline):
#     # Only that made it to the evaluation stage
#     ndf = ndf[ndf['action_timeout'] == False]

#     # map domain paths to domain names
#     ndf['domain_path'] = ndf['domain_path'].apply(
#         lambda x: x.split('/')[-1] if '/' in x else x)

#     for domain in ndf['domain_path'].unique():
#         domain_df = ndf[ndf['domain_path'] == domain]
#         plt.figure(figsize=(10, 6))
#         for desc_class in domain_df['desc_class'].unique():
#             class_df = domain_df[domain_df['desc_class'] == desc_class]
#             plt.plot(class_df['trial'], class_df['h_scores'], marker='o', label=f'H Scores - {desc_class}')
#             plt.plot(class_df['trial'], class_df['true_scores'], marker='x', label=f'True Scores - {desc_class}')

def get_latest_results_file():
    import glob
    import os
    files = glob.glob("results/*/results.csv")
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
        print(f"plotting results for {results_file}")

    save_previous_figs_and_clear()
    

    df = pd.read_csv(results_file)
    df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

    #df = df[(df['model'] != 'deepseek-chat') & (df['model'] != 'deepseek-reasoner')]
    # ndf = df[(df['feedback_pipeline'] == 'none')]
    # plt_average_eval_all_domains(ndf.copy(deep=True), title="none")
    # ndf = df[(df['feedback_pipeline'] == 'none') |  
    #          (df['feedback_pipeline'] == 'landmark-random-single') |
    #          (df['feedback_pipeline'] == 'validate-random-single')
    #         ]
    # plt_average_eval_all_domains(ndf.copy(deep=True), title="random") 
    # ndf = df[(df['feedback_pipeline'] == 'none') |  
    #         (df['feedback_pipeline'] == 'landmark-random-single') |
    #         (df['feedback_pipeline'] == 'validate-random-single') |
    #         (df['feedback_pipeline'] == 'landmark-search') |
    #         (df['feedback_pipeline'] == 'validate-search')
    #     ]
    df = df[df["domain_path"] != "data/domains/sudoku-9x9"]
    df = df[df["domain_path"] != "data/domains/sudoku"]
    ndf = df
    plt_average_eval_all_domains(ndf.copy(deep=True), title="all")
    for domain in df['domain_path'].unique():
        ndf = df[df['domain_path'] == domain]
        plt_average_eval_all_domains(ndf.copy(deep=True), title="domain-"+domain.split('/')[-1])