let stockChart = null;

async function searchStock() {
    const symbol = document.getElementById("stockSymbol").value;
    const response = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `symbol=${symbol}`
    });
    const data = await response.json();
    
    document.getElementById("stockResults").innerHTML = `
        <div class="stock-card">
            <h3>${data["01. symbol"]}</h3>
            <p>Price: $${data["05. price"]}</p>
            <button onclick="addToWatchlist('${data["01. symbol"]}')">+ Watchlist</button>
        </div>
    `;
    
    // Load historical data
    loadHistoricalData(symbol);
}

async function loadHistoricalData(symbol) {
    const response = await fetch("/historical", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `symbol=${symbol}`
    });
    const data = await response.json();
    
    const dates = Object.keys(data).reverse();
    const prices = dates.map(date => parseFloat(data[date]["4. close"]));
    
    if (stockChart) stockChart.destroy();
    
    const ctx = document.getElementById("stockChart").getContext("2d");
    stockChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [{
                label: `${symbol} Price`,
                data: prices,
                borderColor: "rgba(75, 192, 192, 1)",
                tension: 0.1
            }]
        }
    });
}

async function addToWatchlist(symbol) {
    await fetch("/watchlist/add", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `symbol=${symbol}`
    });
    loadWatchlist();
}

async function loadWatchlist() {
    const response = await fetch("/watchlist");
    const watchlist = await response.json();
    
    let html = "";
    watchlist.forEach(item => {
        html += `<div class="watchlist-item">${item.symbol}</div>`;
    });
    
    document.getElementById("watchlistItems").innerHTML = html;
}

// Initialize
loadWatchlist();
