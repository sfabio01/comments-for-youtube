export var DateDiff = {
    inSeconds: function (d1, d2) {
        var t2 = d2.getTime();
        var t1 = d1.getTime();

        return parseInt((t2 - t1) / (1000));
    },

    inMinutes: function (d1, d2) {
        var t2 = d2.getTime();
        var t1 = d1.getTime();

        return parseInt((t2 - t1) / (60 * 1000));
    },

    inHours: function (d1, d2) {
        var t2 = d2.getTime();
        var t1 = d1.getTime();

        return parseInt((t2 - t1) / (3600 * 1000));
    },

    inDays: function (d1, d2) {
        var t2 = d2.getTime();
        var t1 = d1.getTime();

        return parseInt((t2 - t1) / (24 * 3600 * 1000));
    },

    inWeeks: function (d1, d2) {
        var t2 = d2.getTime();
        var t1 = d1.getTime();

        return parseInt((t2 - t1) / (24 * 3600 * 1000 * 7));
    },

    inMonths: function (d1, d2) {
        var d1Y = d1.getFullYear();
        var d2Y = d2.getFullYear();
        var d1M = d1.getMonth();
        var d2M = d2.getMonth();

        return (d2M + 12 * d2Y) - (d1M + 12 * d1Y);
    },

    inYears: function (d1, d2) {
        return d2.getFullYear() - d1.getFullYear();
    },

    getString: function (d1, d2) {
        var secs = this.inSeconds(d1, d2);
        if (secs < 60) // < 60 seconds
            return "Just now";
        if (secs < 3600) // < 60 minutes
            return this.inMinutes(d1, d2) + " minutes ago";
        if (secs < 3600 * 24) // < 24 hours
            return this.inHours(d1, d2) + " hours ago";
        if (secs < 3600 * 24 * 7) // < 7 days
            return this.inDays(d1, d2) + " days ago";

        return this.inWeeks(d1, d2) + " weeks ago"; // > 7 days
    }

}