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

.PHONY: venv install clean clean-pyc console
