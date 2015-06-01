$(function(){
    $('#login-form').submit(function(e){
        e.preventDefault();
        var email = $('#emailL').val();
        var pw = $('#passwordL').val();
        var myReg = /^[-_A-Za-z0-9]+@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,3}$/;
        if(!myReg.test(email)){
            alert('email format illegal!');
        }else {
            $.getJSON($SCRIPT_ROOT + '/_login',
                {email: email, pw: pw},
                function (data) {
                    alert(data.status);
                    if (data.status == 'success') {
                        location.reload();
                    }
                });
        }
    });
});
