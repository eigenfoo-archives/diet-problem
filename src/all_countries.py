'''
Solving the diet problem for all countries.

This script reads nutrition and pricing data, groups the data by country,
locality and market (in that order) and solves the diet problem for each group,
and writes the results to an output csv. The results include the minimum, the
minimum value, the optimization status, and the slack (a.k.a. dual) variables.

Author: George Ho (gh@eigenfoo.xyz)
'''

import numpy as np
import pandas as pd
from scipy.optimize import linprog

NUTRITION_FILE = '../data/nutrition.csv'
PRICING_FILE = '../data/pricing.csv'

# If a particular market does not have a food, we set
# its price to be "infinity" (i.e. 999999). np.nan
# does not suffice, as we must have float datatypes.
INFINITY = 999999

# Read in data csvs
nutrition = pd.read_csv(NUTRITION_FILE, index_col=0)
pricing = pd.read_csv(PRICING_FILE, index_col=0)

# Group by country, locality and market, in that order.
grouped = pricing.groupby(['country_name', 'locality_name', 'market_name'])

solns = {}

# Solve diet problem for all groups
# (i.e. all markets in all localities in all countries)
for market, idx in grouped.groups.items():
    df = pricing.loc[idx]

    # Form A matrix (nutritional values of each food) and
    # b vector (dietary requirements for each nutrient).
    # Dietary requirements: protein, fat, carbs, fiber, in that order.
    # From http://www.netrition.com/rdi_page.html
    A_ub = -np.transpose(nutrition.values)
    b_ub = -np.array([50, 65, 300, 25])

    # Construct c vector appropriately (i.e. add INFINITYs to
    # the appropriate foods)
    c = pd.Series(data=INFINITY*np.ones(84), index=nutrition.index)
    c.loc[df.commodity_name] = df.price.values
    c = c.values

    # Solve LP using the default simplex algorithm.
    solns[market] = linprog(c, A_ub, b_ub)

# Collect optimization status, minimum value and minimum into one array
data = np.hstack([
    np.transpose(
        np.vstack([[soln.status for soln in solns.values()],
                   [soln.fun for soln in solns.values()]])
    ),
    [soln.x for soln in solns.values()],
    [soln.slack for soln in solns.values()]
])

# Cast array in a dataframe and save to a csv.
cols = (['status', 'fun']
        + nutrition.index.tolist()
        + ['protein_ineq', 'fat_ineq', 'carbs_ineq', 'fiber_ineq'])

df = pd.DataFrame(data=data,
                  index=solns.keys(),
                  columns=cols)
df.to_csv('all_countries.csv')
