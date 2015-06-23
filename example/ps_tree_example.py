import json
import os

import transaction
from pyramid.config import Configurator
from pyramid.response import Response
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

    def ps_tree_fields(self, request):
        url_visible = request.route_url(
            'node_toggle_visible',
            tablename=self.__tablename__,
            id=self.id
        )
        return {
            'visible': self.visible,
            'url_visible': url_visible
        }


def node_toggle_visible(request):
    id = request.matchdict['id']
    tablename = request.matchdict['tablename']
    settings = request.registry.settings
    models = settings['ps_tree.models']
    for model in models:
        if model.__tablename__ == tablename:
            break
    node = DBSession.query(model).filter_by(id=id).one()
    node.visible = not node.visible
    transaction.commit()
    return Response('OK')


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
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('ps_tree_example:templates')
    config.add_static_view('ps_tree_example_static', 'static')
    config.include(database_settings)

    fixture = Fixtures(DBSession)
    fixture.add(PageTree, 'fixtures/pages.json')
    fixture.add(PageTree, 'fixtures/country.json')

    config.add_route('node_toggle_visible', '/toggle/visible/{tablename}/{id}')
    config.add_view(node_toggle_visible, route_name='node_toggle_visible')

    config.include(sacrud_settings)
    return config.make_wsgi_app()


if __name__ == '__main__':
    settings = {
        'sqlalchemy.url': 'sqlite:///example.sqlite',
    }
    app = main({}, **settings)

    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)
