
$('#connectBtn').on('click',function(){
    const email = document.getElementById('username').value;
    const password = document.getElementById('username').value;
    
    $.ajax({
        type:'POST',
        url:'/api/login',
        data:{email:email,password:password},
        success(response){
            if (response['status'] === 'success'){
                window.location = '/';
            }else{
                const msg = (response.msg ? response['msg'] :"Une erreur est survenue.")
                showToast({'message':msg,'type':'error','title':'Erreur'})
                setTimeout(function(){window.location = "/login"}, 500)
            }
        }
    })
});