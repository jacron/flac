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

function openfinderPerformer(performerId) {
    const data = {
        arg: performerId,
        cmd: 'openfinder_performer'
    };
    ajaxPost(data);
}

function openfinderComponist(componistId) {
    const data = {
        arg: componistId,
        cmd: 'openfinder_componist'
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