$(function() {
    $('body').on('click', '.post-link', function(e) {
        e.preventDefault();
        $('<form action="' + this.href + '" method="POST" />').submit();
    })
    .on('mousedown', '.ajax-link', function(e) {
        $(this).attr('last-click', new Date().getMilliseconds());
    })
    .on('click', '.ajax-link', function(e) {
        var lastClick = $(this).attr('last-click'),
            interval = Math.abs(new Date().getMilliseconds() - lastClick);

        e.preventDefault();
        $(this).attr('last-click', null);

        if (interval <= 100) {
            $.ajax({ url: this.href });
        }

        return false;
    });

    $('[data-rand-cmd-colors]').on('click', function() {
        randCommandBtnColors();
        return false;
    });

    // Add bootstrap error class to the django form css error class
    $('.errorlist').addClass('text-error');

    selectMenuItem();
    randCommandBtnColors();
});

function randCommandBtnColors() {
    $('.command-btn').each(function(idx, el) {
        var randColor = function() { return Math.floor(Math.random(idx) * 256) },
            hue = 'rgb(' + [randColor(), randColor(), randColor()].join(',') + ')';

        $(el).css('background-color', hue);
    });
}

function selectMenuItem() {
    var links = $('.nav li a').sort(function (a, b) { return b.href.length - a.href.length });

    for (var i = 0; i < links.length; i++) {
        var link = $(links[i]),
            item = link.parent('li'),
            re = new RegExp('^.+://' + window.location.host),
            currentUrl = window.location.href.replace(re, '').replace(/[\/#]$/, '').replace(/\?.*?$/, '');

        if (currentUrl.match(link.attr('href'))) {
            item.addClass('active');
            break;
        }
    }
}
