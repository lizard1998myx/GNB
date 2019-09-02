import nonebot
import config
import os


def main():
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'awesome', 'plugins'),
        'awesome.plugins'
    )
    nonebot.run()


if __name__ == '__main__':
    main()