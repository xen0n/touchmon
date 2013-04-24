# touchmon

## Introduction

`touchmon` is a simple filesystem observer that spawns subprocesses with
pre-configured arguments, whenever the corresponding files are touched or
modified. This can be really handy if you have some kind of "timestamp files"
set up, that get touched if something interesting happens, e.g. a deploy
instruction.

This script is Linux-specific, as it uses the
[`pyinotify`](http://seb-m.github.io/pyinotify/) library to access the
underlying `inotify` API for its functionality.


## Installation

Easy. You can install it anywhere, with or without a virtualenv.


    $ git clone https://github.com/xen0n/touchmon.git
    $ cd touchmon/
    $ pip install -r requirements.txt

This installs the dependency into the global site packages directory. If you
don't want this to happen, you can choose to install it inside a dedicated
virtualenv.

You should be all set; go define some actions :D


## Action files

`touchmon` reads its configuration from action files specified on the command
line. Action files are plain JSON files with a structure like this:

```json
{
    "path/to/file/to/monitor": {
        "argv": [
            "program-name",
            "argv[1]",
            "argv[2]"
            ],
        "user": "user1"
        },
    "path/to/another/file": {
        "argv": [
            "another-program",
            "another-arg"
            ],
        "user": "user2"
        }
}
```


## Invocation

### Basic usage

The script is invoked with a list of action files:

    # ./touchmon.py path/to/action1.json path/to/action2.json

The `.json` extension is not required, but recommended to keep the name clear.
Action files are read in the order specified; if more than one action for a
particular file is defined, the last one is taken.

The script does not daemonize after starting. To achieve this, you may use a
process manager like [supervisor](http://supervisord.org/). Here is an example
entry to put in `supervisord.conf`:

    [program:touchmon]
    command=/path/to/touchmon.py /path/to/action/file.json
    directory=/path/to/
    autostart=true
    autorestart=unexpected
    stopsignal=INT
    user=root


### Running inside a virtualenv

To avoid installing packages into the global `site-packages` directory, you
can install the dependency into a virtualenv. Your invocation would be a bit
more complex though, due to existence of the virtualenv. Fortunately you
would only have to add one extra line in the program entry described earlier:

    environment=PATH=/path/to/venv/bin,VIRTUALENV=/path/to/venv

That makes the script aware of its intended environment.


## Security

To be able to `set{g,u}id` its subprocesses, `touchmon` must be run as root.
As the program does nothing except watching the files, this should not be
a problem. However, if you do notice some security flaws, please notice me.


## License

BSD license; see the `LICENSES` file for details.


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8 syn=markdown: -->
