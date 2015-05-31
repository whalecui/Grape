$(function(){
    $('#join').click(function(){
        var input = $('#confirm').val();
        var url = window.location.href;
        var patt = /gp+[0-9]*/g;
        url = url.match(patt)[0];
        patt = /[^0-9]/g;
        var group_id = url.replace(patt, '');
        $.getJSON($SCRIPT_ROOT + '/_join_group',
            {group_id: group_id, confirm:input},
            function(data){
                if(data.status == 'joined'){
                    alert('joined!');
                }else if(data.status == 'fail'){
                    alert('fail!!');
                }else if(data.status == 'non-ex') {
                    alert('non-ex!');
                }
                location.reload();
        });
    });
});

$(function(){
    $('#quit').click(function(){
        var url = window.location.href;
        var patt = /gp+[0-9]*/g;
        url = url.match(patt)[0];
        patt = /[^0-9]/g;
        var group_id = url.replace(patt, '');
        $.getJSON($SCRIPT_ROOT + '/_quit_group',
            {group_id: group_id},
            function(data){
                if(data.status == '0'){
                    alert('fail!!');
                }else if(data.status == '1') {
                    alert('success');
                }
                location.reload();
        });
    });
});