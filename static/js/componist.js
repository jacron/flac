/**
 * Created by orion on 15/10/2017.
 */

'use strict';

function addComponist0(componistId, albumId) {
    const data = {
        cmd: 'add_componist',
        componistid: componistId,
        albumid: albumId
    };
    ajaxPost(data);
    location.reload();
}

function addComponist($select) {
    addComponist0($select.val(), $select.attr('albumid'));
}

function addComponist2($target) {
    addComponist0($target.attr('id'), $('#album_id').val());
}

function newComponist($input) {
    const data = {
        cmd: 'new_componist',
        name: $input.val(),
        albumid: $input.attr('albumid')
    };
    ajaxPost(data);
    location.reload();
}

function addNewComponist($input) {
    const data = {
        cmd: 'abs_new_componist',
        name: $input.val()
    };
    ajaxPost(data, function (id) {
        console.log(id);
        $('.componist-added').text(id);
    });
    // location.reload();
}

function removeComponist($this) {
    const data = {
        cmd: 'remove_componist',
        id: $this.attr('id'),
        albumid: $('#album_id').val()
    };
    ajaxPost(data);
    location.reload();
}

function editComponistName($this) {
    const data = {
        cmd: 'update_componist_name',
        name: $this.text().trim(),
        id: $this.attr('componist_id')
    };
    ajaxPost(data);
}

function editComponistYears($this, cmd, val) {
    const data = {
        cmd: cmd,
        years: val.trim(),
        id: $this.attr('componist_id')
    };
    console.log('data', data);
    ajaxPost(data);
}


$(function () {
    // componist
    $('button.select-componist').click(function () {
        addComponist($('select.select-componist'));
    });
    $('button.add-componist').click(function () {
        newComponist($('input.add-componist'));
    });
    $('input.add-componist').keydown(function (e) {
        if (e.key === 'Enter') {
            newComponist($('input.add-componist'));
        }
    });
    $('select.select-componist').keydown(function (e) {
        if (e.key === 'Enter') {
            addComponist($('select.select-componist'));
        }
    });
    $('.add-componist').click(function (e) {
        addComponist2($(e.target));
    });

    $('.jump-to-letter').keydown(function(e){
        const $target = $(e.target),
            search = $target.val().toUpperCase();
        if (e.key === 'Enter') {
            jumpToSearched(search);
        }
    });
    $('.componist-period').keydown(function (e) {
        if (e.key === 'Enter') {
            const $target = $(e.target);
            location.href = '/componist/' + $target.val() + '/period/';
        }
    });
    const componist_id = $('#componist_id').val();
    if (componist_id) {
        $('.componist .remove').click(function () {
            removeComponist($(this));
        });

        $('.edit-componist-name').keydown(function (e) {
            if (e.key === 'Tab') {
                editComponistName($(this));
            }
        });
        // $('.edit-componist-years').keydown(function (e) {
        //     if (e.key === 'Tab') {
        //         editComponistYears($(this), 'update_componist_years', $(this).attr);
        //     }
        // });
        $('.edit-componist-birth')
            .focus(function(){$(this).select()})
            .mouseup(function(e){e.preventDefault()})
            .keydown(function(e) {
            if (e.key === 'Tab' || e.key === 'Enter') {
                editComponistYears($(this), 'update_componist_birth', $(this).val());
            }
        });
        $('.edit-componist-death')
            .focus(function(){$(this).select()})
            .mouseup(function(e){e.preventDefault()})
            .keydown(function(e) {
            if (e.key === 'Tab' || e.key === 'Enter') {
                editComponistYears($(this), 'update_componist_death', $(this).val());
            }
        });
    }
});

