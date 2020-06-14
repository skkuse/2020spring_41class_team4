// $('#btn_login').on('click', function() {
//     $.ajax({
//         url:'http://127.0.0.1:8000/rest/users/',
//         method:'GET',
//         dataType:'jsonp',
//         contentType:'application/json',
//         success:function(data) {
//             console.log(data);
//             if(data.status == 'OK') {
//                 $('.login-page').hide();
//                 $('.user-page').css('visibility', 'visible');
//                 $('#txt_welcome').text('Welcome ' + data.login_id);
//             } else {
//                 $('#message').text(data.err_msg);
//             }
//         },
//         error:function(err) {
//             console.log(err);
//             $('#message').text(err.responseText);
//         }
//     });
// });