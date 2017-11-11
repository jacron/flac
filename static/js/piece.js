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

function openfinderComponisten() {
    const data = {
        arg: null,
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
                $makeCuesheet.val(titleOfPiece($(val)));
            }
            active = true;
            ids.push(val.id);
        }
    });
    $makeCuesheet.toggle(active);
    return ids;
}

function selectSiblingsInBetween($selectForCuesheet) {
    // console.log($selectForCuesheet);
    // if between checked items there are unchecked, check them
    var active = false;
    var keys = [];
    // var checkboxes = [];
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
    // console.log(ids);
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
    })
});