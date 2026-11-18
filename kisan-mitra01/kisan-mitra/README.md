# 🌾 KisanMitra (किसान मित्र) - Krishi Setu Platform

> **Direct Farmer-to-Buyer Marketplace & Government Schemes Discovery Portal**
> 
> *0% Middlemen Brokerage • 100% Farmer Profit • Nature & Crop-Themed Accessible UI*

---

## 🌟 Key Features

1. **🏛️ Government Schemes & Smart Eligibility Engine**:
   - Comprehensive repository of 15+ Central & State agricultural schemes (PM-Kisan, PM-KUSUM Solar Pumps 90% subsidy, PM Fasal Bima Yojana, Kisan Credit Card 4% loans, SMAM Tractor Subsidies, PKVY Organic Farming ₹50,000 grant, Soil Health Card, e-NAM, and more).
   - **Interactive Eligibility Matcher**: Input land size, state, crop type, and irrigation to get instant tailored subsidy matches.
   - **Kisan Audio Sahayak (Voice Reader)**: Web Speech API reading scheme benefits and steps out loud in Hindi and English.
   - Document checklist with interactive checkboxes and direct links to official government portals.

2. **🛒 Direct Farmer-to-Buyer Marketplace**:
   - **Zero Middlemen**: Eliminates broker commissions, giving farmers 20-30% higher earnings while providing consumers with fresh harvest at fair prices.
   - Farm gate listings with real photos, organic badges, mandi benchmark price comparison, and quantity available.
   - **Direct WhatsApp & Phone Connect**: 1-click WhatsApp chat link with pre-filled crop details.
   - In-app price negotiation and direct purchase offers.

3. **🚜 Dual Personas (Farmer vs. Buyer)**:
   - Dedicated **Farmer View**: Manage crop harvest listings, review incoming buyer offers, calculate middleman commission savings, and track eligible subsidies.
   - Dedicated **Buyer / Consumer View**: Browse farm-fresh produce, filter by organic certification, place buy offers, and connect directly with farmers.
   - 1-click **Quick Demo Switcher** in header to test both experiences effortlessly.

4. **📈 Live Mandi Market Rates & Trends**:
   - Live APMC mandi modal rates across major states.
   - Interactive 7-day Chart.js price trend graphs (Paddy, Wheat, Mustard, Onion, Cotton).

5. **⛅ Weather & ICAR Agro-Advisories**:
   - Live agro-meteorological widget with temperature, humidity, rainfall risks, and optimal pesticide spray windows.
   - Scientific seasonal crop advisories for Kharif, Rabi, and Zaid crops.

6. **🤖 Kisan AI Smart Assistant**:
   - Interactive conversational assistant answering farmer queries regarding solar subsidies, organic certification, pesticide treatment, and direct sales.

7. **📱 Cross-Platform Progressive Web App (PWA)**:
   - Fully responsive on Mobile, Tablet, and Desktop.
   - PWA Web Manifest & Service Worker for instant offline access and "Add to Home Screen" installation on Android, iOS, Windows, and macOS.

8. **🌐 Multilingual & Voice TTS Support (13 Languages)**:
   - English, हिन्दी (Hindi), ਪੰਜਾਬੀ (Punjabi), मराठी (Marathi), తెలుగు (Telugu), اردو (Urdu), தமிழ் (Tamil), বাংলা (Bengali), 日本語 (Japanese), Deutsch (German), Français (French), 中文 (Chinese), and 한국어 (Korean).
   - Includes real-time Text-to-Speech (TTS) voice narration with localized speech synthesis for all languages.

---

## 🚀 How to Run the App

1. Open your terminal in this directory:
   ```bash
   cd C:\Users\bishw\.gemini\antigravity\scratch\kisan-mitra
   ```

2. Start the Flask application:
   ```bash
   python app.py
   ```

3. Open your browser and visit:
   ```
   http://127.0.0.1:5000
   ```

---

## 🧪 Running Automated Tests

Run the unit test suite:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
