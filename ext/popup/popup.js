document.addEventListener('DOMContentLoaded',
  async function () {
        let response = await fetch("https://hackathon.midnight.wtf/auth/verify", {
            method: "GET",
            credentials: "include",
            mode: "cors",
        });
        if (response.ok) {
            console.log("User is logged in");
            document.getElementById("loginForm").style.display = "none";
            document.getElementById("mainContent").style.display = "block";

        } else {
            console.log("User is not logged in");
            document.getElementById("loginForm").style.display = "block";
            document.getElementById("mainContent").style.display = "none";
        }
        document.getElementById("loginButton").addEventListener("click", login);
        document.getElementById("searchButton").addEventListener("click", fetchData);

    }, false
);

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const url = `https://hackathon.midnight.wtf/auth/login`;
    const obj = {
        username: username,
        password: password
    }
    let resp = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(obj),
        credentials: 'include',
        mode: "cors",
    })
    const data = await resp.json();
    console.log(data);
    if (resp.ok) {
        // alert("Login successful!");
        document.getElementById("loginForm").style.display = "none";  // Hide login form
        document.getElementById("mainContent").style.display = "block"; // Show main content
    } else {
        // alert("Incorrect username or password.");
    }
}

// Function to fetch data from URL and display it
async function fetchData() {
    const query = document.getElementById("searchBar").value;
    // const url = `http://10.125.190.27:8000/search/${query}`;
    const url = `https://hackathon.midnight.wtf/search/${query}`;
    const response = await fetch(url, {
        method: "GET",  // Using GET method
        credentials: "include",  // Important: Include credentials (cookies)
        headers: {
            "Content-Type": "application/json"  // Add content type if necessary
        }
    });
    const data = await response.text();
    // Display data in #displayArea
    document.getElementById("displayArea").innerHTML = `
        <h3>Search Results</h3>
        <p>${data}</p>
    `;
}