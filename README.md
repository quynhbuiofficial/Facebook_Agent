# Facebook AI Agent Assistant

Automatically generate and post Facebook content using the AI Agent framework (autogen), integrated with the latest news search from the internet (DuckDuckGo), optimized for Digital Marketing and brand building.

## 🚀 Key Features

- **Automatic Facebook Post Creation & Publishing**: The AI Agent automatically fetches the latest news about AI, marketing, technology, creativity, etc. from the internet, summarizes, and posts to your fanpage.
- **Integrated with Agent framework autogen**: Uses autogen-agentchat to build an Assistant Agent, automating the process of fetching news, writing, and posting content.
- **News search via DuckDuckGo**: Utilizes the `ddgs` library to fetch the latest news, filter domains, extract content and images.
- **Customizable Content**: Posts are formatted with bold highlights, key phrases, and automatically include contact info and brand tagline.

## 🛠️ Installation

1. **Clone the repo & install dependencies**
   ```bash
   git clone <repo-url>
   cd push_github
   pip install -r requirements.txt
   ```

2. **Create a `.env` file with the following variables:**
   ```
   FB_ACCESS_TOKEN=...
   PAGE_ID=...
   GITHUB_TOKEN=...
   MODEL=...
   BLOCKED_DOMAINS=...
   ```
   - `FB_ACCESS_TOKEN`, `PAGE_ID`: Obtain from Facebook Developer (Graph API).
   - `GITHUB_TOKEN`: Token for Azure AI model (if using Azure).
   - `MODEL`: AI model name (e.g., gpt-4, gpt-3.5-turbo...).
   - `BLOCKED_DOMAINS`: (Optional) List of domains to exclude from news search.

## ⚡️ Manual Run

```bash
python fb_post.py
```
- The agent will automatically fetch news, summarize, write, and post to your Facebook Page.

## 🧠 How It Works

1. **Agent Assistant** (using autogen-agentchat) will:
   - Call the `get_news_internet` tool to fetch the latest news from DuckDuckGo.
   - Summarize and rewrite the content in an engaging way, highlight the brand, and add contact info.
   - Call the `post_facebook` tool to publish the post to the fanpage.
   - End with the message "THANKS_NE" (as per autogen workflow).

2. **News Fetching & Extraction**:
   - Uses DuckDuckGo (`ddgs`) to get the latest articles.
   - Filters out unwanted domains.
   - Extracts the title, main paragraphs, and the largest image from the article.

3. **Formatting & Posting**:
   - Automatically bolds key phrases (**bold**).
   - Adds tagline, contact info, and news source.
   - Posts with image to Facebook via Graph API.

## 🖥️ Automated Run with GitHub Actions

- Pre-configured workflow in `fb_agent.yml` to run periodically or manually via GitHub Actions.
- You need to set up the following secrets in your GitHub repo:
  - `FB_ACCESS_TOKEN`, `PAGE_ID`, `GITHUB_TOKEN`, `MODEL`, `BLOCKED_DOMAINS`, `VERIFY_TOKEN`

## 📦 Dependencies

- `autogen-agentchat`, `autogen-ext[azure]`: Build AI Agent, integrate with Azure AI.
- `ddgs`: DuckDuckGo news search.
- `requests`, `beautifulsoup4`: HTTP requests, web content extraction.
- `python-dotenv`: Environment variable management.
- `Pillow`: Image processing.
- `aiohttp`: Async support.

## 📄 Main Files Structure

- `fb_post.py`: Main code, defines the Agent, tools, news fetching, and posting logic.
- `fb_agent.yml`: GitHub Actions workflow.
- `requirements.txt`: List of dependencies.

## 📬 Contact

- 📧 Email: quynhsydaole@gmail.com
- 📺 YouTube: https://www.youtube.com/@QuynhBuiOffical 
