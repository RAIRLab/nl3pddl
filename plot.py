
"""
This script generates all the plots from the results.csv file.

TODO: Overhaul this entire file, it is slop.
"""

import pandas as pd
import matplotlib.pyplot as plt

if __name__ != "__main__":
    raise RuntimeError("This script is intended to be run" \
    " directly, not imported.")

# ==============================================================================
# Average HDE Steps by Model and Description Class

df = pd.read_csv("results.csv")

# Filter out rows where action_runs == 5
df = df[df['action_runs'] != 5]

# Rename hde_runs to hde_steps
df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

# Compute average HDE Steps by model and description class
grouped = df.groupby(['model', 'desc_class'])['hde_steps'].mean().unstack()

# Plot grouped bar chart
ax = grouped.plot(kind='bar', figsize=(8, 5))
ax.set_xlabel('Model')
ax.set_ylabel('Average HDE Steps')
ax.set_title('Average HDE Steps by Model and Description Class')
plt.xticks(rotation=0)
plt.legend(title='Description Class')
plt.tight_layout()

plt.savefig('figs/avgHDEbM.png')

# ==============================================================================
# Average HDE Steps by Domain and Description Class

df = pd.read_csv("results.csv")

# Filter out rows where action_runs == 5
df = df[df['action_runs'] != 5]

# Rename hde_runs to hde_steps
df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

# map domain paths to domain names
df['domain_path'] = df['domain_path'].apply(lambda x: x.split('/')[-1] if '/' in x else x)

# Compute average HDE Steps by domain and description class
grouped = df.groupby(['domain_path', 'desc_class'])['hde_steps'].mean().unstack()

# Plot grouped bar chart
ax = grouped.plot(kind='bar', figsize=(10, 6))
ax.set_xlabel('Domain')
ax.set_ylabel('Average HDE Steps')
ax.set_title('Average HDE Steps by Domain and Description Class')
plt.xticks(rotation=0)
plt.legend(title='Description Class')
plt.tight_layout()
plt.savefig('figs/avgHDEbD.png')


# ==============================================================================

df = pd.read_csv("results.csv")

# Prepare counts
models = df['model'].unique()
data = []
for m in models:
    subset = df[df['model'] == m]
    failed = (subset['action_runs'] == 5).sum()
    successful = (subset['action_runs'] != 5).sum()
    data.append({'model': m, 'successful': successful, 'failed': failed})

summary = pd.DataFrame(data)

# Plot
plt.figure()
plt.bar(summary['model'], summary['successful'], label='Successful')
plt.bar(summary['model'], summary['failed'], bottom=summary['successful'], label='Failed')
plt.xlabel('Model')
plt.ylabel('Count of Runs')
plt.title('Successful vs Failed Runs by Model')
plt.legend()
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig('figs/SvFbM.png')

# ==============================================================================
df = pd.read_csv("results.csv")
for model in df['model'].unique():
    df = pd.read_csv("results.csv")

    # Extract simple domain name
    df['domain'] = df['domain_path'].apply(lambda x: x.split('/')[-1])

    # Only look at model runs
    df = df[df['model'] == model]

    # Count failed and successful runs by domain
    domains = df['domain'].unique()
    data = []
    for d in domains:
        subset = df[df['domain'] == d]
        failed = (subset['action_runs'] == 5).sum()
        successful = (subset['action_runs'] != 5).sum()
        data.append({'domain': d, 'successful': successful, 'failed': failed})

    summary = pd.DataFrame(data).set_index('domain')

    # Plot stacked bar chart
    summary.plot(kind='bar', stacked=True)
    plt.xlabel('Domain')
    plt.ylabel('Count of Runs')
    plt.title(f'Successful vs Failed Runs by Domain {model}')
    plt.tight_layout()

    plt.savefig(f'figs/SvFbD-{model}.png')

    df = pd.read_csv("results.csv")

    # Filter by model
    df = df[df['model'] == model]

    # Filter out rows where action_runs == 5
    df = df[df['action_runs'] != 5]

    # Rename hde_runs to hde_steps
    df.rename(columns={'hde_runs': 'hde_steps'}, inplace=True)

    # map domain paths to domain names
    df['domain_path'] = df['domain_path'].apply(lambda x: x.split('/')[-1] if '/' in x else x)

    # Compute average HDE Steps by domain and description class
    grouped = df.groupby(['domain_path', 'desc_class'])['hde_steps'].mean().unstack()

    # Plot grouped bar chart
    ax = grouped.plot(kind='bar', figsize=(10, 6))
    ax.set_xlabel('Domain')
    ax.set_ylabel('Average HDE Steps')
    ax.set_title(f'Average HDE Steps by Domain and Description Class: {model}')
    plt.xticks(rotation=0)
    plt.legend(title='Description Class')
    plt.tight_layout()
    plt.savefig(f'figs/avgHDEbD-{model}.png')

# ==============================================================================
