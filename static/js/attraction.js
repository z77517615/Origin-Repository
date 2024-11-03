document.addEventListener("DOMContentLoaded", () => {
  const fee = document.querySelector("#fee");
  const morning = document.querySelector('input[value="morning"]');
  const afternoon = document.querySelector('input[value="afternoon"]');
  const slideIndex = 1;

  morning.addEventListener("click", () => {
    fee.innerText = 2000;
  });

  afternoon.addEventListener("click", () => {
    fee.innerText = 2500;
  });

  const fetchAttractionData = async (id) => {
    try {
      const response = await fetch(`/api/attraction/${id}`);
      const data = await response.json();
      return data.data;
    } catch (error) {
      console.error("Error fetching attraction data:", error);
    }
  };

  const updateAttractionDetails = (data) => {
    document.getElementById("name").innerText = data.name;
    document.getElementById("location").innerText = `${data.category} at ${data.mrt}站`;
    document.getElementById("description").innerText = data.description;
    document.getElementById("address").innerText = data.address;
    document.getElementById("transport").innerText = data.transport;
  };

  const createImageElements = (imgURLs) => {
    const imagesContainer = document.getElementById("images");
    const dotNav = document.getElementById("dot__nav");

    imgURLs.forEach((url, index) => {
      const image = document.createElement("img");
      const div = document.createElement("div");
      const dot = document.createElement("span");

      image.src = url;
      div.appendChild(image);
      dotNav.appendChild(dot);
      imagesContainer.appendChild(div);

      div.classList.add("mySlides");
      image.classList.add("img");
      dot.classList.add("dot");
      dot.setAttribute("onclick", `btm_slide(${index + 1})`);
    });
  };

  const initializeSlides = () => {
    const slides = document.getElementsByClassName("mySlides");
    const dots = document.getElementsByClassName("dot");

    const showSlides = (n) => {
      let slideIndex = n;
      if (n > slides.length) slideIndex = 1;
      if (n < 1) slideIndex = slides.length;

      Array.from(slides).forEach((slide) => (slide.style.display = "none"));
      Array.from(dots).forEach((dot) => dot.classList.remove("active"));

      slides[slideIndex - 1].style.display = "block";
      dots[slideIndex - 1].classList.add("active");
    };

    const sideSlide = (n) => showSlides((slideIndex += n));
    const btmSlide = (n) => showSlides((slideIndex = n));

    window.side_slide = sideSlide;
    window.btm_slide = btmSlide;

    showSlides(slideIndex);
  };

  const init = async () => {
    const urlSegments = location.href.split("/");
    const id = urlSegments[4];
    const data = await fetchAttractionData(id);

    if (data) {
      updateAttractionDetails(data);
      createImageElements(data.images);
      initializeSlides();
    }
  };

  init();
});
