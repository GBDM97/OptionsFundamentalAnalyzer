const xpath = '/html/body/div[3]/main/div/div/div/div[2]/div/div/div[2]/div/table/tbody';
const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
const tbody = result.singleNodeValue;

if (tbody) {
  // Find all <tr> inside the tbody that have a data-rowkey
  const rows = tbody.querySelectorAll('tr[data-rowkey]');
  
  // Extract the codes
  const codes = Array.from(rows)
    .map(row => row.getAttribute('data-rowkey'))
    .filter(key => key.includes(':') && !key.split(':')[1].includes('/'))
    .map(key => key.split(':')[1].replace('.','-'));

  console.log(codes);
} else {
  console.warn("XPath didn't match any element.");
}
//https://www.tradingview.com/screener/