# flake8: noqa


def test_imports():
    """ Ensures all submodules are importable
    Acts as a simple smoketest.
    """

    from tg_apicore import apps
    from tg_apicore import docs
    from tg_apicore import pagination
    from tg_apicore import parsers
    from tg_apicore import renderers
    from tg_apicore import routers
    from tg_apicore import schemas
    from tg_apicore import test
    from tg_apicore import transformers
    from tg_apicore import views
    import tg_apicore
