import requests

# Step 1: Register a user
# Step 2: Log in to obtain the JWT token
# breakpoint()
#
# url = "http://0.0.0.0:8021/auth/jwt/login"
#
# payload = 'grant_type=password&username=user%40example.com&password=merlin'
# headers = {
#   'accept': 'application/json',
#   'Content-Type': 'application/x-www-form-urlencoded'
# }
#
# response = requests.request("POST", url, headers=headers, data=payload)


# print(response.text)
breakpoint()
url = "http://0.0.0.0:8021/authenticated-route"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NmYyN2U4M2ZjZjVjMjRlYWMzZTQwNWEiLCJhdWQiOlsiZmFzdGFwaS11c2VyczphdXRoIl0sImV4cCI6MTcyNzE3NDM2MX0.b-TmzRoiaNc16O5RZT6l9fWSdrqRQNIyJD5oF5iMZQA",
}
response = requests.request("GET", url, headers=headers)

breakpoint()
