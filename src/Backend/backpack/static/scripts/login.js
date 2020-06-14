

var hidden    	= false
, form      	= $('.login-form')
, passInput 	= $('.password')
, toggleType 	= $('.toggle-type')



$('.toggle-password').on('click', function () {

if (hidden) {
hidden = false
$(this).text('Mask password')
form.toggleClass('confirming')
toggleType.attr('type', 'text')
}

else {
hidden = true
$(this).text('Show password')
form.toggleClass('confirming')
toggleType.attr('type', 'password')
}

})