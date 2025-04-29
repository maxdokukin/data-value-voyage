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
- To Understand if Americans have greater buying power over 

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

By dividing average monthly income by CPI-based prices for a basket of goods, we measured how many units an average consumer could afford per month. Comparing the 1920s to the 2020s shows declines across all items.

Flour and sugar affordability dropped by over 90%, eggs fell ~13%, pork chops and bacon by ~40–45%, milk by ~57%, and butter became effectively unaffordable.

Using Lorenz curves and Gini coefficients, income distribution was quantified from 1900 to 2020. The Gini rose from ~0.45 to >0.49, indicating growing inequality.

Normalized metrics (Palma Ratio, Housing Delta, Productivity Gap) served as alpha/beta parameters in a Gamma distribution, revealing increasing skew and dispersion over time.

Our housing analysis combined Sankey diagrams, budget trend charts, and affordability delta metrics to assess structural barriers in homeownership.

A 20% down payment requirement and cumulative costs (interest, taxes, insurance) disproportionately exclude lower-income households. The gap between actual housing expenditures and the recommended 30% budget has widened, straining disposable income.

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


