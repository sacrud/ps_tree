Settings
========

For create models with tree structure use mixin from the :class:`sqlalchemy_mptt.mixins.BaseNestedSets`.

initialize
----------

.. code-block:: python

    config.include('ps_tree')
    config.registry.settings['ps_tree.models'] = (PageTree, )

    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = ('', PageTree)

context menu
------------

Soon ...

template
--------

You can redefine template of tree in ``youproject/templates/ps_tree/tree.jinja2``.

.. literalinclude:: ../../ps_tree/templates/ps_tree/tree.jinja2
   :caption: Default template ``tree.jinja2``
   :language: html
