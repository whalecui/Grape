$(function(){
	$("#validcheck").click(function(){
		var ops = new Array();
		var or_name = "vote1-option";
		var is_checked = false;
		var mid=false;
		var order = 1;
		$("input.options").each(function(key,value)
		{
			ops[key] = $(this).attr("name");
			if (ops[key]!=or_name)
			{
				if (!is_checked)
				{
					alert("the No."+order+" content hasn't been voted");
					mid = true;
					return false;
				}
				++order;
				is_checked = false;
				or_name = ops[key];
			}

			if ($(this).prop("checked"))
			{
				is_checked = true;
			}

		});
		if (!is_checked&&!mid)
			alert("the last content hasn't been voted");
		return is_checked;

	});
}
	);