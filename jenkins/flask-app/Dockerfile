# base: runtime dependencies + app code
FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# test: lint + unit tests
FROM base AS test
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY test_app.py .
RUN ruff check . && python -m pytest -q && touch /tmp/tests-passed

# final
FROM base AS final
COPY --from=test /tmp/tests-passed /tmp/tests-passed
RUN useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]