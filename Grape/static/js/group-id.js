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
                    // location.reload();
                    location.href='/';
                }
        });
    });
});

$(function(){
    $('.createDiscussion').submit(function(e){
        e.preventDefault();
        var title = $('#discuss-title').val();
        var content = $('#discuss-content').val();
        // alert(title);
        if(!title){
            alert('Title cannot be empty!');
        }else if(!content) {
            alert('Topic cannot be empty!');
        }else{
            var url = window.location.href;
            var patt = /gp+[0-9]*/g;
            url = url.match(patt)[0];
            patt = /[^0-9]/g;
            var group_id = url.replace(patt, '');
            $.getJSON($SCRIPT_ROOT + '/_create_discussion/' + group_id,
                {title: title, content: content},
                function (data) {
                    if (data.status == '1') {
                        location.hash = 'discussions';
                        location.reload();
                    }else{
                        alert(data.status);
                    }
                });
        }
    });
});

$(function(){
    $('.createBulletin').submit(function(e){
        e.preventDefault();
        var title = $('#bulletin-title').val();
        var text = $('#bulletin-text').val();
        if(!title){
            alert('Title cannot be empty!');
        }else if(!text) {
            alert('Topic cannot be empty!');
        }else{
            var url = window.location.href;
            var patt = /gp+[0-9]*/g;
            url = url.match(patt)[0];
            patt = /[^0-9]/g;
            var group_id = url.replace(patt, '');
            $.getJSON($SCRIPT_ROOT + '/_create_bulletin/' + group_id,
                {title: title, text: text},
                function (data) {
                    if (data.status == '1') {
                        location.hash = 'bulletin';
                        location.reload();
                    }else{
                        alert(data.status);
                    }
                });
        }
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.discuss-delete').click(function(){
            var discuss_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(discuss_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_discussion',
                {discuss_id: discuss_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.bulletin-delete').click(function(){
            var id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(bulletin_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_bulletin',
                {bulletin_id: bulletin_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});

$(function () {
    $(".countdown_timepicker").datetimepicker({
        //showOn: "button",
        //buttonImage: "./css/images/icon_calendar.gif",
        //buttonImageOnly: true,
        showButtonPanel: false,
        timeOnly: true,
        showSecond: true,
        timeFormat: 'hh:mm:ss',
        stepHour: 1,
        stepMinute: 1,
        stepSecond: 1
    });

    $(".ui_timepicker").datetimepicker({
        //showOn: "button",
        //buttonImage: "./css/images/icon_calendar.gif",
        //buttonImageOnly: true,
        //showButtonPanel: false,
        //timeOnly: true,
        showSecond: true,
        timeFormat: 'hh:mm:ss',
        stepHour: 1,
        stepMinute: 1,
        stepSecond: 1
    });
});


function optionReady_instant(){
    var options = 0;
    $('.addOption').click(function(){
        ++options;
        var vote_options_num = document.getElementById('vote-options-num');
        vote_options_num.setAttribute('value',options.toString());

        //var vote_option = document.createElement('input');
        //vote_option.setAttribute('type','radio');
        //vote_option.setAttribute('class','vote-option');
        //vote_option.setAttribute('name','vote-option[]');

        var vote_option_content = document.createElement('input');
        //vote_option_content.setAttribute('type','text');
        vote_option_content.setAttribute('class','vote-option-content form-control');
        vote_option_content.setAttribute('name','vote-option-content-'+options.toString());
        vote_option_content.readOnly = true;
        vote_option_content.setAttribute('value','double click to change value');

        // remove button
        option_remove_button = document.createElement('i');
        option_remove_button.setAttribute('class', 'fa fa-lg fa-minus-square-o');
        option_remove_button.setAttribute('id', 'remove-option-'+options.toString());

        vote_option_content.ondblclick = function()
        {
            this.value = ''
            this.readOnly = false;
            this.className = "vote-option-content-edit";
        }
        vote_option_content.onblur = function()
        {
            if (this.value == '')
            {
                this.value = "double click to change value";
            }

            this.readOnly = true;
            this.className = "vote-option-content";
        }

        option_remove_button.onclick = function()
        {
            options--;
            vote_options_num.setAttribute('value',options.toString());
            var tempArray = vote_option_content.name.split('-');
            var currentNum = parseInt(tempArray[tempArray.length - 1]);
            var next = vote_wrap.nextSibling;
            while( next.value != "Add new choices" )
            {
                next.firstChild.innerHTML = String.fromCharCode(64+currentNum);
                next.firstChild.nextSibling.name = 'vote-option-content-'+currentNum.toString();
                next.lastChild.setAttribute('id', 'remove-option-'+currentNum.toString());
                next = next.nextSibling;
                currentNum++;
            }
            vote_wrap.parentNode.removeChild(vote_wrap);
        }
        //var vote_change_row = document.createElement('br');
        var vote_order = String.fromCharCode(64+options); //limit to 26 options

        var vote_wrap = document.createElement('div');
        vote_wrap.innerHTML = "<span>"+vote_order+"</span>";
        //vote_wrap.appendChild(vote_option);
        vote_wrap.appendChild(vote_option_content);
        vote_wrap.appendChild(option_remove_button);


        var vote_add_form = document.getElementById("vote-add-form");
        var vote_add_button = document.getElementById("vote-add-button");

        vote_add_form.insertBefore(vote_wrap,vote_add_button);
    });
}

// if I have time, I want to realize the drag part;
function optionReady(){
    var options = 0;
    $('.addOption').click(function(){
        this.disable = true;
        ++options;
        var vote_add_target = this.parentNode;
        var target_id = $(vote_add_target).attr("id");
        var vote_order = target_id.replace(/[^0-9]/ig,""); 
        var vote_options_num = document.getElementById('vote-options-num-'+vote_order); // specify it
        vote_options_num.setAttribute('value',options.toString());
        var vote_option_content = document.createElement('input');
        vote_option_content.setAttribute('class','vote-option-content form-control');
        vote_option_content.setAttribute('name',target_id+'-option-content-'+options.toString());
        vote_option_content.readOnly = true;
        vote_option_content.setAttribute('value','double click to change value');
        
        // remove button
        option_remove_button = document.createElement('i');
        option_remove_button.setAttribute('class', 'fa fa-lg fa-minus-square-o');
        option_remove_button.setAttribute('id', target_id+'-remove-option-'+options.toString());        

        vote_option_content.ondblclick = function()
        {
            this.value = '';
            this.readOnly = false;
            this.className = "vote-option-content-edit";
        };
        vote_option_content.onblur = function()
        {
            if (this.value == '')
            {
                this.value = "double click to change value";
            }
            this.readOnly = true;
            this.className = "vote-option-content";
            
        };
        option_remove_button.onclick = function()
        {
            options--;
            vote_options_num.setAttribute('value',options.toString());
            var tempArray = vote_option_content.name.split('-');
            var currentNum = parseInt(tempArray[tempArray.length - 1]);
            var next = vote_wrap.nextSibling;
            while( next.value != "Add new choices" )
            {
                next.firstChild.innerHTML = String.fromCharCode(64+currentNum);

                next.firstChild.nextSibling.name = target_id+'-option-content-'+currentNum.toString();
                next.lastChild.setAttribute('id', target_id+'-remove-option-'+currentNum.toString());
                next = next.nextSibling;
                currentNum++;
            }
            vote_wrap.parentNode.removeChild(vote_wrap);
        }
        //var vote_change_row = document.createElement('br');
        var vote_wrap = document.createElement('div');
        var option_order = String.fromCharCode(64+options); //limit to 26 options
        var vote_add_button = vote_add_target.getElementsByClassName("addOption")[0];

        vote_wrap.innerHTML = "<span>"+option_order+"</span>";
        //vote_wrap.appendChild(vote_option);
        vote_wrap.appendChild(vote_option_content);
        vote_wrap.appendChild(option_remove_button);


        vote_add_target.insertBefore(vote_wrap, vote_add_button);
        this.disable = false;
    });
};

function voteReady()
{
    var votes = 1;
    $('.addVote').click(function()
    {
        ++votes;
        var votes_num = $("#votes-num");
        $(votes_num).val(votes.toString());
        var vote_li = document.createElement('li');
        $(vote_li).attr('class','list-group-item');
        $(vote_li).attr('id','vote'+votes.toString());

        $(vote_li).html(
            "<label for=\"vote-content-"+votes+"\">Title of the item</label>" +
            "<input class=\"form-control\" type=\"text\" name=\"vote-content-"+votes+
            "\" id=\"vote-content-"+votes+"\"/>" +
            "<input class=\"form-control\" type=\"text\" name=\"vote-options-num-"+votes+
            "\" id=\"vote-options-num-"+votes+"\" style=\"display:none;\" value=\"0\"/><br>" +
            "<input type=\"button\" class=\"addOption btn btn-default\"" +
            "value=\"Add new choices\"/>"
        );

        var votes_content_set = document.getElementById("votes_content_set");
        votes_content_set.appendChild(vote_li);
        optionReady();
    }
    );
}

$(function(){
    $('.changeTimeSet').click(function(){
        var time = document.getElementById("timeinterval");
        var datetime = document.getElementById("datetime");
        var endtime_selection = document.getElementById("endtime-selection");

        if (endtime_selection.value == "2")
        {
            datetime.style['display'] = "none";
            time.style['display'] = "block";
            endtime_selection.value = "1";
        }
        else
        {
            time.style['display'] = "none";
            datetime.style['display'] = "block";
            endtime_selection.value = "2";
        }
    });
});

$(function(){
    $('#instant_vote').click(function(){
        // $('#vote-add-form').html("");
        $('#vote-add-form').html(
            "<label for=\"vote-content\">Title of the Vote</label>" +
            "<input class=\"form-control\" type=\"text\" name=\"vote-content\"" +
            "id=\"vote-content\"/>" +
            "<input class=\"form-control\" type=\"text\" name=\"vote-options-num\"" +
            "id=\"vote-options-num\" style=\"display:none;\" value=\"0\"/><br>" +
            "<input type=\"button\" class=\"addOption btn btn-default\" id=\"vote-add-button\"" +
            "value=\"Add new choices\"/><br><br>" +
            "<input class=\"form-control\" type=\"text\" id=\"endtime-selection\"" +
            "name=\"endtime-selection\" value = \"0\" style=\"display:none\"/>" +
            "<label for=\"endtime\">Set the time</label>" +
            "<input type=\"text\" id=\"endtime\" name=\"endtime\"" +
            "class=\"countdown_timepicker form-control\" value=\"00:00:00\" /><br>" +
            "<button type=\"submit\" class=\"btn btn-default\">let's vote!</button>"
        );
        $(".countdown_timepicker").datetimepicker({
        //showOn: "button",
        //buttonImage: "./css/images/icon_calendar.gif",
        //buttonImageOnly: true,
        showButtonPanel: false,
        timeOnly: true,
        showSecond: true,
        timeFormat: 'hh:mm:ss',
        stepHour: 1,
        stepMinute: 1,
        stepSecond: 1
        });

        optionReady_instant();
    }
    )
}
);

$(function(){
    $('#longlasting_vote').click(function(){
        // $("vote-add-form").html("");
        $("#vote-add-form").html(
            "<label for=\"title\">Title of the Vote</label>" +
            "<input class=\"form-control\" type=\"text\" name=\"title\"/>" +
                "<ul id=\"votes_content_set\">" +
                    "<li class=\"list-group-item\" id=\"vote1\">" +
                    "<label for=\"vote-content-1\">Title of the item</label>" +
                    "<input class=\"form-control\" type=\"text\" name=\"vote-content-1\"" +
                    "id=\"vote-content-1\"/>" +
                    "<input class=\"form-control\" type=\"text\" name=\"vote-options-num-1\"" +
                    "id=\"vote-options-num-1\" style=\"display:none;\" value=\"0\"/><br>" +
                    "<input type=\"button\" class=\"addOption btn btn-default\"" +
                    "value=\"Add new choices\"/>" +
                    "</li>" +
                "</ul>" +
            "<input class=\"form-control\" type=\"text\" name=\"votes-num\"" +
            "id=\"votes-num\" style=\"display:none;\" value=\"1\"/>" +
            "<input type=\"button\" class=\"addVote btn btn-default\"" +
            "value=\"Add new vote content\"/><br><br>" +
            "<input class=\"form-control\" type=\"text\" id=\"endtime-selection\"" +
            "name=\"endtime-selection\" value = \"1\" style=\"display:none\"/>" +
            "<label for=\"endtime\">Set the datetime</label>" +
            "<input type=\"text\" id=\"endtime\" name=\"endtime\"" +
            "class=\"ui_timepicker form-control\" value=\"\"/><br>" +
            "<button type=\"submit\" class=\"btn btn-default\">let's vote!</button>"
        )
        $(".ui_timepicker").datetimepicker({
        //showOn: "button",
        //buttonImage: "./css/images/icon_calendar.gif",
        //buttonImageOnly: true,
        //showButtonPanel: false,
        //timeOnly: true,
        dateFormat: 'yy-mm-dd',
        showSecond: true,
        timeFormat: 'hh:mm:ss',
        stepHour: 1,
        stepMinute: 1,
        stepSecond: 1
        });

        voteReady();
        optionReady();
    }
    )
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.vote-delete').click(function(){
            var vote_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(vote_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_vote',
                {vote_id: vote_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});