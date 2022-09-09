# ring

Command line utility for notifying user

## Usage:

Your computer will beep and notify you when command has finished running

```bash
$ long_script.sh; ring
```

Use `-l` or `--loop` to loop ringing until you press enter

View `ring_config.py` to change the default settings

## Installation

#### Windows:

Create file ring.bat and ringloop.bat somewhere in your PATH

```ring.bat
python C:\path\to\ring.py
```

```ringloop.bat
python C:\path\to\ring.py --loop
```

#### Linux:

Execute following commands

```bash
chmod +x /path/to/ring.py
ln -s /path/to/ring.py /usr/bin/ring
```
