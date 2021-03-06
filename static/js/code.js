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

    function proposeKCode(text, keywords) {
        // console.log(text);
        var proposal = '';
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
        } else {
            // speciaal geval, e.g. 'BWV1004'
            for (var k = 1; k < w.length; k++) {
                var word = w[k];
                if (word.substr(0, 3).toLowerCase() == 'bwv') {
                    var n = word.substr(3);
                    while (n.substr(0,1) == '0') {
                        n = n.substr(1);
                    }
                    return proposal + n;
                }
            }
            if (nrs.length) {
                proposal += '_' + nrs[0];
            }
        }

        return proposal;
    }

    function addCodeAll($this) {
        $('.add-code.first').each(function(){
            addCode($(this), true);
        });
        $('.saved').removeClass('saved');
        $this.addClass('saved');
    }

    const KEYWORDS = {
        K: {
            prefix: 'K ',
            codes: ['K. ', 'K.', 'K ', 'K']
        },
        BWV: {
            prefix: 'bwv ',
            codes: ['BWV ', 'BWV.', 'Bwv ', 'BWV']
        },
        gold: {
            prefix: 'gold ',
            codes: ['variation ', 'Variation ']
        },
        KV: {
            prefix: 'KV ',
            codes: ['K. ', 'K.', 'K ', 'KV ', 'KV', 'K']
        }
    };

    function postCode(id, code, $this, $code, nomark) {
        ajaxPost({
            cmd: 'add_code',
            id: id,
            code: code
        }, function() {
            if (!nomark) {
                $('.saved').removeClass('saved');
                $this.addClass('saved');
            }
            $code.text('<' + code + '>');
        });
    }

    function addCode($this, nomark) {
        console.log($this);
        const
            id = $this.attr('id'),
            doPrompt = $this.attr('prompt'),
            hyperlink = $this.parents('.hyperlink'),
            $code = hyperlink.find('.code'),
            $title = hyperlink.find('.title'),
            text = $title.text(),
            c = KEYWORDS.K, // choose your keywords here
            proposal = proposeKCode(text, c.codes);

        // const proposal = proposeCode(text, 'cs ');
        var code = c.prefix + proposal;
        console.log(doPrompt);
        if (doPrompt && doPrompt === 'true') {
            code = prompt('Code', code);
            if (code === null) {  // escape
                return;
            }
        } else {
            if (!proposal.length) {  // empty code
                return;
            }
        }
        postCode(id, code, $this, $code, nomark);
    }

    function removeCodeAll($this) {
        $('.add-code.first').each(function(){
            removeCode($(this));
        });
        $('.saved').removeClass('saved');
        $this.addClass('saved');
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
        $('.add-code-all').click(function() {
            addCodeAll($(this));
        });
        $('.remove-code-all').click(function() {
            removeCodeAll($(this));
        });
    }
});