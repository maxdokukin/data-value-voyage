from dash import html, dash_table, dcc
from src.fetch.from_csv import fetch_final_goods_affordable
from components.topbar import get_topbar

# Parameters for fetching data
goods_list = [
    'bacon','bread','butter','coffee','eggs','flour','milk',
    'pork chop','round steak','sugar','gas'
]
regions = ['united states']
income_data_source = 'FRED'
salary_interval = 'monthly'

# Fetch decade data
# 1920s average affordability
df_1920s = fetch_final_goods_affordable(
    year_range=(1920, 1929),
    goods_list=goods_list,
    regions=regions,
    income_data_source=income_data_source,
    salary_interval=salary_interval,
    output_format='df'
)

# 2020s average affordability
df_2020s = fetch_final_goods_affordable(
    year_range=(2020, 2029),
    goods_list=goods_list,
    regions=regions,
    income_data_source=income_data_source,
    salary_interval=salary_interval,
    output_format='df'
)

# Map good names to units
unit_map = df_1920s.set_index('name')['good_unit'].to_dict()

# Compute average affordable quantities
avg_1920s = df_1920s.groupby('name')['final_goods_affordable'].mean()
avg_2020s = df_2020s.groupby('name')['final_goods_affordable'].mean()

# Build comparison records
comparison_records = []
for name in goods_list:
    unit = unit_map.get(name, '')
    val_1920 = int(round(avg_1920s.get(name, 0)))
    val_2020 = int(round(avg_2020s.get(name, 0)))
    delta = val_2020 - val_1920
    pct_change = round((delta / val_1920 * 100), 1) if val_1920 else 0
    comparison_records.append({
        'Good (Unit)': f"{name.title()} ({unit})",
        '1920s': val_1920,
        '2020s': val_2020,
        'Delta': delta,
        '% Change': pct_change
    })

# Sort by percent change descending
comparison_records = sorted(
    comparison_records,
    key=lambda x: x['% Change'],
    reverse=True
)

# Findings page layout
layout = html.Div(className='container-objectives', children=[
        get_topbar(current_path="/findings", overlay=False),

        html.Link(rel='stylesheet', href='/static/css/objective-styles.css'),

        # Written summary of findings
        html.Div(
            className="findings-summary",
            children=[
                html.H2('Key Findings'),
                html.P(
                    'Between the 1920s and the 2020s, the average consumer’s monthly purchasing power ' 
                    'declined for every good examined. Staple food items such as flour and sugar saw ' 
                    'the steepest drops—over 90%—while eggs remained the most resilient, decreasing by ' 
                    'approximately 13%. Goods like pork chops and bacon fell by 40–45%, and milk by about 57%. ' 
                    'Notably, butter became effectively unaffordable within average monthly income constraints.'
                ),
                html.P(
                    'These shifts underscore how sustained inflation has outpaced income growth, ' 
                    'making it increasingly difficult for consumers to maintain the same standard of living ' 
                    'a century ago. The dramatic declines in affordability for basic necessities ' 
                    'highlight widening economic pressures faced by households today.'
                )
            ]
        ),

        # Comparison table of affordability changes
        html.Div(
            className="table-container",
            children=dash_table.DataTable(
                id="affordable-comparison-table",
                columns=[{'name': col, 'id': col} for col in comparison_records[0].keys()],
                data=comparison_records,
                style_table={'height': 'auto', 'width': '100%'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '8px',
                    'fontSize': '14px'
                },
                style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': '#f4f4f4',
                    'padding': '8px'
                }
            )
        )
    ]
)
