const sign = document.getElementById("sign")
const signout = document.getElementById("signout")
const background_color= document.querySelector(".background_color")
const signin_member= document.querySelector(".signin_member")
const signup_member= document.querySelector(".signup_member")
const signinForm = document.querySelector("#signin")
const signupForm = document.querySelector("#signup")
const message = document.querySelector('.message')



//切換選單出現
function showsign_in(){
    background_color.style.display="block";
    signin_member.style.display="block";
}

function closesign_in(){
    background_color.style.display="none";
    signin_member.style.display="none";
}

function closesign_up(){
    background_color.style.display="none";
    signup_member.style.display="none";
}

function towardsign_up(){
    signup_member.style.display="block";
    background_color.style.display="block";
    signin_member.style.display="none";
}

function towardsign_in(){
    signup_member.style.display="none";
    background_color.style.display="block";
    signin_member.style.display="block";
}

function closesign(){
    signup_member.style.display="none";
    background_color.style.display="none";
    signin_member.style.display="none";
}

function signout_toggle(){
    sign.style.display="none";
    signout.style.display="block";
}

function signin_toggle(){
    sign.style.display="block";
    signout.style.display="none";
}




//登入
signinForm.addEventListener('submit', signin)
function signin(e){
    e.preventDefault()
    let data = {
        "email" : this.querySelector('input[name="email"]').value,
        "password" : this.querySelector('input[name="password"]').value 
    }
    fetch(`/api/user`, {
        method: 'PATCH',
        body: JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json'
            }
    }).then(response => response.json())
    .then(data => {
    if(data["ok"] == true){
        signout_toggle();
        closesign();
        window.location.reload();
    }else{
        message.innerText = data["message"]
        }   
    })
}

//註冊
signupForm.addEventListener('submit', signup)
function signup(e){
    e.preventDefault()
    let data = {
        "name": this.querySelector('input[name="name"]').value,
        "email" : this.querySelector('input[name="email"]').value,
        "password" : this.querySelector('input[name="password"]').value 
    }
    fetch(`/api/user`, {
        method: 'POST',
        body: JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json'
            }
        }).then(response => response.json())
        .then(data => {
        let message = this.querySelector('.message')
        if(data["ok"] == true){
            message.innerText = "註冊成功"
        }else{
            message.innerText = data["message"]
            }   
        })
    }
        
//取得資訊
function get_userdata(){
    fetch(`/api/user`,{
        method: "GET",
    }).then(response => response.json())
    .then(data => {
        if(data.data == null){
            signin_toggle() 
        }else{
            signout_toggle()
        }
    })
}
get_userdata()

//登出
function sign_out(){
    fetch(`/api/user`,{
        method: 'DELETE',
    }).then(response => response.json())
    .then(data => {
        if(data){
        signin_toggle();
        window.location.reload();                    
        }
    })
}