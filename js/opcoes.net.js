const assetNames = Array.from(document.querySelectorAll("tbody tr"))
  .map(row => row.querySelector("td")?.textContent.trim()+'.SA');

console.log(assetNames);

//https://opcoes.net.br/estudos/liquidez/opcoes