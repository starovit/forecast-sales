## Project Structure

```
data/
  raw/         # Source data (CSVs)
notebooks/
  EDA.ipynb    # Full exploratory analysis
src/           # Future scripts and modeling code
README.md      # Project overview
pyproject.toml # Poetry environment & dependencies
```

## How to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/starovit/forecast-sales.git
   cd forecast-sales
   ```

2. **Install dependencies** (Poetry recommended):

   ```bash
   poetry install
   poetry shell
   ```

3. **Run any notebook** in Jupyter:

   ```
   jupyter notebook notebooks/*.ipynb
   ```

## Status

* **EDA completed.**
* Ready for modeling and further feature engineering.