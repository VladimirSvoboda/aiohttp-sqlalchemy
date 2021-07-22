import pytest


def test_deprecation() -> None:
    from aiohttp_sqlalchemy import views, web_handlers
    assert views is web_handlers

    from aiohttp_sqlalchemy import SAItemAddMixin, UnitAddMixin
    assert SAItemAddMixin is UnitAddMixin

    from aiohttp_sqlalchemy.web_handlers import ListAddMixin, SAListAddMixin
    assert SAListAddMixin is ListAddMixin

    with pytest.raises(ImportError):
        from aiohttp_sqlalchemy import NotExist
        assert bool(NotExist)
