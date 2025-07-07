# Bookstore API Automation Testing

Automated API tests for the [FakeRestAPI Bookstore](https://fakerestapi.azurewebsites.net/index.html).\
Covers both functional (happy path) and edge-case scenarios for Books and Authors endpoints.

## ⚠️ API Limitations & Observations (some issues)

**Books API – POST**

- No validation for unique `id` – allows creating books with duplicate IDs.
- No validation for `pageCount` – possible to submit negative or nonsensical values.
- No validation for string length – excessively long strings can result in server error (502).

**Books API – PUT**

- No validation whether the book with given `id` exists – API allows updating non-existent books.
- No validation for correlation between path `id` and the `id` in request body.
- No validation for `pageCount` – negative values are accepted.
- No validation for string length – excessively long values may cause 502 error.

**Authors API**

- GET returns a different number of results on each request – responses are non-deterministic, so comparing repeated requests is not reliable.
- No validation whether the referenced book exists when adding a new author.

> If the API were to enforce such validation rules, **additional test cases would be recommended to cover these scenarios**.

**Test Structure**

- Depending on API evolution, some common request logic can be refactored into shared helpers to reduce code duplication.

---

## 🐍 Prerequisites

- **Python 3.13** (or compatible 3.11+)\
  [Download Python](https://www.python.org/downloads/)
- Optional (for Allure reports): [Allure Commandline](https://docs.qameta.io/allure/#_installing_a_commandline)

Check your version:

```bash
python --version
```

---

## 🚀 Setup

**1. Clone the repository**

```bash
git clone https://github.com/mar-tin-666/bookstore-api-automation.git
cd bookstore-api-automation
```

**2. Create and activate a virtual environment**

- **Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows (CMD or PowerShell):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🧪 Running the tests

**Basic run:**

```bash
pytest -v
```

**With HTML report:**

```bash
pytest --html=reports/pytest-report.html --self-contained-html
```

**With Allure report:**

```bash
pytest --alluredir=reports/allure-results
```

---

## 📊 Test Reports

- **HTML Report:**\
  Open `reports/pytest-report.html` in any web browser.

- **Allure Report:**

  1. Install Allure CLI ([installation guide](https://docs.qameta.io/allure/#_installing_a_commandline))
  2. Generate and view:
     ```bash
     allure serve reports/allure-results
     ```
     Or generate static HTML:
     ```bash
     allure generate reports/allure-results --clean -o allure-report
     ```

---

## ✅ What’s covered

- **Books API:** Full CRUD, positive & negative tests, schema validation
- **Authors API:** Full CRUD, positive & negative tests, schema validation
- **Validation:**
  - JSON Schema (strict contract with OpenAPI)
  - Pydantic models (Pythonic validation & typing)
- **Reusable helpers:** API clients, fixtures, data generators

---

## 🔁 CI/CD

**For GitLab CI**
- Pre-configured `.gitlab-ci.yml` pipeline

**For GitHub Actions**
- Pre-configured `.github/workflows/ci.ym` pipeline

**Common info**
- Runs all tests on each commit/merge request
- Publishes JUnit test report (browsable in pipeline "Tests" tab)
- Publishes HTML and Allure reports as downloadable artifacts
- Tests are executed inside a Python Docker image. A GitLab runner with internet access is required.

Download artifacts and view full reports locally if needed.

---

## 🗑️ Clean up

To remove the virtual environment and test reports:

```bash
deactivate
rm -rf venv/ reports/
```

---

## 📝 Notes

- All endpoints and data structures follow the [FakeRestAPI Swagger](https://fakerestapi.azurewebsites.net/swagger/v1/swagger.json)
- Allure CLI is **not** included in `requirements.txt` – install system-wide per [official docs](https://docs.qameta.io/allure/#_installing_a_commandline)

---

## 🙋‍♂️ Questions?

Create an Issue or contact the repository maintainer.
