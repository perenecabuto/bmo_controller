$(function() {
    $('.post-link').on('click', function(e) {
        e.preventDefault();
        $('<form action="' + this.href + '" method="POST" />').submit();
    });

    $('.ajax-link').on('mousedown', function(e) {
        $(this).attr('last-click', new Date().getMilliseconds());
    });

    $('.ajax-link').live('click', function(e) {
        var lastClick = $(this).attr('last-click'),
            interval = Math.abs(new Date().getMilliseconds() - lastClick);

        e.preventDefault();
        $(this).attr('last-click', null);

        if (interval <= 100) {
            $.ajax({ url: this.href });
        }

        return false;
    });

    $('.nav li').each(function(idx, menuItem) {
        var item = $(menuItem),
        link = item.find('a:eq(0)'),
        re = new RegExp('^.+://' + window.location.host);

        if (link.attr('href') == window.location.href.replace(re, '')) {
            item.addClass('active');
        }
    });

    $('[data-rand-cmd-colors]').on('click', function() {
        randCommandBtnColors();
        return false;
    });

    randCommandBtnColors();
});

function randCommandBtnColors() {
    $('.command-btn').each(function(idx, el) {
        var randColor = function() { return Math.floor(Math.random(idx) * 256) },
            hue = 'rgb(' + [randColor(), randColor(), randColor()].join(',') + ')';

        $(el).css('background-color', hue);
    });
}
