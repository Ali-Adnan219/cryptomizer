# ----- linux -----
install-linux:
	@echo "Installing..."
	sudo cp dist/main /usr/local/bin/cryptomizer
	@echo "Done"

uninstall-linux:
	@echo "Uninstalling..."
	sudo rm /usr/local/bin/cryptomizer
	@echo "Done."

ctk := $(shell python -c 'import customtkinter;import os.path; print(os.path.split(customtkinter.__file__)[0]);')
build-linux:
	python -m nuitka src/main.py --output-dir=dist --onefile --linux-onefile-icon=assets/icon.png --assume-yes-for-downloads --include-data-dir="$(ctk)=customtkinter/" --enable-plugin=tk-inter -o dist/cryptomizer

# ----- windows -----
build-windows:
	python -m nuitka src/main.py --output-dir=dist --onefile --mingw64 --assume-yes-for-downloads --windows-icon-from-ico=assets/icon.ico --include-data-dir="$(ctk)=customtkinter/" --enable-plugin=tk-inter -o dist/cryptomizer.exe

# ----- mac-os -----
build-macos:
	python -m nuitka src/main.py --output-dir=dist --onefile --linux-onefile-icon=assets/icon.png --assume-yes-for-downloads --include-data-dir="$(ctk)=customtkinter/" -o dist/cryptomizer
