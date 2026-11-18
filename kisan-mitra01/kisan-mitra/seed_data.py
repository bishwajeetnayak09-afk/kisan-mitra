import json
from models import db, User, Produce, Scheme, MandiPrice, CropAdvisory

def seed_database():
    # Only seed if users table is empty
    if User.query.first():
        return

    print("Seeding KisanMitra database with comprehensive agricultural data...")

    # 1. Seed Users (Demo Farmer & Demo Buyer)
    farmer_ramesh = User(
        name='Ramesh Kumar Yadav (रमेश कुमार यादव)',
        email_or_phone='farmer@kisanmitra.in',
        role='farmer',
        phone='+91 98765 43210',
        state='Uttar Pradesh',
        district='Varanasi',
        village_or_city='Kashi Gram, Rajatalab',
        avatar_icon='tractor',
        verified=True,
        bio='Progressive farmer with 5 acres irrigated land. Specializing in organic basmati rice, mustard, and seasonal vegetables.',
        rating=4.9
    )
    farmer_ramesh.set_password('farmer123')

    farmer_gurpreet = User(
        name='Sardar Gurpreet Singh (ਗੁਰਪ੍ਰੀਤ ਸਿੰਘ)',
        email_or_phone='gurpreet@kisanmitra.in',
        role='farmer',
        phone='+91 98123 45678',
        state='Punjab',
        district='Ludhiana',
        village_or_city='Samrala Village',
        avatar_icon='wheat',
        verified=True,
        bio='Experienced wheat and pulse grower. 100% pesticide-free organic farming practices with APEDA certification.',
        rating=5.0
    )
    farmer_gurpreet.set_password('farmer123')

    buyer_priya = User(
        name='Priya Sharma (प्रिया शर्मा)',
        email_or_phone='buyer@kisanmitra.in',
        role='buyer',
        phone='+91 99887 76655',
        state='Delhi NCR',
        district='South Delhi',
        village_or_city='Hauz Khas Market',
        avatar_icon='shopping-bag',
        verified=True,
        bio='Organic grocery retail founder and farm-to-table consumer collective manager.',
        rating=4.8
    )
    buyer_priya.set_password('buyer123')

    buyer_anand = User(
        name='Anand Wholesale Agro Traders',
        email_or_phone='trader@kisanmitra.in',
        role='buyer',
        phone='+91 97766 55443',
        state='Maharashtra',
        district='Mumbai',
        village_or_city='Vashi APMC Hub',
        avatar_icon='building',
        verified=True,
        bio='Bulk procurement partner for food processing companies and supermarket chains looking for direct farm contracts.',
        rating=4.7
    )
    buyer_anand.set_password('buyer123')

    db.session.add_all([farmer_ramesh, farmer_gurpreet, buyer_priya, buyer_anand])
    db.session.commit()

    # 2. Seed Government Schemes
    schemes_data = [
        {
            'title_en': 'PM-Kisan Samman Nidhi Yojana',
            'title_hi': 'प्रधानमंत्री किसान सम्मान निधि योजना',
            'category': 'financial_subsidy',
            'organizing_body': 'Department of Agriculture & Farmers Welfare, Central Govt',
            'description_en': 'Provides direct income support of ₹6,000 per year in 3 equal installments of ₹2,000 directly deposited into farmers bank accounts every 4 months to help meet agricultural input costs.',
            'description_hi': 'सभी भूमिधारक किसान परिवारों को कृषि और संबद्ध गतिविधियों के साथ-साथ घरेलू जरूरतों के लिए ₹6,000 प्रति वर्ष 3 समान किस्तों में सीधे बैंक खाते में आर्थिक सहायता।',
            'subsidy_amount_text': '₹6,000 / Year Direct in Bank Account',
            'max_benefit_amount': 6000.0,
            'subsidy_percentage': '100% Direct Cash Grant',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.1,
            'max_land_hectares': 50.0,
            'eligible_crops': 'All agricultural landholding farmers',
            'eligible_states': 'All States and Union Territories of India',
            'irrigation_required': 'any',
            'documents_required': [
                'Aadhaar Card linked with Mobile Number',
                'Land Ownership Document (Khatauni / Jamabandi / 7/12 extract)',
                'Bank Account Passbook (Aadhaar & NPCI linked)',
                'e-KYC verification confirmation'
            ],
            'application_steps': [
                'Visit official portal pmkisan.gov.in or nearest CSC / e-Mitra Center',
                'Click on "New Farmer Registration" and enter Aadhaar Number & Mobile OTP',
                'Fill State, District, Sub-District, Block, and Village details',
                'Enter Land Khata / Khasra number and upload verified land records',
                'Complete e-KYC using Aadhaar OTP or Biometrics to start receiving ₹2,000 installments'
            ],
            'official_url': 'https://pmkisan.gov.in',
            'helpline_number': '155261 / 011-24300606',
            'deadline_info': 'Continuous Enrollment (Open 365 Days)',
            'badge_color': 'emerald',
            'icon_name': 'wallet'
        },
        {
            'title_en': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
            'title_hi': 'प्रधानमंत्री फसल बीमा योजना (PMFBY)',
            'category': 'crop_insurance',
            'organizing_body': 'Ministry of Agriculture & Farmers Welfare',
            'description_en': 'Comprehensive crop insurance covering non-preventable natural risks like drought, flood, pests, unseasonal rain, and hailstorms with minimal premium (2% for Kharif, 1.5% for Rabi, 5% for commercial/horticulture).',
            'description_hi': 'सूखा, बाढ़, कीट प्रकोप, ओलावृष्टि व बेमौसम बारिश से फसल बर्बादी पर पूर्ण वित्तीय सुरक्षा। केवल 2% खरीफ और 1.5% रबी का नाममात्र प्रीमियम किसान द्वारा देय।',
            'subsidy_amount_text': 'Full Crop Loss Compensation at 1.5% - 2% Premium',
            'max_benefit_amount': 150000.0,
            'subsidy_percentage': 'Govt pays up to 90% of total premium',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.1,
            'max_land_hectares': 100.0,
            'eligible_crops': 'Food crops (Cereals, Millets, Pulses), Oilseeds, Annual Commercial / Horticultural crops',
            'eligible_states': 'Participating States across India',
            'irrigation_required': 'any',
            'documents_required': [
                'Land Possession Certificate (LPC) / Land Revenue Receipt',
                'Sowing Certificate / Crop Sowing Self-Declaration from Patwari/Kisan Sahayak',
                'Bank Account details with IFSC',
                'Aadhaar Card'
            ],
            'application_steps': [
                'Apply through pmfby.gov.in, local Bank branch, or Common Service Center (CSC)',
                'Register/Login and select the current cropping season (Kharif / Rabi)',
                'Enter Land details, survey number, and crop sown details',
                'Pay nominal premium online or via KCC bank account before cut-off date',
                'In case of localized disaster, report within 72 hours via Crop Insurance App to claim quick settlement'
            ],
            'official_url': 'https://pmfby.gov.in',
            'helpline_number': '14447 / 1800-180-1551',
            'deadline_info': 'Seasonal: Kharif (July 31) / Rabi (Dec 31)',
            'badge_color': 'blue',
            'icon_name': 'shield-check'
        },
        {
            'title_en': 'PM-KUSUM Solar Pump Scheme (Component B & C)',
            'title_hi': 'प्रधानमंत्री कुसुम योजना (सोलर कृषि पंप सब्सिडी)',
            'category': 'solar_energy',
            'organizing_body': 'Ministry of New and Renewable Energy (MNRE)',
            'description_en': 'Provides up to 60% to 90% capital subsidy on Standalone Solar Agricultural Pumps (3HP to 10HP) and solarisation of grid-connected agricultural pumps, freeing farmers from diesel costs and unreliable electricity.',
            'description_hi': '3HP से 10HP तक सोलर वाटर पंप लगाने पर 60% से 90% तक सरकारी सब्सिडी। बिजली बिल और महंगे डीजल से मुक्ति, दिन में सुनिश्चित सिंचाई और बची बिजली बेचकर अतिरिक्त कमाई।',
            'subsidy_amount_text': '60% to 90% Subsidy on Solar Pump Cost',
            'max_benefit_amount': 250000.0,
            'subsidy_percentage': '60% - 90% Subsidy',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.5,
            'max_land_hectares': 50.0,
            'eligible_crops': 'All crops needing irrigation (Wheat, Paddy, Sugarcane, Vegetables, Orchards)',
            'eligible_states': 'Pan-India',
            'irrigation_required': 'any',
            'documents_required': [
                'Aadhaar Card & Identity Proof',
                'Land Ownership Document / Khasra-Khatauni',
                'Source of Water Declaration (Borewell / Open Well / Canal connection)',
                'Electricity Connection Bill (for Component C solarisation)'
            ],
            'application_steps': [
                'Visit your State Renewable Energy Agency portal (e.g. UPNEDA, HAREDA, MEDA) or pmkusum.mnre.gov.in',
                'Register with Aadhaar and enter farm land location coordinates',
                'Select required Solar Pump Capacity (3HP, 5HP, 7.5HP, 10HP) and pump type (AC/DC Submersible/Surface)',
                'Pay farmer contribution (only 10% - 40% of total equipment cost)',
                'Authorized empaneled solar vendor installs system with 5-year comprehensive warranty'
            ],
            'official_url': 'https://pmkusum.mnre.gov.in',
            'helpline_number': '1800-180-3333',
            'deadline_info': 'State-wise Scheme Tranches Open Now',
            'badge_color': 'amber',
            'icon_name': 'sun'
        },
        {
            'title_en': 'Kisan Credit Card (KCC) & 4% Interest Subvention',
            'title_hi': 'किसान क्रेडिट कार्ड (KCC) रियायती कृषि ऋण',
            'category': 'credit_loan',
            'organizing_body': 'Reserve Bank of India & NABARD',
            'description_en': 'Short-term credit up to ₹3,00,000 for purchasing seeds, fertilizers, pesticides, diesel, and meeting harvest expenses at an effective interest rate of only 4% per annum upon prompt repayment.',
            'description_hi': 'खाद, बीज, कीटनाशक व कृषि खर्चों के लिए ₹3 लाख तक का आसान ऋण। समय पर चुकाने पर केवल 4% वार्षिक ब्याज। कोई गिरवी रखने की आवश्यकता नहीं (₹1.60 लाख तक)।',
            'subsidy_amount_text': 'Up to ₹3 Lakh Credit @ 4% Effective Interest',
            'max_benefit_amount': 300000.0,
            'subsidy_percentage': '3% Interest Subvention + 2% Prompt Repayment Incentive',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.1,
            'max_land_hectares': 50.0,
            'eligible_crops': 'Crops, Horticulture, Animal Husbandry, Dairy, Fisheries',
            'eligible_states': 'All Nationalized, Regional Rural & Cooperative Banks',
            'irrigation_required': 'any',
            'documents_required': [
                'Simplified 1-page KCC Application Form',
                'Land Record Copy certified by Revenue Officer',
                'Aadhaar Card and PAN Card',
                'No-Dues Certificate from nearby banks'
            ],
            'application_steps': [
                'Download 1-page KCC Form from bank website or visit nearest Bank Branch / CSC',
                'Fill crop pattern, acreage sown, and bank account number',
                'Submit along with land ownership copy',
                'Bank processes and issues RuPay Kisan Credit Card within 14 days',
                'Use RuPay KCC card to withdraw cash at ATMs or swipe at fertilizer and seed stores'
            ],
            'official_url': 'https://myscheme.gov.in/schemes/kcc',
            'helpline_number': '1800-180-1111',
            'deadline_info': 'Always Open (All Commercial Banks)',
            'badge_color': 'green',
            'icon_name': 'credit-card'
        },
        {
            'title_en': 'Sub-Mission on Agricultural Mechanization (SMAM)',
            'title_hi': 'कृषि यंत्रीकरण उप-मिशन (SMAM ट्रैक्टर व मशीन सब्सिडी)',
            'category': 'machinery_tools',
            'organizing_body': 'Mechanization & Technology Division, Ministry of Agriculture',
            'description_en': 'Provides 40% to 80% subsidy for purchasing farm equipment such as Tractors, Rotavators, Super Seeders, Combine Harvesters, Power Tillers, and setting up Custom Hiring Centers (CHC).',
            'description_hi': 'ट्रैक्टर, रोटावेटर, रीपर, सुपर सीडर, थ्रेशर जैसी आधुनिक कृषि मशीनों पर 50% से 80% तक की भारी सब्सिडी। छोटे व सीमांत किसानों और महिला किसानों को विशेष प्राथमिकता।',
            'subsidy_amount_text': '50% to 80% Subsidy on Agricultural Machinery',
            'max_benefit_amount': 500000.0,
            'subsidy_percentage': '50% - 80% Subsidy',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.1,
            'max_land_hectares': 50.0,
            'eligible_crops': 'All farming operations',
            'eligible_states': 'Pan-India',
            'irrigation_required': 'any',
            'documents_required': [
                'Aadhaar Card',
                'Land Record (Khatauni / 7-12 Extract)',
                'Bank Passbook Copy',
                'Quotation / Proforma Invoice from authorized farm equipment dealer',
                'Caste Certificate (if applying under SC/ST/OBC category for extra subsidy)'
            ],
            'application_steps': [
                'Register on portal agrimachinery.nic.in using Aadhaar and mobile number',
                'Select District, Block, and desired farm implement / machinery from the approved catalog',
                'Upload dealer proforma invoice and land documents',
                'Upon verification and lottery approval, purchase equipment from authorized manufacturer',
                'Physical verification conducted by Agriculture Officer and subsidy directly credited to bank account'
            ],
            'official_url': 'https://agrimachinery.nic.in',
            'helpline_number': '011-23382926',
            'deadline_info': 'Annual Target Allocations Active',
            'badge_color': 'purple',
            'icon_name': 'tool'
        },
        {
            'title_en': 'Paramparagat Krishi Vikas Yojana (PKVY - Organic Farming)',
            'title_hi': 'परंपरागत कृषि विकास योजना (जैविक खेती सहायता)',
            'category': 'organic_farming',
            'organizing_body': 'National Project on Organic Farming (NPOF)',
            'description_en': 'Provides ₹50,000 per hectare financial assistance over 3 years for cluster-based organic farming, PGS certification, organic inputs (neem cake, vermicompost, bio-fertilizers), and direct market branding.',
            'description_hi': 'जैविक खेती अपनाने वाले किसान समूहों को ₹50,000 प्रति हेक्टेयर (3 वर्ष में) सहायता। जैविक खाद, केंचुआ खाद, जैविक कीटनाशक व निःशुल्क प्रमाणीकरण एवं ब्रांडिंग सहायता।',
            'subsidy_amount_text': '₹50,000 / Hectare for Organic Cultivation & Certification',
            'max_benefit_amount': 50000.0,
            'subsidy_percentage': '100% Grant Support for Cluster Formation & Inputs',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.2,
            'max_land_hectares': 20.0,
            'eligible_crops': 'Grains, Spices, Vegetables, Medicinal Plants, Pulses, Fruits',
            'eligible_states': 'All Indian States and UTs',
            'irrigation_required': 'any',
            'documents_required': [
                'Aadhaar Card',
                'Land Record Verification',
                'Farmer Group / Self Help Group membership or individual cluster declaration',
                'Bank Account details'
            ],
            'application_steps': [
                'Form or join a Farmer Interest Group (FIG) of 20-50 farmers with minimum 20-50 hectares',
                'Contact District Agriculture Officer / KVK or apply on pgsorganic-india.gov.in',
                'Receive training and ₹31,000 direct bank transfer per hectare for on-farm organic inputs',
                'Obtain PGS-India Organic Certification after conversion period',
                'Sell certified organic produce at 20-40% premium prices directly on KisanMitra marketplace'
            ],
            'official_url': 'https://pgsorganic-india.gov.in',
            'helpline_number': '0120-2460645',
            'deadline_info': 'Continuous Cluster Onboarding',
            'badge_color': 'emerald',
            'icon_name': 'leaf'
        },
        {
            'title_en': 'Pradhan Mantri Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop)',
            'title_hi': 'प्रधानमंत्री कृषि सिंचाई योजना (ड्रिप एवं स्प्रिंकलर सूक्ष्म सिंचाई)',
            'category': 'irrigation',
            'organizing_body': 'Department of Agriculture and Farmers Welfare',
            'description_en': 'Provides 45% to 55% financial subsidy on installing Micro Irrigation systems (Drip Irrigation and Sprinkler Irrigation), saving up to 50% water and increasing crop yield by 20-40%.',
            'description_hi': 'ड्रिप एवं स्प्रिंकलर सिंचाई सिस्टम लगाने पर 45% से 55% तक सब्सिडी। 50% तक पानी की बचत, उर्वरक दक्षता में वृद्धि और फसल उत्पादन में 30% से 40% की बढ़ोतरी।',
            'subsidy_amount_text': '45% to 55% Subsidy on Drip & Sprinkler Systems',
            'max_benefit_amount': 85000.0,
            'subsidy_percentage': '55% for Small/Marginal Farmers, 45% for Others',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.2,
            'max_land_hectares': 15.0,
            'eligible_crops': 'Sugarcane, Cotton, Banana, Vegetables, Orchards, Pulses, Wheat',
            'eligible_states': 'All States in India',
            'irrigation_required': 'any',
            'documents_required': [
                'Land Khatauni / 7-12 Extract',
                'Aadhaar Card & Passport Photo',
                'Bank Account Details',
                'Water Source proof (Tubewell, Well, River, Farm Pond)'
            ],
            'application_steps': [
                'Register on State Horticulture / Agriculture Micro Irrigation Portal (e.g., upagriculture.com / mahadbt)',
                'Select empaneled micro-irrigation manufacturer (Jain Irrigation, Netafim, EPC, etc.)',
                'Technical engineer visits field to measure land and prepare customized layout plan',
                'Pay farmer share of quotation (after deducting subsidy)',
                'System installed and tested; subsidy settled directly'
            ],
            'official_url': 'https://pmksy.gov.in',
            'helpline_number': '1800-180-1551',
            'deadline_info': 'Open throughout Financial Year',
            'badge_color': 'cyan',
            'icon_name': 'droplet'
        },
        {
            'title_en': 'Soil Health Card Scheme',
            'title_hi': 'मृदा स्वास्थ्य कार्ड योजना (मुफ्त मिट्टी परीक्षण)',
            'category': 'financial_subsidy',
            'organizing_body': 'Ministry of Agriculture and Farmers Welfare',
            'description_en': 'Provides free comprehensive testing of 12 soil chemical and nutrient parameters (N, P, K, pH, Zinc, Boron, Organic Carbon, etc.) with customized fertilizer dose recommendations every 2 years.',
            'description_hi': 'खेत की मिट्टी का 12 प्रमुख पोषक तत्वों पर मुफ्त वैज्ञानिक परीक्षण। फसलवार संतुलित खाद व उर्वरक उपयोग की सटीक सिफारिश जिससे खाद का अनावश्यक खर्च बचता है।',
            'subsidy_amount_text': '100% Free Soil Nutrient Testing & Advisory Card',
            'max_benefit_amount': 2000.0,
            'subsidy_percentage': '100% Free Government Service',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.1,
            'max_land_hectares': 100.0,
            'eligible_crops': 'All field crops and horticultural plantations',
            'eligible_states': 'Pan-India',
            'irrigation_required': 'any',
            'documents_required': [
                'Aadhaar Card',
                'Land details and Survey/Khasra number',
                'Mobile number for SMS advisory'
            ],
            'application_steps': [
                'Contact Village Agricultural Assistant or visit nearest Soil Testing Lab / KVK',
                'Soil sample collected from your field (composite 8-10 spots at 15cm depth)',
                'Lab tests Nitrogen, Phosphorus, Potassium, micronutrients and organic carbon',
                'Soil Health Card printed and delivered with personalized crop-wise fertilizer dosage guide'
            ],
            'official_url': 'https://soilhealth.dac.gov.in',
            'helpline_number': '1800-180-1551',
            'deadline_info': 'Bi-annual Cycle Active',
            'badge_color': 'amber',
            'icon_name': 'clipboard-check'
        },
        {
            'title_en': 'Kisan Drone Subsidy Scheme (SMAM Extension)',
            'title_hi': 'किसान ड्रोन योजना (कीटनाशक व नैनो यूरिया छिड़काव ड्रोन)',
            'category': 'machinery_tools',
            'organizing_body': 'ICAR & Department of Agriculture',
            'description_en': 'Provides up to 50% subsidy (up to ₹5,00,000) for purchase of agricultural drones for precision spraying of fertilizers, micronutrients, pesticides, and crop health monitoring.',
            'description_hi': 'नैनो यूरिया व कीटनाशकों के सुरक्षित व त्वरित छिड़काव के लिए कृषि ड्रोन खरीद पर ₹5 लाख तक (50%) सब्सिडी। FPO और कस्टम हायरिंग सेंटरों को 75% तक अनुदान।',
            'subsidy_amount_text': '50% Subsidy (up to ₹5 Lakh) on Agri-Drones',
            'max_benefit_amount': 500000.0,
            'subsidy_percentage': '50% for Individual Farmers, 75% for FPOs',
            'eligible_land_type': 'medium',
            'min_land_hectares': 1.0,
            'max_land_hectares': 100.0,
            'eligible_crops': 'Paddy, Wheat, Cotton, Sugarcane, Maize, Orchards',
            'eligible_states': 'All States & UTs',
            'irrigation_required': 'any',
            'documents_required': [
                'Aadhaar Card',
                'DGCA certified Drone Pilot Training Certificate (or tie-up)',
                'Land records and FPO / Farmer ID',
                'Quotation from DGCA approved Type-Certified Drone Manufacturer'
            ],
            'application_steps': [
                'Apply through state agricultural mechanization DBT portal',
                'Complete mandatory DGCA Remote Pilot License training at recognized RPTO',
                'Select approved Agri Drone model (Garuda, IoTechWorld, Marut, etc.)',
                'Submit bank guarantee/share and receive subsidy disbursement upon verification'
            ],
            'official_url': 'https://agrimachinery.nic.in',
            'helpline_number': '011-23381012',
            'deadline_info': 'Active Financial Year Allocations',
            'badge_color': 'indigo',
            'icon_name': 'crosshair'
        },
        {
            'title_en': 'National Beekeeping & Honey Mission (NBHM)',
            'title_hi': 'राष्ट्रीय मधुमक्खी पालन एवं शहद मिशन (मीठी क्रांति)',
            'category': 'organic_farming',
            'organizing_body': 'National Bee Board (NBB)',
            'description_en': 'Provides up to 80% to 85% financial assistance for setting up Beehives, Honey Extraction units, Queen Bee rearing facilities, and customized migration gear to boost farmer supplementary income and improve crop pollination.',
            'description_hi': 'मधुमक्खी के बक्से, कालोनियां, शहद निष्कर्षण उपकरण खरीदने पर 80% से 85% तक अनुदान। फसलों के परागण से उपज में 25% वृद्धि और शुद्ध शहद बेचकर ₹1-3 लाख अतिरिक्त आय।',
            'subsidy_amount_text': '80% - 85% Subsidy on Beehives & Equipment',
            'max_benefit_amount': 120000.0,
            'subsidy_percentage': '80% - 85% Capital Subsidy',
            'eligible_land_type': 'all',
            'min_land_hectares': 0.0,
            'max_land_hectares': 50.0,
            'eligible_crops': 'Mustard, Sunflower, Litchi, Apple, Coriander, Eucalyptus plantations',
            'eligible_states': 'Pan-India (Major in UP, Bihar, Punjab, WB, Kashmir)',
            'irrigation_required': 'any',
            'documents_required': [
                'Aadhaar Card',
                'Proof of beekeeping training / willing declaration for 5-day training',
                'Bank Account Details'
            ],
            'application_steps': [
                'Register on Madhukranti portal (madhukranti.in) or National Bee Board',
                'Submit application for Bee Colony & Wooden Box unit (Set of 10 to 50 boxes)',
                'Receive sanctioned subsidy and get trained at nearest KVK',
                'Harvest raw honey and sell directly to consumers on KisanMitra'
            ],
            'official_url': 'https://nbb.gov.in',
            'helpline_number': '011-23382717',
            'deadline_info': 'Rolling Allocations',
            'badge_color': 'amber',
            'icon_name': 'hexagon'
        }
    ]

    for s_info in schemes_data:
        scheme_obj = Scheme(
            title_en=s_info['title_en'],
            title_hi=s_info['title_hi'],
            category=s_info['category'],
            organizing_body=s_info['organizing_body'],
            description_en=s_info['description_en'],
            description_hi=s_info['description_hi'],
            subsidy_amount_text=s_info['subsidy_amount_text'],
            max_benefit_amount=s_info['max_benefit_amount'],
            subsidy_percentage=s_info['subsidy_percentage'],
            eligible_land_type=s_info['eligible_land_type'],
            min_land_hectares=s_info['min_land_hectares'],
            max_land_hectares=s_info['max_land_hectares'],
            eligible_crops=s_info['eligible_crops'],
            eligible_states=s_info['eligible_states'],
            irrigation_required=s_info['irrigation_required'],
            documents_required=json.dumps(s_info['documents_required']),
            application_steps=json.dumps(s_info['application_steps']),
            official_url=s_info['official_url'],
            helpline_number=s_info['helpline_number'],
            deadline_info=s_info['deadline_info'],
            badge_color=s_info['badge_color'],
            icon_name=s_info['icon_name']
        )
        db.session.add(scheme_obj)

    # 3. Seed Produce Listings (Direct from Farmers)
    produce_list = [
        {
            'farmer_id': farmer_ramesh.id,
            'crop_name': 'Traditional 1121 Basmati Paddy Rice',
            'hindi_name': '1121 बासमती धान / चावल',
            'category': 'Grains',
            'variety': 'Pusa Basmati 1121 Long Grain',
            'quantity': 45.0,
            'unit': 'Quintal',
            'price_per_unit': 3850.0,
            'mandi_benchmark_price': 3200.0,
            'expected_harvest_date': 'Ready in Stock (Fresh Milled)',
            'state': 'Uttar Pradesh',
            'district': 'Varanasi',
            'location_text': 'Rajatalab Mandi Road, Varanasi',
            'organic_certified': True,
            'description': 'Aromatic, extra-long grain Pusa 1121 Basmati paddy. Cultivated with natural compost and neem-oil pest management. Zero chemical residue.',
            'image_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80',
            'status': 'available',
            'views': 124
        },
        {
            'farmer_id': farmer_gurpreet.id,
            'crop_name': 'Organic Sharbati Golden Wheat',
            'hindi_name': 'जैविक शरबती प्रीमियम गेहूं',
            'category': 'Grains',
            'variety': 'C-306 Sharbati Premium',
            'quantity': 120.0,
            'unit': 'Quintal',
            'price_per_unit': 2750.0,
            'mandi_benchmark_price': 2350.0,
            'expected_harvest_date': 'Freshly Harvested & Cleaned',
            'state': 'Punjab',
            'district': 'Ludhiana',
            'location_text': 'Samrala Tehsil, Ludhiana',
            'organic_certified': True,
            'description': 'Authentic golden-grain Sharbati wheat known for making the softest rotis. Grown using zero synthetic pesticides and certified by PGS-India.',
            'image_url': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=600&q=80',
            'status': 'available',
            'views': 210
        },
        {
            'farmer_id': farmer_ramesh.id,
            'crop_name': 'Fresh Red Onions (Nashik Quality)',
            'hindi_name': 'ताजा लाल प्याज (उत्कृष्ट गुणवत्ता)',
            'category': 'Vegetables',
            'variety': 'Garwa High Shelf-Life',
            'quantity': 60.0,
            'unit': 'Quintal',
            'price_per_unit': 2200.0,
            'mandi_benchmark_price': 1750.0,
            'expected_harvest_date': 'Freshly Dug - Sun Cured',
            'state': 'Uttar Pradesh',
            'district': 'Varanasi',
            'location_text': 'Kashi Rural Belt',
            'organic_certified': False,
            'description': 'Medium to large size crisp red onions with excellent 4-month storage life. Direct farm gate loading available for buyers and retail stores.',
            'image_url': 'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?auto=format&fit=crop&w=600&q=80',
            'status': 'available',
            'views': 89
        },
        {
            'farmer_id': farmer_gurpreet.id,
            'crop_name': 'Yellow Mustard Seeds (Sarson)',
            'hindi_name': 'पीली सरसों (उच्च तेल मात्रा)',
            'category': 'Oilseeds',
            'variety': 'Pusa Mustard-30',
            'quantity': 30.0,
            'unit': 'Quintal',
            'price_per_unit': 5400.0,
            'mandi_benchmark_price': 4800.0,
            'expected_harvest_date': 'Sun Dried & Machine Graded',
            'state': 'Punjab',
            'district': 'Ludhiana',
            'location_text': 'Khanna Agro Belt, Punjab',
            'organic_certified': True,
            'description': 'High oil content (42%+) yellow mustard seeds, ideal for cold-press virgin mustard oil extraction and organic spice manufacturing.',
            'image_url': 'https://images.unsplash.com/photo-1508873696983-2df5703bc20d?auto=format&fit=crop&w=600&q=80',
            'status': 'available',
            'views': 156
        },
        {
            'farmer_id': farmer_ramesh.id,
            'crop_name': 'Farm Fresh Vine-Ripened Tomatoes',
            'hindi_name': 'खेत के ताजा लाल टमाटर',
            'category': 'Vegetables',
            'variety': 'Abhinav Hybrid F1',
            'quantity': 1500.0,
            'unit': 'kg',
            'price_per_unit': 28.0,
            'mandi_benchmark_price': 18.0,
            'expected_harvest_date': 'Daily Fresh Plucking',
            'state': 'Uttar Pradesh',
            'district': 'Varanasi',
            'location_text': 'Chandauli Border, Varanasi',
            'organic_certified': False,
            'description': 'Solid, juicy, bright red tomatoes with thick skin for transport durability. Ideal for supermarkets, restaurants, and wholesale bulk buyers.',
            'image_url': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=600&q=80',
            'status': 'available',
            'views': 95
        },
        {
            'farmer_id': farmer_gurpreet.id,
            'crop_name': 'Pure Raw Multi-Flora Forest Honey',
            'hindi_name': 'शुद्ध कच्चा वन शहद (बिना मिलावट)',
            'category': 'Organic Special',
            'variety': 'Mustard & Acacia Blossom',
            'quantity': 350.0,
            'unit': 'kg',
            'price_per_unit': 420.0,
            'mandi_benchmark_price': 260.0,
            'expected_harvest_date': 'Unheated & Raw Filtered',
            'state': 'Punjab',
            'district': 'Ludhiana',
            'location_text': 'Bee Farm, Samrala',
            'organic_certified': True,
            'description': '100% natural, raw, unprocessed bee honey harvested directly from our apiary boxes. Rich in active enzymes and natural pollen.',
            'image_url': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=600&q=80',
            'status': 'available',
            'views': 312
        }
    ]

    for p_info in produce_list:
        p_obj = Produce(**p_info)
        db.session.add(p_obj)

    # 4. Seed Mandi Prices
    mandi_data = [
        {
            'crop_name': 'Wheat (गेहूं)',
            'hindi_name': 'गेहूं',
            'category': 'Grains',
            'market_name': 'Khanna APMC Mandi',
            'district': 'Ludhiana',
            'state': 'Punjab',
            'min_price': 2275.0,
            'max_price': 2550.0,
            'modal_price': 2425.0,
            'unit': '₹/Quintal',
            'change_trend': 'up',
            'change_percent': +1.8,
            'historical_prices_json': json.dumps([
                {'date': 'Day -6', 'price': 2380},
                {'date': 'Day -5', 'price': 2390},
                {'date': 'Day -4', 'price': 2400},
                {'date': 'Day -3', 'price': 2410},
                {'date': 'Day -2', 'price': 2415},
                {'date': 'Day -1', 'price': 2420},
                {'date': 'Today', 'price': 2425}
            ]),
            'updated_date': 'Today Live'
        },
        {
            'crop_name': 'Basmati Paddy (बासमती धान)',
            'hindi_name': 'बासमती धान',
            'category': 'Grains',
            'market_name': 'Karnal Grain Mandi',
            'district': 'Karnal',
            'state': 'Haryana',
            'min_price': 3400.0,
            'max_price': 4100.0,
            'modal_price': 3850.0,
            'unit': '₹/Quintal',
            'change_trend': 'up',
            'change_percent': +3.2,
            'historical_prices_json': json.dumps([
                {'date': 'Day -6', 'price': 3650},
                {'date': 'Day -5', 'price': 3700},
                {'date': 'Day -4', 'price': 3720},
                {'date': 'Day -3', 'price': 3780},
                {'date': 'Day -2', 'price': 3810},
                {'date': 'Day -1', 'price': 3830},
                {'date': 'Today', 'price': 3850}
            ]),
            'updated_date': 'Today Live'
        },
        {
            'crop_name': 'Red Onion (लाल प्याज)',
            'hindi_name': 'प्याज',
            'category': 'Vegetables',
            'market_name': 'Lasalgaon Mandi',
            'district': 'Nashik',
            'state': 'Maharashtra',
            'min_price': 1600.0,
            'max_price': 2350.0,
            'modal_price': 1950.0,
            'unit': '₹/Quintal',
            'change_trend': 'down',
            'change_percent': -2.1,
            'historical_prices_json': json.dumps([
                {'date': 'Day -6', 'price': 2100},
                {'date': 'Day -5', 'price': 2080},
                {'date': 'Day -4', 'price': 2040},
                {'date': 'Day -3', 'price': 2000},
                {'date': 'Day -2', 'price': 1980},
                {'date': 'Day -1', 'price': 1960},
                {'date': 'Today', 'price': 1950}
            ]),
            'updated_date': 'Today Live'
        },
        {
            'crop_name': 'Mustard Seed (सरसों)',
            'hindi_name': 'सरसों',
            'category': 'Oilseeds',
            'market_name': 'Alwar Mandi',
            'district': 'Alwar',
            'state': 'Rajasthan',
            'min_price': 5100.0,
            'max_price': 5650.0,
            'modal_price': 5380.0,
            'unit': '₹/Quintal',
            'change_trend': 'up',
            'change_percent': +1.5,
            'historical_prices_json': json.dumps([
                {'date': 'Day -6', 'price': 5250},
                {'date': 'Day -5', 'price': 5280},
                {'date': 'Day -4', 'price': 5310},
                {'date': 'Day -3', 'price': 5330},
                {'date': 'Day -2', 'price': 5350},
                {'date': 'Day -1', 'price': 5370},
                {'date': 'Today', 'price': 5380}
            ]),
            'updated_date': 'Today Live'
        },
        {
            'crop_name': 'Cotton (कपास)',
            'hindi_name': 'कपास',
            'category': 'Commercial',
            'market_name': 'Rajkot APMC',
            'district': 'Rajkot',
            'state': 'Gujarat',
            'min_price': 6800.0,
            'max_price': 7600.0,
            'modal_price': 7250.0,
            'unit': '₹/Quintal',
            'change_trend': 'stable',
            'change_percent': 0.0,
            'historical_prices_json': json.dumps([
                {'date': 'Day -6', 'price': 7200},
                {'date': 'Day -5', 'price': 7220},
                {'date': 'Day -4', 'price': 7250},
                {'date': 'Day -3', 'price': 7240},
                {'date': 'Day -2', 'price': 7250},
                {'date': 'Day -1', 'price': 7250},
                {'date': 'Today', 'price': 7250}
            ]),
            'updated_date': 'Today Live'
        }
    ]

    for m_info in mandi_data:
        m_obj = MandiPrice(**m_info)
        db.session.add(m_obj)

    # 5. Seed Crop Advisory
    advisories = [
        {
            'crop_name': 'Paddy / Rice (धान)',
            'hindi_name': 'धान की फसल',
            'season': 'Kharif',
            'soil_type': 'Clayey or clay loam with high water holding capacity',
            'sowing_window': 'May 20 - June 25 (Nursery), July (Transplanting)',
            'harvesting_window': 'October - November',
            'watering_tips': 'Maintain 3-5 cm standing water during tillering and flowering stage. Drain field 10 days prior to harvesting.',
            'pest_control_tips': 'For Stem Borer / Brown Plant Hopper: Spray Cartap Hydrochloride 50 SP @ 2g/liter or use Neem oil 1500 ppm for organic plots.',
            'fertilizer_tips': 'Apply recommended N:P:K 120:60:40 kg/ha. Apply Zinc Sulphate (25 kg/ha) at basal stage to prevent Khaira disease.',
            'weather_alert': 'Monsoon showers favorable this week. Ensure proper drainage channels in low-lying plots to avoid root rot.',
            'badge': 'Active Kharif Season'
        },
        {
            'crop_name': 'Wheat (गेहूं)',
            'hindi_name': 'गेहूं की फसल',
            'season': 'Rabi',
            'soil_type': 'Well-drained fertile loamy soil',
            'sowing_window': 'November 01 - November 25 (Optimum)',
            'harvesting_window': 'March - April',
            'watering_tips': 'Crucial irrigations at: (1) Crown Root Initiation (21 days after sowing), (2) Tillering, (3) Flowering, (4) Grain filling.',
            'pest_control_tips': 'Watch for Yellow Rust on leaves. Spray Propiconazole 25 EC (Tilt) @ 1 ml/L upon early detection.',
            'fertilizer_tips': 'Use DAP (50 kg/acre) + MOP (20 kg/acre) as basal dose. Top-dress with Urea in 2 splits after 1st and 2nd watering.',
            'weather_alert': 'Cool nights promote tillering. Ensure seed treatment with Trichoderma viride before sowing.',
            'badge': 'Upcoming Rabi Planning'
        },
        {
            'crop_name': 'Mustard (सरसों)',
            'hindi_name': 'सरसों की खेती',
            'season': 'Rabi',
            'soil_type': 'Light to heavy loamy soils with pH 6.0 - 7.5',
            'sowing_window': 'October 01 - October 20',
            'harvesting_window': 'February - March',
            'watering_tips': 'Requires 2 irrigations: 1st at 30-35 DAS (flowering initiation) and 2nd at 60-65 DAS (pod development).',
            'pest_control_tips': 'For Aphid (चेपा) attack: Spray Dimethoate 30 EC or bio-pesticide Verticillium lecanii @ 5g/L.',
            'fertilizer_tips': 'Mustard is highly responsive to Sulphur. Apply Elemental Sulphur @ 20 kg/ha or Gypsum 100 kg/ha for 15% higher oil content.',
            'weather_alert': 'Avoid excessive humidity during flowering to prevent White Rust.',
            'badge': 'High Profit Crop'
        }
    ]

    for adv_info in advisories:
        adv_obj = CropAdvisory(**adv_info)
        db.session.add(adv_obj)

    db.session.commit()
    print("Database seeding successfully completed!")
