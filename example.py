from aiohttp import web
import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_engine, sa_middleware
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm


metadata = sa.MetaData()
Base = orm.declarative_base(metadata=metadata)


class Request(Base):
    __tablename__ = 'requests'
    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


async def main(request):
    async with app['sa_main'].begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with request['sa_main'].begin():
        request['sa_main'].add_all([Request()])
        result = await request['sa_main'].execute(sa.select(Request))
        data = {r.id: r.timestamp.isoformat() for r in result.scalars()}
        return web.json_response(data)


app = web.Application(middlewares=[sa_middleware()])
app.router.add_get('/', main)
aiohttp_sqlalchemy.setup(app, [sa_engine(url='sqlite+aiosqlite:///')])
web.run_app(app)
