footer = document.querySelector("footer");
container = document.querySelector("#container");
search = document.querySelector(".sec2 form");
main = document.querySelector("main");
let keyword = "";
let page = 0;

let options = {
  root: null,
  rootMargins: "0px",
  threshold: 0.9,
};

const observer = new IntersectionObserver(handleIntersect, options);
observer.observe(footer);

function handleIntersect(enteries) {
  if (enteries[0].isIntersecting) {
    if (page == "null" || undefined) {
      observer.unobserve(footer);
    } else if (page !== "null" && keyword == "") {
      URL = "/api/attractions?page=" + page;
      fetch(URL)
        .then(function (response) {
          return response.json();
        })
        .then(function (result) {
          data = result.data;
          page = result["next_page"];
          if (page !== "null") {
            createattractions();
          } else {
            observer.unobserve(footer);
          }
        });
    } else if (page == 0 && keyword !== "") {
      URL = `/api/attractions?page=${page}&keyword=${keyword}`;
      fetch(URL)
        .then(function (response) {
          return response.json();
        })
        .then(function (result) {
          data = result.data;
          page = result["next_page"];
          if (page !== null) {
            createattractions();
          }
        });
    } else {
      observer.unobserve(footer);
    }
  }
}

search.addEventListener("submit", Searching);
function Searching(e) {
  e.preventDefault();
  observer.unobserve(footer);
  observer.observe(footer);
  keyword = this.querySelector("input").value;
  if (keyword !== "") {
    page = 0;
    main.innerHTML = "";
    handleIntersect();
  } else {
    observer.unobserve(footer);
    main.innerHTML = "";
  }
}

function createattractions() {
  for (let i = 0; i < data.length; i++) {
    let image = data[i].images[0];
    let aTag = data[i].category;
    let mrt = data[i].mrt;
    let name = data[i].name;
    let pageid = data[i].id;

    let a = document.createElement("a");
    let newDiv = document.createElement("div");
    let div1 = document.createElement("div");
    let images = document.createElement("img");
    let title = document.createElement("p");
    let div2 = document.createElement("div");
    let mrttitle = document.createElement("p");
    let categoryname = document.createElement("p");

    document.getElementById("container").appendChild(a);
    a.appendChild(newDiv);
    newDiv.appendChild(div1);
    newDiv.appendChild(div2);
    div1.appendChild(images);
    div1.appendChild(categoryname);
    div2.appendChild(mrttitle);
    div2.appendChild(title);

    images.setAttribute("id", "image");
    title.setAttribute("id", "title");
    mrttitle.setAttribute("id", "mrttitle");
    categoryname.setAttribute("id", "categoryname");
    newDiv.setAttribute("id", "newdiv");
    div2.setAttribute("id", "div2");

    title.textContent = aTag;
    mrttitle.textContent = mrt;
    categoryname.textContent = name;
    images.src = image;
    a.href = `/attraction/${pageid}`;
  }
}
