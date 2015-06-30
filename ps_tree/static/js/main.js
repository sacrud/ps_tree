'use strict';

if (typeof $ === 'undefined') { require('jquery'); }

require('./vendor/jquery.cookie.js');

(function($){

  $(window).load(function(){

    var $tree = $('#tree');

    var data = $.ajax({
      'url': DATA_URL,
      'async': false
    });


    $tree.tree({
      data: data.responseJSON,
      dragAndDrop: true,
      useContextMenu: true,
      autoOpen: true,
      saveState: 'ps_tree_' + '{{ table.name }}',

      onCreateLi: function(node, $li) {
        var item = $li.find('.jqtree-title');
        var itemCheckbox = $('<input />')
              .attr({ type: 'checkbox',
                      name: 'selected_item',
                      value: node.list_of_pk })
              .addClass('jqtree-checkbox');
        item.before(itemCheckbox);
        itemCheckbox.on('click', function (event) {
          event.stopPropagation();
        });
      }
    });

    $tree.jqTreeContextMenu($('#treeContextMenu'), {
      'edit': function(node) {
        console.log('Edit node: ' + node.name);
      },
      'visible': function(node) {
        console.log('Visible node: ' + node.name);
      },
      'delete': function(node) {
        console.log('Delete node: ' + node.name);
      },
      'add': function(node) {
        console.log('Add node: ' + node.name);
      }
    });

    $tree.bind('tree.click', function(event) {
        window.location = event.node.url_update;
      }
    );

    $tree.bind('tree.move', function(event) {
      event.preventDefault();

      var url = MOVE_URL +
        event.move_info.moved_node.id + '/' +
        event.move_info.position + '/' +
        event.move_info.target_node.id + '/';

      var status = $.ajax({
        'url': url,
        'async': false
      }).status;

      if (status === 200) {
        event.move_info.do_move();
        $tree.tree('loadDataFromUrl', DATA_URL);
      } else {
        window.alert('Error');
      }

    });
  });
})(jQuery);