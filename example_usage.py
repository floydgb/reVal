#!/usr/bin/env python3
"""
Example usage of reVal Agent
Demonstrates how to generate a property valuation report
"""

import os
from src.reval_agent import ReValAgent

def main():
    """Example of how to use the reVal agent"""
    
    # Check if environment variables are set
    if not os.getenv('RAPIDAPI_KEY'):
        print("❌ Error: RAPIDAPI_KEY not found in environment variables")
        print("📝 Please:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your RapidAPI key to the .env file")
        print("   3. Run: source .env")
        return
    
    # Create the agent
    print("🏠 Initializing reVal Agent...")
    agent = ReValAgent()
    
    # Example property
    address = "123 Main Street"
    city = "Seattle"
    state = "WA"
    
    print(f"🔍 Generating report for: {address}, {city}, {state}")
    
    # Generate the report
    pdf_path = agent.generate_property_report(address, city, state)
    
    if pdf_path:
        print(f"✅ Report generated successfully!")
        print(f"📄 PDF saved to: {pdf_path}")
    else:
        print("❌ Failed to generate report")
        print("💡 Check your API key and property address")

if __name__ == "__main__":
    main()
