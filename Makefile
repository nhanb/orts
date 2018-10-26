dist: binary assets

binary: orts.py
	poetry run pyinstaller --onefile orts.py

assets:
	rm -rf dist/data dist/web
	cp -r data dist/
	cp -r web dist/

clean:
	rm -r dist/* orts.spec
