var isCheckedId = false;

$('#login_id').change(function() {
    if(isCheckedId) {
        isCheckedId = false;
    }
    console.log($('#login_id').val());
});
$('#btn_check_id').on('click', function() {
    if($('#login_id').val().length < 5){
        alert('5자 이상');
    } else {
        $.ajax({
            url:'/login/checkid?login_id='+$('#login_id').val(),
            method:'GET',
            success:function(data) {
                if(data == 'OK'){
                    isCheckedId = true;
                    $('#message').text('id 사용 가능');
                } else if(data == 'DUPLICATED') {
                    isCheckedId = false;
                    $('#message').text('id 사용 불가');
                } else{
                    isCheckedId = false;
                    $('#message').text('error 발생, 재시도..');
                }
            },
            error:function(err) {
                isCheckedId = false;
                $('#message').text('id 사용 불가능');
            }
        });
    }
});

$('#btn_signup').on('click', function() {
    if(!isCheckedId){
        alert('ID 체크해~');
        return;
    }
    if($('#user_name').val().length < 3) {
        alert('이름이 짧아~');
        return;
    }
    if($('#login_pwd').val() != $('#confirm_pwd').val() ) {
        alert('비밀번호 달라~');
        return;
    }
    $.ajax({
        url:'/login/create',
        method:'POST',
        dataType:'json',
        contentType:'application/json',
        data:JSON.stringify({
            'user_name':$('#user_name').val(),
            'login_id':$('#login_id').val(),
            'login_pwd':$('#login_pwd').val(),
            'email':$('#email').val()
        }),
        success:function(data) {
            window.location.replace('/board/list');
        },
        error:function(err) {
            $('#message').text('error 발생, 재시도..');
        }
    });
});