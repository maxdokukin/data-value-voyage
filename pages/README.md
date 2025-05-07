# Value Voyge - A Journey Through Decades of Prices
This project makes the Consumer Price Index (CPI) and purchasing power relatable by visualizing inflation's impact on everyday goods (eggs, housing, gas) from 1900-2020. By analyzing historical income data, we'll show how much of these essentials an average person could afford in different decades. 
<p align="center">
  <a href="https://value-voyage-cs163.uw.r.appspot.com">
    <img width="1089" alt="Screenshot 2025-04-29 at 1 36 49 PM" src="https://github.com/user-attachments/assets/4117cec6-2801-477f-b915-c5d53b949b76" /> 
  </a>
</p>
<h2 align="center">
  <a href="https://value-voyage-cs163.uw.r.appspot.com" style="text-decoration: none; color: inherit;">Visit Our Website</a>
</h2>

---
<details>
<summary>📚 Table of Contents</summary>
  
- [Objectives](#objectives)
- [Methodology](#methodology)
  - [Affordable Quantity](#affordable-quantity)
  - [Gini Index Income Inequality Analysis](#gini-index-income-inequality-analysis)
  - [Housing Affordability Analysis](#housing-affordability-analysis)
- [Findings](#findings)
- [Data Sources](#data-sources)
- [About Us](#about-us)

</details>

---

## Objectives

#### Primary Objective
Transform CPI and purchasing‑power data into quantities of everyday goods and calculate how many units an average consumer could buy per month, across decades from 1900 to 2020 (10‑year intervals).

- Convert CPI indices into quantities of goods (milk, eggs, sugar, etc.)
- Model average monthly purchasing power for each decade
- Visualize trends in a clear, user‑friendly format

#### Secondary Objectives
- Analyze generational income data and affordability shifts
- Identify historical periods of relative economic prosperity
- Experiment with ML‑based forecasting of future price trends

#### Broader Impact
Offer an accessible dashboard that demystifies inflation and purchasing power, helping non‑expert users grasp the real‑world impact of price changes.

---

## Methodology

We broke our Methodology Down into three main ideas to answer our hypothesis.
- To understand if Americans have greater buying power compared to previous decades, we wanted to look at the amount of goods a person could buy compared to their monthly income.
- To understand if Income Inequality has been growing, shrinking or somewhere inbetween we built a statistical model to help us visualize the Gini index, which is a measure of the amount of income distributed across a population and how skewd it is away from perfect equality.
- To understand if how much the cost of housing has changed and how much more expensive it is to own a home compared to previous decades, we compared the True cost of owning a home, as the mortgage payments + home insurrance + property taxes, to 30% of the median monthly income representing an "affordable" housing budget. Then analysed how far this gap has grown across the decades.

---

### Affordable Quantity
This page details how we transformed CPI indices into tangible units of everyday goods and computed the number of units an average consumer could afford each month from 1900 to 2020 (10-year intervals).
<p align="center">
  <img width="854" alt="Screenshot 2025-04-29 at 2 48 15 PM" src="https://github.com/user-attachments/assets/f05ccc32-bebb-4ba6-9331-223db3911848" />
</p>

---

### Gini Index Income Inequality Analysis

This page summarizes the methodology and metrics used to quantify income inequality over time. Using the Palma Ratio, Housing Affordability Delta, and the Productivity Gap, we normalized each metric and derived Alpha and Beta parameters to simulate income distributions via a Gamma distribution. Gini coefficients and Lorenz curves offer visual and numeric validation of inequality over time.
<p align="center">
  <img width="1375" alt="Screenshot 2025-04-29 at 2 50 15 PM" src="https://github.com/user-attachments/assets/68d4bb93-f35f-46bd-b508-481fe8833ae1" />
</p>

---

### Housing Affordability Analysis

To Better understand the growing gap between incomes and housing affordability we looked broke down what it means to be able to afford a home, and we looked at the structural barriers to home ownership. 

#### Structural Barriers to Homeownership and Wealth Accumulation
 - The 20% Down Payment Threshold
A 20% down payment is conventionally required to avoid Private Mortgage Insurance (PMI), an additional cost that disproportionately burdens lower-income buyers. This upfront financial hurdle exacerbates wealth stratification, as those without intergenerational wealth or substantial savings are effectively excluded from the market or forced into costlier financing structures.

#### The True Cost of Ownership and Intergenerational Disparities
The Sankey diagram illustrates how interest payments, property taxes, and insurance compound over a 30-year mortgage, significantly inflating the total expenditure. This dynamic entrenches intergenerational inequality, as households that purchased homes in earlier decades (when prices were lower relative to income) benefit from equity accumulation, while newer entrants face diminished purchasing power due to stagnant wage growth and rising housing costs.

#### Housing Budget Affordability Delta: A Metric of Economic Polarization
The delta between monthly housing costs (mortgage + taxes + insurance) and the recommended 30% housing budget serves as a stark indicator of affordability erosion. As this gap widens, middle- and working-class households are forced to allocate a larger share of income to housing, reducing disposable income for savings, education, or investment—key drivers of upward mobility.

<p align="center">
  <img width="1385" alt="Screenshot 2025-04-29 at 2 53 58 PM" src="https://github.com/user-attachments/assets/2279fb52-7e27-4cfb-90fe-7eb78b1c2d60" />
</p>

<p align="center">
  <img width="829" alt="Screenshot 2025-04-29 at 2 53 08 PM" src="https://github.com/user-attachments/assets/1413f6cd-6193-46e1-93cc-9de968cbea6d" />
</p>


---

## Findings

**Purchasing Power Findings**
By dividing average monthly income by CPI-adjusted prices for a standardized basket of goods, we can see how many units an average consumer could afford per month in the 1920s versus the 2020s. Contrary to the notion that basic staples have become more expensive relative to income, the ability to purchase both eggs and bread has actually soared over the past century. In the 1920s, an average household could afford roughly 110 dozen eggs each month; by the 2020s, that figure has climbed to about 2,474 dozen, representing a more than 2,100 percent increase in egg-purchasing power. Likewise, the number of one-pound loaves of bread purchasable with an average monthly income rose from approximately 648 to 3,237, a nearly 400 percent gain.

**Income Inequality Findings**
We quantified income distribution from 1900 through 2020 using Lorenz curves and Gini coefficients. Over that period, the Gini coefficient increased from around 0.45 to about 0.49, signaling a clear uptick in inequality. To capture changes in the distribution’s shape, we converted normalized metrics—such as the Palma ratio, a housing-cost gap indicator, and a productivity-gap measure—into the alpha and beta parameters of a Gamma distribution. The resulting shifts in those parameters reveal a steadily growing right skew and wider dispersion, underscoring that income gains are increasingly concentrated among higher-earning households.

**Housing Affordability Findings**
Our housing analysis—incorporating Sankey diagrams, multi-decade budget-trend charts, and “affordability delta” metrics—highlights structural barriers faced by would-be homeowners. A standard 20 percent down-payment requirement, together with the cumulative burden of mortgage interest, property taxes, and insurance, effectively excludes many lower-income families. At the same time, the share of household income devoted to housing has drifted well above the 30 percent benchmark commonly viewed as sustainable, squeezing disposable income and intensifying financial strain.

---

## Data Sources

To Build our Visualizations on our website we organized our raw data and designed this data streaming system.
<p align="center">
  <img width="1632" alt="Screenshot 2025-04-29 at 3 13 53 PM" src="https://github.com/user-attachments/assets/efe8fd0a-6360-4cb0-91e0-d6750a826f06" />
</p>

#### To Learn more about our data sources visit the data page on our website.

<h2 align="center">
  <a href="https://value-voyage-cs163.uw.r.appspot.com/data-sources" style="text-decoration: none; color: inherit;">Data Sources</a>
</h2>


---


## About Us

<p align="center">
  <a href="https://value-voyage-cs163.uw.r.appspot.com/about-us">
    <img width="828" alt="Screenshot 2025-04-29 at 2 26 46 PM" src="https://github.com/user-attachments/assets/9a1f1ffd-c990-4e27-96c7-7fefc132b287" />
  </a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/maxdokukin/">Max Dokukin LinkedIn</a> |
  <a href="https://github.com/maxdokukin">Max Dokukin GitHub</a> |
  <a href="https://www.linkedin.com/in/ryan-fernald/">Ryan Fernald LinkedIn</a> |
  <a href="https://github.com/ryanfernald">Ryan Fernald GitHub</a>
</p>


