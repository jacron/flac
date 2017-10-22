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
    if ($this.hasClass('fa-caret-right')) {
        $this.addClass('fa-caret-down');
        $this.removeClass('fa-caret-right');
        next.first().show();
    } else {
        $this.addClass('fa-caret-right');
        $this.removeClass('fa-caret-down');
        next.first().hide();
    }
}

function copyTitle($this) {
    var parent = $this.parents('.cue-header').find('span').first(),
        title = parent.text(),
        $title = $('.edit-title');

    $title.text(title);
    const data = {
        cmd: 'update_album_title',
        title: title,
        albumid: $title.attr('albumid')
    };
    ajaxPost(data);
}

$(function () {
    $('.album-image').click(function () {
        $(this).toggleClass('expanded');
    });
    $('.edit-title').keydown(function (e) {
        if (e.key === 'Tab') {
            editAlbumTitle($(this));
        }
    });
    $('.toggle-content').click(function () {
        toggleContent($(this), 'div', 'table');
    });
    $('.toggle-edit').click(function () {
        toggleContent($(this), 'div', '.content.edit');
    });
    $('.toggle-cue').click(function () {
        toggleContent($(this), 'div', '.content.cue');
    });
    $('.cue-plus').click(function () {
        copyTitle($(this));
    });
});