const booking_name=document.getElementById("booking_name")
const input_name=document.getElementById("contact_name")
const input_email=document.getElementById("booking_email")
const booking_signout = document.getElementById("booking_signout")
const booking_delete= document.getElementById("booking_delete")
const booking_info=document.getElementById('booking_info')
const booking_container=document.querySelector('.booking_container')
const total_price=document.querySelector('.total_price')
const booking_information=document.querySelector('.booking_information')
const no_booking=document.querySelector('.no_booking')


//取得用戶資訊
function get_userdata(){
    fetch(`/api/user`,{
        method: "GET",
    }).then(response => response.json())
    .then(data => {
        if(data.data == null){
            window.location.href='/';
        }else{
            input_name.value= data.data['name']
            input_email.value= data.data['email']
            booking_name.innerText = data.data['name']
            getbookinginfo()
        }
    })
}
get_userdata()

//建立圖片
function getbookinginfo(){
    fetch(`/api/booking`,{
        method: "GET",
    }).then(response => response.json())
    .then(data => {
        if (data.data !== null){
            let imgURL = data['data']['attraction']['image']
            let attr_name = data['data']['attraction']['name']
            let address = data['data']['attraction']['address']
            let cost = data['data']['price']
            let date = data['data']['date']
            let time =data['data']['time']
            if (time == "morning"){
                text="早上9點到12點"
            }else{
                text="下午1點到4點"
            };

            booking_img=document.getElementById('booking_img')
            booking_img.src=imgURL

            div_name=document.createElement("div");
            div_date=document.createElement("div");
            div_fee=document.createElement("div");
            div_address=document.createElement("div");
            div_time=document.createElement("div");

            div_name.innerText="台北一日遊： " + attr_name;
            div_date.innerText="日期： ";
            div_fee.innerText="費用： " ;
            div_address.innerText="地點： ";
            div_time.innerText="時間： " ;


            booking_info.append(div_name,div_date,div_time,div_fee,div_address);

            div_name.setAttribute("class","div_name")
            div_date.setAttribute("class","div_text")
            div_fee.setAttribute("class","div_text")
            div_address.setAttribute("class","div_text")
            div_time.setAttribute("class","div_text")

            date_span=document.createElement("span");
            date_span.innerText=date;
            div_date.append(date_span);

            time_span=document.createElement("span");
            time_span.innerText=text;
            div_time.append(time_span);

            fee_span=document.createElement("span");
            fee_span.innerText= cost;
            div_fee.append(fee_span);

            address_span=document.createElement("span");
            address_span.innerText=address;
            div_address.append(address_span);

            total_price.innerText= "新台幣 : "+ cost +"元";

        }else{
            booking_information.innerHTML = '';
            no_booking.style.display="block";
        }
    })
}

booking_signout.addEventListener("click", ()=>{
    window.location.href="/";
});

//刪除鍵
booking_delete.addEventListener("click", ()=>{
    info_delete()
})
function info_delete(){
    fetch(`/api/booking`,{
        method: "DELETE",
    }).then(response => response.json())
    .then(data => {
        if(data["ok"]){
            booking_information.innerHTML = '';
            no_booking.style.display="block";
            window.location.reload();
        }

    })
}


