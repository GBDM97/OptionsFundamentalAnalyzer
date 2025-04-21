let resultValues = [];
    let debtValues = [];
    fetch('https://statusinvest.com.br/acoes/eua/{ticker}')
      .then(response => response.text())
      .then(html => {{
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        const xpaths = [
          '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div/div/strong',
          '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/strong',
          '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[3]/div/div/strong',
          '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[4]/div/div/strong',
          '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[5]/div/div/strong',
          '/html/body/main/div[3]/div/div/div[2]/div/div[2]/div/div[6]/div/div/strong'
        ];

        debtValues = xpaths.map(xpath => {{
          const node = doc.evaluate(xpath, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
          return node ? node.textContent.trim() : null;
        }});

        const companyId = doc.querySelector('div[data-companyid]')?.getAttribute('data-companyid')
        if(companyId){{
          fetch(`https://statusinvest.com.br/stock/getincomestatment?companyid=${{companyId}}&type=1&futureData=false`)
            .then(res => res.json())
            .then(json => {{
                resultValues = json.data.grid[18].gridLineModel.values;
                
          }});
        }}
      }}
    )
    .catch(error => console.error('Fetch error:', error));
    console.log(resultValues)
    return resultValues