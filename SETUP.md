# reVal Setup Instructions

## 🚀 Quick Start

### 1. Get RapidAPI Access
1. Go to [RapidAPI Zillow API](https://rapidapi.com/apimaker/api/zillow-com1/)
2. Subscribe to a plan (free tier available)
3. Copy your API key

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API key
# RAPIDAPI_KEY=your_actual_api_key_here
```

### 4. Run Example
```bash
# Run the example script
python example_usage.py
```

## 📁 Project Structure

```
reVal/
├── src/
│   ├── __init__.py
│   ├── zillow_client.py      # RapidAPI Zillow client
│   ├── pdf_generator.py      # PDF report generator
│   └── reval_agent.py        # Main orchestrator
├── output/                   # Generated PDF reports
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
└── example_usage.py         # Usage example
```

## 🔧 Configuration

### Environment Variables
- `RAPIDAPI_KEY`: Your RapidAPI key for Zillow access
- `RAPIDAPI_HOST`: API host (default: zillow-com1.p.rapidapi.com)
- `OUTPUT_DIR`: PDF output directory (default: ./output)

### Customization
- Modify scoring algorithms in `reval_agent.py`
- Customize PDF styling in `pdf_generator.py`
- Add new data sources in `zillow_client.py`

## 📊 API Usage

### RapidAPI Zillow Endpoints Used:
1. **Property Search**: Find properties by address
2. **Property Details**: Get detailed information by ZPID
3. **Comparable Sales**: Get similar recent sales

### Rate Limits:
- Free tier: Limited requests per month
- Paid tiers: Higher limits and more features

## 🎯 Next Steps

1. **Test with real properties** in your area
2. **Customize the 10-factor analysis** for your market
3. **Enhance PDF styling** with your branding
4. **Add more data sources** for comprehensive analysis
5. **Deploy as a web service** for broader access

## 🐛 Troubleshooting

### Common Issues:
- **API Key Error**: Check your .env file and RapidAPI subscription
- **No Properties Found**: Verify address format and availability
- **PDF Generation Error**: Ensure output directory exists and has write permissions

### Support:
- Check logs for detailed error messages
- Verify API quotas on RapidAPI dashboard
- Test with different property addresses
