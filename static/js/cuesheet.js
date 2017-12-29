/**
 * Created by orion on 08/10/2017.
 */
'use strict';

function titleOfPiece($val) {
    var parent = $val.parents('.hyperlink').first();
    return parent.find('a').first().text();
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

function getAlbumComponisten() {
    var items = [];
    $.each($('li.hyperlink.componist'), function(key, li){
        items.push($(li).find('a').text().trim());
    });
    return items;
}

function copyComponist(componist, $makeCuesheet) {
    // const normalizedComponist = componist.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
    var val = $makeCuesheet.val();
    if (val[0] !== ' ' && val[0] !== '-') {val = ' - ' + val;}
    $makeCuesheet.val(componist + val);
}

function similar($selectForCuesheet) {
    var titles = [];
    var ids = [];
    var common = '';
    var active = false;
    var old_common = '';
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            active = true;
        }
        if (active) {
            val.checked = false;
            ids.push(val.id);
            titles.push(titleOfPiece($(val)));
            common = lcs(titles);
            if (titles.length > 2 && common.length < old_common.length - 2) {
                titles.pop();
                ids.pop();
                val.checked = true;
                return false;  // break each()
            }
            old_common = common;
        }
    });
    return {
        titles: titles,
        ids: ids
    };
}

function rtrim(s, a) {
    a.forEach(function(c){
       if (s.substr(s.length - c.length) === c) {
            s = s.substr(0, s.length - c.length);
            s = s.trim();
        }
    });
    return s;
}

function ltrim(s, a) {
    a.forEach(function(c){
       if (s.length < 2) {
           return;
       }
       if (s.substr(0, 1) === c) {
            s = s.substr(1);
            s = s.trim();
        }
    });
    return s;
}

function trimNr(s) {
    s = s.trim();
    s = rtrim(s, ['No.', 'I', '-', ',', '.flac', ':']);
    s = ltrim(s, ['.', '-']);
    return s.trim();
}

function lcs_pieces($selectForCuesheet, $makeCuesheet){
    var titles = [];
    var ids = [];
    $.each($selectForCuesheet, function(key, val) {
        if (val.checked) {
            titles.push(titleOfPiece($(val)));
            ids.push(val.id);
        }
    });
    if (titles.length === 1) {
        const data = similar($selectForCuesheet);
        titles = data.titles;
        ids = data.ids;
    }
    $makeCuesheet.val(trimNr(lcs(titles)));
    return ids;
}

function markTestedCuesheets(ids) {
    var pieces = $('.stukken .piece');
    pieces.removeClass('selected');
    ids.forEach(function(id){
        $.each(pieces, function(){
            var $this = $(this);
            if ($this.attr('id') === id) {
                $this.addClass('selected');
            }
        })
    });
}

$(function () {
    function unmarkTestedCuesheets() {
        var pieces = $('.stukken .piece');
        pieces.removeClass('selected');
    }

    function autoCreate($selectForCuesheet, cuesheetIds, $makeCuesheet, $typeahead) {
        $selectForCuesheet.first().get(0).checked = true; // init following function
        do {
            cuesheetIds = lcs_pieces($selectForCuesheet, $makeCuesheet);
            if (cuesheetIds.length) {
                console.log(cuesheetIds);
                createCuesheet($makeCuesheet, cuesheetIds, $typeahead);
            }
        } while (cuesheetIds.length);
        location.reload();
    }

    function afterPostMake($makeCuesheet, $typeahead) {
        $makeCuesheet.val('');
        var items = getAlbumComponisten();
        if (items.length === 1) {$typeahead.val(items[0]); }
        else { $typeahead.val('')}
        unmarkTestedCuesheets();
    }

    function createCuesheet($makeCuesheet, cuesheetIds, $typeahead) {
        postMakeCuesheet($makeCuesheet.val(), cuesheetIds, function(response) {
            afterPostMake($makeCuesheet, $typeahead)});
    }

    function prop(v) {
        // special: convert names to numbers
        const names = ['Prelude|Prélude|Praeludium', 'Allemande', 'Courante', 'Sarabande',
            'Menuet|Bourree|Gavotte', 'Gigue'];
        for (var i = 0; i < names.length; i++) {
            const name = names[i],
                w = name.split('|');
            for (var j = 0; j < w.length; j++) {
                if (v.indexOf(w[j]) === 0) {
                    return i + 1;
                }
            }
        }
        // trim right
        [',', '.', ':'].forEach(function(last){
            if (v.substr(v.length-1, 1) === last) {
                v = v.substr(0, v.length-1);
            }
        });
        // trim left
        ['#', 'No.', 'Nr.', 'No', 'no.'].forEach(function(first){
            if (v.indexOf(first) === 0) {
                v = v.substr(first.length);
            }
        });
        // convert roman digits
        const romans = ['I', 'II', 'III', 'IV', 'V', 'VI'];
        const pos = romans.indexOf(v);
        if (pos !== -1) {
            return pos + 1;
        }
        if ($.isNumeric(v)) {
            return v;
        }
    }

    function proposeCode(text, prefix) {
        var proposal = prefix;
        // console.log(text);
        const w = text.split(" ");
        // skip the first (number?) word, so i = 1
        var nrs = [];
        for (var i = 1; i < w.length; i++) {
            var p = prop(w[i]);
            if (p) {
                nrs.push(p);
            }
        }
        if (nrs.length === 1) {
            return proposal + nrs[0];
        }
        // negeer het tweede getal, bijv. 'BWV 1010'
        if (nrs.length > 2) {
            return proposal + nrs[0] + '_' + nrs[2];
        }
        if (nrs.length > 1) {
            return proposal + nrs[0] + '_' + nrs[1];
        }
        return proposal;
    }

    function proposeKCode(text, keywords, proposal) {
        // console.log(text);
        for (var i = 0; i < keywords.length; i++) {
            const keyword = keywords[i],
                pos = text.indexOf(keyword);
            if (pos !== -1) {
                proposal += parseInt(text.substr(pos + keyword.length));
                text = text.substr(pos + keyword.length);
                break;
            }
        }
        const w = text.split(" ");
        var nrs = [];
        // skip first word, is already parsed
        for (var i = 1; i < w.length; i++) {
            var p = prop(w[i]);
            if (p) {
                nrs.push(p);
            }
        }
        if (nrs.length) {
            proposal += '_' + nrs[0];
        }
        return proposal;
    }

    function addCode($this) {
        const hyperlink = $this.parents('.hyperlink'),
            title = hyperlink.find('.title'),
            text = title.text();
        // Here are some possible propose function calls
        const keywords = {
            K: ['K. ', 'K.'],
            BWV: ['BWV ', 'BWV.'],
            gold: ['variation ', 'Variation ']
        };
        const proposal = proposeKCode(text, keywords.BWV, 'bwv ');
        // const proposal = proposeKCode(text, keywords.k, 'K ');
        // const proposal = proposeCode(text, 'cs ');
        // const proposal = proposeKCode(text, keywords.gold, 'gold ');
        // if (!proposal) {
        //     return;
        // }
        var code = proposal;
        var interactive = $this.attr('prompt') === 'true';
        if (interactive) {
            code = prompt('Code', proposal);
            if (code === '0') {
                return;
            }
        }
        ajaxPost({
            cmd: 'add_code',
            id: $this.attr('id'),
            code: code
        }, function() {
            $('.add-code').removeClass('saved');
            $this.addClass('saved');
            const hyperlink = $this.parents('.hyperlink'),
                $code = hyperlink.find('.code');
            $code.text('<' + code + '>');
        });
    }

    function removeCode($this) {
        ajaxPost({
            cmd: 'remove_code',
            id: $this.attr('id')
        }, function() {
            $('.add-code').removeClass('saved');
            $this.removeClass('selected');
            $this.addClass('saved');
            // $this.prev().text('<None>');
            const hyperlink = $this.parents('.hyperlink'),
                $code = hyperlink.find('.code');
            $code.text('<None>');
        });
    }

    const albumId = $('#album_id').val();
    if (albumId) {
        // functions for the single album page
        const $selectForCuesheet = $('.select-for-cuesheet'),
            $makeCuesheet = $('.make-cuesheet'),
            $typeahead = $('.album-componist.typeahead');
        var cuesheetIds = [];

        $selectForCuesheet.click(function (e) {
            if (e.shiftKey) {
                selectSiblingsInBetween($selectForCuesheet);
            }
            cuesheetIds = getSelectedCuesheetIds($selectForCuesheet, $makeCuesheet);
        });
        $makeCuesheet.keydown(function (e) {
            if (e.key === 'Enter') {
                postMakeCuesheet($(e.target).val(), cuesheetIds, function(response) {
                    afterPostMake($makeCuesheet, $typeahead)});
            }
        });
        $('.test-lcs').click(function(){
            cuesheetIds = lcs_pieces($selectForCuesheet, $makeCuesheet);
            markTestedCuesheets(cuesheetIds);
        });
        $('.auto-create').click(function(){
            autoCreate($selectForCuesheet, cuesheetIds, $makeCuesheet, $typeahead);
        });
        typeaheadAlbumComponisten($typeahead, $makeCuesheet);
        $('.album-componist-to-make').click(function () {
            copyComponist($typeahead.val(), $makeCuesheet);
        });
        $('.create-cuesheet').click(function(){
            createCuesheet($makeCuesheet, cuesheetIds, $typeahead);
        });
        $('.rename-cuesheet').click(function(){
            postRenameCuesheet(this.id, $('#album_id').val(), function(response) {
                location.reload();
            });
        });
        $('.stukken .check-all').click(function () {
            cuesheetIds = selectCheckboxes($selectForCuesheet, $makeCuesheet, true);
        });
        $('.stukken .check-nothing').click(function () {
            cuesheetIds = selectCheckboxes($selectForCuesheet, $makeCuesheet, false);
        });
        $('.add-code').click(function() {
            addCode($(this));
        });
        $('.remove-code').click(function() {
            removeCode($(this));
        });
    }
});