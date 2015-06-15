# from sacrud.common import pk_to_list
from pyramid.view import view_config

from pyramid_sacrud.security import (PYRAMID_SACRUD_DELETE,
                                     PYRAMID_SACRUD_UPDATE)
from sacrud.common import pk_to_list

from . import CONFIG_MODELS, PS_TREE_GET_TREE, PS_TREE_PAGE_MOVE


def get_pages_model(settings, tablename):
    for model in settings[CONFIG_MODELS]:
        if model.__tablename__ == tablename:
            return model
    return None


@view_config(
    route_name=PS_TREE_GET_TREE,
    permission=PS_TREE_GET_TREE,
    renderer='json'
)
def get_tree(request):
    def fields(node):
        node_list_of_pk = pk_to_list(node, True),
        url_delete = request.route_url(
            PYRAMID_SACRUD_DELETE,
            table=node.__tablename__,
            pk=pk_to_list(node))
        url_update = request.route_url(
            PYRAMID_SACRUD_UPDATE,
            table=node.__tablename__,
            pk=pk_to_list(node))
        return {
            'url_delete': url_delete,
            'url_update': url_update,
            'list_of_pk': node_list_of_pk,
        }
    table = get_pages_model(request.registry.settings,
                            request.matchdict['tablename'])
    return table.get_tree(request.dbsession, json=True, json_fields=fields)


@view_config(
    route_name=PS_TREE_PAGE_MOVE,
    permission=PS_TREE_PAGE_MOVE,
    renderer='json'
)
def page_move(request):
    node = request.matchdict['node']
    method = request.matchdict['method']
    tablename = request.matchdict['tablename']
    left_sibling = request.matchdict['leftsibling']

    table = get_pages_model(request.registry.settings, tablename)
    pk = getattr(table, table.get_pk())
    page = request.dbsession.query(table).filter(pk == node).one()

    if method == 'inside':
        page.move_inside(left_sibling)
    if method == 'after':
        page.move_after(left_sibling)
    if method == 'before':
        page.move_before(left_sibling)
    return ''
