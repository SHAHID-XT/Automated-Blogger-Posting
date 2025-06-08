import os
import json
from dotenv import load_dotenv
import google.generativeai as genai


class GeminiBlogGenerator:
    def __init__(self):
        self._load_env()
        self._configure_gemini()
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def _load_env(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("❌ API_KEY not found in .env file.")

    def _configure_gemini(self):
        genai.configure(api_key=self.api_key)

    def _build_prompt(self,blog_url):
            return """
You are a professional blog content writer and SEO expert.

🎯 Task:
Write a fully original, human-like blog post inspired by this article URL:  
""" + blog_url + """
\n
⚠️ Note:
- The provided URL may sometimes be invalid, inaccessible, or not suitable for creating a blog post.
- If you cannot create a blog post based on the URL for any reason,
- OR if the content you generate is NOT a blog post (e.g., unrelated text, summary, list, or other content types),
please respond ONLY with a valid JSON where "title" and "content" are null, and other fields are empty lists or null.

💡 Guidelines:
- Use natural, friendly, human language.
- Title and content should sound like a real person, not AI.
- Create fully formatted content for Blogger (use clean HTML).
- Include SEO details like keywords, tags, and categories.
- Content should be long, detailed, and engaging.

📦 Output format (return JSON only):

{
  "title": "Blog title or null if blog cannot be created",
  "slug": "seo-friendly-url-slug or null",
  "meta_description": "SEO-friendly description under 160 characters or null",
  "seo_keywords": ["keyword1", "keyword2", "..."] or [],
  "tags": ["tag1", "tag2", "..."] or [],
  "content": "<h1>Formatted HTML content for Blogger with headings, paragraphs, and lists</h1> or null",
  "category": ["category1", "category2"] or [],
  "image_prompt": "A descriptive, creative prompt that can be used to generate an AI image related to this blog post."
}

Only return valid JSON. No explanations, notes, or markdown formatting.
"""

    def generate_blog_json(self,blog_url):
        prompt = self._build_prompt(blog_url)
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip().replace("```json", "").replace("```", "")
            blog_data = json.loads(raw_text)

            if "title" not in blog_data or "content" not in blog_data:
                raise ValueError("Missing 'title' or 'content' key in the generated blog JSON.")

            return blog_data

        except (json.JSONDecodeError, ValueError) as e:
            print(f"❌ JSON parse or validation error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

        return {
            "title": None,
            "slug": None,
            "meta_description": None,
            "seo_keywords": [],
            "tags": [],
            "content": None,
            "category": []
        }


