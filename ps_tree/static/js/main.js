'use strict';

if (typeof $ === 'undefined') { require('jquery'); }

(function($){

  $(window).load(function(){

    var $tree = $('#tree'),
        deleteButton = '.toolbar-button__item_type_delete',
        deleteButtonState = 'toolbar-button__item_state_disable',
        selectAllButton = '#SelectAll',
        selectedNodes = 0,
        allNodes = 0;

    var data = $.ajax({
      'url': DATA_URL,
      'async': false
    });

    $tree
      .on('tree.init', function(){
        var treeData = $tree.tree('getTree');

        treeData.iterate(function(node) {
          if($tree.tree('isNodeSelected', node)) {
            selectedNodes += 1;
          }
          allNodes += 1;
          return true;
        });
        if(selectedNodes !== 0){
          $(deleteButton).removeClass(deleteButtonState);
        }
        if(selectedNodes === allNodes){
          $(selectAllButton).prop('checked', 'checked');
          $(deleteButton).removeClass(deleteButtonState);
        }

      })
      .tree({
        data: data.responseJSON,
        dragAndDrop: true,
        useContextMenu: true,
        autoOpen: true,
        selectable: false,
        saveState: 'ps_tree_' + '{{ table.name }}',

        onCreateLi: function(node, $li) {
          var item = $li.find('.jqtree-title');
          var itemCheckbox = $('<input />')
                .attr({ type: 'checkbox',
                        name: 'selected_item',
                        value: node.list_of_pk })
                .addClass('jqtree-checkbox');
          item.before(itemCheckbox);

          if($tree.tree('isNodeSelected', node)) {
            itemCheckbox.prop('checked', true);
          }
        }
      })
      .on('tree.click', function(event){
        if($(event.click_event.target).is('.jqtree-checkbox')) {
          event.preventDefault();
          var node = event.node;

          if($tree.tree('isNodeSelected', node)) {
            selectedNodes -= 1;
            $tree.tree('removeFromSelection', node);
            $(this).prop('checked', false);
            $tree.find('.jqtree-selected .jqtree-checkbox').prop('checked', false);
            node.iterate(function(child_node) {
              $tree.tree('removeFromSelection', child_node);
              return true;
            });

          } else {
            selectedNodes += 1;
            $tree.tree('addToSelection', node);
            $(this).prop('checked', true);
            $tree.find('.jqtree-selected .jqtree-checkbox').prop('checked', 'checked');
            node.iterate(function(child_node) {
              $tree.tree('addToSelection', child_node);
              return true;
            });
          }
        } else {
          window.location = event.node.url_update;
          localStorage.clear();
        }

        if(selectedNodes === allNodes){
          $(selectAllButton).prop('checked', 'checked');
        } else {
          $(selectAllButton).removeAttr('checked');
        }
      })
      .on('tree.contextmenu', function(event) {
          var node = event.node;
          $tree.tree('addToSelection', node);
          node.iterate(function(child_node) {
            $tree.tree('addToSelection', child_node);
            return true;
          });
          $tree.find('.jqtree-selected .jqtree-checkbox').prop('checked', 'checked');
      })
      .on('tree.move', function(event){
        event.preventDefault();
        var url = MOVE_URL +
            event.move_info.moved_node.id + '/' +
            event.move_info.position + '/' +
            event.move_info.target_node.id + '/';

        var status = $.ajax({
          'url': url,
          'async': false
        }).status;

        if(status === 200) {
          event.move_info.do_move();
          $tree.tree('loadDataFromUrl', DATA_URL);
        } else {
          window.alert('Error');
        }
      });

    $(selectAllButton).on('click', function() {
      var treeData = $tree.tree('getTree'),
          state = $(this).prop('checked');

      treeData.iterate(function(node) {
        var checkbox = $tree.find('input');
        if(state === true){
          $tree.tree('addToSelection', node);
          $(deleteButton).removeClass(deleteButtonState);
          checkbox.prop('checked', true);
        } else if (state === false) {
          $tree.tree('removeFromSelection', node);
          $(deleteButton).addClass(deleteButtonState);
          checkbox.prop('checked', false);
        }
        return true;
      });
    });


    $tree.jqTreeContextMenu($('#treeContextMenu'), {
      'delete': function(node) {
        $tree.tree('addToSelection', node);
        node.iterate(function(child_node) {
          $tree.tree('addToSelection', child_node);
          return true;
        });
        $tree.find('.jqtree-selected .jqtree-checkbox').prop('checked', 'checked');
        var popup = window.popup;
        popup.showDeletePopup();
      }
    });

  });
})(jQuery);
