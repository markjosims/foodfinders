.PHONY: IDB2.log

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Windows
    PYTHON   := python                 # on my machine it's python
    PIP      := pip3
    PYLINT   := pylint
    COVERAGE := coverage
    PYDOC    := python -m pydoc        # on my machine it's pydoc
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint3
    COVERAGE := coverage
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
endif

models.html: app/models.py
	$(PYDOC) -w models

IDB2.log:
	git log > IDB2.log

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  Tests.tmp
	rm -f IDB2.log
	rm -rf __pycache__

scrub:
	make clean
	rm -f main.html
	rm -f IDB2.log

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

versions:
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	which git
	git	--version
	@echo
	which make
	make --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version

log: IDB2.log