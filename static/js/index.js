footer=document.querySelector('footer')
container=document.querySelector('#container')
// URL="http://52.194.56.157:3000/api/attraction?page=0"
URL="/api/attractions?page=0"

document.addEventListener("DOMContentLoaded",() => {
    let options = {
        root:null,
        rootMargins:"0px",
        threshold:0.5
    };

    const observer = new IntersectionObserver(handleIntersect,options);
    observer.observe(footer)
    getData()
    // observer.unobserve(footer)
});

function handleIntersect(enteries){
    if (enteries[0].isIntersecting){
        // getData()
    }
}

function getData(){
    fetch (URL).then(function(response){
        return response.json();
    }).then(function(result){
        result=result.data
        for(let i=0;i<result.length;i++){
            let image=result[i].images[0]
            let aTag=result[i].category
            let mrt=result[i].mrt
            let name=result[i].name
            
            let newDiv=document.createElement("div");
            let div1=document.createElement("div");
            let images=document.createElement("img");
            let title=document.createElement("p");
            let div2=document.createElement("div");
            let mrttitle=document.createElement("p")
            let categoryname=document.createElement("p")

            document.getElementById("container").appendChild(newDiv);
            newDiv.appendChild(div1);
            newDiv.appendChild(div2);
            div1.appendChild(images);
            div1.appendChild(title);
            div2.appendChild(mrttitle);
            div2.appendChild(categoryname);

            images.setAttribute("id","image")
            title.setAttribute("id","title")
            mrttitle.setAttribute("id","mrttitle")
            categoryname.setAttribute("id","categoryname")
            newDiv.setAttribute("id","newdiv")
            div2.setAttribute("id","div2")

            title.textContent=aTag;
            mrttitle.textContent=mrt;
            categoryname.textContent=name;
            images.src=image;


    };
    });
}