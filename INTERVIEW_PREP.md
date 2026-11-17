# Python Interview Prep: Software Engineer (Energy Analytics)

The job spec says the practical Python tasks will be about **analytics, data processing,
automation, APIs and prototype/R&D code**, and that you must be able to **write, read, test,
debug and maintain** it. So expect:
- a small data-processing task (parse a file → clean → aggregate → output)
- time-series questions (half-hourly readings, gaps, resampling, peaks)
- an algorithm question with a "what's the complexity / can you do better?" follow-up
- reading or debugging someone else's code
- "how would you test this?"

Linux, databases, maths and energy concepts are in [ROLE_CHEATSHEET.md](ROLE_CHEATSHEET.md).

## Setup
```
pip install -r requirements.txt
cd examples
```
Run the examples from inside `examples/`; they use relative paths like `data/input.txt`.

---

## Morning plan (~60 min, finish by 9:00)
| Time | File | Why for this role |
|---|---|---|
| 15 min | [example_21_pandas_timeseries.py](examples/example_21_pandas_timeseries.py) ⭐ | Time-series analytics is the core of the job: resample, rolling, missing values, kW vs kWh, z-scores |
| 10 min | [example_20_sql_timeseries.py](examples/example_20_sql_timeseries.py) ⭐ | Python + SQL together: parameterised queries, GROUP BY, window functions |
| 15 min | [problem_10_battery_arbitrage.py](problems/problem_10_battery_arbitrage.py) ⭐ | Energy-flavoured algorithm question: write O(n²) first, then O(n) |
| 10 min | [example_17_gotchas.py](examples/example_17_gotchas.py) | "What does this print?" / debugging questions |
| 10 min | Skim the **Python questions to answer out loud** below | |

---

## All material, grouped by what the job asks for

### Data processing & analytics
| File | Topics |
|---|---|
| [example_21_pandas_timeseries.py](examples/example_21_pandas_timeseries.py) | DatetimeIndex, `resample`, `rolling`, `interpolate`, `describe`, `quantile`, z-score anomalies, `groupby(index.hour)` profiles, `diff`/`shift`, `corr` |
| [example_20_sql_timeseries.py](examples/example_20_sql_timeseries.py) | `sqlite3`, schema with PK/FK, indexes, JOIN, GROUP BY/HAVING, time bucketing, `LAG` and moving averages, finding NULLs, `EXPLAIN` |
| [example_6_csv_files.py](examples/example_6_csv_files.py), [example_7_json.py](examples/example_7_json.py) | reading/writing CSV and JSON |
| [example_18_collections_itertools.py](examples/example_18_collections_itertools.py) | `Counter`, `defaultdict`, `deque` (sliding windows!), `groupby`, Big-O cheat sheet |
| [example_12_comprehensions.py](examples/example_12_comprehensions.py) | comprehensions, generator expressions |
| [example_13_generators.py](examples/example_13_generators.py) | lazy processing of big files and data streams |

### Algorithms & complexity
| File | Topics |
|---|---|
| [problems/solutions/problem_10_battery_arbitrage.py](problems/solutions/problem_10_battery_arbitrage.py) | O(n²) brute force → O(n) single pass, round-trip efficiency |
| [problems/solutions/problem_1_primes.py](problems/solutions/problem_1_primes.py) + [problem_1_ai.py](problems/solutions/problem_1_ai.py) | trial division O(n√n) vs Sieve of Eratosthenes O(n log log n) |
| [problems/solutions/problem_8_cache_decorator.py](problems/solutions/problem_8_cache_decorator.py) | memoisation: 2.7 million calls → 31 |

### Writing maintainable code (modules, prototypes)
| File | Topics |
|---|---|
| [example_14_classes.py](examples/example_14_classes.py) | classes, `@property`, class/static methods, dunder methods, inheritance, `@dataclass` |
| [example_15_decorators.py](examples/example_15_decorators.py) | timing and retry decorators (retry is very relevant to flaky APIs/devices), `lru_cache` |
| [example_16_context_managers.py](examples/example_16_context_managers.py) | `with`, `__enter__`/`__exit__`, `@contextmanager` |
| [example_3b_advanced_exceptions.py](examples/example_3b_advanced_exceptions.py) | `try/except/else/finally`, custom exceptions |

### Testing & debugging
| File | Topics |
|---|---|
| [example_19_pytest.py](examples/example_19_pytest.py) | `parametrize`, `pytest.raises`, `approx` (floats!), fixtures, `tmp_path` |
| [example_17_gotchas.py](examples/example_17_gotchas.py) | mutable defaults, `is` vs `==`, copying, late binding, float comparison |

### APIs & automation
| File | Topics |
|---|---|
| [example_8_requests.py](examples/example_8_requests.py), [bonus_3_rest_api.py](examples/bonus/bonus_3_rest_api.py) | calling REST APIs |
| [bonus_5_secrets.py](examples/bonus/bonus_5_secrets.py) | API keys in `.env`, never in code |
| [project/Solutions/c_more_data/scraper.py](project/Solutions/c_more_data/scraper.py) | a full fetch → parse → save pipeline (good "walk me through it" code) |

### Practice problems (try first, then check `problems/solutions/`)
| Problem | Practises |
|---|---|
| [problem_10_battery_arbitrage.py](problems/problem_10_battery_arbitrage.py) ⭐ | algorithms, complexity, energy domain |
| [problem_9_csv_pipeline.py](problems/problem_9_csv_pipeline.py) | generators, `csv`, passing functions around |
| [problem_7_library.py](problems/problem_7_library.py) | classes, dataclasses, custom exceptions |
| [problem_8_cache_decorator.py](problems/problem_8_cache_decorator.py) | decorators, closures |
| [problem_6_word_frequency.py](problems/problem_6_word_frequency.py) | parsing, regex, `Counter` |

---

## Python questions to answer out loud

**Data & time-series**
- How do you load a CSV of half-hourly meter readings and get daily totals? → `pd.read_csv(..., parse_dates=["ts"], index_col="ts")`, then `.resample("D").sum()`
- Some readings are missing. What do you do? → find them with `isna()`; then interpolate, forward-fill, or leave them as NaN, depending on what the data is used for. **Say the trade-off** and flag gaps rather than hiding them
- Power is in kW per half hour. How do you get energy? → kWh = kW × 0.5, then sum
- How do you find outliers? → z-score (|z| > 3) or IQR (below Q1 − 1.5·IQR or above Q3 + 1.5·IQR)
- The file is 50 GB and doesn't fit in memory. → read in chunks (`pd.read_csv(chunksize=...)`), use generators, push aggregation into the database, or use Polars/DuckDB
- Why is numpy faster than a Python loop? → vectorised operations run in C on contiguous arrays, with no per-element Python overhead
- Timezones? → store in UTC; convert for display; watch for DST days with 46/50 half-hours

**Core Python**
- List vs tuple vs set vs dict, and the Big-O of `in` for each
- What's a generator, and when would you use one? (streams, big files)
- `@dataclass` vs a normal class vs a dict for a record
- Mutable default argument bug: spot it and fix it
- `is` vs `==`; shallow vs deep copy
- What is the GIL? → only one thread runs Python bytecode at a time, so threads help with **I/O-bound** work (APIs, files) but not **CPU-bound** work; for CPU-bound work use `multiprocessing` or numpy, or move the hot path to Rust/C
- `*args` / `**kwargs`, decorators, context managers: be able to write each from scratch

**Testing & debugging**
- How would you test a function that calls an external API? → `unittest.mock.patch` / dependency injection, so tests don't hit the network
- How do you compare floats in tests? → `pytest.approx` / `math.isclose`
- How do you debug slow code? → measure first (`cProfile`, `time.perf_counter`), then fix the algorithm, then vectorise
- How do you debug wrong output? → reproduce it with a small input, add a failing test, use a debugger (`breakpoint()`) or logging, check assumptions about the data (types, NaNs, timezones, duplicates)

**Engineering practice**
- Project layout, virtual environments, `requirements.txt` / `pyproject.toml`
- `logging` instead of `print` in real code
- Type hints + `mypy`, formatting/linting with `ruff`/`black`
- Git workflow: branch → commit → pull request → code review

---

## Not covered here (lower priority for tomorrow)
`asyncio`, threading/multiprocessing code, abstract base classes, writing `__iter__`/`__next__`,
FastAPI, `scipy.optimize.linprog` (see the optimisation section in [ROLE_CHEATSHEET.md](ROLE_CHEATSHEET.md)).
