/**
 * Created by orion on 08/10/2017.
 */
'use strict';

$(function () {

    function prop(v) {
        // special: convert names to numbers
        var cello_suites = false;
        if (cello_suites) {
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
        const romans = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];
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
        for (var j = 1; j < w.length; j++) {
            var p = prop(w[j]);
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
        const keywords = {
            K: ['K. ', 'K.'],
            BWV: ['BWV ', 'BWV.'],
            gold: ['variation ', 'Variation ']
        };
        // Here are some possible propose function calls
        // you can select one by NOT commenting it out
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
        $('.add-code').click(function() {
            addCode($(this));
        });
        $('.remove-code').click(function() {
            removeCode($(this));
        });
    }
});