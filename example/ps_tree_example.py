import json
import os

import transaction
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from pyramid_pages.models import BaseSacrudMpttPage

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class PageTree(Base, BaseSacrudMpttPage):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)


def sacrud_settings(config):
    config.include('ps_tree')
    config.registry.settings['ps_tree.models'] = (PageTree, )
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = ('', PageTree)


def database_settings(config):
    from sqlalchemy import engine_from_config
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()


class Fixtures(object):

    def __init__(self, session):
        self.session = session

    def add(self, model, fixtures):
        here = os.path.dirname(os.path.realpath(__file__))
        file = open(os.path.join(here, fixtures))
        fixtures = json.loads(file.read())
        for fixture in fixtures:
            self.session.add(model(**fixture))
        transaction.commit()


def main(global_settings, **settings):
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    config = Configurator(
        session_factory=my_session_factory,
        settings=settings
    )
    config.include(database_settings)

    fixture = Fixtures(DBSession)
    fixture.add(PageTree, 'fixtures/pages.json')
    fixture.add(PageTree, 'fixtures/country.json')

    config.include(sacrud_settings)
    return config.make_wsgi_app()


if __name__ == '__main__':
    settings = {
        'sqlalchemy.url': 'sqlite:///example.sqlite',
    }
    app = main({}, **settings)

    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
