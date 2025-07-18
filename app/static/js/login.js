
$('#connectBtn').on('click',function(){
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    $.ajax({
        type:'POST',
        url:'/api/login',
        data:{email:email,password:password},
        success(response){
            if (response['status'] === 'success'){
                showToast({'message':'Vous vous êtes identifié !','title':'Succès','type':'success'});
                setTimeout(function(){window.location = '/';},1000);
            }else{
                const msg = (response.msg ? response['msg'] :"Une erreur est survenue.")
                showToast({'message':msg,'type':'error','title':'Erreur'})
                setTimeout(function(){window.location = "/login"}, 500)
            }
        }
    })
});