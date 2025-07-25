from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up Flask app
app = Flask(__name__)

def generate_section(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    industry = data.get("industry", "")
    geography = data.get("geography", "")
    product_focus = data.get("product_focus", "")
    timeframe = data.get("timeframe", "")
    sections = {}

    if data.get("generate_industry"):
        prompt = f"Write an industry overview for a CIM. Industry: {industry}, Geography: {geography}, Product Focus: {product_focus}, Timeframe: {timeframe}."
        sections["industry"] = generate_section(prompt)

    if data.get("generate_company"):
        prompt = f"Write a sample company overview section for a CIM. Assume a typical small business in {industry} within {geography}."
        sections["company"] = generate_section(prompt)

    if data.get("generate_swot"):
        prompt = f"Write a SWOT analysis for a typical {industry} company in {geography}. Focus on strengths, weaknesses, opportunities, and threats."
        sections["swot"] = generate_section(prompt)

    if data.get("generate_financials"):
        prompt = f"Write a financial highlights section for a typical {industry} company operating in {geography} with a focus on {product_focus}."
        sections["financials"] = generate_section(prompt)

    if data.get("generate_comps"):
        prompt = f"Write a comparables analysis overview for a {industry} company in {geography}."
        sections["comps"] = generate_section(prompt)

    return jsonify(sections)

if __name__ == "__main__":
    app.run(debug=True)
