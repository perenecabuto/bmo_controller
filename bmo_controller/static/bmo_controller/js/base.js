$(function() {
    $('body')
        .on('click', '.post-link', function(e) {
            e.preventDefault();

            var form = $('<form action="' + this.href + '" method="POST" />'),
                csrf = $('[name=csrfmiddlewaretoken]:eq(0)');

            form.append(csrf);
            form.submit();

            return false;
        })
        .on('mousedown', '.ajax-link', function(e) {
            return $(this).attr('last-click', new Date().getTime());
        })
        .on('click', '.ajax-link', function(e) {
            var that = $(this),
                now = new Date().getTime(),
                lastClick = parseInt(that.attr('last-click')) || now,
                interval = Math.abs(now - lastClick);

            e.preventDefault();

            console.log(that.attr('disabled'), lastClick, now, interval);

            if (that.attr('disabled')) {
                return false;
            }

            if (interval <= 300) {
                var enableLink = function(response) {
                    that.animate({opacity: 1}, {
                        complete: function() {
                            that.attr('disabled', false);
                        }
                    });
                };

                that.animate({'opacity': 0.3});
                that.attr('disabled', true);

                $.ajax({ url: this.href, complete: enableLink });
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
    $('.random-bg').each(function(idx, el) {
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
