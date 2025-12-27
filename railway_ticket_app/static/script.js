function bookTicket() {
    fetch("/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            train_no: document.getElementById("train").value,
            name: document.getElementById("name").value,
            age: document.getElementById("age").value,
            passengers: document.getElementById("passengers").value,
            berth: document.getElementById("berth").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            result.innerText = data.error;
        } else {
            result.innerHTML = "✅ Ticket Booked<br>PNR: " + data.pnr;
        }
    });
}

function viewTicket() {
    let pnr = document.getElementById("pnr").value;
    fetch("/view/" + pnr)
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            result.innerText = data.error;
        } else {
            result.innerHTML =
                "Train: " + data.train + "<br>" +
                "Name: " + data.name + "<br>" +
                "Passengers: " + data.passengers + "<br>" +
                "Berth: " + data.berth + "<br>" +
                "Fare: ₹" + data.fare;
        }
    });
}

function cancelTicket() {
    let pnr = document.getElementById("pnr").value;
    fetch("/cancel/" + pnr)
    .then(res => res.json())
    .then(data => {
        result.innerText = data.message || data.error;
    });
}
