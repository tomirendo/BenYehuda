function remove_nikud (txt){
    var res = ""
    var minNikud = 1416;
    var maxNikud = 1479;
    var alef = 1488;

    for (var i=0; i < txt.length; i++){
        if (txt.charCodeAt(i) < minNikud || txt.charCodeAt(i) >= alef){
            res += txt[i];
        }
    }
    return res;
};