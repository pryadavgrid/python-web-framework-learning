# 🌐 REST API

REST API (Representational State Transfer) is a way for different systems (like frontend and backend) to communicate over the web using HTTP.

* It follows a **client-server architecture**
* The **client** sends a request
* The **server** processes it and returns a response
* Data is usually sent in **JSON format**

👉 Important:

* REST is **not a protocol**, it is an **architectural style**
* Developers can design REST APIs in different ways by following its rules

---

# 🧱 REST Architectural Constraints

REST APIs follow these 5 main constraints:

1. Client-Server
2. Stateless
3. Cacheable
4. Uniform Interface (Most Important)
5. Layered System

---

## 1. Client-Server

* Client and server are **separate**
* Frontend → Handles UI
* Backend → Handles logic & database

👉 Benefit: Independent development

---

## 2. Stateless

* Server does **NOT store previous request data**
* Each request must contain all required information

### Example:

```
GET /profile
Authorization: Bearer token123
```

👉 Benefit: Easy to scale

---

## 3. Cacheable

* Responses can be stored (cached)
* Helps reduce server load
* Improves performance

---

## 4. Uniform Interface ⭐ (Most Important)

APIs must follow a **consistent structure**

### Rules:

* Use proper HTTP methods
* Use clean and meaningful URLs
* Return clear and standard responses

### Example:

```
GET    /users        → Get all users
POST   /users        → Create user
PUT    /users/1      → Update user
DELETE /users/1      → Delete user
```

👉 Benefit: Easy to understand and use

---

## 5. Layered System

* API can have multiple layers (security, business logic, database)
* Client does not know about these layers

👉 Benefit: Better security & scalability

---

# 🏷️ REST Resource Naming

Resource naming is **how you design your API URLs (endpoints)**.
Good naming makes APIs easy to understand and use.

---

## ✅ Best Practices

### 1. Use Nouns (Not Verbs)

* ❌ `/getUsers`
* ✅ `/users`

👉 Because HTTP methods already define action

---

### 2. Use Plural Names

* ❌ `/user`
* ✅ `/users`

---

### 3. Use Hierarchy for Relationships

```
/users/1/posts
```

👉 User with ID 1 ke posts

---

### 4. Use Proper HTTP Methods

| Method | Use Case       | Example    |
| ------ | -------------- | ---------- |
| GET    | Read data      | `/users`   |
| POST   | Create data    | `/users`   |
| PUT    | Update full    | `/users/1` |
| PATCH  | Update partial | `/users/1` |
| DELETE | Delete data    | `/users/1` |

---

### 5. Use Lowercase and Hyphens

* ✅ `/user-profiles`
* ❌ `/UserProfiles`

---

### 6. Avoid File Extensions

* ❌ `/users.json`
* ✅ `/users`

---

### 7. Use Query Parameters for Filtering

```
/users?age=25
/users?sort=desc
```

---

### 8. Use Clear and Meaningful Names

* ❌ `/data`
* ✅ `/orders`

---

# 🔍 GraphQL

GraphQL is a **query language for APIs** (developed by Facebook).

* Client can request **only the data it needs**
* Avoids over-fetching and under-fetching

### Example:

```graphql
query {
  user(id: 1) {
    name
    email
  }
}
```

👉 Response will include only `name` and `email`

---

# ⚡ gRPC (Google Remote Procedure Call)

gRPC is a **high-performance API technology** developed by Google.

* Uses **Protocol Buffers (binary format)** instead of JSON
* Faster and more efficient
* Works over **HTTP/2**

### Example:

```proto
service UserService {
  rpc GetUser (UserRequest) returns (UserResponse);
}
```

---

# ⚖️ REST vs GraphQL vs gRPC

| Feature       | REST       | GraphQL              | gRPC                      |
| ------------- | ---------- | -------------------- | ------------------------- |
| Data Format   | JSON / XML | GraphQL Query Format | Protocol Buffers (Binary) |
| Data Fetching | Fixed data | Custom data          | Defined via proto         |
| Transport     | HTTP/1.1   | HTTP                 | HTTP/2                    |
| Performance   | Medium     | Better than REST     | Fastest                   |
| Flexibility   | Low        | High                 | Medium                    |

---

# 📌 Use Cases

## REST

* Twitter API
* GitHub API
* Stripe API

👉 Best for: Simple, widely-used web APIs

---

## GraphQL

* Facebook API
* Shopify API
* GitHub API v4

👉 Best for: Complex frontend apps (React, mobile apps)

---

## gRPC

* Google APIs
* Netflix (internal services)
* Cisco APIs

👉 Best for: Microservices & high-performance systems

---

# ✅ Summary

* **REST** → Simple, standard, easy to use
* **GraphQL** → Flexible, client controls data
* **gRPC** → Fast, efficient, best for backend systems

---
