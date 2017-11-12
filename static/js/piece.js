/**
 * Created by orion on 08/10/2017.
 */
'use strict';

function openfinder(objectId, kind) {
    const data = {
        objectid: objectId,
        cmd: 'openfinder',
        kind: kind
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

function copyTitle($this) {
    var parent = $this.parents('.cue-header').find('span').first(),
        title = parent.text(),
        $title = $('.edit-title');

    if (confirm('Use this title for the album? ' + title)) {
        $title.text(title);
        const data = {
            cmd: 'update_album_title',
            title: title,
            albumid: $title.attr('albumid')
        };
        ajaxPost(data);
    }
}

function titleOfPiece($val) {
    var parent = $val.parents('.hyperlink').first();
    return parent.find('a').first().text();
}

function postMakeCuesheet(name, ids) {
    ajaxPost({
        cmd: 'makecuesheet',
        ids: ids,
        name: name,
        albumid: $('#album_id').val()
    }, function(response){
        console.log(response);
        location.reload();
    })
}

function getSelectedCuesheetIds($selectForCuesheet, $makeCuesheet) {
    var active = false;
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            if (!active) {
                // first time making active true
                if ($makeCuesheet.val() === '') {
                    $makeCuesheet.val(titleOfPiece($(val)));
                }
            }
            active = true;
            ids.push(val.id);
        }
    });
    return ids;
}

function selectSiblingsInBetween($selectForCuesheet) {
    // if between checked items there are unchecked, check them
    var keys = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            keys.push(key);
        }
    });
    if (keys.length > 1) {
        for (var i = 1; i < keys.length; i++) {
            if (keys[i] - keys[i-1] > 1) {
                for (var j = keys[i-1] + 1; j < keys[i]; j++) {
                    $selectForCuesheet.get(j).checked = true;
                }
            }
        }
    }
}

function selectCheckboxes($selectForCuesheet, $makeCuesheet, mode) {
    var active = false;
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        val.checked = mode;
        if (mode) {
            ids.push(val.id);
            if (!active) {
                // first time making active true: use title of piece for cuesheet title
                if ($makeCuesheet.val() === '') {
                    $makeCuesheet.val(titleOfPiece($(val)));
                }
                active = true;
            }
        }
    });
    return ids;
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
    $('.toggle-cue-lines').click(function () {
        toggleContents($(this), 'li', '.content.cue-lines');
    });
    $('.cue-plus').click(function () {
        copyTitle($(this));
    });

    const $selectForCuesheet = $('.select-for-cuesheet'),
          $makeCuesheet = $('.make-cuesheet');
    var ids = [];

    $selectForCuesheet.click(function(e){
        if (e.shiftKey) {
            selectSiblingsInBetween($selectForCuesheet);
        }
        ids = getSelectedCuesheetIds($selectForCuesheet, $makeCuesheet);
    });
    $makeCuesheet.keydown(function(e) {
        if (e.key === 'Enter') {
            postMakeCuesheet($(e.target).val(), ids);
        }
    });
    $('.stukken .check-all').click(function() {
        ids = selectCheckboxes($selectForCuesheet, $makeCuesheet, true);
    });
    $('.stukken .check-nothing').click(function() {
        ids = selectCheckboxes($selectForCuesheet, $makeCuesheet, false);
    });
    $('.rename-cuesheet').click(function(){
        console.log(this.id);
        ajaxPost({
            cmd: 'renamecue',
            id: this.id,
            albumid: $('#album_id').val()
        }, function(response){
            console.log(response);
            location.reload();
        })
    });
    $('.create-cuesheet').click(function(){
        postMakeCuesheet($makeCuesheet.val(), ids);
    });
});