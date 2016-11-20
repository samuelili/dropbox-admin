/**
 * Created by samuel on 11/19/16.
 */
String.prototype.format = function (values) {
    var string = this;
    for (var key in values)
        if (values.hasOwnProperty(key)) {
            var regex = new RegExp("{" + key + "}", "g");
            string = string.replace(regex, values[key]);
        }

    return string;
};