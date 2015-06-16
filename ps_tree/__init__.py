#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Show pyramid_sacrud records as tree.
"""
from pyramid.events import ApplicationCreated

CONFIG_MODELS = 'ps_tree.models'
PS_TREE_GET_TREE = 'ps_tree_get_tree'
PS_TREE_PAGE_MOVE = 'ps_tree_page_move'


def models_preparing(app):
    settings = app.app.registry.settings
    models = settings[CONFIG_MODELS]
    for model in models:
        if hasattr(model, 'sacrud_list_template'):
            continue
        model.sacrud_list_template = 'ps_tree/tree.jinja2'


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("templates")
    config.add_static_view('/ps_tree_static', 'ps_tree:static')
    config.add_subscriber(models_preparing, ApplicationCreated)

    config.add_route(
        PS_TREE_GET_TREE,
        '/ps_tree/{tablename}/get/tree/'
    )
    config.add_route(
        PS_TREE_PAGE_MOVE,
        '/ps_tree/{tablename}/move/{node_id}/{method}/{target_id}/'
    )
    config.scan('.views')
