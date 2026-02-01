# nathantebbs.com

Personal developer website.

## Build from source

1. Clone the repo

```bash
git clone --depth=1 https://github.com/nathantebs/nathantebbs.com
```

2. Setup Python venv

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

3. Verify: list packages and run the build script

```bash
$ pip list
$ python3 build.py
```
