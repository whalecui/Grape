$(function(){
    var check = new Array(0,0,0);
    var btn = $('.register').find('button[type="submit"]');
    var ok = '<i class="fa fa-check"></i>';
    var error = '<i class="fa fa-times"></i>'
    for (var x in check){
        if(x == 0){
            btn.attr('disabled', 'disabled');
        }
    }   //check email
    $('#emailR').blur(function(){
        var input = $(this).val();
        var myReg = /^[-_A-Za-z0-9]+@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,3}$/;
        var tmp = $(this).parent().find('i')[0];
        if(!myReg.test(input)){
            check[0] = 0;
            btn.attr('disabled', 'disabled');
            if(tmp){ $(tmp).remove(); }
            $(this).before(error);
        }else{
            $.getJSON($SCRIPT_ROOT + '/_check_email',
                {email: input},
                function (data) {
                    if (data.valid == '0') {
                        check[0] = 0;
                        btn.attr('disabled', 'disabled');
                        if(tmp){ $(tmp).remove(); }
                        $('#emailR').before(error);
                    } else {
                        check[0] = 1;
                        $(btn).removeAttr('disabled');
                        for (var x in check) {
                            if (check[x] == 0){
                                btn.attr('disabled', 'disabled');
                            }
                        }
                        if(tmp){ $(tmp).remove(); }
                        $('#emailR').before(ok);
                    }
                });
        }
    });
    //check username
    $('#usernameR').blur(function(){
        var input = $(this).val();
        var tmp = $('#usernameR').parent().find('i')[0];
        if(input == ''){
            check[1] = 0;
            btn.attr('disabled', 'disabled');
            if(tmp){ $(tmp).remove(); }
            $('#usernameR').before(error);
        }else {
            $.getJSON($SCRIPT_ROOT + '/_check_users',
                {username: input},
                function (data) {
                    if (data.valid == '0') {
                        check[1] = 0;
                        btn.attr('disabled', 'disabled');
                        if(tmp){ $(tmp).remove(); }
                        $('#usernameR').before(error);
                    } else {
                        check[1] = 1;
                        $(btn).removeAttr('disabled');
                        for (var x in check) {
                            if (check[x] == 0){
                                btn.attr('disabled', 'disabled');
                            }
                        }
                        if(tmp){ $(tmp).remove(); }
                        $('#usernameR').before(ok);
                    }
                });
        }
    });
    //check password
    $('#confirmR').blur(function(){
        var input = $(this).val();
        var pw = $('#passwordR').val();
        var tmp = $(this).parent().find('i')[0];
        if(pw == input && input != ''){
            check[2] = 1;
            $(btn).removeAttr('disabled');
            for (var x in check){
                if(check[x] == 0){
                    btn.attr('disabled', 'disabled');
                }
            }
            if(tmp){ $(tmp).remove(); }
            $(this).before(ok);
        }else{
            check[2] = 0;
            btn.attr('disabled', 'disabled');
            if(tmp){ $(tmp).remove(); }
            $(this).before(error);
        }
    });

    $('#passwordR').blur(function(){
        var input = $('#confirmR').val();
        var pw = $('#passwordR').val();

        if(pw == input && pw != ''){
            check[2] = 1;
            $(btn).removeAttr('disabled');
            for (var x in check){
                if(check[x] == 0){
                    btn.attr('disabled', 'disabled');
                }
            }
            var tmp = $('#confirmR').parent().find('i')[0]
            if(tmp){ $(tmp).remove(); }
            $('#confirmR').before(ok);
        }else if(pw == ''){
            check[2] = 0;
            btn.attr('disabled', 'disabled');
            var tmp = $(this).parent().find('i')[0];
            if(tmp){ $(tmp).remove(); }
            $(this).before(error);
            var tmp = $('#confirmR').parent().find('i')[0]
            if(tmp){ $(tmp).remove(); }
            $('#confirmR').before(error);
        }else{
            check[2] = 0;
            btn.attr('disabled', 'disabled');
            var tmp = $(this).parent().find('i')[0];
            if(tmp){ $(tmp).remove(); }
            $(this).before(ok);
            var tmp = $('#confirmR').parent().find('i')[0]
            if(tmp){ $(tmp).remove(); }
            $('#confirmR').before(error);
        }
    });
});