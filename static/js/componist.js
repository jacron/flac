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

function editComponistYears($this) {
    const data = {
        cmd: 'update_componist_years',
        years: $this.text().trim(),
        id: $this.attr('componist_id')
    };
    ajaxPost(data);
}

function preventSpilledDrop(obj) {
    obj.on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    obj.on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        obj.css('border', '2px dotted #0B85A1');
    });
    obj.on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
}

function uploadFile(fd, obj) {
    const url = '/ajax/';
    const headers = {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
        url: url,
        data: fd,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, // NEEDED, DON'T OMIT THIS
        headers: headers,
        success: function(msg){
            console.log(msg);
            obj.css('border', 'none');
            location.reload();
        },
        failure: function(msg){
            console.log(msg);
            obj.css('border', 'none');
        }
    });
}

function handleFileUpload(files, obj, personId, fieldName) {
    for (var i = 0; i < files.length; i++) {
        const file = files[i];
        console.log(file);
        var fd = new FormData();
        fd.append('file', file);
        fd.append('cmd', 'upload');
        fd.append(fieldName, personId);
        uploadFile(fd, obj);
    }
}

function handleDroppedUrl(url, obj, personId, fieldName) {
    const data = {
        cmd: 'url',
        url: url
    };
    data[fieldName] = personId;
    ajaxPost(data, function() {
        obj.css('border', 'none');
        location.reload();
    });
}

function handleDrop(obj, personId, fieldName) {
    obj.on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px solid #0B85A1');
    });
    obj.on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });
    obj.on('drop', function (e) {
        $(this).css('border', '2px dotted #0B85A1');
        e.preventDefault();
        const dt = e.originalEvent.dataTransfer;
        const files = dt.files;
        if (files.length) {
            handleFileUpload(files, obj, personId, fieldName);
        } else {
            const url = dt.getData('url');
            console.log(url);
            handleDroppedUrl(url, obj, personId, fieldName);
        }
    });
}

$(function () {
    // componist
    $('.edit-componist-name').keydown(function (e) {
        if (e.key === 'Tab') {
            editComponistName($(this));
        }
    });
    $('.edit-componist-years').keydown(function (e) {
        if (e.key === 'Tab') {
            editComponistYears($(this));
        }
    });
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
    $('.componist .remove').click(function () {
        removeComponist($(this));
    });
    $('.add-componist').click(function (e) {
        addComponist2($(e.target));
    });

    const componist_id = $('#componist_id').val();
    if (componist_id) {
        handleDrop($('#drop-area-componist'), componist_id, 'componist_id');
        preventSpilledDrop($('.componist'));
    }

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
});

