import os
import json
import pickle
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from blog_generator import GeminiBlogGenerator
from image_generator import AIImageGenerator
from search_api import GoogleCustomSearch

class BloggerPoster:
    def __init__(self, credentials_path='credentials.json', token_path='token.pkl'):
        self.SCOPES = ['https://www.googleapis.com/auth/blogger']
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
            creds = flow.run_local_server(port=0)
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('blogger', 'v3', credentials=creds)

    def get_blog_id(self):
        blogs = self.service.blogs().listByUser(userId='self').execute()
        return blogs['items'][0]['id']  # Pick the first blog

    def post_blog(self, blog_id, blog_data):
        body = {
            "kind": "blogger#post",
            "title": blog_data['title'],
            "content": blog_data['content'],
            "labels": blog_data.get('tags', []),
        }
        post = self.service.posts().insert(blogId=blog_id, body=body, isDraft=False).execute()
        print(f"✅ Blog posted successfully: {post['url']}")


    def encode_image_to_base64(self,image_path):
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        return encoded_string


    def add_base64_cover_image(self,content, image_path):
        base64_img = self.encode_image_to_base64(image_path)
        img_tag = f'<img src="data:image/png;base64,{base64_img}" alt="Cover Image" style="max-width:100%; height:auto; margin-bottom:20px;" />'
        return img_tag + content


if __name__ == "__main__":
    gcs = GoogleCustomSearch()
    keyword = "Cyber News"
    result = gcs.search_one_unique(keyword)
    if result:
        blog_url = result['link']

        generator = GeminiBlogGenerator()
        blog_json = generator.generate_blog_json(blog_url=blog_url)
        print(blog_json)

        if not blog_json["title"]:
            print("Failed to generate blog.")
        else:
            image_generator = AIImageGenerator()
            poster = BloggerPoster()
            image_path = "image.png"
            image_prompt = blog_json.get("image_prompt", "blog related image")
            image_generator.generate_image(image_prompt, save_path=image_path)
        
            # Embed the generated image as base64 in blog content
            blog_json["content"] = poster.add_base64_cover_image(blog_json["content"], image_path)
            
            # Post the blog
            blog_id = poster.get_blog_id()
            poster.post_blog(blog_id, blog_json)
