$.fn.scanEvents = function(eventsUrl, newCommandUrl, replayEventUrl) {
    new EventsScanner(this, eventsUrl, newCommandUrl, replayEventUrl).updateEvents();
};

var EventsScanner = function(eventListEl, eventsUrl, newCommandUrl, replayEventUrl) {
    this.eventListEl = $(eventListEl);
    this.newCommandUrl = newCommandUrl || this.newCommandUrl;
    this.eventsUrl = eventsUrl || this.eventsUrl;
    this.replayEventUrl = replayEventUrl || this.replayEventUrl;
}

EventsScanner.prototype = {
    eventListEl: null,
    newCommandUrl: '/command/new',
    replayEventUrl: '/replay/TYPE/CODE/BITS/PROTOCOL',
    updateTimeout: 1000,

    buildReplayUrl: function(bmo_message) {
        var m = bmo_message;

        return this.replayEventUrl.replace('TYPE', m.type).replace('CODE', m.code)
            .replace('BITS', m.bits).replace('PROTOCOL', m.protocol);
    },

    updateEvents: function(lastEventDate) {
        var url = lastEventDate ? this.eventsUrl + "?after=" + lastEventDate : this.eventsUrl,
            that = this;

        $.ajax({
            url: url,
            dataType: "json",
        }).done(function(events) {
            if (events.length > 0) {
                var newEvents = [];

                lastEventDate = events[0].date;

                for (var i = 0; i < events.length; i++) {
                    var e = events[i],
                        m = e.message;

                    newEvents.push(
                        '<tr>'
                        + '<td>' + e.date + '</td>'
                        + '<td>' + m.type + '</td>'
                        + '<td>' + m.code + '</td>'
                        + '<td>' + m.bits + '</td>'
                        + '<td>'+ m.protocol + '</td>'
                        + '<td>'
                        + '<a href="' + that.buildReplayUrl(m) + '" class="ajax-link">replay</a> '
                        + '<a href="' + that.newCommandUrl + '?type='+ m.type + '&code='+ m.code + '&bits='+ m.bits + '&protocol='+ m.protocol
                        + '">save</a>'
                        + '</td>'
                        + '</tr>'
                    );
                }

                that.eventListEl.prepend(newEvents.join(""));
            }

            setTimeout(function() {
                that.updateEvents(lastEventDate);
            }, that.updateTimeout);
        });
    }
}
