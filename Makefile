# ---- Install ----
venv:
	@test -d venv || virtualenv venv

install: venv
	@source venv/bin/activate; pip install -r requirements.txt
clean: clean-pyc
	@rm -rf venv
clean-pyc:
	@ find . -name "*.pyc" -exec rm -rf {} \;

# ---- Console ----
console:
	@source venv/bin/activate; ipython -i -c 'from stockfighter import api'

# ---- Documentation ----
docs:
	@source venv/bin/activate; cd docs; make html;
	@cd ../python-stockfighter-docs/html; git add .; git commit -m "rebuilt docs"; git push origin gh-pages

.PHONY: venv install clean clean-pyc console docs
