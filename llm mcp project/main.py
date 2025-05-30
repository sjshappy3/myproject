from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Mount static files (for CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# MCP Configuration (Ideally, these would be more securely managed)
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
MINIMAX_GROUP_ID = os.getenv("MINIMAX_GROUP_ID") # Added for Minimax API calls
AMAP_API_KEY = os.getenv("AMAP_API_KEY")

import ollama

# --- Helper Functions for MCP Calls ---
async def generate_travel_guide_with_ollama(city_name: str):
    prompt = f"""请为我提供关于中国{city_name}的详细旅游攻略，请严格按照以下格式组织内容，每个部分以【】包裹标题，例如【经典景点】：

【经典景点】
[此处列出3-5个经典景点，每个景点附带简短描述]

【三日游玩路线规划】
[此处提供一个为期三天的详细游玩路线建议，包括每天的主要活动和景点安排]

【当地特色美食推荐】
[此处推荐3-5种当地特色美食，并简要介绍]

【住宿类型建议】
[此处提供一些住宿类型的建议，例如酒店、民宿、客栈等，并说明各自特点]
"""
    try:
        response = ollama.chat(
            model='qwen3:1.7b',
            messages=[{'role': 'user', 'content': prompt}],
            # stream=False # 确保获取完整响应
        )
        content = response['message']['content']

        # 解析Ollama的响应
        guide_data = {
            "attractions": "未能解析景点信息。",
            "itinerary": "未能解析路线信息。",
            "food": "未能解析美食信息。",
            "accommodation_general": "未能解析住宿信息。"
        }

        sections = {
            "【经典景点】": "attractions",
            "【三日游玩路线规划】": "itinerary",
            "【当地特色美食推荐】": "food",
            "【住宿类型建议】": "accommodation_general"
        }
        
        current_section_key = None
        current_content = []

        for line in content.split('\n'):
            found_new_section = False
            for header, key in sections.items():
                if header in line:
                    if current_section_key and current_content:
                        guide_data[sections[current_section_key]] = "\n".join(current_content).strip()
                    current_section_key = header
                    current_content = []
                    # Remove the header itself from the content if needed, or keep it if it's part of the description
                    # line_content = line.replace(header, "").strip()
                    # if line_content:
                    #    current_content.append(line_content)
                    found_new_section = True
                    break
            if not found_new_section and current_section_key:
                if line.strip(): # Add non-empty lines
                    current_content.append(line.strip())
        
        # Add the last section's content
        if current_section_key and current_content:
            guide_data[sections[current_section_key]] = "\n".join(current_content).strip()
        
        # Fallback if parsing fails for some sections
        for key, value in guide_data.items():
            if value.startswith("未能解析") and key in content: # Basic check if the keyword exists at all
                 # A more sophisticated extraction might be needed if the above loop fails
                 pass # Keep the default error message

        return guide_data

    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return {
            "attractions": f"调用Ollama模型生成景点信息时出错: {e}",
            "itinerary": f"调用Ollama模型生成路线信息时出错: {e}",
            "food": f"调用Ollama模型生成美食信息时出错: {e}",
            "accommodation_general": f"调用Ollama模型生成住宿信息时出错: {e}",
            "error": str(e)
        }

async def get_travel_guide_from_minimax(city_name: str): # Keep the old function as a fallback or for other purposes if needed, or remove it.
    # This is a placeholder. Replace with actual Minimax API call logic.
    # You'll need to structure the prompt to Minimax to get:
    # - Classic attractions
    # - Itinerary planning
    # - Local food recommendations
    # - Accommodation suggestions (general types, Minimax won't know specific hotels)
    prompt = f"请为我提供关于中国{city_name}的旅游攻略，包括经典景点介绍、三日游玩路线规划、当地特色美食推荐以及住宿类型建议。"
    
    # Example of calling a hypothetical Minimax text generation endpoint
    # response = requests.post(
    #     "MINIMAX_TEXT_GENERATION_ENDPOINT", 
    #     headers={"Authorization": f"Bearer {MINIMAX_API_KEY}"},
    #     json={"prompt": prompt, "model": "text-davinci-003"} # Adjust model as needed
    # )
    # response.raise_for_status()
    # data = response.json()
    # return data.get("choices")[0].get("text")
    
    # Placeholder data for now
    return {
        "attractions": f"{city_name}著名景点：xxx, yyy, zzz。",
        "itinerary": f"三日游路线：第一天..., 第二天..., 第三天...",
        "food": f"当地美食：aaa, bbb, ccc。",
        "accommodation_general": "住宿建议：可以选择市中心的酒店、有特色的民宿或者靠近景区的客栈。"
    }

async def get_amap_location_and_traffic(city_name: str, place_name: str = None):
    # This is a placeholder. Replace with actual Amap API call logic.
    # 1. Geocode city_name to get coordinates if needed for broader searches
    # 2. Search for specific places (attractions, restaurants, hotels) to get their precise locations
    # 3. Get traffic information for routes or general city traffic status
    
    # Placeholder for geocoding city
    # city_geo_url = f"https://restapi.amap.com/v3/geocode/geo?address={city_name}&key={AMAP_API_KEY}"
    # city_response = requests.get(city_geo_url)
    # city_data = city_response.json()
    # city_location = city_data['geocodes'][0]['location'] if city_data['status'] == '1' and city_data['geocodes'] else None

    # Placeholder for POI search (e.g., for a specific hotel or attraction)
    poi_data = []
    if place_name:
        # poi_search_url = f"https://restapi.amap.com/v3/place/text?keywords={place_name}&city={city_name}&key={AMAP_API_KEY}"
        # poi_response = requests.get(poi_search_url)
        # data = poi_response.json()
        # if data['status'] == '1' and data['pois']:
        #     poi_data = [{'name': p['name'], 'location': p['location'], 'address': p['address']} for p in data['pois']]
        poi_data = [{'name': f'{place_name} (示例)', 'location': '116.404,39.915', 'address': f'{city_name}的某个地址'}]

    # Placeholder for traffic (this is complex, might need specific route planning)
    # For simplicity, let's assume we get some general advice or link to Amap for live traffic
    traffic_info = "出行建议：请使用高德地图App查看实时交通路况和规划具体路线。"
    
    return {
        "poi_data": poi_data,
        "traffic_info": traffic_info
    }

import httpx

async def generate_image_with_minimax(prompt: str, image_type: str = "generic"):
    """
    Generates an image using the Minimax Text-to-Image API.
    Returns a URL to the generated image or a placeholder on error.
    `image_type` is used for logging or error placeholders.
    """
    if not MINIMAX_API_KEY or not MINIMAX_GROUP_ID:
        print("Minimax API Key or Group ID not configured for image generation.")
        return f"https://via.placeholder.com/400x300.png?text=MinimaxConfigError:{image_type}"

    api_url = f"https://api.minimax.ai/v1/text_to_image?groupId={MINIMAX_GROUP_ID}"
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "image-01",  # Default model for image generation
        "prompt": prompt,
        "n": 1, # Generate one image
        "aspect_ratio": "16:9", # Common aspect ratio
        "prompt_optimizer": True # Use prompt optimization
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client: # Increased timeout for image generation
            response = await client.post(api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            
            response_data = response.json()
            if response_data.get("base_resp", {}).get("status_code") != 0:
                error_msg = response_data.get("base_resp", {}).get("status_msg", "Unknown API error")
                print(f"Minimax API Error: {error_msg}")
                return f"https://via.placeholder.com/400x300.png?text=MinimaxAPIError:{image_type}"

            if response_data.get("data") and isinstance(response_data["data"], list) and len(response_data["data"]) > 0:
                image_url = response_data["data"][0].get("url")
                if image_url:
                    return image_url
                else:
                    print("Minimax API response did not contain an image URL.")
                    return f"https://via.placeholder.com/400x300.png?text=NoImageUrlReturned:{image_type}"
            else:
                print("Minimax API response format unexpected or no data.")
                return f"https://via.placeholder.com/400x300.png?text=InvalidResponseFormat:{image_type}"

    except httpx.HTTPStatusError as e:
        print(f"HTTP error calling Minimax Image API: {e.response.status_code} - {e.response.text}")
        return f"https://via.placeholder.com/400x300.png?text=HttpError_{e.response.status_code}:{image_type}"
    except httpx.RequestError as e:
        print(f"Request error calling Minimax Image API: {e}")
        return f"https://via.placeholder.com/400x300.png?text=RequestError:{image_type}"
    except Exception as e:
        print(f"Unexpected error calling Minimax Image API: {e}")
        return f"https://via.placeholder.com/400x300.png?text=GeneralError:{image_type}"

# --- FastAPI Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search_city(request: Request, city: str = Form(...)):
    error_message = None
    guide_data = None
    amap_data = None
    images = {}

    try:
        guide_data = await generate_travel_guide_with_ollama(city)
        # guide_data = await get_travel_guide_from_minimax(city) # Old call, commented out
        # For simplicity, let's assume we want to get locations for some attractions mentioned
        # In a real app, you'd parse guide_data.attractions to get specific names
        # amap_data = await get_amap_location_and_traffic(city, "某个推荐景点") 
        amap_data = await get_amap_location_and_traffic(city)

        # Generate images based on guide content
        if guide_data:
            if guide_data.get("attractions") and guide_data.get("attractions") != "未能解析景点信息。":
                images['attractions_image'] = await generate_image_with_minimax(
                    f"中国{city}的景点: {guide_data['attractions'][:100]}", "attractions"
                )
            if guide_data.get("itinerary") and guide_data.get("itinerary") != "未能解析路线信息。":
                images['itinerary_image'] = await generate_image_with_minimax(
                    f"中国{city}的游玩路线: {guide_data['itinerary'][:100]}", "itinerary"
                )
            if guide_data.get("food") and guide_data.get("food") != "未能解析美食信息。":
                images['food_image'] = await generate_image_with_minimax(
                    f"中国{city}的美食: {guide_data['food'][:100]}", "food"
                )
        if guide_data:
            if guide_data.get("attractions"):
                images['attractions'] = await generate_image_with_minimax(f"{city}景点 {guide_data['attractions'][:30]}")
            if guide_data.get("food"):
                images['food'] = await generate_image_with_minimax(f"{city}美食 {guide_data['food'][:30]}")
            
    except requests.exceptions.RequestException as e:
        error_message = f"API请求失败: {e}"
    except Exception as e:
        error_message = f"发生错误: {e}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "city": city,
        "guide_data": guide_data,
        "amap_data": amap_data,
        "images": images,
        "error_message": error_message
    })

if __name__ == "__main__":
    # Create dummy .env if it doesn't exist for local testing
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("MINIMAX_API_KEY=your_minimax_api_key_here\n")
            f.write("AMAP_API_KEY=your_amap_api_key_here\n")
        print("Created a dummy .env file. Please replace placeholder API keys.")
    uvicorn.run(app, host="0.0.0.0", port=8000)