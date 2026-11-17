# Software Engineer (Energy Analytics): Cheat Sheet

The job spec says the interview tests: **Linux, Python tasks, database paradigms, maths concepts**.
Read this top to bottom: it's ordered by what they explicitly said they'll test.

---

## 1. Linux & command line

### Moving around and files
| Command | What it does |
|---|---|
| `pwd`, `cd dir`, `cd ..`, `cd ~`, `cd -` | where am I / move / home / previous dir |
| `ls -la` | list all files with permissions, sizes, hidden files |
| `mkdir -p a/b/c` | make nested folders |
| `cp -r src dst`, `mv old new`, `rm -r dir` | copy, move/rename, delete (no recycle bin!) |
| `cat f`, `less f`, `head -n 20 f`, `tail -n 20 f` | view files |
| `tail -f app.log` | **follow a log live** (very common question) |
| `touch f`, `nano f` / `vim f` | create / edit (vim: `i` insert, `Esc :wq` save & quit, `:q!` quit without saving) |

### Searching and text processing
| Command | What it does |
|---|---|
| `grep -rn "error" .` | search recursively, with line numbers (`-i` ignore case, `-v` invert, `-c` count) |
| `find . -name "*.py"` | find files by name (`-mtime -1` modified in last day, `-size +100M`) |
| `wc -l f` | count lines |
| `sort f \| uniq -c \| sort -rn \| head` | **count and rank duplicates** (classic) |
| `cut -d, -f2 data.csv` | take column 2 of a CSV |
| `awk -F, '{sum += $3} END {print sum}' data.csv` | sum column 3 |
| `sed 's/old/new/g' f` | find and replace |

### Pipes and redirection
- `cmd1 | cmd2`: output of one becomes input of the next
- `> file` overwrite, `>> file` append, `2> err.txt` redirect errors, `2>&1` errors into output, `> /dev/null` discard
- `cmd1 && cmd2` run cmd2 only if cmd1 succeeded; `cmd1 || cmd2` only if it failed

### Permissions
- `ls -l` shows `-rwxr-xr--` = owner / group / others; r=4, w=2, x=1
- `chmod 755 script.sh` (owner rwx, others r-x), `chmod +x script.sh`, `chown user:group f`
- `sudo cmd` runs as root

### Processes and system
| Command | What it does |
|---|---|
| `ps aux \| grep python` | find a process |
| `top` / `htop` | live CPU/memory usage |
| `kill PID`, `kill -9 PID` | stop politely (SIGTERM) / force (SIGKILL) |
| `cmd &`, `jobs`, `fg`, `Ctrl+Z`, `Ctrl+C` | background, list, foreground, pause, stop |
| `nohup python run.py &` | keep running after logout |
| `df -h`, `du -sh *`, `free -h` | disk space, folder sizes, memory |
| `systemctl status nginx`, `journalctl -u nginx -f` | services and their logs |
| `crontab -e` | schedule jobs: `*/30 * * * * python /path/job.py` = every 30 min |

### Networking and remote
- `ssh user@host`, `scp file user@host:/path`, `rsync -av src/ host:dst/`
- `curl -s https://api.example.com/data | python -m json.tool`, `wget url`
- `ping host`, `ss -tulpn` / `netstat -tulpn` (which ports are open), `lsof -i :8000`

### Environment and Python
- `echo $PATH`, `export API_KEY=abc`, `env`, `which python`
- `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- `tar -czf archive.tar.gz dir/`, `tar -xzf archive.tar.gz`

### Debugging a broken service: say this out loud
1. Is it running? `systemctl status` / `ps aux | grep`
2. What do the logs say? `journalctl -u app -n 100` / `tail -f app.log`
3. Resources? `df -h` (disk full is common!), `free -h`, `top`
4. Network? `curl localhost:8000/health`, `ss -tulpn`, `ping`
5. What changed recently? `git log`, deploy history

---

## 2. Database paradigms (they care about *when to use which*)

| Paradigm | Examples | Good for | Weak at |
|---|---|---|---|
| **Relational (SQL)** | PostgreSQL, MySQL, SQLite | structured data with relationships, transactions, consistency: customers, sites, contracts, billing | massive write rates, flexible/changing schemas |
| **Document (NoSQL)** | MongoDB, CouchDB | nested JSON-like records whose shape varies, e.g. device configs, API payloads | joins across collections, strict consistency |
| **Key-value** | Redis, DynamoDB | very fast lookups by key: caching, sessions, latest value of a sensor, queues | querying by anything other than the key |
| **Time-series** | InfluxDB, TimescaleDB (Postgres extension), Prometheus | timestamped measurements: meter readings, prices, sensor data | updates/deletes of old data, complex relationships |

**Time-series database features worth naming:** append-heavy writes; time-partitioned storage
(chunks/shards by time); compression; **downsampling** (keep 1-min data for 30 days, hourly forever);
**retention policies** (auto-delete old raw data); built-in time bucketing (`time_bucket('1 hour', ts)` in TimescaleDB);
gap filling and interpolation.

**Typical energy system answer:** "Postgres for sites/customers/assets (relational), TimescaleDB or Influx
for meter and sensor readings, Redis to cache the latest readings and as a simple queue."

### SQL essentials (see [example_20_sql_timeseries.py](examples/example_20_sql_timeseries.py))
- Order: `SELECT ... FROM ... JOIN ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT`
- `WHERE` filters rows **before** grouping, `HAVING` filters groups **after**
- **JOINs:** `INNER` (matches only), `LEFT` (all from left, NULLs where no match), `FULL OUTER`
- **Window functions:** `LAG()`, `LEAD()`, `ROW_NUMBER()`, `RANK()`, `AVG() OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`
- **Keys:** primary key = unique row id; foreign key = reference to another table's key
- **Normalisation:** don't repeat data; split it into related tables (1NF: atomic values, 2NF/3NF: every column depends on the key, the whole key, and nothing but the key)
- **Indexes:** speed up reads (B-tree, like a book index), slow down writes, cost space. Composite index on `(site_id, ts)` for time-series queries
- **ACID:** Atomic (all or nothing), Consistent, Isolated, Durable. Use a transaction when e.g. moving money
- **SQL injection:** never build SQL with f-strings; use parameters (`?` or `%s`)
- `NULL`: use `IS NULL`, not `= NULL`. `COUNT(*)` counts rows, `COUNT(col)` skips NULLs
- **CAP theorem** (distributed DBs): during a network partition you choose Consistency or Availability

---

## 3. Maths concepts

### Statistics
- **Mean** (sensitive to outliers) vs **median** (robust) vs **mode**
- **Variance** = average squared distance from the mean; **standard deviation** = √variance (same units as the data)
- **Percentiles/quantiles:** p95 = 95% of values are below this (used for peak demand planning)
- **Z-score** = (x − mean) / std → |z| > 3 is a common outlier rule
- **Correlation** (−1 to 1): strength of a linear relationship. *Correlation ≠ causation*
- **Normal distribution:** 68% within 1σ, 95% within 2σ, 99.7% within 3σ
- **Linear regression:** y = mx + c, fitted by least squares (minimise the sum of squared errors); R² = share of variance explained
- **Error metrics for forecasts:** MAE (mean absolute error), RMSE (punishes big errors more), MAPE (percentage, breaks when actual ≈ 0)

### Time-series
- **Components:** trend + seasonality (daily/weekly/yearly cycles) + noise
- **Moving average** smooths noise; **exponential smoothing** weights recent values more
- **Resampling:** downsample (half-hourly → daily: sum energy, average power) / upsample (needs interpolation)
- **Stationarity:** mean/variance don't change over time; differencing (`diff()`) helps achieve it
- **Autocorrelation:** correlation of a series with a lagged copy of itself (electricity demand is strongly correlated with the same time yesterday and last week)
- **Forecasting baseline:** "same as last week" (seasonal naive), always compare models against it
- **Train/test split by time**, never randomly (otherwise you're using the future to predict the past)
- **Timezones and DST:** store in UTC; in the UK a DST day has 46 or 50 half-hour periods, not 48

### Optimisation
- **Parts of the problem:** decision variables (e.g. charge/discharge each half hour), objective (maximise profit / minimise cost), constraints (battery capacity, power limit, state of charge ≥ 0)
- **Linear programming (LP):** linear objective + linear constraints → solved exactly (simplex). Tools: `scipy.optimize.linprog`, PuLP, Pyomo, OR-Tools
- **MILP:** some variables are integers/binary (e.g. on/off generator). Much harder: NP-hard in general
- **Gradient descent:** step in the direction of steepest decrease; learning rate controls step size; may find a local minimum instead of the global one
- **Convex** problems: any local minimum is the global minimum, so they're "easy"
- **Greedy vs dynamic programming:** greedy picks the best option now; DP solves sub-problems and reuses them (battery scheduling over time is a classic DP/LP problem)

### Linear algebra & calculus (conceptual)
- Vectors and matrices, dot product, matrix multiplication (shapes: (m×n)·(n×p) = m×p)
- Derivative = rate of change (power is the derivative of energy; energy is the integral of power)
- Numerical integration: trapezoidal rule (`np.trapezoid`) to get kWh from kW samples

### Complexity (Big-O)
- O(1) dict lookup, O(log n) binary search, O(n) one loop, O(n log n) sorting, O(n²) nested loops
- Be ready to say the time **and** space complexity of anything you write

---

## 4. Energy domain basics (a "distinct advantage")

- **Power (kW, MW)** = rate; **energy (kWh, MWh)** = power × time. 2 kW for 30 min = 1 kWh
- **Load profile:** demand over a day; **peak demand** drives grid costs; **base load** = minimum constant demand
- **Capacity factor** = actual output ÷ maximum possible output (UK solar ≈ 10–12%, onshore wind ≈ 25–35%)
- **UK settlement periods:** 48 half-hours per day; electricity is traded and settled per half-hour
- **Markets:** day-ahead and intraday wholesale markets; **imbalance price** for being off your forecast; prices in £/MWh
- **Batteries (BESS):** capacity (MWh) vs power rating (MW); a 2-hour battery = 50 MW / 100 MWh; **state of charge (SoC)**; **round-trip efficiency** ≈ 85–90%; **arbitrage** = charge cheap, discharge expensive (see [problem_10](problems/problem_10_battery_arbitrage.py)); **degradation** with cycling
- **Grid frequency:** 50 Hz in the UK/Europe; frequency response services balance supply and demand in seconds
- **Renewables:** variable and weather-dependent → forecasting matters; **curtailment** = turning generation down
- **Demand response / flexibility:** shifting load to cheaper or greener times
- **Smart meters** produce half-hourly time-series data; **SCADA** = industrial monitoring/control systems
- **Carbon intensity** (gCO₂/kWh) changes through the day with the generation mix

---

## 5. APIs, messaging, Docker, cloud (quick definitions)

- **REST:** resources + HTTP verbs (GET read, POST create, PUT/PATCH update, DELETE); status codes 200 OK, 201 Created, 400 bad request, 401 unauthenticated, 403 forbidden, 404 not found, 429 rate-limited, 500 server error. Course examples: [example_8_requests.py](examples/example_8_requests.py), [bonus_3_rest_api.py](examples/bonus/bonus_3_rest_api.py)
- **Python API frameworks:** FastAPI (async, type hints, auto docs), Flask, Django
- **Messaging:** **queue** = each message processed by one consumer (RabbitMQ, SQS); **pub/sub / stream** = many consumers, replayable log (Kafka); **MQTT** = lightweight pub/sub for IoT devices and meters. Why: decouple producers and consumers, absorb spikes, retry on failure
- **Delivery guarantees:** at-most-once / at-least-once (make consumers **idempotent**) / exactly-once (hard)
- **Docker:** an **image** is a template, a **container** is a running instance of one. `Dockerfile` (FROM, COPY, RUN, CMD), `docker build -t app .`, `docker run -p 8000:8000 app`, `docker ps`, `docker logs -f id`, `docker exec -it id bash`, `docker compose up`. Containers vs VMs: containers share the host kernel, so they're lighter
- **Cloud:** compute (EC2 / Azure VMs), serverless (Lambda / Azure Functions), object storage (S3 / Blob), managed DBs (RDS), queues (SQS)
- **Other languages:** Rust/C++/Go for speed; Python calls into fast code (numpy is C underneath). Know *why*: compiled vs interpreted, the GIL, memory control

## 6. ML / LLM (conceptual)
- **Supervised** (labelled data: regression for numbers, classification for categories) vs **unsupervised** (clustering, anomaly detection)
- **Overfitting:** great on training data, bad on new data → fix with more data, a simpler model, regularisation, cross-validation
- Common energy uses: load and price forecasting (gradient boosting such as XGBoost/LightGBM is strong on tabular data), anomaly detection, predictive maintenance
- **LLMs:** transformer neural networks trained to predict the next **token**; context window; temperature (randomness); hallucination; **RAG** = retrieve relevant documents and put them in the prompt. Course examples: [example_10_ollama.py](examples/example_10_ollama.py), [example_11_hf_api_requests.py](examples/example_11_hf_api_requests.py)

---

## 7. Behavioural answers to prepare (the spec stresses these)
Have one short story (situation → what you did → result) for each:
- Working **independently** on something with little guidance
- **Debugging** a hard problem: how you narrowed it down
- **Defending a technical view** when someone disagreed (and what happened)
- **Explaining something technical to a non-technical person**
- **Learning something new quickly**
