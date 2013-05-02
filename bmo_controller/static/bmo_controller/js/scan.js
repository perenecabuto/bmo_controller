$.fn.scanEvents = function(eventsUrl) {
    var $eventList = $('#event-list');

    function updateEvents(lastEventDate) {
        var url = lastEventDate ? eventsUrl + "?after=" + lastEventDate : eventsUrl;

        $.ajax({
            url: url,
            dataType: "json",
        }).done(function(events) {
            if (events.length > 0) {
                var newEvents = [];

                lastEventDate = events[0].date;

                for (var i = 0; i < events.length; i++) {
                    var e = events[i];
                    newEvents.push(
                        '<li>At ' + e.date + ': ' + JSON.stringify(e.message)
                        + '<a href="/replay/'+ e.message.type +'/'+ e.message.code +'" class="ajax-link">replay</a> '
                        + '<a href="/command/new?type='+ e.message.type +'&code='+ e.message.code +'">save</a> '
                        + '</li>'
                    );
                }

                $eventList.prepend(newEvents.join(""));
            }

            setTimeout(function() {
                updateEvents(lastEventDate);
            }, 500);
        });
    }

    var date = new Date(),
        formatedDate =
            date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate() + " " +
            date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();

    updateEvents();
};

