// also need to handle the form.

function generateCupcakeHTML(cupcake) {
  return `
  <div>
    <img class="cupcake-img" src="${cupcake.image}" alt="cupcake image" width="150px" height="auto">
    <li data-id=${cupcake.id}>
      Flavor: ${cupcake.flavor} <br>
      Rating: ${cupcake.rating} <br>
      Size: ${cupcake.size} <br>
    </li>
  </div>
  `;
}

async function getCupcakeData() {
  const data = (await axios.get("/api/cupcakes")).data;
  return data
}

async function showCupcakes() {
  let data = await getCupcakeData();
  for (let cupcake of data.cupcakes) {
    let html = $(generateCupcakeHTML(cupcake));
    $(".cupcake-list").append(html);
  }
}

$("form").on("submit", async function (evt) {
  evt.preventDefault();
  let flavor = $("#flavor").val();
  let rating = $("#rating").val();
  let size = $("#size").val();
  let image = $("#image").val();

  const resp = await axios.post("/api/cupcakes", {
    flavor,
    rating,
    size,
    image
  });

  let html = $(generateCupcakeHTML(resp.data.cupcake))
  $(".cupcake-list").append(html);
  $("form").trigger("reset");
})

addEventListener("DOMContentLoaded", showCupcakes);

