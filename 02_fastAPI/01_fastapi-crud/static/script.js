const BASE_URL = "http://127.0.0.1:8000";

/* ================= USERS ================= */

document.getElementById("createUserBtn").addEventListener("click", createUser);
document.getElementById("loadUsersBtn").addEventListener("click", getUsers);

async function getUsers() {
    const response = await fetch(`${BASE_URL}/users/`);
    const users = await response.json();

    const userList = document.getElementById("userList");
    userList.innerHTML = "";

    users.forEach(user => {
        const div = document.createElement("div");
        div.className = "list-item";

        div.innerHTML = `
            <strong>${user.name}</strong> (${user.email})
            <button class="delete-btn" onclick="deleteUser(${user.id})">Delete</button>
        `;

        userList.appendChild(div);
    });
}

async function createUser() {
    const name = document.getElementById("userName").value;
    const email = document.getElementById("userEmail").value;

    if (!name || !email) {
        alert("Please enter name and email");
        return;
    }

    await fetch(`${BASE_URL}/users/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email })
    });

    document.getElementById("userName").value = "";
    document.getElementById("userEmail").value = "";

    getUsers();
}

async function deleteUser(id) {
    await fetch(`${BASE_URL}/users/${id}`, {
        method: "DELETE"
    });

    getUsers();
}


/* ================= ITEMS ================= */

document.getElementById("createItemBtn").addEventListener("click", createItem);
document.getElementById("loadItemsBtn").addEventListener("click", getItems);

// GET /items/
async function getItems() {
    const response = await fetch(`${BASE_URL}/items/`);
    const items = await response.json();

    const itemList = document.getElementById("itemList");
    itemList.innerHTML = "";

    items.forEach(item => {
        const div = document.createElement("div");
        // console.log(item)
        div.className = "list-item";

        div.innerHTML = `
            <strong>${item.item_name}</strong><br>
            <small>${item.item_detail}</small>
        `;

        itemList.appendChild(div);
    });
}

// POST /items/
async function createItem() {
    const item_name = document.getElementById("itemName").value;
    const item_detail = document.getElementById("itemDetail").value;

    if (!item_name || !item_detail) {
        alert("Please fill all fields");
        return;
    }

    await fetch(`${BASE_URL}/items/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            item_name: item_name,
            item_detail: item_detail
        })
    });

    document.getElementById("itemName").value = "";
    document.getElementById("itemDetail").value = "";

    getItems();
}