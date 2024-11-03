const booking_name = document.getElementById("booking_name");
const input_name = document.getElementById("contact_name");
const input_email = document.getElementById("booking_email");
const input_phone = document.getElementById("phone");
const booking_signout = document.getElementById("booking_signout");
const booking_delete = document.getElementById("booking_delete");
const booking_info = document.getElementById("booking_info");
const booking_container = document.querySelector(".booking_container");
const total_price = document.querySelector(".total_price");
const booking_information = document.querySelector(".booking_information");
const no_booking = document.querySelector(".no_booking");
const submitButton = document.querySelector('button[type="submit"]');
const orderForm = document.querySelector(".order");

document.addEventListener("DOMContentLoaded", () => {
  getUserData();
  setupTPDirect();
  booking_signout.addEventListener("click", () => window.location.href = "/");
  booking_delete.addEventListener("click", deleteBookingInfo);
});

// 取得用戶資訊
function getUserData() {
  fetch(`/api/user`)
    .then(response => response.json())
    .then(data => {
      if (!data.data) {
        window.location.href = "/";
      } else {
        const { name, email } = data.data;
        input_name.value = name;
        input_email.value = email;
        booking_name.innerText = name;
        getBookingInfo();
      }
    });
}

// 建立圖片
function getBookingInfo() {
  fetch(`/api/booking`)
    .then(response => response.json())
    .then(data => {
      if (data.data) {
        displayBookingInfo(data.data);
      } else {
        booking_information.innerHTML = "";
        no_booking.style.display = "block";
      }
    });
}

function displayBookingInfo(bookingData) {
  const { attraction, price, date, time } = bookingData;
  const { image, name, address } = attraction;
  const timeText = time === "morning" ? "早上9點到12點" : "下午1點到4點";

  document.getElementById("booking_img").src = image;

  const infoElements = [
    createInfoElement("台北一日遊： ", name, "div_name"),
    createInfoElement("日期： ", date, "div_text"),
    createInfoElement("時間： ", timeText, "div_text"),
    createInfoElement("費用： ", price, "div_text"),
    createInfoElement("地點： ", address, "div_text")
  ];

  booking_info.append(...infoElements);
  total_price.innerText = `新台幣 : ${price}元`;

  orderForm.addEventListener("submit", (e) => checkOrder(e, bookingData, price));
}

function createInfoElement(label, text, className) {
  const div = document.createElement("div");
  div.className = className;
  div.innerText = label;
  const span = document.createElement("span");
  span.innerText = text;
  div.appendChild(span);
  return div;
}

//取得 prime
function checkOrder(e, bookingData, price) {
  e.preventDefault();

// 取得 TapPay Fields 的 status
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();
  if (!tappayStatus.canGetPrime) {
    alert("can not get prime");
    return;
  }

  TPDirect.card.getPrime(result => {
    if (result.status !== 0) {
      alert(`get prime error ${result.msg}`);
      return;
    }

    const orderData = {
      prime: result.card.prime,
      order: {
        price,
        trip: {
          attraction: {
            id: bookingData.attraction.id,
            name: bookingData.attraction.name,
            address: bookingData.attraction.address,
            image: bookingData.attraction.image
          },
          date: bookingData.date,
          time: bookingData.time
        },
        contact: {
          name: input_name.value,
          email: input_email.value,
          phone: input_phone.value
        }
      }
    };

    fetch("/api/orders", {
      method: "POST",
      body: JSON.stringify(orderData),
      headers: { "Content-Type": "application/json" }
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          window.location = `/`;
        } else {
          window.location = `/thankyou?number=${data.data.order_number}`;
        }
      });
  });
}

function deleteBookingInfo() {
  fetch(`/api/booking`, { method: "DELETE" })
    .then(response => response.json())
    .then(data => {
      if (data.ok) {
        booking_information.innerHTML = "";
        no_booking.style.display = "block";
        window.location.reload();
      }
    });
}

// 付款
function setupTPDirect() {
  TPDirect.setupSDK(123971, "app_DVh7uThRN2I5iYCuLKq73U6qGkvGioDxV5GzW54kFZcpcMrqWxymdh7riXr8", "sandbox");

  const fields = {
    number: { element: "#card-number", placeholder: "**** **** **** ****" },
    expirationDate: { element: "#card-expiration-date", placeholder: "MM / YY" },
    ccv: { element: "#card-ccv", placeholder: "CVV" }
  };

  TPDirect.card.setup({
    fields,
    styles: {
      ":focus": { color: "black" },
      ".valid": { color: "green" },
      ".invalid": { color: "red" }
    }
  });

  TPDirect.card.onUpdate(update => {
    submitButton.disabled = !update.canGetPrime;

    updateFieldStatus(update.status.number, ".card-number-group");
    updateFieldStatus(update.status.expiry, ".expiration-date-group");
    updateFieldStatus(update.status.ccv, ".cvc-group");
  });
}

function updateFieldStatus(status, selector) {
  if (status === 2) {
    setFieldStatus(selector, "has-error", "has-success");
  } else if (status === 0) {
    setFieldStatus(selector, "has-success", "has-error");
  } else {
    setFieldStatus(selector, "", "has-error has-success");
  }
}

function setFieldStatus(selector, addClass, removeClass) {
  const element = document.querySelector(selector);
  element.classList.add(addClass);
  element.classList.remove(removeClass);
}
