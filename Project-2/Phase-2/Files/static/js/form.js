function descriptiveFunctionName() {

  $('#form2').on('submit', function(event) {
  console.log("form 2 executed") ;
    $.ajax({
      data : {
        content : $('#content').val(),
          topic_2 : $('#topic_2 option:selected').val()
      },
      type : 'POST',
      url : '/publisher'
    })
    .done(function(data) {

      if (data.error) {
        $('#errorAlert').text(data.error).show();
        $('#successAlert').hide();
      }
      else {
        $('#successAlert').text(data.content).show();
        $('#errorAlert').hide();
      }

    });

    event.preventDefault();

  });
}
var id = -1;
function anotherDescriptiveFunctionName() {

  $('#form1').on('submit', function(event) {
  console.log("form1 executed") ;
		$.ajax({
			data : {
				pubsubtype : $('input[name = type]:checked').val(),
                topic : $('#topic option:selected').val(),
                userid: $('#userid').val()
			},
			type : 'POST',
			url : '/selectPubSub'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert1').text(data.error).show();
				$('#successAlert1').hide();
			}
			else {
			    console.log(data.pubsubtype);
				$('#successAlert1').text(data.pubsubtype).show();
				if (data.pubsubtype == 'Publisher') {
                    $('#publisherform').show();
                }
                else {
                    console.log("Subscriber function called");
                    subscriberFunc();
                }
				$('#errorAlert1').hide();
			}

		});

		event.preventDefault();

	});
}

$(document).ready(function() {
    descriptiveFunctionName();
    anotherDescriptiveFunctionName();
});
