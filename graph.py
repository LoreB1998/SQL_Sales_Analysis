import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'Query_result_csv'

# ── Palette & stile globale ───────────────────────────────────────────────────
BG       = '#0f1117'
SURFACE  = '#1a1e2e'
BLUE     = '#4f9de8'
TEAL     = '#2ec4b6'
AMBER    = '#f5a623'
RED      = '#e05c5c'
GRAY     = '#6b7280'
WHITE    = '#e8eaf0'
LGRAY    = '#374151'

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor':   BG,
    'axes.edgecolor':   LGRAY,
    'axes.labelcolor':  WHITE,
    'xtick.color':      GRAY,
    'ytick.color':      GRAY,
    'text.color':       WHITE,
    'grid.color':       LGRAY,
    'grid.linewidth':   0.5,
    'font.family':      'DejaVu Sans',
})

def title_sub(fig, title, sub, y=0.97):
    fig.text(0.5, y,      title, ha='center', fontsize=14, fontweight='bold', color=WHITE)
    fig.text(0.5, y-0.05, sub,   ha='center', fontsize=10, color=GRAY)

def save(fig, name):
    fig.savefig(name, dpi=150, bbox_inches='tight', facecolor=BG)
    print(f'Salvato: {name}')

# ════════════════════════════════════════════════════════════════════════════════
# GRAFICO 1 — Customer Segmentation (torta LTV + barre avg LTV)
# ════════════════════════════════════════════════════════════════════════════════
df2 = pd.read_csv(DATA_DIR / 'Query1.csv')
df2 = df2.sort_values('customer_segment')
labels   = ['Low-Value', 'Mid-Value', 'High-Value']
ltv_vals = df2['total_ltv'].values
avg_vals = df2['avg_ltv'].values
counts   = df2['customer_count'].values
colors_seg = [RED, AMBER, TEAL]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
title_sub(fig, 'Customer Segmentation by Lifetime Value',
          'Revenue distribution and average LTV across customer segments')

# Torta
wedges, texts, autotexts = ax1.pie(
    ltv_vals, labels=None, colors=colors_seg,
    autopct='%1.1f%%', startangle=90,
    wedgeprops={'edgecolor': BG, 'linewidth': 2.5},
    pctdistance=0.72
)
for at in autotexts:
    at.set(color=BG, fontsize=11, fontweight='bold')
ax1.set_facecolor(BG)
legend_labels = [f'{l}  ({c:,} customers)' for l, c in zip(labels, counts)]
ax1.legend(wedges, legend_labels, loc='lower center',
           bbox_to_anchor=(0.5, -0.12), fontsize=9,
           facecolor=SURFACE, edgecolor=LGRAY, labelcolor=WHITE, framealpha=0.9)
ax1.set_title('Total LTV Distribution', color=WHITE, fontsize=11, pad=12)

# Barre avg LTV
bars = ax2.barh(labels, avg_vals, color=colors_seg, height=0.5)
for bar, val in zip(bars, avg_vals):
    ax2.text(bar.get_width() + 80, bar.get_y() + bar.get_height() / 2,
             f'${val:,.2f}', va='center', color=WHITE, fontsize=10)
ax2.set_xlabel('Average LTV per Customer ($)', fontsize=10)
ax2.set_title('Avg LTV per Segment', color=WHITE, fontsize=11, pad=12)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${int(v):,}'))
ax2.set_xlim(0, max(avg_vals) * 1.28)
ax2.grid(axis='x', alpha=0.3)
ax2.spines[['top', 'right']].set_visible(False)

plt.tight_layout(rect=[0, 0, 1, 0.90])
save(fig, 'chart_1_segmentation.png')
plt.close()

# ════════════════════════════════════════════════════════════════════════════════
# GRAFICO 2 — Customer Revenue by First Purchase Year (adjusted)
# ════════════════════════════════════════════════════════════════════════════════
df23 = pd.read_csv(DATA_DIR / 'Query23.csv').sort_values('cohort_year')
x_labels = df23['cohort_year'].astype(str).values
x = np.arange(len(x_labels))
customer_revenue = df23['customer_revenue'].values

# Trend esponenziale come nel grafico di riferimento
coeffs = np.polyfit(x, np.log(customer_revenue), 1)
a_fit, b_fit = np.exp(coeffs[1]), coeffs[0]
x_fit = np.linspace(0, len(x) - 1, 300)
y_fit = a_fit * np.exp(b_fit * x_fit)

fig, ax = plt.subplots(figsize=(12, 6.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
title_sub(fig, 'Customer Revenue by First Purchase Year',
          'Adjusted for Time in Market')

bars = ax.bar(x, customer_revenue, width=0.8, color=BLUE, alpha=0.85,
              zorder=2, label='Customer Revenue (Adjusted)')
line, = ax.plot(x_fit, y_fit, color=AMBER, linestyle='--', linewidth=2.4,
                zorder=3, label='Exponential Trend')

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=11, rotation=45)
ax.set_xlabel('Cohort Year', fontsize=11, labelpad=8, color=WHITE)
ax.set_ylabel('Customer Revenue ($)', fontsize=11, labelpad=10, color=WHITE)
ax.tick_params(axis='x', colors=GRAY)
ax.tick_params(axis='y', colors=GRAY)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
ax.set_ylim(0, max(customer_revenue) * 1.08)
ax.grid(axis='y', alpha=0.2)
ax.spines['left'].set_color(LGRAY)
ax.spines['bottom'].set_color(LGRAY)
ax.spines[['top', 'right']].set_visible(False)

patch = mpatches.Patch(facecolor=BLUE, alpha=0.85, label='Customer Revenue (Adjusted)')
ax.legend(handles=[line, patch], loc='upper right', facecolor=SURFACE,
          edgecolor=LGRAY, fontsize=10, framealpha=0.9, labelcolor=WHITE)

plt.tight_layout(rect=[0, 0, 1, 0.90])
save(fig, 'chart_2_cohort.png')
plt.close()

# ════════════════════════════════════════════════════════════════════════════════
# GRAFICO 3 — Monthly revenue + 3-month rolling avg LTV
# ════════════════════════════════════════════════════════════════════════════════
df12 = pd.read_csv(DATA_DIR / 'Query24.csv')
df12['year_month'] = pd.to_datetime(df12['year_month'])
df12 = df12.sort_values('year_month')
df12['rolling_rev']  = df12['total_revenue'].rolling(3, center=True).mean()
df12['rolling_cust'] = df12['total_customers'].rolling(3, center=True).mean()

fig, ax1 = plt.subplots(figsize=(14, 6))
title_sub(fig, 'Monthly Revenue & Customer Trends (3-Month Rolling Avg)',
          'Revenue and customer count peaked in 2022–2023, both declining in 2024')

ax2 = ax1.twinx()

ax1.fill_between(df12['year_month'], df12['total_revenue'] / 1e6,
                 alpha=0.15, color=TEAL)
ax1.plot(df12['year_month'], df12['rolling_rev'] / 1e6,
         color=TEAL, linewidth=2, label='Revenue (3mo avg)')

ax2.plot(df12['year_month'], df12['rolling_cust'],
         color=AMBER, linewidth=2, linestyle='--', label='Customers (3mo avg)')

ax1.set_xlabel('Month', fontsize=11, labelpad=8)
ax1.set_ylabel('Total Revenue ($M)', color=TEAL, fontsize=11, labelpad=10)
ax1.tick_params(axis='y', colors=TEAL)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:.1f}M'))
ax1.grid(axis='y', alpha=0.2)
ax1.spines[['top', 'right']].set_color(LGRAY)

ax2.set_ylabel('Total Customers', color=AMBER, fontsize=11, labelpad=10)
ax2.tick_params(axis='y', colors=AMBER)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
ax2.spines[['top', 'left']].set_color(LGRAY)

h1 = mpatches.Patch(color=TEAL,  label='Revenue (3mo rolling avg)')
h2, = ax1.plot([], [], color=AMBER, linestyle='--', linewidth=2, label='Customers (3mo rolling avg)')
ax1.legend(handles=[h1, h2], loc='upper left', facecolor=SURFACE,
           edgecolor=LGRAY, labelcolor=WHITE, fontsize=9, framealpha=0.9)

plt.tight_layout(rect=[0, 0, 1, 0.90])
save(fig, 'chart_3_monthly.png')
plt.close()

# ════════════════════════════════════════════════════════════════════════════════
# GRAFICO 4 — Retention / Churn per cohort (barre impilate %)
# ════════════════════════════════════════════════════════════════════════════════
df3 = pd.read_csv(DATA_DIR / 'Query3.csv')
active  = df3[df3['customer_status'] == 'Active'].set_index('cohort_year')
churned = df3[df3['customer_status'] == 'Churned'].set_index('cohort_year')
years   = active.index.astype(str).tolist()
act_pct = (active['status_pct'] * 100).values
churn_pct = (churned['status_pct'] * 100).values

fig, ax = plt.subplots(figsize=(11, 5.5))
title_sub(fig, 'Customer Retention & Churn by Cohort Year',
          'Churn stabilizes at ~90% across all cohorts — a systemic retention challenge')

x = np.arange(len(years))
w = 0.55
b1 = ax.bar(x, churn_pct, width=w, color=RED,  alpha=0.85, label='Churned')
b2 = ax.bar(x, act_pct,   width=w, color=TEAL, alpha=0.85, label='Active',
            bottom=churn_pct)

for xi, cp, ap in zip(x, churn_pct, act_pct):
    ax.text(xi, cp / 2,        f'{cp:.0f}%', ha='center', va='center',
            color=BG, fontsize=9, fontweight='bold')
    ax.text(xi, cp + ap / 2,   f'{ap:.0f}%', ha='center', va='center',
            color=BG, fontsize=9, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=11)
ax.set_xlabel('Cohort Year', fontsize=11, labelpad=8)
ax.set_ylabel('% of Customers', fontsize=11, labelpad=10)
ax.set_ylim(0, 108)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v)}%'))
ax.grid(axis='y', alpha=0.2)
ax.spines[['top', 'right']].set_visible(False)
ax.legend(facecolor=SURFACE, edgecolor=LGRAY, labelcolor=WHITE,
          fontsize=10, framealpha=0.9, loc='upper right')

plt.tight_layout(rect=[0, 0, 1, 0.90])
save(fig, 'chart_4_retention.png')
plt.close()

print('\nTutti i grafici generati.')