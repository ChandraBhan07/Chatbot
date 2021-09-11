$(document).ready(()=>{

	var count = 0

	$('.button').on('click', ()=>{

		

		var text = $('.inpt').val()

		console.log($('.inpt').val())

		msgid = "msg"+count

		var gentext = '<br><div class="message" id="# #" >% %</div>'
			gentext = gentext.replace('% %', text)
			gentext = gentext.replace('# #', msgid)

		if(count == 0){
			document.querySelector('.button').insertAdjacentHTML('afterend', gentext)
		}
		else{
			document.querySelector('.message').insertAdjacentHTML('afterend', gentext)
		}



		req = $.ajax({
			url : '/update',
			type : 'POST',
			data : {text : text}
		});

		req.done(function(data){

			var gentext = '<br><div class="reply">%data.%</div><br>'
			gentext = gentext.replace('%data.%', data.data)

			var classid = '#msg' + count
			document.querySelector(classid).insertAdjacentHTML('afterend', gentext)
			console.log(classid)

			count = count+1

		});

	});

});


