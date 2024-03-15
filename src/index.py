import requests
from pymongo import MongoClient

# Function to fetch users data from API and store it in the database
def fetch_and_store_users(api_key, db):
    url = "https://dummyapi.io/data/v1/user"
    headers = {"app-id": api_key}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    # print(data)
    
    users_collection = db["users"]
    users_collection.delete_many({})  # Clear existing data
    
    for user in data['data']:
        user_id = user['id']
        name = user['firstName'] + " " + user['lastName']
        picture = user['picture']
        
        users_collection.insert_one({"user_id": user_id, "name": name, "picture": picture})

# Function to fetch posts data for each user and store it in the database
def fetch_and_store_posts(api_key, db):
    users_collection = db["users"]
    posts_collection = db["posts"]
    
    users = users_collection.find()
    url_base = "https://dummyapi.io/data/v1/user"
    headers = {"app-id": api_key}
    
    for user in users:
        user_id = user['user_id']
        url = f"{url_base}/{user_id}/post"
        
        response = requests.get(url, headers=headers)
        posts_data = response.json()
        
        print('post Date : ',posts_data)

        for post in posts_data['data']:
            post_id = post['id']
            title = post['text'] if 'text' in post else ''
            content = post['image'] if 'image' in post else ''
            
            posts_collection.insert_one({"post_id": post_id, "user_id": user_id, "title": title, "content": content})

def main():
    api_key = "65f19c15e5c046193603759e"
    client = MongoClient('localhost', 27017)
    db = client["users_posts_db"]
    
    fetch_and_store_users(api_key, db)
    fetch_and_store_posts(api_key, db)
    
    client.close()

if __name__ == "__main__":
    main()
