"""
Smart Text Response System for PromptAgro
Provides professional advice when AI image generation is unavailable
"""

def create_smart_packaging_advice(product_data):
    """
    Create intelligent, professional packaging advice based on user input
    Simple language, encouraging tone, business-focused
    """
    
    product_name = product_data.get("productName", "your product")
    tagline = product_data.get("tagline", "")
    colors = product_data.get("preferredColors", "green")
    emotion = product_data.get("desiredEmotion", "trust")
    platform = product_data.get("salesPlatform", "local market")
    story = product_data.get("productStory", "")
    
    # Parse colors if it's a JSON string
    if isinstance(colors, str) and colors.startswith('['):
        import json
        try:
            colors = json.loads(colors)
        except:
            colors = ["green"]
    
    if isinstance(colors, list) and colors:
        primary_color = colors[0]
        color_scheme = " and ".join(colors[:3])
    else:
        primary_color = "green"
        color_scheme = "green"
    
    # Smart advice based on their choices
    advice_parts = []
    
    # Opening - show we understand their vision
    advice_parts.append(f"Perfect! I can see exactly what you're going for with {product_name}.")
    
    # Color psychology advice
    color_psychology = {
        "green": "Green is excellent for agricultural products - it instantly communicates freshness, nature, and health. Your customers will trust this choice.",
        "blue": "Blue conveys trust and reliability - perfect for premium products. It suggests quality and professionalism.",
        "red": "Red creates excitement and urgency - great for grabbing attention on shelves and driving quick purchase decisions.",
        "yellow": "Yellow represents energy and freshness - ideal for products like honey, citrus, or anything that should feel vibrant and natural.",
        "orange": "Orange is warm and friendly - it makes your product feel approachable and suggests natural goodness.",
        "brown": "Brown suggests authenticity and earthiness - perfect for organic or traditional products that emphasize natural origins."
    }
    
    if primary_color.lower() in color_psychology:
        advice_parts.append(color_psychology[primary_color.lower()])
    
    # Platform-specific advice
    platform_advice = {
        "farmers-market": "For farmers markets, you want packaging that tells your story and builds personal connection. People shop there for authenticity.",
        "premium-retail": "Premium retail requires sophisticated packaging that justifies higher prices. Focus on quality cues and professional presentation.",
        "online": "Online sales need packaging that photographs well and creates excitement when customers receive it. Think 'unboxing experience'.",
        "local-market": "Local markets love products that feel familiar yet special. Balance approachability with quality indicators."
    }
    
    if platform in platform_advice:
        advice_parts.append(platform_advice[platform])
    
    # Emotion-driven advice
    emotion_advice = {
        "trust": "Building trust is smart - use clean fonts, clear information, and avoid cluttered designs. Less is more for trustworthy packaging.",
        "excitement": "Creating excitement means bold colors, dynamic layouts, and maybe some creative typography. Make it pop on the shelf!",
        "comfort": "Comfort comes from familiar, warm designs. Think rounded corners, soft colors, and friendly messaging.",
        "premium": "Premium feeling needs sophistication - consider gold accents, elegant fonts, and plenty of white space."
    }
    
    if emotion in emotion_advice:
        advice_parts.append(emotion_advice[emotion])
    
    # Specific product advice based on story or name
    if "honey" in product_name.lower():
        advice_parts.append("For honey, consider hexagon patterns (like honeycomb) and warm golden colors. Customers love these natural connections.")
    elif "tomato" in product_name.lower():
        advice_parts.append("Tomato products work great with vine imagery or farm scenes. Show the freshness and farm-to-table story.")
    elif "organic" in product_name.lower() or "organic" in tagline.lower():
        advice_parts.append("Organic products should emphasize natural elements - leaves, earth tones, or simple clean designs that say 'pure'.")
    
    # Story integration
    if story and len(story.strip()) > 10:
        advice_parts.append(f"Your story about {story[:50]}... is gold! Put a short version right on the package - people buy stories, not just products.")
    
    # Next steps
    advice_parts.append("Here's what I recommend for your next steps:")
    advice_parts.append(f"✓ Use your {color_scheme} color scheme consistently across all materials")
    advice_parts.append("✓ Keep your tagline short and memorable - it should fit on the package clearly")
    advice_parts.append("✓ Consider adding a small logo or symbol that represents your farm/brand")
    advice_parts.append("✓ Test your design by asking: 'Would I pick this up in the store?'")
    
    # Encouraging closing
    advice_parts.append("You've given me great information to work with. Your product has real potential!")
    advice_parts.append("We're working on upgrading our image generation system, but for now, use this advice to sketch or work with a local designer.")
    
    return "\n\n".join(advice_parts)


def create_concept_summary(product_data):
    """Create a summary of marketing concepts"""
    
    product_name = product_data.get("productName", "Product")
    emotion = product_data.get("desiredEmotion", "trust")
    platform = product_data.get("salesPlatform", "local market")
    
    concepts = [
        f"Brand positioning: Premium {product_name.lower()} for {platform} customers",
        f"Emotional appeal: Designed to create {emotion} and connection",
        f"Visual strategy: Clean, professional packaging that stands out",
        f"Target message: Quality you can trust, freshness you can see"
    ]
    
    return concepts
