import transaction
from pyramid.httpexceptions import HTTPInternalServerError
from pyramid.view import view_config

from pyramid_sacrud.security import (PYRAMID_SACRUD_DELETE,
                                     PYRAMID_SACRUD_UPDATE)
from sacrud.common import pk_to_list

from . import CONFIG_MODELS, PS_TREE_GET_TREE, PS_TREE_PAGE_MOVE


def get_model(settings, tablename):
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
    table = get_model(request.registry.settings,
                      request.matchdict['tablename'])
    return table.get_tree(request.dbsession, json=True, json_fields=fields)


@view_config(
    route_name=PS_TREE_PAGE_MOVE,
    permission=PS_TREE_PAGE_MOVE,
    renderer='json'
)
def page_move(request):
    method = request.matchdict['method']
    node_id = request.matchdict['node_id']
    target_id = request.matchdict['target_id']
    tablename = request.matchdict['tablename']

    table = get_model(request.registry.settings, tablename)
    pk = table.get_pk_column()
    page = request.dbsession.query(table).filter(pk == node_id).one()

    if method == 'inside':
        page.move_inside(target_id)
    elif method == 'after':
        page.move_after(target_id)
    elif method == 'before':
        page.move_before(target_id)
    else:
        raise HTTPInternalServerError("Unavailable method {}".format(method))
    try:
        request.dbsession.commit()
    except AssertionError:
        transaction.commit()
    return ''
