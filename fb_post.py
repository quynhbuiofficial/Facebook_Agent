from dotenv import load_dotenv
import requests
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.tools import FunctionTool
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential
from bs4 import BeautifulSoup
import re
from utils import SYSTEM_MESSAGE, INPUT_MESSAGE
from autogen_agentchat.ui import Console
import random
from PIL import Image
from io import BytesIO
from ddgs import DDGS


class Agent_Post_FB():
    def __init__(self):
        load_dotenv()
        self.input_message = INPUT_MESSAGE
        self.system_message = SYSTEM_MESSAGE
        self.image_url = "" 
        self.PAGE_ID = os.getenv("PAGE_ID")
        self.FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
        self.post_url = f"https://graph.facebook.com/v23.0/{self.PAGE_ID}/photos"
        self.model_client = AzureAIChatCompletionClient(
            model=os.getenv("MODEL"),
            endpoint="https://models.inference.ai.azure.com",
            credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN")),
            model_info={
                "json_output": False,
                "function_calling": True,
                "vision": False,
                "family": "unknown",
                "structured_output": False,
            },
            temperature=0.4
        )
    
    def bold_unicode(self, text):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        bold = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭" + "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇" +"𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
        trans = str.maketrans(normal, bold)
        return text.translate(trans)
    
    def format_bold_sections(self, text):
        # Tìm các đoạn nằm giữa **...**
        def replacer(match):
            return self.bold_unicode(match.group(1))
        return re.sub(r"\*\*(.*?)\*\*", replacer, text, flags=re.DOTALL)


    def post_facebook(self, post_content: str):
        formatted_content = self.format_bold_sections(post_content)
        payload = {
            "message": formatted_content,
            "access_token": self.FB_ACCESS_TOKEN,
            "url": self.image_url 
        }
        r = requests.post(self.post_url, data=payload)
        return str(r.text)
    

    def extract_text_from_url(self, url):
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            # 👉 Lấy tiêu đề từ thẻ <h1>
            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else ""

            # Lấy đoạn văn
            paragraphs = soup.find_all("p")
            content = "\n".join([
                p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 77
            ])
            # Tìm ảnh toàn trang
            image_urls = []
            for img in soup.find_all("img"):
                src = (
                    img.get("data-src") or
                    img.get("data-srcset") or
                    img.get("data-original") or
                    img.get("src")
                )
                if not src:
                    continue
                src = re.sub(r"[\s\n\r\t]+", "", src.strip())
                if src.startswith("https://") and re.search(r"\.(jpg|jpeg|png)(\?|$)", src.lower()) and "icon" not in src.lower() and "logo" not in src.lower():
                    try:
                        response = requests.get(src, timeout=5)
                        image = Image.open(BytesIO(response.content))
                        width, height = image.size

                        if width >= 512 and height >= 512:
                            print("✅ LARGE CONTENT IMAGE:", src, f"({width}x{height})")
                            image_urls.append(src)
                    except Exception as e:
                        print(f"⚠️ Không lấy được ảnh {src}: {e}")

            selected_image = image_urls[0] if image_urls else []
            full_content = f"{title}\n\n{content}"
            return full_content, selected_image

        except Exception as e:
            print(f"⚠️ Lỗi khi crawl {url}: {e}")
            return None, ""

    def get_news_internet(self, input_query:str):
        results = list(DDGS().text(input_query, max_results=6))
        print("results: ", results)
        blocked_domains = os.getenv("BLOCKED_DOMAINS", "")
        print("blocked_domains: ", blocked_domains)
        blocked_domains = [domain.strip().lower() for domain in blocked_domains.split(",") if domain.strip()]
        filtered_results = [item for item in results 
                    if all(domain not in item.get("href", "").lower() for domain in blocked_domains)]
        selected_news = random.sample(filtered_results, 2) if len(filtered_results) >= 2 else filtered_results
        full_content = ""
        for idx, item in enumerate(selected_news):
            title = item.get('title')
            url = item.get('href')
            print(f"\n--- {title} ---")
            print(f"📰 Link: {url}")

            content, img_url = self.extract_text_from_url(url)
            if content:
                full_content += content[:1500] + "\nNguồn:" + url + "\n\n"
            if img_url and self.image_url == "":
                print(f" {idx + 1} - ẢNH SỬ DỤNG Tìm thấy ảnh: ", img_url)
                self.image_url = img_url
        return full_content
    
    async def run(self):
        post_tool = FunctionTool(self.post_facebook, 
                                 description= "Post content to Facebook")
        get_news_internet_tool = FunctionTool(self.get_news_internet,
                                              description="Fetch latest news by keyword")

        assistant_agent = AssistantAgent(
            name="assistant",
            description="An assistant that writes and posts content to Facebook using internet news.",
            model_client=self.model_client,
            tools=[post_tool, get_news_internet_tool],
            system_message=self.system_message,
            reflect_on_tool_use=True,
        )
        text_termination = TextMentionTermination("THANKS_NE")
        team = RoundRobinGroupChat([assistant_agent], max_turns=3, termination_condition=text_termination)
        await Console(team.run_stream(task=self.input_message))

        

async def main():
    fb = Agent_Post_FB()
    await fb.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main=main())
    
