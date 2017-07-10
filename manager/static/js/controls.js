$(document).ready(function(){


			// Timezone loader

			Date.prototype.toDateInputValue = (function(){
			var local = new Date(this);
			local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
			return local.toJSON().slice(0,10);
			})

			// Default today time

			$('.date').val(new Date().toDateInputValue());




			// Matching Acc-names and Acc-nbrs
			$('.account_number').val($('.account_name').val());
			$('.acc_balance').val($('.account_name').val());

			$('.account_name').on('change', function(){
				$('.account_number').val(this.value);
				$('.acc_balance').val(this.value);
			})



			// Check,Cash controller

			$('#cheque_number').hide();

			$('.type').on('change', function(){
				if(this.value === 'Cheque')
				{
					$('#cheque_number').show();

				}
				else
				{
					$('#cheque_number').hide();
				}
			})


			// Kubuza gusohora amafaranga arengeje arimo
			
			$('.withdrew_amount').on('input', function(){
				var x = $('.sum').val()-200;
				if(this.value > x)
				{
					alert("Not enough funds on this account!");
					location.reload();
				}
			})

		})
