$(function(){
    var check = new Array(0,0,0);
    var btn = $('.register').find('button[type="submit"]');
    for (var x in check){
        if(x == 0){
            btn.attr('disabled', 'disabled');
        }
    }
    //check email
    $('#emailR').blur(function(){
        var input = $(this).val();
        var myReg = /^[-_A-Za-z0-9]+@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,3}$/;
        if(!myReg.test(input)){
            btn.attr('disabled', 'disabled');
        }else{
            check[0] = 1;
            $(btn).removeAttr('disabled');
            for (var x in check){
                if(check[x] == 0){
                    btn.attr('disabled', 'disabled');
                }
            }
        }
    });
    //check username
    $('#usernameR').blur(function(){
        var input = $(this).val();
        $.getJSON($SCRIPT_ROOT + '/_check_users',
            {username: input},
            function(data){
                if(data.valid == '0'){
                    btn.attr('disabled', 'disabled');
                }else{
                    check[1] = 1;
                    $(btn).removeAttr('disabled');
                    for (var x in check){
                        if(check[x] == 0){
                            btn.attr('disabled', 'disabled');
                        }
                    }
                }
        });
    });
    //check password
    $('#confirmR').blur(function(){
        var input = $(this).val();
        var pw = $('#passwordR').val();
        if(pw == input && input != ''){
            check[2] = 1;
            $(btn).removeAttr('disabled');
            for (var x in check){
                if(check[x] == 0){
                    btn.attr('disabled', 'disabled');
                }
            }
        }else{
            btn.attr('disabled', 'disabled');
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
        }else{
            btn.attr('disabled', 'disabled');
        }
    });
});