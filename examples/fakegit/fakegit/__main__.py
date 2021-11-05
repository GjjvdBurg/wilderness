# -*- coding: utf-8 -*-


def main():
    from .console import build_application

    app = build_application()
    app.run()


if __name__ == "__main__":
    main()
