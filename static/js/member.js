const sign = document.getElementById("sign");
const signout = document.getElementById("signout");
const backgroundColor = document.querySelector(".background_color");
const signinMember = document.querySelector(".signin_member");
const signupMember = document.querySelector(".signup_member");
const signinForm = document.querySelector("#signin");
const signupForm = document.querySelector("#signup");
const message = document.querySelector(".message");
const schedule = document.getElementById("schedule");
const bookingForm = document.querySelector(".booking_form");

const toggleDisplay = (element, displayStyle) => {
  element.style.display = displayStyle;
};

const showSignIn = () => {
  toggleDisplay(backgroundColor, "block");
  toggleDisplay(signinMember, "block");
};

const closeSignIn = () => {
  toggleDisplay(backgroundColor, "none");
  toggleDisplay(signinMember, "none");
};

const closeSignUp = () => {
  toggleDisplay(backgroundColor, "none");
  toggleDisplay(signupMember, "none");
};

const switchToSignUp = () => {
  toggleDisplay(signupMember, "block");
  toggleDisplay(backgroundColor, "block");
  toggleDisplay(signinMember, "none");
};

const switchToSignIn = () => {
  toggleDisplay(signupMember, "none");
  toggleDisplay(backgroundColor, "block");
  toggleDisplay(signinMember, "block");
};

const closeSign = () => {
  toggleDisplay(signupMember, "none");
  toggleDisplay(backgroundColor, "none");
  toggleDisplay(signinMember, "none");
};

const signoutToggle = () => {
  toggleDisplay(sign, "none");
  toggleDisplay(signout, "block");
};

const signinToggle = () => {
  toggleDisplay(sign, "block");
  toggleDisplay(signout, "none");
};

const handleResponse = (response) => response.json();

const handleSignin = (e) => {
  e.preventDefault();
  const data = {
    email: e.target.querySelector('input[name="email"]').value,
    password: e.target.querySelector('input[name="password"]').value,
  };

  fetch(`/api/user`, {
    method: "PATCH",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(handleResponse)
    .then((data) => {
      if (data.ok) {
        signoutToggle();
        closeSign();
        window.location.reload();
      } else {
        message.innerText = data.message;
      }
    });
};

const handleSignup = (e) => {
  e.preventDefault();
  const data = {
    name: e.target.querySelector('input[name="name"]').value,
    email: e.target.querySelector('input[name="email"]').value,
    password: e.target.querySelector('input[name="password"]').value,
  };

  fetch(`/api/user`, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(handleResponse)
    .then((data) => {
      const messageElement = e.target.querySelector(".message");
      messageElement.innerText = data.ok ? "註冊成功" : data.message;
    });
};

const getUserData = () => {
  fetch(`/api/user`, { method: "GET" })
    .then(handleResponse)
    .then((data) => {
      data.data ? signoutToggle() : signinToggle();
    });
};

const signOut = () => {
  fetch(`/api/user`, { method: "DELETE" })
    .then(handleResponse)
    .then(() => {
      signinToggle();
      window.location.reload();
    });
};

const handleScheduleClick = () => {
  fetch("/api/user", { method: "GET" })
    .then(handleResponse)
    .then((data) => {
      data.data ? (window.location.href = "/booking") : switchToSignIn();
    });
};

const handleBooking = (e) => {
  e.preventDefault();
  fetch(`/api/user`, { method: "GET" })
    .then(handleResponse)
    .then((data) => {
      if (data.data) {
        const bookingInfo = {
          AttractionID: location.pathname.split("/")[2],
          date: e.target.querySelector('input[name="date"]').value,
          time: e.target.querySelector('input[name="time"]').value,
          fee: e.target.querySelector("#fee").innerText,
        };

        fetch(`/api/booking`, {
          method: "POST",
          body: JSON.stringify(bookingInfo),
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then(handleResponse)
          .then(() => {
            window.location.href = "/booking";
          });
      } else {
        switchToSignIn();
      }
    });
};

signinForm.addEventListener("submit", handleSignin);
signupForm.addEventListener("submit", handleSignup);
schedule.addEventListener("click", handleScheduleClick);
bookingForm.addEventListener("submit", handleBooking);

getUserData();
