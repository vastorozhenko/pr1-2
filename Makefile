
.PHONY: init run semgrep bandit audit zap up down docker-build

init:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run:
	FLASK_APP=src/app.py FLASK_ENV=development python src/db.py && flask run

semgrep:
	semgrep scan --error --config auto || true

bandit:
	bandit -r src || true

audit:
	pip-audit || true

up:
	docker-compose up -d --build

down:
	docker-compose down

zap:
	mkdir -p reports/zap && docker run --rm -v $$PWD/reports/zap:/zap/wrk 		owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:5000 -r zap.html -x zap.xml || true
