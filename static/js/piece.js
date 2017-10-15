/**
 * Created by orion on 08/10/2017.
 */
'use strict';

function openfinder(albumId) {
    const data = {
        arg: albumId,
        cmd: 'openfinder'
    };
    ajaxPost(data);
}

function play(idPiece) {
    const data = {
        arg: idPiece,
        cmd: 'play'
    };
    ajaxPost(data);
}

function editAlbumTitle($this) {
   const data = {
       cmd: 'update_album_title',
       title: $this.text().trim(),
       albumid: $this.attr('albumid')
   };
   ajaxPost(data);
}

function toggleContent($this, parent, sibling) {
    const next = $this.parents(parent).siblings(sibling);
    if ($this.hasClass('fa-caret-up')) {
        $this.addClass('fa-caret-down');
        $this.removeClass('fa-caret-up');
        next.show();
    } else {
        $this.addClass('fa-caret-up');
        $this.removeClass('fa-caret-down');
        next.hide();
    }
}

$(function() {
   $('.album-image').click(function(){
      $(this).toggleClass('expanded');
   });
   $('.edit-title').keydown(function(e) {
       if (e.key === 'Tab') {
           editAlbumTitle($(this));
       }
   });
   $('.toggle-content').click(function(){
       toggleContent($(this), 'h4', 'table');
   });
   $('.toggle-edit').click(function(){
       toggleContent($(this), 'h4', '.content.edit');
   });
});