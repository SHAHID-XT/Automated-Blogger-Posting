
# Automated Blogger Posting with Google Custom Search and AI Image Generation

This project automates the process of generating and posting blogs on a Blogger account using data fetched from Google Custom Search API. It integrates an AI-powered blog content generator and AI image generator to create engaging posts with relevant images, then posts them automatically on your Blogger site.

---

## Features

- **Google Custom Search API** to find unique and recent article URLs based on keywords.
- **GeminiBlogGenerator**: Custom blog content generator (assumed AI or scraping-based) that creates blog text and metadata from an article URL.
- **AIImageGenerator**: Generates relevant images using AI based on blog content prompts.
- **Blogger API integration** for seamless authentication and posting.
- Supports embedding generated images directly into blog content as base64 inline images.
- Persistent token storage for Google API authentication.
- Skips duplicate articles with link tracking.

---

## Components

| Module               | Description                                  |
|----------------------|----------------------------------------------|
| `main.py`            | Orchestrates search, blog generation, image creation, and posting. |
| `search_api.py`      | Implements Google Custom Search API wrapper with filtering logic.  |
| `blog_generator.py`  | Contains `GeminiBlogGenerator` to create blog content from URLs.  |
| `image_generator.py` | Contains `AIImageGenerator` to create images from prompts.         |

---

## Prerequisites

- Python 3.7+
- Google Cloud project with:
  - Google Custom Search API enabled.
  - Blogger API enabled.
- Credentials JSON file for Google APIs (OAuth client credentials).
- `.env` file with Google Custom Search API key and CX ID (for `search_api.py`).
- Required Python packages installed.

---

## Installation


1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Setup your environment variables in `.env` file:

```
search_api=YOUR_GOOGLE_CUSTOM_SEARCH_API_KEY
CX=YOUR_CUSTOM_SEARCH_ENGINE_ID
```

3. Place your Google API OAuth credentials file (`credentials.json`) in the project root.

---

## Usage

Run the main script to generate and post a blog automatically:

```bash
python main.py
```

### What happens?

* Searches Google Custom Search for a recent unique article matching your keyword (default: `"Cyber News"`).
* Generates blog content and metadata from the article URL using `GeminiBlogGenerator`.
* Generates a relevant AI image based on blog content prompt.
* Encodes and embeds the image as a base64 cover image in the blog post content.
* Authenticates with Blogger API and posts the blog directly to your first linked blog.
* Prints the published blog URL upon success.

---

## Configuration

* **Keyword:** Change the search keyword inside `main.py`:

```python
keyword = "Cyber News"
```

* **Credentials:** Place your `credentials.json` for Google OAuth (Blogger API access).
* **Token Storage:** OAuth tokens are saved to `token.pkl` for reuse.
* **Image Save Path:** Default image saved as `image.png` in the project directory.
* **Blog Content Generation:** Modify or extend `GeminiBlogGenerator` in `blog_generator.py`.
* **Image Generation:** Customize `AIImageGenerator` prompts or settings in `image_generator.py`.

---

## Authentication Flow

* On first run, browser window opens for Google OAuth consent.
* Token saved locally for subsequent runs.
* Uses Google Blogger API v3 for posting.

---

## Notes & Limitations

* Ensure your Google Custom Search engine is properly configured for your target search.
* API usage is subject to Google quotas and limits.
* AI generators (`GeminiBlogGenerator`, `AIImageGenerator`) require proper implementation and API keys as applicable.
* Image embedding as base64 may increase post size.
* The script posts to the first blog associated with your Google account — modify `get_blog_id()` if you have multiple blogs.

---

## Dependencies

* `google-auth-oauthlib`
* `google-api-python-client`
* `requests`
* `python-dotenv`
* Any dependencies required by your AI blog/image generators

---



## Acknowledgements

* Google Custom Search API & Blogger API



## Author

SHAHIDXT — | GitHub: [SHAHID-XT](https://github.com/SHAHID-XT)