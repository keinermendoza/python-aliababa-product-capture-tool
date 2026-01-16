(() => {
  const data = {
    company_name: "",
    company_url: "",
    product_name: "",
    product_url: "",
    minimum_quantity: "",
    price_offered: ""
  };

  // Product
  const h1 = document.querySelector("h1");
  if (h1) {
    data.product_name = h1.title || h1.innerText.trim();
  }
  data.product_url = location.href;

  // Company
  const companyAnchor = document.querySelector(
    ".product-company .product-company-info .company-name a"
  );

  if (companyAnchor) {
    data.company_name = companyAnchor.innerText.trim();
    data.company_url = companyAnchor.href;
  }

  // Price
  const modulePrice = document.querySelector(".module_price .price-item");

  if (modulePrice) {
    if (modulePrice.firstChild?.innerText) {
      data.minimum_quantity = modulePrice.firstChild.innerText.trim();
    }

    if (modulePrice.children[1]) {
      data.price_offered = modulePrice.children[1].innerText.trim().replace("$", "");
    }
  }

  console.log("SCRAPED DATA:", data);

  const serverUrl = "http://127.0.0.1:5000/webhook"
  fetch(serverUrl, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.ok) {
      console.log("recibido")
    } else {
      console.log("Respuesta de red OK pero respuesta HTTP no OK");
    }
  })
  .catch(function (error) {
    console.log("Hubo un problema con la petición Fetch:" + error.message);
  });

})();
