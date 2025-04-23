import json
import pandas as pd

# ── CSV FILE PATH CONSTANTS ────────────────────────────────────────────
INCOMES_CSV       = "data/csv/incomes.csv"
GOODS_PRICES_CSV  = "data/csv/goods_prices.csv"
# ───────────────────────────────────────────────────────────────────────

def fetch_incomes(
    year_range=(1990, 2000),
    data_source_name='FRED',
    regions=None,
    output_format='df'
):
    start_year, end_year = year_range
    if regions is None:
        regions = ['united states']

    df = pd.read_csv(INCOMES_CSV, dtype={'region': str, 'source_name': str})
    # ensure types
    df['year'] = df['year'].astype(int)

    # filter
    mask = (
        df['year'].between(start_year, end_year) &
        (df['source_name'] == data_source_name) &
        df['region'].isin(regions)
    )
    df = df.loc[mask, ['year', 'average_income_unadjusted', 'region']].sort_values('year')

    if output_format == 'df':
        return df.reset_index(drop=True)
    else:
        return df.to_json(orient='records')

def fetch_goods_prices(
    year_range=(1990, 2000),
    goods_list=None,
    use_year_averages=True,
    output_format='df'
):
    start_year, end_year = year_range

    df = pd.read_csv(GOODS_PRICES_CSV, parse_dates=['date'])
    df['year'] = df['date'].dt.year

    # basic filters
    mask = df['year'].between(start_year, end_year)
    if goods_list:
        mask &= df['name'].isin(goods_list)
    if use_year_averages:
        mask &= df['date'].dt.strftime('%m-%d') == '07-02'
    else:
        mask &= df['date'].dt.strftime('%m-%d') != '07-02'

    df = df.loc[mask, ['name', 'price', 'date', 'good_unit', 'data_source', 'year']]

    # keep latest entry per good/year
    df = (
        df.sort_values('date', ascending=False)
          .drop_duplicates(subset=['name', 'year'], keep='first')
          .sort_values(['name', 'date'], ascending=[True, False])
          .reset_index(drop=True)
    )

    if output_format == 'df':
        return df
    elif output_format == 'json':
        return df.to_json(orient='records', date_format='iso')
    else:
        raise ValueError("Output formats supported: 'df' or 'json'")

def fetch_final_goods_affordable(
    year_range=(1990, 2000),
    goods_list=None,
    regions=None,
    income_data_source='FRED',
    salary_interval='monthly',
    output_format='df'
):
    inc = fetch_incomes(
        year_range=year_range,
        data_source_name=income_data_source,
        regions=regions,
        output_format='df'
    )
    goods = fetch_goods_prices(
        year_range=year_range,
        goods_list=goods_list,
        use_year_averages=True,
        output_format='df'
    )
    df = pd.merge(goods, inc, on='year', how='inner')

    if salary_interval == 'monthly':
        df['final_goods_affordable'] = (df['average_income_unadjusted'] / 12) / df['price']
    elif salary_interval == 'annually':
        df['final_goods_affordable'] = df['average_income_unadjusted'] / df['price']
    else:
        raise ValueError("salary_interval must be 'monthly' or 'annually'")

    df['final_goods_affordable'] = df['final_goods_affordable'].astype(int)
    df = df[['name', 'final_goods_affordable', 'good_unit', 'date', 'year', 'region']]

    return df if output_format == 'df' else df.to_json(orient='records')

def fetch_income_intervals_to_purchase(
    year_range=(1990, 2000),
    goods_list=None,
    regions=None,
    income_data_source='FRED',
    salary_interval='annually',
    output_format='df'
):
    inc = fetch_incomes(
        year_range=year_range,
        data_source_name=income_data_source,
        regions=regions,
        output_format='df'
    )
    goods = fetch_goods_prices(
        year_range=year_range,
        goods_list=goods_list,
        use_year_averages=True,
        output_format='df'
    )
    df = pd.merge(goods, inc, on='year', how='inner')

    if salary_interval == 'monthly':
        interval = inc['average_income_unadjusted'] / 12
    else:
        interval = inc['average_income_unadjusted']

    df['income_intervals_to_purchase'] = (df['price'] / interval).astype(float)
    df = df[['name', 'income_intervals_to_purchase', 'good_unit', 'date', 'year', 'region']]

    return df if output_format == 'df' else df.to_json(orient='records')

def fetch_bea_incomes():
    df = pd.read_csv(INCOMES_CSV, dtype={'source_name': str})
    df = df[df['source_name'] == 'BEA'][['year', 'average_income_unadjusted', 'region', 'source_name']]
    return df.sort_values('year').reset_index(drop=True)

if __name__ == '__main__':
    # Example:
    # print(fetch_incomes((1929, 2024), data_source_name='FRED', regions=['united states']))
    pass
