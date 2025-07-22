
$('#registerBtn').on('click',function(){
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const password_verify = document.getElementById('passwordVerify').value;

    if (password !== password_verify){
        showToast({'message':'Les mots de passe ne sont pas identique.','title':'Erreur','type':'error'});
        return;
    };

    $.ajax({
        type:'POST',
        url:'/api/register',
        data:{email:email,password:password},
        success(response){
            if (response['status'] === 'success'){
                showToast({'message':'Vous avez créer un compte !','title':'Succès','type':'success'});
                setTimeout(function(){window.location = '/';},1000);
            }else{
                const msg = response.msg? response.msg :"Une erreur est survenu";
                showToast({'message':msg,'title':'Erreur','type':'error'});
                setTimeout(function(){window.location = '/signin';},1000);
            }
        },
        error(xhr) {
            if (xhr.status === 429) {
                showToast({ message: 'Trop de tentatives, réessayez plus tard.', title: 'Limite atteinte', type: 'warning' });
            } else {
                showToast({ message: 'Erreur serveur. Réessayez.', title: 'Erreur', type: 'error' });
            }
        }
    })
});