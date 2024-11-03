window.addEventListener("load", async () => {
  const orderNumber = new URLSearchParams(window.location.search).get("order");
  try {
    const response = await fetch(`/api/orders/${orderNumber}`);
    const { data: orderData } = await response.json();

    const {
      trip: { attraction: { image, name, address }, date, time },
      price,
      number
    } = orderData;

    const timeText = time === "morning" ? "早上9點到12點" : "下午1點到4點";

    document.getElementById("booking_img").src = image;

    const bookingInfo = document.getElementById("booking_info");
    bookingInfo.innerHTML = `
      <div class="div_name">台北一日遊： ${name}</div>
      <div class="div_text">日期： <span>${date}</span></div>
      <div class="div_text">時間： <span>${timeText}</span></div>
      <div class="div_text">費用： <span>${price}</span></div>
      <div class="div_text">地點： <span>${address}</span></div>
    `;

    document.getElementById("order_number").innerText = `訂單編號 : ${number}`;
    document.getElementById("total_price").innerText = `新台幣 : ${price}元`;
  } catch (error) {
    console.error("Error fetching order data:", error);
  }
});
