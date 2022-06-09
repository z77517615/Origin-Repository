const fee = document.querySelector("#fee");
const morning = document.querySelector('input[value="morning"]');
const afternoon = document.querySelector('input[value="afternoon"]');

morning.addEventListener("click", () => {
  fee.innerText = 2000;
});
afternoon.addEventListener("click", () => {
  fee.innerText = 2500;
});

window.addEventListener("load", () => {
  let array = location.href.split("/");
  let id = array[4];
  URL = `/api/attraction/${id}`;
  fetch(URL)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let name = data["data"]["name"];
      let attr_loc =
        data["data"]["category"] + " at " + data["data"]["mrt"] + "站";
      let description = data["data"]["description"];
      let address = data["data"]["address"];
      let transport = data["data"]["transport"];
      let imgURLs = data["data"]["images"];

      document.getElementById("name").innerHTML = name;
      document.getElementById("location").innerHTML = attr_loc;
      document.getElementById("description").innerHTML = description;
      document.getElementById("address").innerHTML = address;
      document.getElementById("transport").innerHTML = transport;

      for (i = 0; i <= imgURLs.length - 1; i++) {
        let j = i + 1;
        let image = document.createElement("img");
        let div = document.createElement("div");
        let dot = document.createElement("span");
        image.src = imgURLs[i];
        div.appendChild(image);
        dot__nav.append(dot);
        images.append(div);
        div.setAttribute("class", "mySlides");
        image.setAttribute("class", "img");
        dot.setAttribute("class", "dot");
        dot.setAttribute("onclick", `btm_slide(${j})`);
      }
      showSlides(slideIndex);
    });
});
let slides = document.getElementsByClassName("mySlides");
let slideIndex = 1;
function showSlides(n) {
  var i;
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace("active", "");
  }

  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

function side_slide(n) {
  showSlides((slideIndex += n));
}

function btm_slide(n) {
  showSlides((slideIndex = n));
}
