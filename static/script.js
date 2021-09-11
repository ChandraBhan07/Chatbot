$(document).ready(()=>{

	document.addEventListener('keypress', (event)=>{

		if(document.querySelector('.input').value!==''){

			if(event.keyCode === 13 || event.which === 13){

				var text, message, reply;

				text = $('.input').val()
				console.log(text)

				message = '<div class="conversation"><div class="message">% %</div></div>'
				message = message.replace('% %', text)
			
				document.querySelector('.input_submit_container').insertAdjacentHTML('beforebegin', message)		

				document.querySelector('.input').value=''

				req = $.ajax({
					url : '/update',
					type : 'POST',
					data : {text : text}
				});

				req.done(function(data){

					reply = '<div class="conversation"><div class="reply_grp"><div class="reply">% %</div><div class="reply_pic"></div></div></div>'
					reply = reply.replace('% %', data.data)
					document.querySelector('.input_submit_container').insertAdjacentHTML('beforebegin', reply)

				});
			}
		}
	});

	$('.button').on('click', ()=>{

		if(document.querySelector('.input').value!==''){
			var text, message, reply;

			text = $('.input').val()
			console.log(text)

			message = '<div class="conversation"><div class="message">% %</div></div>'
			message = message.replace('% %', text)
		
			document.querySelector('.input_submit_container').insertAdjacentHTML('beforebegin', message)		

			document.querySelector('.input').value=''

			req = $.ajax({
				url : '/update',
				type : 'POST',
				data : {text : text}
			});

			req.done(function(data){

				reply = '<div class="conversation"><div class="reply_grp"><div class="reply">% %</div><div class="reply_pic"></div></div></div>'
				reply = reply.replace('% %', data.data)
				document.querySelector('.input_submit_container').insertAdjacentHTML('beforebegin', reply)

			});
		}
	});

});
