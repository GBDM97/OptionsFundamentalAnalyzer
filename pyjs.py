def fetch_us_fundamentals(driver, ticker):
    js_code = f"""
    const callback = arguments[arguments.length - 1]; // Needed for execute_async_script

    (async () => {{
        const output = {{
            results: [],
            debts: []
        }};

        try {{
            const htmlResponse = await fetch("https://statusinvest.com.br/acoes/eua/{ticker}");
            const html = await htmlResponse.text();
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

            output.debts = xpaths.map(xpath => {{
                const node = doc.evaluate(xpath, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                return node ? parseFloat(node.textContent.trim().replaceAll('.','').replaceAll(',','.')) : null;
            }});

            const companyId = doc.querySelector('div[data-companyid]')?.getAttribute('data-companyid');

            if (companyId) {{
                const jsonRes0 = await fetch(`https://statusinvest.com.br/stock/getincomestatment?companyid=${{companyId}}&type=0&futureData=false`);
                const jsonRes1 = await fetch(`https://statusinvest.com.br/stock/getincomestatment?companyid=${{companyId}}&type=1&futureData=false`);
                const json0 = await jsonRes0.json();
                const json1 = await jsonRes1.json();

                output.debts.unshift(
                    parseFloat(json0.data.grid[10].gridLineModel.values[0])
                );

                output.results = json1.data.grid[18].gridLineModel.values;
            }}

            callback(output); // THIS sends data back to Python

        }} catch (err) {{
            callback({{ error: err.message || 'Unknown error' }}); // Ensure error is returned too
        }}
    }})();
    """
    return driver.execute_async_script(js_code)

def fetch_br_fundamentals(driver, ticker):
    ticker = ticker[:-3]
    js_code = f"""
    const callback = arguments[arguments.length - 1]; // Needed for execute_async_script

    (async () => {{
        const output = {{
            results: [],
            debts: []
        }};

        try {{
            const htmlResponse = await fetch("https://statusinvest.com.br/acoes/{ticker}");
            const html = await htmlResponse.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            const xpaths = [
                '/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[1]/div/div/strong',
                '/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[2]/div/div/strong',
                '/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[3]/div/div/strong',
                '/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[4]/div/div/strong',
                '/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[5]/div/div/strong',
                '/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[6]/div/div/strong',
            ];

            output.debts = xpaths.map(xpath => {{
                const node = doc.evaluate(xpath, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                return node ? parseFloat(node.textContent.trim().replaceAll('.','').replaceAll(',','.')) : null;
            }});

            const jsonRes0 = await fetch(`https://statusinvest.com.br/acao/getdre?code={ticker}&type=0&futureData=false`);
            const jsonRes1 = await fetch(`https://statusinvest.com.br/acao/getdre?code={ticker}&type=1&futureData=false`);
            const json0 = await jsonRes0.json();
            const json1 = await jsonRes1.json();

            output.debts.unshift(
                parseFloat(json0.data.grid[5].gridLineModel.values[0])
            );

            output.results = json1.data.grid[11].gridLineModel.values;

            callback(output); // THIS sends data back to Python

        }} catch (err) {{
            callback({{ error: err.message || 'Unknown error' }}); // Ensure error is returned too
        }}
    }})();
    """
    return driver.execute_async_script(js_code)