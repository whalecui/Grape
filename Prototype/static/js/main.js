$(function(){
    $('.email').blur(function(){
        var input = $(this).val();
        var myReg = /^[-_A-Za-z0-9]+@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,3}$/;
        if(!myReg.test(input)){
            var btn = $(this).parent().parent().find('button[type="submit"]');
            btn.attr('disabled', 'disabled');
        }else{
            $(btn).removeAttr('disabled');
        }
    });
    $('.username-login').blur(function(){
        var input = $(this).val();
        $.getJSON($SCRIPT_ROOT + '/_check_users',
            {username: input},
            function(data){
                var btn = $(this).parent().parent().find('button[type="submit"]');
                if(valid == '0'){
                    btn.attr('disabled', 'disabled');
                }else{
                    btn.removeAttr('disabled');
                }
        });
    });
});