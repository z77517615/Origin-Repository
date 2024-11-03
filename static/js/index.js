const footer = document.querySelector("footer");
const container = document.querySelector("#container");
const search = document.querySelector(".sec2 form");
const main = document.querySelector("main");
let keyword = "";
let page = 0;

const options = {
  root: null,
  rootMargin: "0px",
  threshold: 0.9,
};

const observer = new IntersectionObserver(handleIntersect, options);
observer.observe(footer);

function handleIntersect(entries) {
  if (entries[0].isIntersecting) {
    if (page === null || page === undefined) {
      observer.unobserve(footer);
    } else if (page !== null && keyword === "") {
      fetchAttractions(`/api/attractions?page=${page}`);
    } else if (page === 0 && keyword !== "") {
      fetchAttractions(`/api/attractions?page=${page}&keyword=${keyword}`);
    } else {
      observer.unobserve(footer);
    }
  }
}

function fetchAttractions(url) {
  fetch(url)
    .then(response => response.json())
    .then(result => {
      const data = result.data;
      page = result.next_page;
      if (page !== null) {
        createAttractions(data);
      } else {
        observer.unobserve(footer);
      }
    });
}

search.addEventListener("submit", function (e) {
  e.preventDefault();
  observer.unobserve(footer);
  observer.observe(footer);
  keyword = this.querySelector("input").value;
  if (keyword !== "") {
    page = 0;
    main.innerHTML = "";
    handleIntersect([{ isIntersecting: true }]);
  } else {
    observer.unobserve(footer);
    main.innerHTML = "";
  }
});

function createAttractions(data) {
  data.forEach(attraction => {
    const { images, category, mrt, name, id } = attraction;

    const a = document.createElement("a");
    const newDiv = document.createElement("div");
    const div1 = document.createElement("div");
    const img = document.createElement("img");
    const title = document.createElement("p");
    const div2 = document.createElement("div");
    const mrtTitle = document.createElement("p");
    const categoryName = document.createElement("p");

    container.appendChild(a);
    a.appendChild(newDiv);
    newDiv.appendChild(div1);
    newDiv.appendChild(div2);
    div1.appendChild(img);
    div1.appendChild(categoryName);
    div2.appendChild(mrtTitle);
    div2.appendChild(title);

    img.id = "image";
    title.id = "title";
    mrtTitle.id = "mrttitle";
    categoryName.id = "categoryname";
    newDiv.id = "newdiv";
    div2.id = "div2";

    title.textContent = category;
    mrtTitle.textContent = mrt;
    categoryName.textContent = name;
    img.src = images[0];
    a.href = `/attraction/${id}`;
  });
}
