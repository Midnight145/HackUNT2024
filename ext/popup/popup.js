const API_URL = "https://hackathon.midnight.wtf/"

// noinspection JSDeprecatedSymbols,JSUnresolvedReference
browser.runtime.onMessage.addListener(async (message) => {
    // Received from context menu activation
    // We basically "emulate" the search button click, or display the login form
    if (message.search_str) {
        if (await check_logged_in()) {
            await fetchData(message.search_str);
        } else {
            await login();
        }
    }
});


document.addEventListener('DOMContentLoaded',
  async function () {
        if (await check_logged_in()) {
            // defaults to the login screen, we want to skip it if we're already logged in
            toggle_display();
        }
        document.getElementById("loginButton").addEventListener("click", login);
        document.getElementById("searchButton").addEventListener("click", fetchData);

    }, false
);

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const url = API_URL + `auth/login`;
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
        credentials: 'include'
    })
    if (resp.ok) {
        toggle_display();
    } else {
        // alert("Incorrect username or password.");
    }
}

function toggle_display() {
    const loginForm = document.getElementById("loginForm");
    const mainContent = document.getElementById("mainContent");

    const isLoginHidden = loginForm.style.display === "none";
    loginForm.style.display = isLoginHidden ? "block" : "none";
    mainContent.style.display = isLoginHidden ? "none" : "block";
}


async function check_logged_in() {
    let response = await fetch("https://hackathon.midnight.wtf/auth/verify", {
        method: "GET",
        credentials: "include"
    });
    return response.ok;
}

// Function to fetch data from URL and display it
async function fetchData(query = "") {
    // "clamps" the search string to the input box if it's empty
    const to_search =  query === "" ? document.getElementById("search_bar").value : query;
    const url = API_URL + `search/${encodeURIComponent(to_search)}`;
    const response = await fetch(url, {
        method: "GET",
        credentials: "include"
    });
    const data = await response.text();
    // Display data in #displayArea
    document.getElementById("displayArea").innerHTML = `
        <h3>Search Results</h3>
        <p>${data}</p>
    `;
}