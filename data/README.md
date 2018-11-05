# Data Sources

## Food Pricing Data
 - `wfp_market_food_prices.csv` is from [Kaggle](https://www.kaggle.com/jboysen/global-food-prices). This dataset is around 80 MB.

 - We can also consider [the World Food
   Project](https://public.opendatasoft.com/explore/dataset/global-food-prices-database-wfp/table/?sort=period)
   for a significantly larger dataset (at least 1 GB).

## Food Nutrition Data

 - Consider
   [this](https://catalog.data.gov/dataset/mypyramid-food-raw-data-f9ed6) and
   [this](https://data.world/adamhelsinger/food-nutrition-information).

## Other Data Sources

 - `starbucks-breakfast.csv` is from
   [Starbucks](https://www.starbucks.com/menu/catalog/nutrition?food=hot-breakfast#view_control=nutrition).
   This original csv (as downloaded) was both corrupted and not in the correct
   format, and thus required preprocessing. Furthermore, it was missing pricing
   data. I cross-refereced [this
   website](https://www.fastfoodmenuprices.com/starbucks-prices/) for some
   prices, and mean-imputed the rest. This data set leaves much to be desired.
