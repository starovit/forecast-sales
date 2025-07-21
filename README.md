## Project Structure

```
data/
  raw/         # Source data (CSVs)
results/       # Results data (predictions)
notebooks/
  EDA.ipynb    # Full exploratory analysis
src/           # Scripts
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

**Done:**
* EDA completed.
* Simple models tested.

**Next Steps:**
* Future prediction.
* Seperate models for rare SKUs / frequent SKUs.