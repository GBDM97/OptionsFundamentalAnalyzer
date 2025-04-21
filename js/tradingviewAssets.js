const xpath = '/html/body/div[3]/main/div/div[2]/div/div[4]/div[2]/div[2]/div/div/table/tbody';
const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
const tbody = result.singleNodeValue;

if (tbody) {
  // Find all <tr> inside the tbody that have a data-rowkey
  const rows = tbody.querySelectorAll('tr[data-rowkey]');
  
  // Extract the codes
  const codes = Array.from(rows)
    .map(row => row.getAttribute('data-rowkey'))
    .filter(key => key.includes(':'))
    .map(key => key.split(':')[1]);

  console.log(codes);
} else {
  console.warn("XPath didn't match any element.");
}