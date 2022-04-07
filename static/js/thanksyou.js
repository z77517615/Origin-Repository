

window.addEventListener("load", ()=>{
    console.log("1111111111")
    let order=window.location.search.split("=")
    order_number= order[1]
    fetch(`/api/orders/${order_number}`)
    .then((response)=>{
        return response.json();
    }).then((data)=>{
        console.log(data)
        const orderdata=data['data'] 
        let imgURL = orderdata['trip']['attraction']['image']
        let attr_name = orderdata['trip']['attraction']['name']
        let address = orderdata['trip']['attraction']['address']
        let cost = orderdata['price']
        let date = orderdata['trip']['date']
        let time =orderdata['trip']['time']
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
    })    
})
