from dash import dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
from components.topbar import get_topbar

# Sample data for the tables
goods_data = [
  {"Good Name": "bacon", "Good Unit": "lb", "1900":"0.14", "1950": "0.64", "2000": "3.03", "2020": "5.58"},
  {"Good Name": "bread", "Good Unit": "lb", "1900":"...", "1950": "0.14", "2000": "0.93", "2020": "1.45"},
  {"Good Name": "butter", "Good Unit": "lb", "1900":"0.26", "1950": "0.73", "2000": "2.52", "2020": "..."},
  {"Good Name": "coffee", "Good Unit": "lb", "1900":"...", "1950": "0.79", "2000": "3.40", "2020": "4.40"},
  {"Good Name": "eggs", "Good Unit": "dozen", "1900":"0.21", "1950": "0.60", "2000": "0.91", "2020": "1.51"},
  {"Good Name": "flour", "Good Unit": "lb", "1900":"0.03", "1950": "0.10", "2000": "0.29", "2020": "0.41"},
  {"Good Name": "gas", "Good Unit": "gallon", "1900":"...", "1950": "0.27", "2000": "1.52", "2020": "2.25"},
  {"Good Name": "milk", "Good Unit": "1/2 gal", "1900":"0.14", "1950": "0.41", "2000": "2.78", "2020": "3.32"},
  {"Good Name": "pork chop", "Good Unit": "lb", "1900":"0.12", "1950": "0.75", "2000": "3.37", "2020": "4.12"},
  {"Good Name": "round steak", "Good Unit": "lb", "1900":"0.13", "1950": "0.94", "2000": "3.24", "2020": "6.53"},
  {"Good Name": "sugar", "Good Unit": "lb", "1900":"0.06", "1950": "0.10", "2000": "0.42", "2020": "0.63"},
]

housing_table = [
    {"Housing": "Average Cost of Housing", "Interest Rates": "1913-2024", "Year": "1913 - 2024"}
]

income_table = [
    {"Source": "Quarterly Journal of Economics: IRS Income", "Year": "1913 - 1998"},
    {"Source": "Bureau of Economic Analysis (BEA)", "Year": "1929 - 2024"},
    {"Source": "Federal Reserve Data", "Year": "1929 - 2024"},
]

palma_table = [ 
    {"Palma Index": "Palma Index Data", "Year": "1913 - 2024"},
    {"Productivity vs Pay": "Productivity vs Pay Data", "Year": "195 - 2024"},
]


# Accordion content
accordion = dbc.Accordion(
    [

        ### GOODS DATA ###

        dbc.AccordionItem(
            title="Goods Data",
            children=[
                html.H3(
                    "Data for the Price of Various Goods from 1890 to Current Day",
                    style={"marginBottom": "20px"}
                ),
                html.P("Notes: "),
                html.P("Data for Milk was missing data from 1980-1995, but all other goods data after 1980 was very consistent, and any missing data points were interpolated for visualizations. Bread data starts at 1913. Butter data ends in 2013."),
                html.H4("1890-1970", style={"marginBottom": "5px"}),
                html.A(
                    "https://babel.hathitrust.org/cgi/pt?id=umn.31951000014585x&seq=233",
                    href="https://babel.hathitrust.org/cgi/pt?id=umn.31951000014585x&seq=233",
                    target="_blank",
                    style={"marginTop": "1rem"},
                ),
                html.H4("1970-1980", style={"marginBottom": "5px"}),
                html.A(
                    "https://babel.hathitrust.org/cgi/pt?id=mdp.39015008856711&seq=527",
                    href="https://babel.hathitrust.org/cgi/pt?id=mdp.39015008856711&seq=527",
                    target="_blank",
                    style={"marginTop": "1rem"},
                ),
                html.H4("1980-2025", style={"marginBottom": "5px"}),
                html.A(
                    "https://www.bls.gov/regions/mid-atlantic/data/AverageRetailFoodAndEnergyPrices_USandMidwest_Table.htm",
                    href="https://www.bls.gov/regions/mid-atlantic/data/AverageRetailFoodAndEnergyPrices_USandMidwest_Table.htm",
                    target="_blank",
                    style={"marginTop": "1rem"},
                ),
                dbc.Button(
                    "Open Table",
                    id="collapse-button-goods",
                    className="mb-3 open-table-button",
                    color="primary",
                    n_clicks=0,
                    style={"marginBottom": "1rem"},
                ),
                dbc.Collapse(
                    dash_table.DataTable(
                        id="collapse-goods-table",
                        columns=[
                            {"name": col, "id": col} for col in goods_data[0].keys()
                        ],
                        data=goods_data,
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left"},
                    ),
                    id="collapse-goods",
                    is_open=False,
                ),
            ],
        ),


        ### HOUSING DATA ###


        dbc.AccordionItem(
            title="Housing Data",
            children=[
                html.H3(
                    "Data for the Price Median Price of a Home from 1913 to Current Day",
                    style={"marginBottom": "20px"}
                ),
                html.P("Notes: "),
                html.P("Our Housing Data mostly comes from one source, and to get data from before that source, we did research to find the median price of a home in specific marker years like 1910, 1915, 1920, 1925 and so on up to 1950, then through interpolation and some linear regression, we were able to get a good estimate of the median home price from 1913 to 1950. Various Catalot Type Data Sources are Listed Below. The data from 1950 to 2025 was all consistent and we were able to get the data from one source. Data for interest rates we collected from two main verified sources. Going back to 1954, we used the Federal Reserve Economic Data (FRED) to get the interest rates for 1954-2024. And from 1914 to 1954 we used Data from the Federal Reserve Bank of St. Louis (which is reporting for the whole country not just Missouri) to get the interest rates for 1914-1954. This data was consistent with the FRED interest rates we had from 1954-2002 where our second data source cuts off."),
                html.H4("1913-1954", style={"marginBottom": "5px"}),
                html.P("Interpolation and Linear Regression"),
                html.A("1900-1910: https://libraryguides.missouri.edu/pricesandwages/1900-1909#housing", href="https://libraryguides.missouri.edu/pricesandwages/1900-1909#housing", target="_blank",style={"marginTop": "1rem"}),
                html.A("1910-1919: https://libraryguides.missouri.edu/pricesandwages/1910-1919#housing", href="https://libraryguides.missouri.edu/pricesandwages/1910-1919#housing", target="_blank",style={"marginTop": "1rem"}),
                html.A("1920-1929: https://libraryguides.missouri.edu/pricesandwages/1920-1929#housing", href="https://libraryguides.missouri.edu/pricesandwages/1920-1929#housing", target="_blank",style={"marginTop": "1rem"}),
                html.A("1930-1939: https://libraryguides.missouri.edu/pricesandwages/1930-1939#housing", href="https://libraryguides.missouri.edu/pricesandwages/1930-1939#housing", target="_blank",style={"marginTop": "1rem"}),
                html.A("1940-1949: https://libraryguides.missouri.edu/pricesandwages/1940-1949#housing", href="https://libraryguides.missouri.edu/pricesandwages/1940-1949#housing", target="_blank",style={"marginTop": "1rem"}),
                html.H4("1954-2024", style={"marginBottom": "5px"}),
                html.A("https://dqydj.com/historical-home-prices/", href="https://dqydj.com/historical-home-prices/", target="_blank", style={"marginTop": "1rem"}),
                html.H4("Interest Rates", style={"marginBottom": "5px"}),
                html.A("1914-1954: https://fred.stlouisfed.org/series/DISCNTD8", href="https://fred.stlouisfed.org/series/DISCNTD8", target="_blank", style={"marginTop": "1rem"}),
                html.A("1954-2024: https://fred.stlouisfed.org/series/FEDFUNDS", href="https://fred.stlouisfed.org/series/FEDFUNDS", target="_blank", style={"marginTop": "1rem"}),
                
                dbc.Button(
                    "Open Table",
                    id="collapse-button-housing",
                    className="mb-3 open-table-button",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dash_table.DataTable(
                        id="collapse-housing-table",
                        columns=[
                            {"name": col, "id": col} for col in housing_table[0].keys()
                        ],
                        data=housing_table,
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left"},
                    ),
                    id="collapse-housing",
                    is_open=False,
                ),
                html.P(""),
                dbc.Button(
                    "Interest Rate Footnotes",
                    id="collapse-button-interest-rates",
                    className="mb-3 open-table-button",
                    color="secondary",
                    n_clicks=0,
                    style={"marginBottom": "1rem"},
                ),
                dbc.Collapse(
                    html.Div(
                        [
                            html.H4("Interest Rate Footnote"),
                            html.P("For a some of our visualizations for displaying the housing data appropriately with older interest rate data and to conifirm these were appropriate approximatiosn information from this paper: https://fraser.stlouisfed.org/files/docs/publications/frbslreview/pages/1965-1969/62472_1965-1969.pdf"),
                            html.H4("Federal Funds Rate Footnote:"),
                            html.P("The federal funds rate is the interest rate at which depository institutions trade federal funds (balances held at Federal Reserve Banks) with each other overnight. When a depository institution has surplus balances in its reserve account, it lends to other banks in need of larger balances. In simpler terms, a bank with excess cash, which is often referred to as liquidity, will lend to another bank that needs to quickly raise liquidity. (1) The rate that the borrowing institution pays to the lending institution is determined between the two banks; the weighted average rate for all of these types of negotiations is called the effective federal funds rate.(2) The effective federal funds rate is essentially determined by the market but is influenced by the Federal Reserve through open market operations to reach the federal funds rate target.(2)The Federal Open Market Committee (FOMC) meets eight times a year to determine the federal funds target rate. As previously stated, this rate influences the effective federal funds rate through open market operations or by buying and selling of government bonds (government debt).(2) More specifically, the Federal Reserve decreases liquidity by selling government bonds, thereby raising the federal funds rate because banks have less liquidity to trade with other banks. Similarly, the Federal Reserve can increase liquidity by buying government bonds, decreasing the federal funds rate because banks have excess liquidity for trade. Whether the Federal Reserve wants to buy or sell bonds depends on the state of the economy. If the FOMC believes the economy is growing too fast and inflation pressures are inconsistent with the dual mandate of the Federal Reserve, the Committee may set a higher federal funds rate target to temper economic activity. In the opposing scenario, the FOMC may set a lower federal funds rate target to spur greater economic activity. Therefore, the FOMC must observe the current state of the economy to determine the best course of monetary policy that will maximize economic growth while adhering to the dual mandate set forth by Congress. In making its monetary policy decisions, the FOMC considers a wealth of economic data, such as: trends in prices and wages, employment, consumer spending and income, business investments, and foreign exchange markets.The federal funds rate is the central interest rate in the U.S. financial market. It influences other interest rates such as the prime rate, which is the rate banks charge their customers with higher credit ratings. Additionally, the federal funds rate indirectly influences longer- term interest rates such as mortgages, loans, and savings, all of which are very important to consumer wealth and confidence.(2)"),
                            html.H4("References"),
                            html.P("(1) Federal Reserve Bank of New York. Federal funds. Fedpoints, August 2007."),
                            html.P("(2) Board of Governors of the Federal Reserve System. Monetary Policy."),
                            html.H4("Citation:"),
                            html.P("Board of Governors of the Federal Reserve System (US), Federal Funds Effective Rate [FEDFUNDS], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/FEDFUNDS, April 24, 2025.")
                        ],
                        style={"padding": "10px", "backgroundColor": "#f8f9fa", "border": "1px solid #ddd", "borderRadius": "5px"},
                    ),
                    id="collapse-interest-rates",
                    is_open=False,
                ),
            ],
        ),


        ### INCOME DATA ###


        dbc.AccordionItem(
            title="Income Data",
            children=[
                html.H3(
                    "Data for the Average Income of an Individual from 1913 to Current Day",
                    style={"marginBottom": "20px"}
                ),
                html.P("Notes: "),
                html.P("We have three main sources for Income Data, The Bureau of Economic Analysis (BEA), The Federal Reserve and Quarterly Journey of Economics (FRED), which has references data from the IRS. The IRS data came from a Yale study that focused on Income Inequality in the US, with data from 1913 to 1998. The BEA data we have is from 1929 to 2024 and measures Income Per Capita; Per capita personal income is total personal income divided by total midyear population. Finally the FRED income also measures Per Capita Income and provides us with the data from 1929 to 2024. For our Gini Coefficient analysis and the Goods Affordability Analysis we used the BEA data as it was the most consistent and complete."),
                html.H4("1913-1999, IRS Data", style={"marginBottom": "5px"}),
                html.A(
                    "https://eml.berkeley.edu/~saez/pikettyqje.pdf",
                    href="https://eml.berkeley.edu/~saez/pikettyqje.pdf",
                    target="_blank",
                    style={"marginTop": "1rem"},
                ),
                html.H4("1929-2024, Bureau of Economic Analysis (BEA)", style={"marginBottom": "5px"}),
                html.A(
                    "Data Source Link",
                    href="https://apps.bea.gov/iTable/?reqid=70&step=30&isuri=1&major_area=0&area=xx&year=-1&tableid=21&category=421&area_type=0&year_end=-1&classification=non-industry&state=0&statistic=3&yearbegin=-1&unit_of_measure=levels#eyJhcHBpZCI6NzAsInN0ZXBzIjpbMSwyOSwyNSwzMSwyNiwzMCwzMF0sImRhdGEiOltbIm1ham9yX2FyZWEiLCIwIl0sWyJhcmVhIixbIlhYIl1dLFsieWVhciIsWyItMSJdXSxbInRhYmxlaWQiLCIyMSJdLFsieWVhcl9lbmQiLCItMSJdLFsic3RhdGUiLFsiMCJdXSxbInN0YXRpc3RpYyIsIjMiXSxbInllYXJiZWdpbiIsIi0xIl0sWyJ1bml0X29mX21lYXN1cmUiLCJMZXZlbHMiXV19",
                    target="_blank",
                    style={"marginTop": "1rem"},
                ),
                html.H4("1929-2024, Federal Reserve Data", style={"marginBottom": "5px"}),
                html.A(
                    "https://fred.stlouisfed.org/series/A792RC0A052NBEA",
                    href="https://fred.stlouisfed.org/series/A792RC0A052NBEA",
                    target="_blank",
                    style={"marginTop": "1rem"},
                ),
                dbc.Button(
                    "Open Table",
                    id="collapse-button-income",
                    className="mb-3 open-table-button",
                    color="primary",
                    n_clicks=0,
                    style={"marginBottom": "1rem"},
                ),
                dbc.Collapse(
                    dash_table.DataTable(
                        id="collapse-income-table",
                        columns=[
                            {"name": col, "id": col} for col in income_table[0].keys()
                        ],
                        data=income_table,
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left"},
                    ),
                    id="collapse-income",
                    is_open=False,
                ),
                # dbc.Button(
                #     "Income Footnotes",
                #     id="collapse-button-4",
                #     className="mb-3 open-table-button",
                #     color="secondary",
                #     n_clicks=0,
                #     style={"marginBottom": "1rem"},
                # ),
                # dbc.Collapse(
                #     html.Div(
                #         [
                #             html.P(
                #                 "The interest rate data from 1914 to 1954 was sourced from the Federal Reserve Bank of St. Louis. "
                #                 "This data represents the national average and aligns with the FRED data from 1954 onward."
                #             ),
                #             html.P(
                #                 "For the years 1954 to 2024, we used the Federal Reserve Economic Data (FRED) to ensure consistency. "
                #                 "The data was cross-verified with other sources to ensure accuracy."
                #             ),
                #         ],
                #         style={"padding": "10px", "backgroundColor": "#f8f9fa", "border": "1px solid #ddd", "borderRadius": "5px"},
                #     ),
                #     id="collapse-3",
                #     is_open=False,
                # ),
            ],
        ),


        ### PALMA INDEX PAY PRODUCTIVITY DATA ###


        dbc.AccordionItem(
            title="Palma Index Data, Productivity vs Pay Data",
            children=[
                html.H3("Data Palma Ratio and Productivity vs Pay Data", style={"marginBottom": "20px"}),
                html.P("Notes: "),
                html.P("The Data for the Palma Index comes comes from one data source between the years of 1913 and 2023. The Productivity vs Pay data comes from 1948 to 2024 and from one data source. We used both of these metrics in our Gini Coefficient analysis."),
                html.H4("1913-2023, Palma Ratio", style={"marginBottom": "5px"}),
                html.A("https://ourworldindata.org/grapher/palma-ratio-s90s40-ratio?tab=chart&country=~USA", href="https://ourworldindata.org/grapher/palma-ratio-s90s40-ratio?tab=chart&country=~USA", target="_blank", style={"marginTop": "1rem"}),
                html.H4("1950-2024, Productivity vs Pay", style={"marginBottom": "5px"}),
                html.A("https://www.epi.org/productivity-pay-gap/", href="https://www.epi.org/productivity-pay-gap/", target="_blank", style={"marginTop": "1rem"}),
            ],
        ),
    ],
    start_collapsed=False,
    always_open=True,
)

# Layout
layout = html.Div(className="container-data-sources", children=[
    get_topbar(overlay=False, current_path="/data-sources"),

    html.Link(rel="stylesheet", href="/static/css/data-sources-styles.css"),
    
    html.Div(className="data-sources-content", children=[
        html.H2("Data Sources", className="section__title"),
        html.P(
            "Click on a data source to view its description and open its table:",
            className="section__description",
        ),
        accordion,
    ]),
])

# Callbacks for collapsible buttons
@callback(
    Output("collapse-goods", "is_open"),
    Input("collapse-button-goods", "n_clicks"),
    State("collapse-goods", "is_open"),
)
def toggle_goods(n, is_open):
    return not is_open if n else is_open

@callback(
    Output("collapse-housing", "is_open"),
    Input("collapse-button-housing", "n_clicks"),
    State("collapse-housing", "is_open"),
)
def toggle_housing(n, is_open):
    return not is_open if n else is_open

@callback(
    Output("collapse-interest-rates", "is_open"),
    Input("collapse-button-interest-rates", "n_clicks"),
    State("collapse-interest-rates", "is_open"),
)
def toggle_interest_rates(n, is_open):
    return not is_open if n else is_open

@callback(
    Output("collapse-income", "is_open"),
    Input("collapse-button-income", "n_clicks"),
    State("collapse-income", "is_open"),
)
def toggle_income(n, is_open):
    return not is_open if n else is_open