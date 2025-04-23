from dash import html, dash_table, dcc
from src.fetch.from_sqlite import fetch_final_goods_affordable
from components.button import get_button

# Parameters
db_path = 'data/db/sqlite/database.sqlite'
goods_list = [
    'bacon','bread','butter','coffee','eggs','flour','milk',
    'pork chop','round steak','sugar','gas'
]
regions = ['united states']
income_data_source = 'FRED'
salary_interval = 'monthly'

# Fetch decade data
df_1920s = fetch_final_goods_affordable(
    db_path=db_path,
    year_range=(1920, 1929),
    goods_list=goods_list,
    regions=regions,
    income_data_source=income_data_source,
    salary_interval=salary_interval,
    output_format='df'
)

df_2020s = fetch_final_goods_affordable(
    db_path=db_path,
    year_range=(2020, 2029),
    goods_list=goods_list,
    regions=regions,
    income_data_source=income_data_source,
    salary_interval=salary_interval,
    output_format='df'
)

# Map each good to its unit (assumes unit doesn't change across decades)
unit_map = df_1920s.set_index('name')['good_unit'].to_dict()

# Compute average affordable quantity per good
avg_1920s = df_1920s.groupby('name')['final_goods_affordable'].mean()
avg_2020s = df_2020s.groupby('name')['final_goods_affordable'].mean()

# Build comparison records ensuring equal lengths
comparison_records = []
for name in goods_list:
    unit = unit_map.get(name, '')
    val_1920 = int(round(avg_1920s.get(name, 0)))
    val_2020 = int(round(avg_2020s.get(name, 0)))
    delta = val_2020 - val_1920
    pct_change = round((delta / val_1920 * 100), 1) if val_1920 else 0
    comparison_records.append({
        'Good (Unit)': f"{name} ({unit})",
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

# Slide layout with a styled "Learn More" button in the top-right
layout = html.Div(
    className="section-slide",
    children=[
        get_button(
            label="Learn More about this Method",
            link="/methods/quantity-affordable",
            color="#693382",
            size=(300, 50)
        ),
        html.Div(
            className="table-container",
            children=dash_table.DataTable(
                id="affordable-comparison-table",
                columns=[{'name': col, 'id': col} for col in comparison_records[0].keys()],
                data=comparison_records,
                style_table={'height': '100%', 'width': '100%'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'color': 'black'
                },
                style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': '#f0f0f0',
                    'color': 'black'
                }
            )
        ),
        html.Div(className="scroll-hint", children="↓")
    ]
)
