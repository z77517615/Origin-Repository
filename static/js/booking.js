const booking_name=document.getElementById("booking_name")
const input_name=document.getElementById("contact_name")
const input_email=document.getElementById("booking_email")
const input_phone=document.getElementById("phone")
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
            const bookingdata=data['data'] 
            let imgURL = bookingdata['attraction']['image']
            let attr_name = bookingdata['attraction']['name']
            let address = bookingdata['attraction']['address']
            let cost = bookingdata['price']
            let date = bookingdata['date']
            let time =bookingdata['time']
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
 
            orderForm.addEventListener('submit', Checkorder)
            //取得prime
            function Checkorder(e) {
                e.preventDefault()

                // 取得 TapPay Fields 的 status
                const tappayStatus = TPDirect.card.getTappayFieldsStatus()
                console.log(tappayStatus)

                if (tappayStatus.canGetPrime === false) {
                    alert('can not get prime')
                    return
                }
            //Get Prime
                TPDirect.card.getPrime(function (result) {
                    if (result.status !== 0) {
                        alert('get prime error ' + result.msg)
                        return
                    }
                    console.log('get prime 成功，prime: ' + result.card.prime)
            //prime傳遞後端
                    let orderdata={
                        "prime": result.card.prime,
                        "order": {
                            "price": cost,
                            "trip": {
                                "attraction": {
                                "id": bookingdata['attraction']['id'],
                                "name": attr_name,
                                "address": address,
                                "image": imgURL,
                                },
                                "date": date,
                                "time": time,
                            },
                        "contact": {
                            "name": input_name.value,
                            "email": input_email.value,
                            "phone": input_phone.value
                            }
                        }
                    }
                    fetch('/api/orders', {
                        method: "POST",
                        body: JSON.stringify(orderdata),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    }).then(response => response.json())
                    .then((data) => {
                        console.log(data);
                        if (data['error']){
                            window.location = `/`;
                        }
                        else{
                            order_number=data.data['order_number']
                            window.location = `/thankyou?number=${order_number}`;
                        }
                    }) 
                })
            }
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


//付款
TPDirect.setupSDK(123971, 'app_DVh7uThRN2I5iYCuLKq73U6qGkvGioDxV5GzW54kFZcpcMrqWxymdh7riXr8', 'sandbox')
    // Display ccv field
const submitButton=document.querySelector('button[type="submit"]')   
const orderForm=document.querySelector('.order') 

let fields= {
        number: {
            element: '#card-number',
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            element: '#card-expiration-date',
            placeholder: 'MM / YY'
        },
        ccv: {
            element: '#card-ccv',
            placeholder: 'CVV'
        }
    }
TPDirect.card.setup({
    fields: fields,
    styles: {
        ':focus': {
         'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
    }
})
TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        submitButton.removeAttribute('disabled')
    } else {
        // Disable submit Button to get prime.
        submitButton.setAttribute('disabled', true)
    }

    if (update.status.number === 2) {
        setNumberFormGroupToError('.card-number-group')
    } else if (update.status.number === 0) {
        setNumberFormGroupToSuccess('.card-number-group')
    } else {
        setNumberFormGroupToNormal('.card-number-group')
    }

    if (update.status.expiry === 2) {
        setNumberFormGroupToError('.expiration-date-group')
    } else if (update.status.expiry === 0) {
        setNumberFormGroupToSuccess('.expiration-date-group')
    } else {
        setNumberFormGroupToNormal('.expiration-date-group')
    }

    if (update.status.ccv === 2) {
        setNumberFormGroupToError('.cvc-group')
    } else if (update.status.ccv === 0) {
        setNumberFormGroupToSuccess('.cvc-group')
    } else {
        setNumberFormGroupToNormal('.cvc-group')
    }

})
function setNumberFormGroupToError(selector) {
    $(selector).addClass('has-error')
    $(selector).removeClass('has-success')
}

function setNumberFormGroupToSuccess(selector) {
    $(selector).removeClass('has-error')
    $(selector).addClass('has-success')
}

function setNumberFormGroupToNormal(selector) {
    $(selector).removeClass('has-error')
    $(selector).removeClass('has-success')
}


