// need to generate html for the cupcakes.
// also need to handle the form.

addEventListener("DOMContentLoaded", evt => {
  const cupcakeList = document.querySelector(".cupcake-list");
  cupcakes = getCupcakesList();
  console.log()
})

async function getCupcakesList() {
  const cupcakes = await axios.get("/api/cupcakes")
  console.log(cupcakes)
  return cupcakes
}