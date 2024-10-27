const API_URL = "https://hackathon.midnight.wtf/"

async function check_logged_in() {
    let response = await fetch("https://hackathon.midnight.wtf/auth/verify", {
        method: "GET",
        credentials: "include"
    });
    if (response.ok) {
        return await response.json();
    }
    return false;
}

browser.runtime.onMessage.addListener(async (message) => {
    // Received from context menu activation
    // We basically "emulate" the search button click, or display the login form
    if (message.search_str) {
        if (await check_logged_in()) {
            await fetchData(null, message.search_str);
        } else {
            await login();
        }
    }
});

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
        document.getElementById("login").style.display = "none";
        document.getElementById("dashboard").style.display = "block";
    } else {
        alert("Incorrect username or password.");
    }
}

document.addEventListener('DOMContentLoaded',
  async function () {
    let token = await check_logged_in();
        if (token) {
            // defaults to the login screen, we want to skip it if we're already logged in
            toggle_display();
            await get_history(token);
        }
        document.getElementById("loginButton").addEventListener("click", login);
        document.getElementById("searchButton").addEventListener("click", fetchData);
        // document.getElementById("logoutButton").addEventListener("click", logout);

    }, false
);


async function get_history(token) {
    const url = API_URL + `db/fetch_user/` + token.token.sub;
    let resp = await fetch(url, {
        method: "GET",
        credentials: 'include'
    });
    if (resp.ok) {
        let data = await resp.json();
        seen = data.seen_products
        // reverse it
        seen = seen.reverse();
        // get first 5
        if (seen.length > 5) {
            seen = seen.slice(0, 5);
        }

        let history = document.getElementById("historyList");
        history.innerHTML = "";
        for (item in seen) {
            const url = API_URL + `db/fetch_product/` + seen[item];
            resp = await fetch(url, {
                method: "GET",
                credentials: 'include'
            });
            if (!resp.ok) { continue; }
            let data = await resp.json();
            let li = document.createElement("li");
                li.className = "history-item";
                li.textContent = data.product_name;
                history.appendChild(li);
        }
    }
}

async function logout() {
    const url = API_URL + `auth/logout`;
    let resp = await fetch(url, {
        method: "GET",
        credentials: 'include'
    });
    if (resp.ok) {
        toggle_display();
    }
}

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
    const loginForm = document.getElementById("login");
    const mainContent = document.getElementById("dashboard");

    const isLoginHidden = loginForm.style.display === "none";
    loginForm.style.display = isLoginHidden ? "block" : "none";
    mainContent.style.display = isLoginHidden ? "none" : "block";
}


async function check_logged_in() {
    let response = await fetch("https://hackathon.midnight.wtf/auth/verify", {
        method: "GET",
        credentials: "include"
    });
    if (response.ok) {
        return await response.json();
    }
    return false;
}

// Function to fetch data from URL and display it
async function fetchData(click, query = "") {
    // "clamps" the search string to the input box if it's empty
    const to_search =  query === "" ? document.getElementById("search_bar").value : query;
    const url = API_URL + `search/${encodeURIComponent(to_search)}`;
    const response = await fetch(url, {
        method: "GET",
        credentials: "include"
    });
    const json = await response.json();
    // Display data in #displayArea


    document.getElementById("search-result").innerHTML = `${json.project_name}`;
    document.getElementById("review-count").innerHTML = `${json.num_reviews}`;
    document.getElementById("review-pos").innerHTML = `${json.positive_reviews} Good`;
    document.getElementById("review-neu").innerHTML = `${json.num_reviews - json.positive_reviews - json.negative_reviews} Neutral`;
    document.getElementById("review-neg").innerHTML = `${json.negative_reviews} Bad`;


    const starContainer = document.getElementById("stars");
    for (let i = 0; i < starContainer.children.count; i++) {
        starContainer.children[i].classList.remove("full");
        starContainer.children[i].classList.remove("half");
        starContainer.children[i].classList.add("empty");
    }
    for (let i = 0; i < json.stars; i++) {
        starContainer.children[i].classList.add("full");
    }
    if (Math.round(json.stars) != Math.floor(json.stars)) {
        starContainer.children[Math.floor(json.stars)].classList.add("half");
    }

    /*document.getElementById("displayArea").innerHTML = `
        <h3>Search Results for<br>${json.product_name}</h3>
        <p>Stars: ${json.stars}<br>Total Reviews: ${json.num_reviews}<br>Pos/Neu/Neg: ${json.positive_reviews}/${json.num_reviews - json.positive_reviews - json.negative_reviews}/${json.negative_reviews}</p>
    `;*/
}