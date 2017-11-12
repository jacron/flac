/**
 * Created by orion on 12/11/2017.
 */
'use strict';

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

function toggleContents($this, parent, sibling) {
    const next = $this.parents(parent).siblings(sibling);
    if ($this.hasClass('fa-caret-right')) {
        $this.addClass('fa-caret-down');
        $this.removeClass('fa-caret-right');
        next.show();
    } else {
        $this.addClass('fa-caret-right');
        $this.removeClass('fa-caret-down');
        next.hide();
    }
}

$(function () {
    $('.toggle-content').click(function () {
        toggleContent($(this), 'div', 'table');
    });
    $('.toggle-edit').click(function () {
        toggleContent($(this), 'div', '.content.edit');
    });
    $('.toggle-cue').click(function () {
        toggleContent($(this), 'div', '.content.cue');
    });
    $('.toggle-cue-lines').click(function () {
        toggleContents($(this), 'li', '.content.cue-lines');
    });
});