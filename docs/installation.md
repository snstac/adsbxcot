ADSBXCOT's functionality provided by a command-line program called `adsbxcot`.

There are several methods of installing ADSBXCOT. They are listed below, in order of complexity.

# Debian, Ubuntu, Raspberry Pi

Install ADSBXCOT, and prerequisite packages of [PyTAK](https://pytak.rtfd.io) & [AIRCOT](https://aircot.rtfd.io).

```sh linenums="1"
sudo apt update
wget https://github.com/ampledata/aircot/releases/latest/download/python3-aircot_latest_all.deb
sudo apt install -f ./python3-aircot_latest_all.deb
wget https://github.com/ampledata/pytak/releases/latest/download/python3-pytak_latest_all.deb
sudo apt install -f ./python3-pytak_latest_all.deb
wget https://github.com/ampledata/adsbxcot/releases/latest/download/python3-adsbxcot_latest_all.deb
sudo apt install -f ./python3-adsbxcot_latest_all.deb
```

# Windows, Linux

Install from the Python Package Index (PyPI) [Advanced Users]::

```sh
python3 -m pip install adsbxcot
```

# Developers

PRs welcome!

```sh linenums="1"
git clone https://github.com/snstac/adsbxcot.git
cd adsbxcot/
python3 setup.py install
```
