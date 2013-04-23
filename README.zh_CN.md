# touchmon

## 简介

`touchmon` 是一个简单的文件系统观察工具，只要被观察文件被 `touch` 或被修改，就以预先配置的参数启动相应的子进程。如果你设置了一些“时间戳文件”，就会非常方便。“时间戳文件”在某些感兴趣的事件发生的时候会被 `touch`，比方说接到一个部署命令的时候。

这个脚本只能运行在 Linux 环境下，因为它使用 [`pyinotify`](http://seb-m.github.io/pyinotify/) 库访问底层的 `inotify` API 来实现功能。


## 安装

安装过程很简单。你可以把它装到任何地方，用或者不用 virtualenv 都行。

    $ git clone https://github.com/xen0n/touchmon.git
    $ cd touchmon/
    $ pip install -r requirements.txt

这会把依赖关系装到全局的包目录里。如果你不想这么干，你可以选择使用一个单独的 virtualenv。

到这里应该差不多了；该定义一些动作了。:D


## 动作文件

`touchmon` 从命令行上指定的动作文件中读取配置。动作文件就是普通的 JSON 文件，有这样的结构：

```json
{
    "path/to/file/to/monitor": [
        "program-name",
        "argv[1]",
        "argv[2]"
        ],
    "path/to/another/file": [
        "another-program",
        "another-arg",
        ]
}
```


## 运行

### 基本使用方法

脚本接受一个或多个动作文件作为参数：

    $ ./touchmon.py path/to/action1.json path/to/action2.json

`.json` 扩展名不是必需的，但推荐使用它让文件名清晰一点。动作文件是按照指定的顺序读取的；如果为同一个文件定义了多个动作，只有最后一个会生效。

脚本启动之后不会 daemonize。为了实现这个，你可以用个进程管理器，比如 [supervisor](http://supervisord.org/)。这是一个 `supervisord.conf` 程序条目的例子：

    [program:touchmon]
    command=/path/to/touchmon.py /path/to/action/file.json
    directory=/path/to/
    autostart=true
    autorestart=unexpected
    stopsignal=INT
    user=exampleuser


### 在 virtualenv 中运行

为了防止往全局包目录安装包，你可以把依赖关系装进一个 virtualenv。不过因为 virtualenv 的存在，你的调用会相应麻烦一点。幸好你只需要在上面的条目里增加一行：

    environment=PATH=/path/to/venv/bin,VIRTUALENV=/path/to/venv

这就让脚本明白它应该处于的环境了。


## 许可证

BSD 许可证；细节请见 `LICENSES` 文件。


<!-- vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8 syn=markdown: -->
