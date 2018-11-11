dist: binary assets
	zip -r orts-linux64.zip dist/

binary: orts.py
	poetry run pyinstaller orts.py
	printf '#!/bin/sh\n./orts/orts' > dist/start.sh
	chmod +x dist/start.sh

assets:
	rm -rf dist/data dist/web
	cp -r data dist/
	cp -r web dist/

clean:
	rm -rf dist/* build/* orts.spec orts-linux64.tar.gz

test:
	python -m pytest

run:
	python orts.py
