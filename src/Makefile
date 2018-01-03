

.PHONY=main

main:	optimisation.so


optimisation.so: optimisation.pyx setup.py
	python3 setup.py build_ext --inplace
