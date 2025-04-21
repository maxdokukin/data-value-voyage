import os
import pandas as pd
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', '..', 'data', 'csv')

def housing_sankey(selected_year):
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    df = pd.read_csv(csv_path)

    # Filter to July of each year
    df = df[df['Year'].str.endswith('-07')]
    df['Year'] = df['Year'].str[:4]
    df = df[df['Year'] == str(selected_year)]

    row = df.iloc[0]
    price = row['Median Home Price']
    down_payment = 0.2 * price
    mortgage = 0.8 * price
    rate = row['Interest Rate'] / 100
    tax = row['Property Tax'] * 30
    insurance = row['Home Insurance'] * 30

    # Monthly mortgage payment (principal + interest over 30 years)
    monthly_payment = (mortgage * rate / 12) / (1 - (1 + rate / 12) ** -360)
    total_mortgage_payment = monthly_payment * 360

    total_cost = down_payment + total_mortgage_payment + tax + insurance

    label = [
        f"Listing Price (${round(price):.0f})",                   # 0
        f"Down Payment (${round(down_payment):.0f})",             # 1
        f"Mortgage Principal (${round(mortgage):.0f})",           # 2
        "30-Year Additional Costs",                              # 3
        f"Total Mortgage Payments (${round(total_mortgage_payment):.0f})",  # 4
        f"Taxes (${round(tax):.0f})",                             # 5
        f"Insurance (${round(insurance):.0f})",                   # 6
        f"True Cost (${round(total_cost):.0f})"                   # 7
    ]


    # Sankey flow definitions
    source = [0,0,2,3,3,3,4,5,6,1]
    target = [1,2,3,4,5,6,7,7,7,7]
    value = [
        down_payment,
        mortgage,
        mortgage,
        total_mortgage_payment,
        tax,
        insurance,
        total_mortgage_payment,
        tax,
        insurance,
        down_payment
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=label,
            pad=15,
            thickness=20,
            color=[
                "rgba(68, 114, 196, 0.8)",  # Dark Blue - Node 1
                "rgba(114, 170, 219, 0.8)", # Light Blue - Node 2
                "rgba(102, 194, 165, 0.8)", # Green - Node 3
                "rgba(44, 160, 44, 0.8)",   # Dark Green - Node 4
                "rgba(158, 218, 179, 0.8)", # Light Green - Node 5
                "rgba(174, 199, 102, 0.8)", # Olive Green - Node 6
                "rgba(148, 103, 189, 0.8)", # Purple - Node 7
                "rgba(214, 39, 40, 0.8)",   # Red - Node 8
            ]
        ),
        link=dict( 
            source=source,
            target=target,
            value=value,
            color=[
                "rgba(68, 114, 196, 0.6)",  # Dark Blue - Listing Price
                "rgba(114, 170, 219, 0.6)", # Light Blue - Down Payment
                "rgba(102, 194, 165, 0.6)", # Green - Mortgage Principal
                "rgba(44, 160, 44, 0.6)",   # Dark Green - 30-Year Additional Costs
                "rgba(158, 218, 179, 0.6)", # Light Green - Total Mortgage Payments
                "rgba(174, 199, 102, 0.6)", # Olive Green - Taxes
                "rgba(148, 103, 189, 0.6)", # Purple - InsuranceTrue c
                "rgba(214, 39, 40, 0.6)",   # Red - True Cost
                "rgba(174, 199, 102, 0.6)", # Olive Green - Taxes (duplicate for link consistency)
                "rgba(148, 103, 189, 0.6)", # Purple - Insurance (duplicate for link consistency)
            ]
        )
    )])

    fig.update_layout(
        title_text=f"{selected_year} Home: ${round(price):,.0f} @ {round(rate * 100, 1)}%\nTotal 30-Year Cost: ${round(total_cost):,.0f}",
        font_size=14
    )

    return fig

def income_affordability_sankey(selected_year):
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    df = pd.read_csv(csv_path)

    # Filter to July entries
    df = df[df['Year'].str.endswith('-07')]
    df['Year'] = df['Year'].str[:4]
    df = df[df['Year'] == str(selected_year)]

    if df.empty:
        return go.Figure().update_layout(
            title_text=f"No data available for July {selected_year}",
            font_size=14
        )

    row = df.iloc[0]
    annual_income = row['Median Income']
    monthly_income = annual_income / 12
    taxes = monthly_income * 0.22
    after_tax = monthly_income - taxes
    housing_budget = after_tax * 0.30
    remaining_income = after_tax * 0.70

    label = [
        f"Monthly Income (${monthly_income:.2f})",
        f"Taxes (22%) (${taxes:.2f})",
        f"After Tax (${after_tax:.2f})",
        f"Housing Budget (30%) (${housing_budget:.2f})",
        f"Remaining Income (70%) (${remaining_income:.2f})"
    ]

    source = [0, 0, 2, 2]
    target = [1, 2, 3, 4]
    value = [
        float(taxes),
        float(after_tax),
        float(housing_budget),
        float(remaining_income)
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=label,
            pad=15,
            thickness=20,
            color=[
                "rgba(68, 114, 196, 0.8)",  # Dark Blue - Monthly Income
                "rgba(214, 39, 40, 0.8)",   # Red - Taxes
                "rgba(102, 194, 165, 0.8)", # Green - After Tax
                "rgba(255, 127, 0, 0.8)",   # Orange - Housing Budget
                "rgba(148, 103, 189, 0.8)"   # Purple - Remaining Income
            ]
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=[
                "rgba(214, 39, 40, 0.6)",   # Red - Taxes
                "rgba(102, 194, 165, 0.6)", # Green - After Tax
                "rgba(255, 127, 0, 0.6)",   # Orange - Housing Budget
                "rgba(148, 103, 189, 0.6)"   # Purple - Remaining Income
            ]
        )
    )])

    fig.update_layout(
        title_text=f"{selected_year} Annual Salary: {round(annual_income):,.0f} — Monthly Salary: {round(monthly_income):,.0f}",
        font_size=14
    )

    return fig

def housing_vs_budget_trend():
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    df = pd.read_csv(csv_path)

    # Filter to July entries only
    df = df[df['Year'].str.endswith('-07')]
    df['Year'] = df['Year'].str[:4]

    df['Median Income'] = df['Median Income'].astype(float)
    df['Monthly Income'] = df['Median Income'] / 12
    df['Budget (30%)'] = df['Monthly Income'] * 0.30

    df['Median Home Price'] = df['Median Home Price'].astype(float)
    df['Interest Rate'] = df['Interest Rate'] / 100
    df['Down Payment'] = df['Median Home Price'] * 0.2
    df['Mortgage'] = df['Median Home Price'] * 0.8

    # Calculate monthly mortgage payment
    df['Monthly Payment'] = (df['Mortgage'] * df['Interest Rate'] / 12) / (1 - (1 + df['Interest Rate'] / 12) ** -360)
    df['Total Monthly Cost'] = df['Monthly Payment'] + df['Property Tax'] + df['Home Insurance']

    # Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Budget (30%)'],
        mode='lines',
        name='Housing Budget',
        line=dict(color='green'),
        fill=None
    ))

    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Total Monthly Cost'],
        mode='lines',
        name='MTI',
        line=dict(color='red'),
        fill='tonexty',
        fillcolor='rgba(255, 99, 132, 0.2)'
    ))

    fig.update_layout(
        title="Mortgage + Taxes + Insurance vs. Housing Budget (30%)",
        xaxis_title="Year",
        xaxis=dict(
            tickangle=50
        ),
        yaxis_title="Monthly Cost",
        font=dict(size=14),
        hovermode='x unified'
    )

    return fig

def housing_affordability_delta_trend():
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    df = pd.read_csv(csv_path)

    df = df[df['Year'].str.endswith('-07')]
    df['Year'] = df['Year'].str[:4]

    df['Median Income'] = df['Median Income'].astype(float)
    df['Monthly Income'] = df['Median Income'] / 12
    df['Budget (30%)'] = df['Monthly Income'] * 0.30

    df['Median Home Price'] = df['Median Home Price'].astype(float)
    df['Interest Rate'] = df['Interest Rate'] / 100
    df['Mortgage'] = df['Median Home Price'] * 0.8
    df['Monthly Payment'] = (df['Mortgage'] * df['Interest Rate'] / 12) / (1 - (1 + df['Interest Rate'] / 12) ** -360)

    df['Total Monthly Cost'] = df['Monthly Payment'] + df['Property Tax'] + df['Home Insurance']

    df['Affordability Delta'] = df['Budget (30%)'] - df['Total Monthly Cost']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Affordability Delta'],
        mode='lines+markers',
        name='Housing Affordability Delta',
        line=dict(color='orange')
    ))

    fig.update_layout(
        title="Housing Affordability Delta Over Time",
        xaxis_title="Year",
        xaxis=dict(
            tickangle=50
        ),
        yaxis_title="Budget - Actual Cost",
        font=dict(size=14),
        hovermode='x unified'
    )

    return fig