// KisanMitra (किसान मित्र) - Core Frontend Controller

let currentUser = null;
let currentLanguage = 'en';
let allSchemes = [];
let allProduce = [];
let mandiPrices = [];
let mandiChartInstance = null;
let activeCategory = 'all';
let activeSchemeCategory = 'all';
let searchTimeout = null;
let isSpeaking = false;
let currentSpeechUtterance = null;
let deferredPWAInstallPrompt = null;

// Multilingual Dictionary with 13 Supported Languages
const translations = {
    en: {
        announcement: "Direct Farmer-to-Buyer Platform • 0% Middlemen Commission • 100% Farmer Profit",
        tagline: "Empowering Farmers & Direct Consumers",
        nav_schemes: "Govt Schemes",
        nav_marketplace: "Direct Market",
        nav_mandi: "Live Mandi Rates",
        nav_advisory: "Weather & Advisory",
        nav_deals: "My Deals",
        role_farmer: "Farmer View",
        role_buyer: "Buyer View",
        hero_badge: "Zero Brokerage • Direct Farm Gate Procurement",
        hero_title_1: "Connecting Our",
        hero_title_2: "Kisan Brothers",
        hero_title_3: "Directly With Buyers",
        hero_subtitle: "Eliminating intermediaries ensures our farmer brothers get 20% to 30% higher income, while consumers and buyers enjoy 100% farm-fresh authentic harvest at fair wholesale prices.",
        btn_list_harvest: "+ List Your Crop (नई फसल बेचें)",
        btn_check_subsidies: "Find Govt Subsidies",
        schemes_badge: "Central & State Govt Schemes Directory",
        schemes_title: "Government Subsidies & Benefits for Farmers",
        schemes_subtitle: "Discover 100% verified government grants, solar pump 90% subsidies, ₹6,000 PM-Kisan financial transfers, crop insurance, and tractor mechanization schemes.",
        btn_check_eligibility: "Check Your Eligibility (पात्रता जांचें)",
        eligibility_header: "Smart Scheme Eligibility Matcher",
        eligibility_sub: "Enter your farm details to instantly get tailored subsidies and grants you can claim today.",
        label_land_size: "Land Holding (Hectares / Acres)",
        label_state: "Your State (राज्य)",
        label_crop_type: "Primary Crops Grown",
        label_irrigation: "Water Source & Practices",
        btn_find_matching: "Find Matched Schemes",
        mandi_title: "Live Mandi Market Rates & Trends",
        mandi_sub: "Compare today's mandi modal prices before setting your direct farm sale price. Stay informed on price spikes and harvest demand.",
        mandi_board_header: "Today's State-wise Mandi Rates",
        modal_sell_title: "🌾 List Your Crop for Direct Buyers"
    },
    hi: {
        announcement: "किसान-उपभोक्ता सीधा मंच • 0% दलाली • 100% किसान का मुनाफा",
        tagline: "हमारे किसान भाइयों और उपभोक्ताओं का सीधा सेतु",
        nav_schemes: "सरकारी योजनाएं",
        nav_marketplace: "सीधा बाज़ार",
        nav_mandi: "लाइव मंडी भाव",
        nav_advisory: "मौसम व सलाह",
        nav_deals: "मेरे सौदे (Deals)",
        role_farmer: "किसान दृश्य",
        role_buyer: "खरीदार दृश्य",
        hero_badge: "शून्य दलाली • सीधे खेत से खरीदारी",
        hero_title_1: "हमारे",
        hero_title_2: "किसान भाइयों",
        hero_title_3: "को सीधे खरीदारों से जोड़ना",
        hero_subtitle: "बिचौलियों को हटाकर किसान भाइयों को 20% से 30% अधिक आय मिलती है, और उपभोक्ताओं को उचित दर पर ताज़ी शुद्ध फसल मिलती है।",
        btn_list_harvest: "+ अपनी नई फसल बेचें",
        btn_check_subsidies: "सरकारी सब्सिडी देखें",
        schemes_badge: "केंद्रीय एवं राज्य सरकारी योजनाएं",
        schemes_title: "किसानों के लिए सरकारी सब्सिडी व अनुदान",
        schemes_subtitle: "पीएम-किसान ₹6,000, 90% सोलर पंप सब्सिडी, फसल बीमा और ट्रैक्टर यंत्रीकरण योजनाओं की संपूर्ण जानकारी।",
        btn_check_eligibility: "अपनी पात्रता जांचें",
        eligibility_header: "स्मार्ट योजना पात्रता कैलकुलेटर",
        eligibility_sub: "अपने खेत का विवरण दर्ज करें और जानें कि आप किन-किन सरकारी योजनाओं के पात्र हैं।",
        label_land_size: "भूमि का रकबा (हेक्टेयर / एकड़)",
        label_state: "आपका राज्य",
        label_crop_type: "मुख्य बोई जाने वाली फसलें",
        label_irrigation: "सिंचाई साधन एवं पद्धति",
        btn_find_matching: "पात्र योजनाएं खोजें",
        mandi_title: "लाइव मंडी बाजार भाव और रुझान",
        mandi_sub: "अपनी फसल बेचने से पहले आज के मंडी भाव की तुलना करें और सही दाम तय करें।",
        mandi_board_header: "आज के राज्यवार मंडी भाव",
        modal_sell_title: "🌾 सीधी बिक्री के लिए अपनी फसल जोड़ें"
    },
    pa: {
        announcement: "ਕਿਸਾਨ-ਗਾਹਕ ਸਿੱਧਾ ਪਲੇਟਫਾਰਮ • 0% ਦਲਾਲੀ • ਕਿਸਾਨਾਂ ਦਾ ਪੂਰਾ ਮੁਨਾਫਾ",
        tagline: "ਕਿਸਾਨ ਭਰਾਵਾਂ ਅਤੇ ਖਪਤਕਾਰਾਂ ਦਾ ਸਿੱਧਾ ਮੰਚ",
        nav_schemes: "ਸਰਕਾਰੀ ਸਕੀਮਾਂ",
        nav_marketplace: "ਸਿੱਧੀ ਮੰਡੀ",
        nav_mandi: "ਮੰਡੀ ਦੇ ਭਾਅ",
        nav_advisory: "ਮੌਸਮ ਤੇ ਸਲਾਹ",
        nav_deals: "ਮੇਰੇ ਸੌਦੇ",
        role_farmer: "ਕਿਸਾਨ ਮੋਡ",
        role_buyer: "ਖਰੀਦਦਾਰ ਮੋਡ",
        hero_badge: "ਜ਼ੀਰੋ ਕਮਿਸ਼ਨ • ਸਿੱਧਾ ਖੇਤ ਵਿੱਚੋਂ ਖਰੀਦੋ",
        hero_title_1: "ਸਾਡੇ",
        hero_title_2: "ਕਿਸਾਨ ਭਰਾਵਾਂ",
        hero_title_3: "ਨੂੰ ਸਿੱਧਾ ਖਰੀਦਦਾਰਾਂ ਨਾਲ ਜੋੜਨਾ",
        hero_subtitle: "ਵਿਚੋਲਿਆਂ ਨੂੰ ਹਟਾ ਕੇ ਕਿਸਾਨਾਂ ਨੂੰ 20-30% ਵੱਧ ਮੁਨਾਫਾ ਅਤੇ ਖਰੀਦਦਾਰਾਂ ਨੂੰ ਤਾਜ਼ੀ ਫਸਲ ਮਿਲਦੀ ਹੈ।",
        btn_list_harvest: "+ ਨਵੀਂ ਫਸਲ ਵੇਚੋ",
        btn_check_subsidies: "ਸਰਕਾਰੀ ਸਬਸਿਡੀਆਂ",
        schemes_badge: "ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਦੀ ਡਾਇਰੈਕਟਰੀ",
        schemes_title: "ਕਿਸਾਨਾਂ ਲਈ ਸਰਕਾਰੀ ਸਬਸਿਡੀਆਂ ਅਤੇ ਲਾਭ",
        schemes_subtitle: "ਪੀਐਮ-ਕਿਸਾਨ, ਸੋਲਰ ਪੰਪ, ਫਸਲ ਬੀਮਾ ਅਤੇ ਟਰੈਕਟਰ ਸਬਸਿਡੀ ਦੀ ਪੂਰੀ ਜਾਣਕਾਰੀ।",
        btn_check_eligibility: "ਯੋਗਤਾ ਚੈੱਕ ਕਰੋ",
        eligibility_header: "ਸਮਾਰਟ ਸਕੀਮ ਯੋਗਤਾ ਕੈਲਕੁਲੇਟਰ",
        eligibility_sub: "ਆਪਣੇ ਖੇਤ ਦੀ ਜਾਣਕਾਰੀ ਦਰਜ ਕਰੋ ਅਤੇ ਤੁਰੰਤ ਸਬਸਿਡੀਆਂ ਲੱਭੋ।",
        label_land_size: "ਜ਼ਮੀਨ ਦਾ ਰਕਬਾ (ਏਕੜ)",
        label_state: "ਤੁਹਾਡਾ ਸੂਬਾ",
        label_crop_type: "ਮੁੱਖ ਫਸਲ",
        label_irrigation: "ਸਿੰਚਾਈ ਸਾਧਨ",
        btn_find_matching: "ਸਕੀਮਾਂ ਲੱਭੋ",
        mandi_title: "ਲਾਈਵ ਮੰਡੀ ਭਾਅ ਅਤੇ ਰੁਝਾਨ",
        mandi_sub: "ਅੱਜ ਦੇ ਮੰਡੀ ਰੇਟਾਂ ਦੀ ਤੁਲਨਾ ਕਰੋ।",
        mandi_board_header: "ਅੱਜ ਦੇ ਮੰਡੀ ਭਾਅ",
        modal_sell_title: "🌾 ਸਿੱਧੀ ਵਿਕਰੀ ਲਈ ਫਸਲ ਦਰਜ ਕਰੋ"
    },
    mr: {
        announcement: "शेतकरी-ग्राहक थेट बाजार • 0% मध्यस्थ दलाली • 100% शेतकऱ्यांचा नफा",
        tagline: "शेतकरी बांधव आणि थेट ग्राहकांचे हक्काचे व्यासपीठ",
        nav_schemes: "शासकीय योजना",
        nav_marketplace: "थेट बाजारपेठ",
        nav_mandi: "बाजारभाव (मंडी)",
        nav_advisory: "हवामान व सल्ला",
        nav_deals: "माझे सौदे",
        role_farmer: "शेतकरी दृश्य",
        role_buyer: "ग्राहक दृश्य",
        hero_badge: "शून्य दलाली • थेट बांधावरून खरेदी",
        hero_title_1: "आमच्या",
        hero_title_2: "शेतकरी बांधवांना",
        hero_title_3: "थेट ग्राहकांशी जोडणारे",
        hero_subtitle: "दलालांना दूर करून शेतकऱ्यांना 20-30% अधिक नफा आणि ग्राहकांना ताजा शेतमाल वाजवी दरात मिळतो.",
        btn_list_harvest: "+ शेतमाल विक्रीसाठी जोडा",
        btn_check_subsidies: "शासकीय सबसिडी शोधा",
        schemes_badge: "शासकीय कृषी योजना",
        schemes_title: "शेतकऱ्यांसाठी सरकारी योजना व अनुदान",
        schemes_subtitle: "पीएम किसान, कुसुम सोलर पंप, पीक विमा व कृषी यांत्रिकीकरण योजना.",
        btn_check_eligibility: "पात्रता तपासा",
        eligibility_header: "स्मार्ट योजना पात्रता शोध",
        eligibility_sub: "तुमच्या जमिनीची माहिती भरा आणि पात्र सरकारी योजना शोधा.",
        label_land_size: "जमीन क्षेत्र (हेक्टर/एकर)",
        label_state: "राज्य",
        label_crop_type: "पिके",
        label_irrigation: "सिंचन प्रकार",
        btn_find_matching: "योजना शोधा",
        mandi_title: "थेट कृषी उत्पन्न बाजार समिती भाव",
        mandi_sub: "आजचे बाजारभाव तपासा आणि थेट विक्री करा.",
        mandi_board_header: "आजचे थेट बाजारभाव",
        modal_sell_title: "🌾 थेट विक्रीसाठी शेतमाल नोंदवा"
    },
    te: {
        announcement: "రైతు-వినియోగదారుల ప్రత్యక్ష వేదిక • 0% దళారీ కమీషన్ • 100% రైతు లాభం",
        tagline: "రైతు సోదరులు మరియు కొనుగోలుదారుల ప్రత్యక్ష వారధి",
        nav_schemes: "ప్రభుత్వ పథకాలు",
        nav_marketplace: "ప్రత్యక్ష మార్కెట్",
        nav_mandi: "మార్కెట్ ధరలు",
        nav_advisory: "వాతావరణం & సలహాలు",
        nav_deals: "నా ఒప్పందాలు",
        role_farmer: "రైతు మోడ్",
        role_buyer: "కొనుగోలుదారు మోడ్",
        hero_badge: "జీరో బ్రోకరేజ్ • పొలం వద్దే ప్రత్యక్ష కొనుగోలు",
        hero_title_1: "మన",
        hero_title_2: "రైతు సోదరులను",
        hero_title_3: "కొనుగోలుదారులతో అనుసంధానించడం",
        hero_subtitle: "దళారులను తొలగించడం వల్ల రైతులకు 20-30% అధిక ఆదాయం లభిస్తుంది, వినియోగదారులకు తాజా పంట సరసమైన ధరకే లభిస్తుంది.",
        btn_list_harvest: "+ మీ పంటను అమ్మకానికి పెట్టండి",
        btn_check_subsidies: "ప్రభుత్వ సబ్సిడీలను చూడండి",
        schemes_badge: "ప్రభుత్వ పథకాల సమాచారం",
        schemes_title: "రైతుల కోసం ప్రభుత్వ సబ్సిడీలు & ప్రయోజనాలు",
        schemes_subtitle: "పీఎం-కిసాన్, సోలార్ పంపు 90% సబ్సిడీ, పంట బీమా మరియు ట్రాక్టర్ పథకాలు.",
        btn_check_eligibility: "అర్హతను తనిఖీ చేయండి",
        eligibility_header: "స్మార్ట్ పథక అర్హత గణన",
        eligibility_sub: "మీ పొలం వివరాలను నమోదు చేసి అర్హత గల పథకాలను కనుగొనండి.",
        label_land_size: "భూమి విస్తీర్ణం (ఎకరాలు / హెక్టార్లు)",
        label_state: "మీ రాష్ట్రం",
        label_crop_type: "ప్రధాన పంటలు",
        label_irrigation: "నీటి వనరులు & విధానం",
        btn_find_matching: "పథకాలను కనుగొనండి",
        mandi_title: "లైవ్ మార్కెట్ ధరలు & పోకడలు",
        mandi_sub: "ఈ రోజు మార్కెట్ ధరలను సరిపోల్చి సరసమైన ధర నిర్ణయించండి.",
        mandi_board_header: "ఈ రోజు రాష్ట్ర మార్కెట్ ధరలు",
        modal_sell_title: "🌾 ప్రత్యక్ష అమ్మకం కోసం పంటను నమోదు చేయండి"
    },
    ur: {
        announcement: "کسان تا خریدار براہ راست پلیٹ فارم • 0% کمیشن • 100% کسان کا منافع",
        tagline: "کسان بھائیوں اور خریداروں کا براہ راست رابطہ",
        nav_schemes: "سرکاری اسکیمیں",
        nav_marketplace: "براہ راست مارکیٹ",
        nav_mandi: "منڈی کے بھاؤ",
        nav_advisory: "موسم اور زرعی مشورے",
        nav_deals: "میرے سودے",
        role_farmer: "کسان منظر",
        role_buyer: "خریدار منظر",
        hero_badge: "زیرو کمیشن • سیدھے کھیت سے خریداری",
        hero_title_1: "ہمارے",
        hero_title_2: "کسان بھائیوں",
        hero_title_3: "کو براہ راست خریداروں سے جوڑنا",
        hero_subtitle: "درمیانی دلالوں کو ہٹا کر کسانوں کو 20-30 فیصد زیادہ منافع اور صارفین کو تازہ فصل مناسب قیمت پر ملتی ہے۔",
        btn_list_harvest: "+ نئی فصل فروخت کے لیے درج کریں",
        btn_check_subsidies: "سرکاری سبسڈی تلاش کریں",
        schemes_badge: "سرکاری اسکیموں کی ڈائرکٹری",
        schemes_title: "کسانوں کے لیے سرکاری سبسڈیز اور فوائد",
        schemes_subtitle: "پی ایم کسان، سولر پمپ 90% سبسڈی، فصل بیمہ اور ٹریکٹر اسکیمیں حاصل کریں۔",
        btn_check_eligibility: "اہلیت چیک کریں",
        eligibility_header: "اسمارٹ اسکیم اہلیت کیلکولیٹر",
        eligibility_sub: "اپنی زمین کی تفصیل درج کریں اور موزوں اسکیمیں حاصل کریں۔",
        label_land_size: "زمین کا رقبہ (ایکڑ / ہیکٹر)",
        label_state: "آپ کی ریاست",
        label_crop_type: "اہم فصلیں",
        label_irrigation: "آبپاشی کے ذرائع",
        btn_find_matching: "اسکیمیں تلاش کریں",
        mandi_title: "لائیو منڈی ریٹ اور رجحانات",
        mandi_sub: "اپنی فصل بیچنے سے پہلے آج کے منڈی کے بھاؤ دیکھیں۔",
        mandi_board_header: "آج کے ریاستی منڈی ریٹس",
        modal_sell_title: "🌾 براہ راست فروخت کے لیے فصل شامل کریں"
    },
    ta: {
        announcement: "விவசாயி-நுகர்வோர் நேரடி தளம் • 0% தரகு கமிஷன் • 100% விவசாயிக்கு லாபம்",
        tagline: "விவசாய சகோதரர்கள் மற்றும் நுகர்வோரின் நேரடி இணைப்பு",
        nav_schemes: "அரசு திட்டங்கள்",
        nav_marketplace: "நேரடி சந்தை",
        nav_mandi: "மண்டி விலை நிலவரம்",
        nav_advisory: "வானிலை & ஆலோசனைகள்",
        nav_deals: "என் ஒப்பந்தங்கள்",
        role_farmer: "விவசாயி பயன்முறை",
        role_buyer: "வாங்குபவர் பயன்முறை",
        hero_badge: "பூஜ்ஜிய கமிஷன் • பண்ணையிலிருந்து நேரடி கொள்முதல்",
        hero_title_1: "எங்கள்",
        hero_title_2: "விவசாய சகோதரர்களை",
        hero_title_3: "நேரடியாக வாங்குபவர்களுடன் இணைப்பது",
        hero_subtitle: "இடைத்தரகர்களை நீக்குவதன் மூலம் விவசாயிகளுக்கு 20-30% கூடுதல் வருமானமும், நுகர்வோருக்கு புதிய விளைபொருட்களும் கிடைக்கின்றன.",
        btn_list_harvest: "+ புதிய பயிரை விற்பனைக்கு சேர்க்கவும்",
        btn_check_subsidies: "அரசு மானியங்களை காண்க",
        schemes_badge: "அரசு திட்டங்களின் பட்டியல்",
        schemes_title: "விவசாயிகளுக்கான அரசு மானியங்கள் மற்றும் நன்மைகள்",
        schemes_subtitle: "பிஎம்-கிசான், 90% சோலார் பம்ப் மானியம், பயிர் காப்பீடு மற்றும் டிராக்டர் திட்டங்கள்.",
        btn_check_eligibility: "தகுதியை சரிபார்க்கவும்",
        eligibility_header: "ஸ்மார்ட் திட்ட தகுதி சரிபார்ப்பு",
        eligibility_sub: "உங்கள் நில விவரங்களை உள்ளிட்டு தகுதியான மானியங்களை கண்டறியவும்.",
        label_land_size: "நிலத்தின் பரப்பளவு (ஏக்கர் / ஹெக்டேர்)",
        label_state: "உங்கள் மாநிலம்",
        label_crop_type: "பயிரிடப்படும் பயிர்கள்",
        label_irrigation: "பாசன முறை & ஆதாரம்",
        btn_find_matching: "பொருத்தமான திட்டங்களை தேடுக"
    },
    bn: {
        announcement: "কৃষক-ক্রেতা সরাসরি প্ল্যাটফর্ম • ০% দালালি কমিশন • ১০০% কৃষকের লাভ",
        tagline: "আমাদের কৃষক ভাই ও গ্রাহকদের সরাসরি সেতুবন্ধন",
        nav_schemes: "সরকারি প্রকল্প",
        nav_marketplace: "সরাসরি বাজার",
        nav_mandi: "মান্ডি দর",
        nav_advisory: "আবহাওয়া ও পরামর্শ",
        nav_deals: "আমার ডিল",
        role_farmer: "কৃষক মোড",
        role_buyer: "ক্রেতা মোড",
        hero_badge: "জিরো ব্রোকারেজ • মাঠ থেকে সরাসরি কেনাকাটা",
        hero_title_1: "আমাদের",
        hero_title_2: "কৃষক ভাইদের",
        hero_title_3: "সরাসরি ক্রেতাদের সাথে যুক্ত করা",
        hero_subtitle: "মধ্যস্বত্বভোগীদের বাদ দিয়ে কৃষকদের ২০-৩০% বেশি আয় নিশ্চিত করা এবং ভোক্তাদের ন্যায্যমূল্যে তাজা ফসল প্রদান করা।",
        btn_list_harvest: "+ ফসল বিক্রির জন্য যুক্ত করুন",
        btn_check_subsidies: "সরকারি ভর্তুকি খুঁজুন",
        schemes_badge: "সরকারি প্রকল্পের ডিরেক্টরি",
        schemes_title: "কৃষকদের জন্য সরকারি অনুদান ও সুবিধা",
        schemes_subtitle: "পিএম-কিষাণ, ৯০% সোলার পাম্প ভর্তুকি, ফসল বিমা এবং ট্র্যাক্টর যান্ত্রিকীকরণ প্রকল্প।",
        btn_check_eligibility: "যোগ্যতা যাচাই করুন",
        eligibility_header: "স্মার্ট প্রকল্প যোগ্যতা ক্যালকুলেটর",
        eligibility_sub: "আপনার জমির বিবরণ দিন এবং প্রযোজ্য সরকারি প্রকল্পগুলো জানুন।",
        label_land_size: "জমির পরিমাণ (একর / হেক্টর)",
        label_state: "আপনার রাজ্য",
        label_crop_type: "প্রধান ফসল",
        label_irrigation: "সেচ ব্যবস্থা ও উৎস",
        btn_find_matching: "প্রকল্প খুঁজুন",
        mandi_title: "লাইভ মান্ডি বাজারদর ও প্রবণতা",
        mandi_sub: "ফসল বিক্রির আগে আজকের মান্ডি দরের সাথে তুলনা করুন।",
        mandi_board_header: "আজকের রাজ্যভিত্তিক মান্ডি দর",
        modal_sell_title: "🌾 সরাসরি বিক্রির জন্য ফসল যুক্ত করুন"
    },
    ja: {
        announcement: "農家と購入者の直接取引プラットフォーム • 仲介手数料0% • 農家の利益100%",
        tagline: "農家の皆様と直接消費者を結ぶプラットフォーム",
        nav_schemes: "政府補助金制度",
        nav_marketplace: "産直マーケット",
        nav_mandi: "リアルタイム相場",
        nav_advisory: "天気・営農指導",
        nav_deals: "取引一覧",
        role_farmer: "農家モード",
        role_buyer: "購入者モード",
        hero_badge: "手数料ゼロ • 産地直送・直接調達",
        hero_title_1: "私たちの",
        hero_title_2: "農家の皆様",
        hero_title_3: "を購入者と直接つなぐ",
        hero_subtitle: "仲介業者を省くことで農家の収入を20〜30%向上させ、消費者は新鮮で安全な農産物を適正価格で購入できます。",
        btn_list_harvest: "+ 作物を出品する",
        btn_check_subsidies: "補助金制度を探す",
        schemes_badge: "中央・地方政府の農業支援制度一覧",
        schemes_title: "農家のための政府補助金・助成金",
        schemes_subtitle: "PM-Kisan直接給付金、太陽光灌漑ポンプ最大90%補助、農業共済・保険、農機具導入支援。",
        btn_check_eligibility: "受給資格を診断する",
        eligibility_header: "スマート補助金受給資格診断",
        eligibility_sub: "農地規模や作物を入力して、申請可能な補助金を即座にマッチングします。",
        label_land_size: "農地面積（ヘクタール / エーカー）"
    },
    de: {
        announcement: "Direktplattform für Landwirte & Käufer • 0% Zwischenhändler • 100% Gewinn für Landwirte",
        tagline: "Stärkung von Landwirten und Direktverbrauchern",
        nav_schemes: "Förderprogramme",
        nav_marketplace: "Direktmarkt",
        nav_mandi: "Marktpreise",
        nav_advisory: "Wetter & Beratung",
        nav_deals: "Meine Deals",
        role_farmer: "Landwirt-Ansicht",
        role_buyer: "Käufer-Ansicht",
        hero_badge: "Null Provision • Direkter Einkauf ab Hof",
        hero_title_1: "Verbindung unserer",
        hero_title_2: "Landwirte",
        hero_title_3: "direkt mit Käufern",
        hero_subtitle: "Durch den Verzicht auf Zwischenhändler erzielen Landwirte 20-30% mehr Einkommen, während Käufer frische Ernten zu fairen Preisen erhalten.",
        btn_list_harvest: "+ Ernte inserieren",
        btn_check_subsidies: "Zuschüsse finden",
        schemes_badge: "Verzeichnis staatlicher Förderprogramme",
        schemes_title: "Staatliche Subventionen & Zuschüsse für Landwirte",
        schemes_subtitle: "Entdecken Sie PM-Kisan-Zahlungen, 90% Solarpumpen-Zuschüsse, Ernteversicherungen und Maschinensubventionen.",
        btn_check_eligibility: "Berechtigung prüfen",
        eligibility_header: "Intelligenter Förderungs-Rechner",
        eligibility_sub: "Geben Sie Ihre Betriebsdaten ein, um sofort passende Zuschüsse zu erhalten.",
        label_land_size: "Fläche (Hektar / Acres)"
    },
    fr: {
        announcement: "Plateforme directe Agriculteur-Acheteur • 0% de commission • 100% de profit pour l'agriculteur",
        tagline: "Autonomiser les agriculteurs et les consommateurs directs",
        nav_schemes: "Aides de l'État",
        nav_marketplace: "Marché Direct",
        nav_mandi: "Cours du Marché",
        nav_advisory: "Météo & Conseils",
        nav_deals: "Mes Commandes",
        role_farmer: "Mode Agriculteur",
        role_buyer: "Mode Acheteur",
        hero_badge: "Zéro commission • Achat direct à la ferme",
        hero_title_1: "Connecter nos",
        hero_title_2: "Frères Agriculteurs",
        hero_title_3: "Directement aux Acheteurs",
        hero_subtitle: "L'élimination des intermédiaires permet aux agriculteurs de gagner 20 à 30% de plus, tandis que les consommateurs profitent de récoltes fraîches à prix équitables.",
        btn_list_harvest: "+ Publier votre récolte",
        btn_check_subsidies: "Trouver des subventions",
        schemes_badge: "Répertoire des programmes publics d'aide agricole",
        schemes_title: "Subventions et aides gouvernementales pour les agriculteurs",
        schemes_subtitle: "Découvrez l'aide PM-Kisan, jusqu'à 90% de subvention pour pompes solaires, assurances récoltes et aides aux machines agricoles.",
        btn_check_eligibility: "Vérifier votre éligibilité",
        eligibility_header: "Calculateur d'éligibilité aux aides agricoles",
        eligibility_sub: "Renseignez votre exploitation pour trouver les subventions disponibles immédiatement.",
        label_land_size: "Superficie (Hectares / Acres)"
    },
    zh: {
        announcement: "农民与买家直连平台 • 0%中间商佣金 • 100%农民收益",
        tagline: "赋能农民兄弟与直接消费者",
        nav_schemes: "政府补贴政策",
        nav_marketplace: "产地直销市场",
        nav_mandi: "实时批发价格",
        nav_advisory: "天气与农技指导",
        nav_deals: "我的交易",
        role_farmer: "农民模式",
        role_buyer: "买家模式",
        hero_badge: "零中介费 • 农场直采",
        hero_title_1: "将我们的",
        hero_title_2: "农民兄弟",
        hero_title_3: "与买家直接相连",
        hero_subtitle: "消除中间商环节，让农民增收20%-30%，同时让消费者以公道批发价享受100%农场新鲜农产品。",
        btn_list_harvest: "+ 发布农产品",
        btn_check_subsidies: "查询政府补贴",
        schemes_badge: "中央与地方政府惠农政策汇总",
        schemes_title: "面向农民的政府补贴与政策福利",
        schemes_subtitle: "PM-Kisan直补金、高达90%的太阳能灌溉泵补贴、农业保险及农机具购置补贴。",
        btn_check_eligibility: "查询申请资格",
        eligibility_header: "智能农政补贴匹配器",
        eligibility_sub: "输入耕地规模与种植作物，立即获取可申请的政策补贴。",
        label_land_size: "土地面积（公顷 / 英亩）"
    },
    ko: {
        announcement: "농민-구매자 직접 직거래 플랫폼 • 중개수수료 0% • 농가 수익 100%",
        tagline: "농민과 소비자를 잇는 직거래 플랫폼",
        nav_schemes: "정부 지원사업",
        nav_marketplace: "산지 직거래 장터",
        nav_mandi: "실시간 시세",
        nav_advisory: "날씨 & 영농기술",
        nav_deals: "나의 거래",
        role_farmer: "농민 모드",
        role_buyer: "구매자 모드",
        hero_badge: "수수료 0% • 산지 직접 구매",
        hero_title_1: "우리의",
        hero_title_2: "농민 형제들",
        hero_title_3: "을 소비자와 직접 연결",
        hero_subtitle: "중간 유통 마진을 없애 농가 소득을 20~30% 증대시키고, 소비자에게는 신선한 농산물을 합리적인 가격에 제공합니다.",
        btn_list_harvest: "+ 수확 작물 등록",
        btn_check_subsidies: "정부 보조금 찾기",
        schemes_badge: "정부 농업 지원 정책 모음",
        schemes_title: "농민을 위한 정부 보조금 및 지원 혜택",
        schemes_subtitle: "PM-Kisan 직불금, 태양광 관수 펌프 90% 보조금, 농작물 재해보험 및 농기계 지원.",
        btn_check_eligibility: "지원 자격 확인",
        eligibility_header: "스마트 맞춤 보조금 계산기",
        eligibility_sub: "농지 면적과 재배 작물을 입력하여 신청 가능한 지원금을 확인하세요.",
        label_land_size: "농지 면적 (헥타르 / 에이커)"
    }
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize Lucide icons
    if (window.lucide) lucide.createIcons();

    // Check PWA Support
    setupPWA();

    // Fetch initial user & data
    await fetchCurrentUser();
    await loadProduce();
    await loadSchemes();
    await loadMandiPrices();
    await loadAdvisories();
    await loadDeals();
});

// PWA Setup
function setupPWA() {
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPWAInstallPrompt = e;
        const installBtn = document.getElementById('pwaInstallBtn');
        if (installBtn) installBtn.classList.remove('hidden');
    });

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js').catch(err => {
            console.log('SW registration note:', err);
        });
    }
}

function installPWA() {
    if (deferredPWAInstallPrompt) {
        deferredPWAInstallPrompt.prompt();
        deferredPWAInstallPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                const installBtn = document.getElementById('pwaInstallBtn');
                if (installBtn) installBtn.classList.add('hidden');
            }
            deferredPWAInstallPrompt = null;
        });
    }
}

// Switch UI Navigation Tabs
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.nav-btn').forEach(el => {
        el.classList.remove('active', 'bg-kisan-100/80', 'text-kisan-900');
        el.classList.add('text-slate-700');
    });

    const targetTab = document.getElementById(`tab-${tabName}`);
    const targetNav = document.getElementById(`nav-${tabName}`);

    if (targetTab) {
        targetTab.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    if (targetNav) {
        targetNav.classList.add('active', 'bg-kisan-100/80', 'text-kisan-900');
        targetNav.classList.remove('text-slate-700');
    }

    if (tabName === 'mandi') {
        setTimeout(renderMandiChart, 100);
    }
    if (tabName === 'deals') {
        loadDeals();
    }

    if (window.lucide) lucide.createIcons();
}

// User Profile & Role Switcher
async function fetchCurrentUser() {
    try {
        const res = await fetch('/api/auth/current_user');
        const data = await res.json();
        if (data.user) {
            currentUser = data.user;
            updateUserUI();
        }
    } catch (err) {
        console.error('Error loading current user:', err);
    }
}

function updateUserUI() {
    if (!currentUser) return;

    const nameDisplay = document.getElementById('userNameDisplay');
    const roleBadge = document.getElementById('userRoleBadge');
    const userAvatar = document.getElementById('userAvatar');
    const dropdownUserName = document.getElementById('dropdownUserName');
    const dropdownUserLoc = document.getElementById('dropdownUserLocation');
    const dealsRoleIndicator = document.getElementById('dealsRoleIndicator');

    if (nameDisplay) nameDisplay.textContent = currentUser.name.split(' ')[0] + ' ' + (currentUser.name.split(' ')[1] || '');
    if (roleBadge) roleBadge.textContent = currentUser.role.toUpperCase();
    if (dropdownUserName) dropdownUserName.textContent = currentUser.name;
    if (dropdownUserLoc) dropdownUserLoc.textContent = `${currentUser.district || 'Varanasi'}, ${currentUser.state || 'UP'}`;
    if (userAvatar) userAvatar.textContent = currentUser.name.charAt(0).toUpperCase();

    if (dealsRoleIndicator) {
        dealsRoleIndicator.textContent = currentUser.role === 'farmer' ? '🌾 Farmer Incoming Deals' : '🛒 My Purchase Orders';
    }

    // Role Buttons Styling
    const roleBtnFarmer = document.getElementById('roleBtnFarmer');
    const roleBtnBuyer = document.getElementById('roleBtnBuyer');

    if (currentUser.role === 'farmer') {
        roleBtnFarmer.className = "px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 shadow-sm bg-kisan-700 text-white";
        roleBtnBuyer.className = "px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 text-slate-700 hover:text-kisan-800";
    } else {
        roleBtnBuyer.className = "px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 shadow-sm bg-emerald-700 text-white";
        roleBtnFarmer.className = "px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 text-slate-700 hover:text-kisan-800";
    }
}

async function switchDemoRole(role) {
    try {
        const res = await fetch('/api/auth/switch_demo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role })
        });
        const data = await res.json();
        if (data.user) {
            currentUser = data.user;
            updateUserUI();
            loadProduce();
            loadDeals();
            showToast(`Switched to ${role === 'farmer' ? '🚜 Farmer View' : '🛒 Buyer View'}`);
        }
    } catch (err) {
        console.error('Error switching demo role:', err);
    }
}

function toggleUserDropdown() {
    const menu = document.getElementById('userDropdownMenu');
    if (menu) menu.classList.toggle('hidden');
}

// Close dropdown on outside click
document.addEventListener('click', (e) => {
    const menu = document.getElementById('userDropdownMenu');
    if (menu && !menu.contains(e.target) && !e.target.closest('button[onclick="toggleUserDropdown()"]')) {
        menu.classList.add('hidden');
    }
});

// Toast notification helper
function showToast(message) {
    const existing = document.getElementById('kisanToast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.id = 'kisanToast';
    toast.className = 'fixed bottom-20 left-1/2 -translate-x-1/2 z-50 bg-slate-900 text-white px-5 py-2.5 rounded-2xl shadow-xl text-xs font-bold flex items-center gap-2 border border-kisan-500 animate-in fade-in slide-in-from-bottom-5';
    toast.innerHTML = `<span>🌱</span> <span>${message}</span>`;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Multilingual switcher
function changeLanguage(lang) {
    currentLanguage = lang;
    const dict = translations[lang] || translations.en;

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    loadProduce();
    loadSchemes();
}


// ==========================================
// 1. PRODUCE MARKETPLACE LOGIC
// ==========================================

async function loadProduce() {
    try {
        const search = document.getElementById('produceSearchInput')?.value || '';
        const state = document.getElementById('produceStateFilter')?.value || 'all';
        const organicOnly = document.getElementById('produceOrganicFilter')?.checked || false;

        let url = `/api/produce?category=${activeCategory}&search=${encodeURIComponent(search)}&state=${state}&organic_only=${organicOnly}`;
        const res = await fetch(url);
        const data = await res.json();
        allProduce = data.produce || [];
        renderProduceGrid();
    } catch (err) {
        console.error('Error loading produce:', err);
    }
}

function setCategoryFilter(category) {
    activeCategory = category;
    document.querySelectorAll('.cat-pill').forEach(el => {
        el.classList.remove('active', 'bg-kisan-700', 'text-white');
        el.classList.add('bg-gray-100', 'text-slate-700');
    });

    const activePill = event.target;
    if (activePill) {
        activePill.classList.add('active', 'bg-kisan-700', 'text-white');
        activePill.classList.remove('bg-gray-100', 'text-slate-700');
    }
    loadProduce();
}

function debounceSearchProduce() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(loadProduce, 300);
}

function renderProduceGrid() {
    const grid = document.getElementById('produceGrid');
    if (!grid) return;

    if (allProduce.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full py-16 text-center space-y-3 bg-white rounded-3xl border border-dashed border-kisan-300">
                <span class="text-4xl">🌾</span>
                <h4 class="text-base font-bold text-slate-800">No crop produce found matching your filter</h4>
                <p class="text-xs text-slate-500">Try changing your search term or category filters.</p>
                <button onclick="setCategoryFilter('all')" class="px-4 py-2 rounded-xl bg-kisan-700 text-white text-xs font-bold">Reset Filters</button>
            </div>
        `;
        return;
    }

    grid.innerHTML = allProduce.map(p => {
        const isOrganic = p.organic_certified;
        const savingsText = `₹${p.middleman_saving} Middleman Fee Saved`;

        return `
            <div class="produce-card bg-white rounded-3xl overflow-hidden border border-kisan-200/80 shadow-sm flex flex-col justify-between">
                <div>
                    <!-- Image & Badges -->
                    <div class="relative h-48 w-full overflow-hidden bg-gray-100">
                        <img src="${p.image_url}" alt="${p.crop_name}" class="w-full h-full object-cover transform hover:scale-105 transition duration-500" loading="lazy">
                        
                        <div class="absolute top-3 left-3 flex flex-col gap-1">
                            <span class="bg-black/60 backdrop-blur-md text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider">
                                ${p.category}
                            </span>
                            ${isOrganic ? `
                                <span class="bg-emerald-600/90 backdrop-blur-md text-white text-[10px] font-bold px-2.5 py-1 rounded-full flex items-center gap-1 shadow-sm">
                                    <span>🌿</span> 100% Organic
                                </span>
                            ` : ''}
                        </div>

                        <div class="absolute top-3 right-3">
                            <span class="bg-amber-400 text-slate-950 text-[10px] font-extrabold px-2.5 py-1 rounded-full shadow-md">
                                0% Brokerage
                            </span>
                        </div>

                        <div class="absolute bottom-2 left-3 right-3 bg-black/50 backdrop-blur-md px-2.5 py-1 rounded-lg text-white text-[10px] flex justify-between items-center">
                            <span class="truncate">📍 ${p.location_text}</span>
                            <span class="font-semibold text-kisan-300">⭐ ${p.farmer_rating}</span>
                        </div>
                    </div>

                    <!-- Card Body -->
                    <div class="p-5 space-y-3">
                        <div class="space-y-0.5">
                            <div class="text-[11px] font-bold text-kisan-700 flex items-center gap-1">
                                <span>👨‍🌾</span> ${p.farmer_name}
                                ${p.farmer_verified ? '<span class="text-emerald-600 font-bold">✓</span>' : ''}
                            </div>
                            <h3 class="text-base font-extrabold text-slate-900 tracking-tight leading-snug">${p.crop_name}</h3>
                            <p class="text-xs text-slate-500 line-clamp-2">${p.description || p.variety}</p>
                        </div>

                        <!-- Pricing & Zero Middlemen Comparison -->
                        <div class="bg-kisan-50/70 p-3 rounded-2xl border border-kisan-200/60 space-y-1.5">
                            <div class="flex justify-between items-baseline">
                                <div>
                                    <span class="text-lg font-extrabold text-kisan-900">₹${p.price_per_unit}</span>
                                    <span class="text-xs text-slate-600 font-semibold">/ ${p.unit}</span>
                                </div>
                                <span class="text-xs font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-md">
                                    ${p.quantity} ${p.unit} Available
                                </span>
                            </div>

                            <div class="flex items-center justify-between text-[11px] text-slate-600 pt-1 border-t border-kisan-200/50">
                                <span>Mandi Benchmark: <del>₹${p.mandi_benchmark_price}</del></span>
                                <span class="font-bold text-emerald-700">✓ Farmer gets 100%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Card Footer Actions -->
                <div class="p-5 pt-0 flex gap-2">
                    <button onclick="openBuyOfferModal(${p.id})" class="flex-grow py-2.5 px-3 rounded-xl bg-kisan-700 hover:bg-kisan-800 text-white font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5">
                        <i data-lucide="shopping-bag" class="w-3.5 h-3.5"></i>
                        <span>Direct Buy / Offer</span>
                    </button>
                    <a href="https://wa.me/${p.farmer_phone.replace(/[^0-9]/g, '')}?text=Namaste%20${encodeURIComponent(p.farmer_name)}%20ji,%20I%20am%20interested%20in%20your%20${encodeURIComponent(p.crop_name)}%20listing%20on%20KisanMitra." target="_blank" class="py-2.5 px-3 rounded-xl bg-emerald-100 hover:bg-emerald-200 text-emerald-900 font-bold text-xs transition flex items-center justify-center" title="Chat on WhatsApp">
                        <span>💬</span>
                    </a>
                </div>
            </div>
        `;
    }).join('');

    if (window.lucide) lucide.createIcons();
}


// ==========================================
// 2. GOVERNMENT SCHEMES & ELIGIBILITY
// ==========================================

async function loadSchemes() {
    try {
        const res = await fetch(`/api/schemes?category=${activeSchemeCategory}`);
        const data = await res.json();
        allSchemes = data.schemes || [];
        renderSchemesGrid(allSchemes);
    } catch (err) {
        console.error('Error loading schemes:', err);
    }
}

function filterSchemesByCategory(cat) {
    activeSchemeCategory = cat;
    document.querySelectorAll('.scheme-pill').forEach(el => {
        el.classList.remove('active', 'bg-kisan-700', 'text-white');
        el.classList.add('bg-white', 'text-slate-700');
    });

    const pill = event.target;
    if (pill) {
        pill.classList.add('active', 'bg-kisan-700', 'text-white');
        pill.classList.remove('bg-white', 'text-slate-700');
    }
    loadSchemes();
}

function renderSchemesGrid(schemesToRender) {
    const grid = document.getElementById('schemesGrid');
    if (!grid) return;

    grid.innerHTML = schemesToRender.map(s => {
        const isHi = currentLanguage === 'hi';
        const title = isHi ? s.title_hi : s.title_en;
        const desc = isHi ? s.description_hi : s.description_en;

        return `
            <div class="scheme-card bg-white rounded-3xl p-6 border border-kisan-200 shadow-sm flex flex-col justify-between space-y-4">
                <div class="space-y-3">
                    <div class="flex items-start justify-between gap-3">
                        <div class="flex items-center gap-2.5">
                            <div class="w-10 h-10 rounded-2xl bg-emerald-100 text-emerald-900 flex items-center justify-center font-bold text-lg">
                                🏛️
                            </div>
                            <div>
                                <span class="text-[10px] font-bold uppercase tracking-wider bg-emerald-50 text-emerald-800 border border-emerald-200 px-2.5 py-0.5 rounded-full">
                                    ${s.category.replace('_', ' ')}
                                </span>
                                <h3 class="text-base font-extrabold text-slate-900 mt-1">${title}</h3>
                            </div>
                        </div>
                        ${s.match_score ? `
                            <span class="bg-emerald-600 text-white text-xs font-extrabold px-2.5 py-1 rounded-xl shadow-sm animate-pulse">
                                ${s.match_score}% Match
                            </span>
                        ` : ''}
                    </div>

                    <p class="text-xs text-slate-600 leading-relaxed">${desc}</p>

                    <!-- Subsidy Highlight -->
                    <div class="bg-kisan-50 p-3 rounded-2xl border border-kisan-200/80 space-y-1">
                        <div class="text-[10px] font-bold uppercase text-kisan-900">Grant / Benefit Amount (सब्सिडी)</div>
                        <div class="text-sm font-extrabold text-kisan-800">${s.subsidy_amount_text}</div>
                    </div>

                    <!-- Eligibility Tags -->
                    <div class="flex flex-wrap gap-1.5 text-[11px] text-slate-600">
                        <span class="bg-gray-100 px-2 py-0.5 rounded-md">🌾 ${s.eligible_crops.split(',')[0]}</span>
                        <span class="bg-gray-100 px-2 py-0.5 rounded-md">📍 ${s.eligible_states.split(' ')[0]}</span>
                        <span class="bg-gray-100 px-2 py-0.5 rounded-md">⏳ ${s.deadline_info}</span>
                    </div>
                </div>

                <!-- Footer CTA -->
                <div class="pt-2 border-t border-gray-100 flex items-center justify-between gap-2">
                    <button onclick="openSchemeModal(${s.id})" class="flex-grow py-2.5 px-4 rounded-xl bg-kisan-700 hover:bg-kisan-800 text-white font-bold text-xs shadow-md transition flex items-center justify-center gap-1.5">
                        <i data-lucide="info" class="w-3.5 h-3.5"></i>
                        <span>View Details & Checklist</span>
                    </button>
                    <button onclick="speakSchemeDirect(${s.id})" class="p-2.5 rounded-xl bg-amber-100 hover:bg-amber-200 text-amber-900 font-bold text-xs transition" title="Listen Audio">
                        <span>📢</span>
                    </button>
                </div>
            </div>
        `;
    }).join('');

    if (window.lucide) lucide.createIcons();
}

async function calculateEligibility(e) {
    e.preventDefault();
    const land_size = parseFloat(document.getElementById('el_land_size').value);
    const state = document.getElementById('el_state').value;
    const crop_type = document.getElementById('el_crop_type').value;
    const irrigation = document.getElementById('el_irrigation').value;
    const is_organic = document.getElementById('el_is_organic').checked;

    try {
        const res = await fetch('/api/schemes/check_eligibility', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ land_size, state, crop_type, irrigation, is_organic })
        });
        const data = await res.json();
        
        const banner = document.getElementById('eligibilityResultsBanner');
        const countText = document.getElementById('matchCountText');
        if (banner && countText) {
            banner.classList.remove('hidden');
            countText.textContent = `Matched ${data.total_matched} Tailored Government Subsidies for Your Farm!`;
        }

        renderSchemesGrid(data.results || []);
        showToast(`Found ${data.total_matched} matching schemes!`);
    } catch (err) {
        console.error('Error calculating eligibility:', err);
    }
}

function scrollToEligibilityChecker() {
    const el = document.getElementById('eligibilityCheckerBox');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
}


// ==========================================
// 3. SCHEME DETAILS & VOICE AUDIO (TTS)
// ==========================================

let activeModalScheme = null;

function openSchemeModal(schemeId) {
    const scheme = allSchemes.find(s => s.id === schemeId);
    if (!scheme) return;

    activeModalScheme = scheme;

    document.getElementById('modalSchemeCategoryBadge').textContent = scheme.category.replace('_', ' ');
    document.getElementById('modalSchemeTitle').textContent = scheme.title_en;
    document.getElementById('modalSchemeHindiTitle').textContent = scheme.title_hi;
    document.getElementById('modalSchemeSubsidy').textContent = scheme.subsidy_amount_text;
    document.getElementById('modalSchemeDescription').textContent = scheme.description_en + " " + scheme.description_hi;
    document.getElementById('modalSchemeHelpline').textContent = scheme.helpline_number;
    document.getElementById('modalSchemeApplyLink').href = scheme.official_url;

    // Render Checklist
    const docsContainer = document.getElementById('modalSchemeDocuments');
    docsContainer.innerHTML = (scheme.documents_required || []).map((doc, idx) => `
        <label class="flex items-center gap-2 p-2 rounded-xl bg-gray-50 border border-gray-200 cursor-pointer hover:bg-emerald-50">
            <input type="checkbox" class="rounded text-kisan-600 focus:ring-kisan-500">
            <span>${doc}</span>
        </label>
    `).join('');

    // Render Application Steps
    const stepsContainer = document.getElementById('modalSchemeSteps');
    stepsContainer.innerHTML = (scheme.application_steps || []).map((step, idx) => `
        <div class="flex items-start gap-2.5 p-2.5 rounded-xl bg-gray-50 border border-gray-100">
            <span class="w-5 h-5 rounded-full bg-kisan-700 text-white font-bold text-[10px] flex items-center justify-center shrink-0 mt-0.5">${idx + 1}</span>
            <span class="leading-relaxed">${step}</span>
        </div>
    `).join('');

    document.getElementById('schemeDetailModal').classList.remove('hidden');
    if (window.lucide) lucide.createIcons();
}

function closeSchemeModal() {
    stopSchemeSpeech();
    document.getElementById('schemeDetailModal').classList.add('hidden');
}

function toggleSchemeSpeech() {
    if (isSpeaking) {
        stopSchemeSpeech();
    } else if (activeModalScheme) {
        startSchemeSpeech(activeModalScheme);
    }
}

function speakSchemeDirect(schemeId) {
    const scheme = allSchemes.find(s => s.id === schemeId);
    if (!scheme) return;
    openSchemeModal(schemeId);
    startSchemeSpeech(scheme);
}

function startSchemeSpeech(scheme) {
    if (!('speechSynthesis' in window)) {
        alert('Text-to-speech is not supported on this browser.');
        return;
    }

    window.speechSynthesis.cancel();

    const speechLangMap = {
        'hi': 'hi-IN',
        'pa': 'pa-IN',
        'mr': 'mr-IN',
        'te': 'te-IN',
        'ur': 'ur-PK',
        'ta': 'ta-IN',
        'bn': 'bn-IN',
        'ja': 'ja-JP',
        'de': 'de-DE',
        'fr': 'fr-FR',
        'zh': 'zh-CN',
        'ko': 'ko-KR',
        'en': 'en-IN'
    };

    let textToSpeak = `Scheme: ${scheme.title_en}. Benefits: ${scheme.subsidy_amount_text}. Description: ${scheme.description_en}. Helpline: ${scheme.helpline_number}`;
    
    if (currentLanguage === 'hi') {
        textToSpeak = `योजना: ${scheme.title_hi}। लाभ: ${scheme.subsidy_amount_text}। विवरण: ${scheme.description_hi}। हेल्पलाइन: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'pa') {
        textToSpeak = `ਸਰਕਾਰੀ ਸਕੀਮ: ${scheme.title_hi}। ਲਾਭ: ${scheme.subsidy_amount_text}। ਹੈਲਪਲਾਈਨ: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'mr') {
        textToSpeak = `शासकीय योजना: ${scheme.title_hi}। लाभ: ${scheme.subsidy_amount_text}। हेल्पलाइन: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'te') {
        textToSpeak = `ప్రభుత్వ పథకం: ${scheme.title_en}. ప్రయోజనం: ${scheme.subsidy_amount_text}. హెల్ప్‌లైన్: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'ur') {
        textToSpeak = `سرکاری اسکیم: ${scheme.title_hi}۔ فائدہ: ${scheme.subsidy_amount_text}۔ ہیلپ لائن: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'ta') {
        textToSpeak = `அரசு திட்டம்: ${scheme.title_en}. மானிய நன்மை: ${scheme.subsidy_amount_text}. உதவி எண்: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'bn') {
        textToSpeak = `সরকারি প্রকল্প: ${scheme.title_hi}। অনুদান সুবিধা: ${scheme.subsidy_amount_text}। হেল্পলাইন: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'ja') {
        textToSpeak = `政府支援制度: ${scheme.title_en}。補助金給付: ${scheme.subsidy_amount_text}。ヘルプライン: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'de') {
        textToSpeak = `Förderprogramm: ${scheme.title_en}. Zuschuss: ${scheme.subsidy_amount_text}. Helpline: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'fr') {
        textToSpeak = `Programme d'aide: ${scheme.title_en}. Avantage: ${scheme.subsidy_amount_text}. Assistance: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'zh') {
        textToSpeak = `政府惠农政策: ${scheme.title_en}。补贴福利: ${scheme.subsidy_amount_text}。咨询热线: ${scheme.helpline_number}`;
    } else if (currentLanguage === 'ko') {
        textToSpeak = `정부 지원사업: ${scheme.title_en}. 지원 혜택: ${scheme.subsidy_amount_text}. 문의전화: ${scheme.helpline_number}`;
    }

    currentSpeechUtterance = new SpeechSynthesisUtterance(textToSpeak);
    currentSpeechUtterance.rate = 0.95;
    currentSpeechUtterance.pitch = 1.0;
    currentSpeechUtterance.lang = speechLangMap[currentLanguage] || 'en-IN';

    currentSpeechUtterance.onstart = () => {
        isSpeaking = true;
        const btnText = document.getElementById('ttsBtnText');
        if (btnText) btnText.textContent = 'Stop Audio (रोकें)';
    };

    currentSpeechUtterance.onend = () => {
        stopSchemeSpeech();
    };

    currentSpeechUtterance.onerror = () => {
        stopSchemeSpeech();
    };

    window.speechSynthesis.speak(currentSpeechUtterance);
}

function stopSchemeSpeech() {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
    isSpeaking = false;
    const btnText = document.getElementById('ttsBtnText');
    if (btnText) btnText.textContent = 'Play Audio (सुनें)';
}


// ==========================================
// 4. SELL HARVEST MODAL (FOR FARMERS)
// ==========================================

function openCreateListingModal() {
    if (!currentUser || currentUser.role !== 'farmer') {
        switchDemoRole('farmer');
    }
    document.getElementById('createListingModal').classList.remove('hidden');
    if (window.lucide) lucide.createIcons();
}

function closeCreateListingModal() {
    document.getElementById('createListingModal').classList.add('hidden');
}

async function submitCreateListing(e) {
    e.preventDefault();
    const crop_name = document.getElementById('new_crop_name').value.trim();
    const category = document.getElementById('new_category').value;
    const variety = document.getElementById('new_variety').value.trim();
    const quantity = parseFloat(document.getElementById('new_quantity').value);
    const unit = document.getElementById('new_unit').value;
    const price_per_unit = parseFloat(document.getElementById('new_price_per_unit').value);
    const state = document.getElementById('new_state').value;
    const district = document.getElementById('new_district').value.trim();
    const organic_certified = document.getElementById('new_organic_certified').checked;
    const description = document.getElementById('new_description').value.trim();

    try {
        const res = await fetch('/api/produce', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop_name, category, variety, quantity, unit,
                price_per_unit, state, district, organic_certified, description
            })
        });
        const data = await res.json();
        if (res.ok) {
            closeCreateListingModal();
            loadProduce();
            showToast('🌾 Your crop harvest has been published for direct buyers!');
        } else {
            alert(data.error || 'Failed to create listing');
        }
    } catch (err) {
        console.error('Error submitting listing:', err);
    }
}


// ==========================================
// 5. DIRECT BUY OFFER MODAL (FOR BUYERS)
// ==========================================

let activeBuyProduce = null;

function openBuyOfferModal(produceId) {
    const produce = allProduce.find(p => p.id === produceId);
    if (!produce) return;

    activeBuyProduce = produce;
    document.getElementById('offer_produce_id').value = produce.id;
    document.getElementById('buyOfferCropTitle').textContent = `${produce.crop_name} (${produce.category})`;
    document.getElementById('buyOfferFarmerName').innerHTML = `<span>${produce.farmer_name}</span> <span class="text-[10px] bg-emerald-200 text-emerald-900 font-bold px-1.5 py-0.2 rounded">✓ Verified Kisan</span>`;
    document.getElementById('buyOfferLocation').textContent = produce.location_text;
    document.getElementById('buyOfferListedRate').textContent = `₹${produce.price_per_unit} / ${produce.unit}`;
    document.getElementById('offerUnitLabel').textContent = produce.unit;
    document.getElementById('offer_quantity').value = Math.min(10, produce.quantity);
    document.getElementById('offer_price').value = produce.price_per_unit;

    // Direct WhatsApp Link
    const cleanPhone = produce.farmer_phone.replace(/[^0-9]/g, '');
    const waText = encodeURIComponent(`Namaste ${produce.farmer_name} ji, I want to purchase ${produce.crop_name} listed on KisanMitra at ₹${produce.price_per_unit}/${produce.unit}. Please connect.`);
    document.getElementById('offerWhatsAppBtn').href = `https://wa.me/${cleanPhone}?text=${waText}`;

    recalcOfferTotal();
    document.getElementById('buyOfferModal').classList.remove('hidden');
    if (window.lucide) lucide.createIcons();
}

function closeBuyOfferModal() {
    document.getElementById('buyOfferModal').classList.add('hidden');
}

function recalcOfferTotal() {
    const qty = parseFloat(document.getElementById('offer_quantity').value) || 0;
    const price = parseFloat(document.getElementById('offer_price').value) || 0;
    const total = qty * price;
    document.getElementById('offerTotalCalculated').textContent = `₹${total.toLocaleString('en-IN')}`;
}

async function submitBuyOffer(e) {
    e.preventDefault();
    if (!currentUser || currentUser.role !== 'buyer') {
        await switchDemoRole('buyer');
    }

    const produce_id = parseInt(document.getElementById('offer_produce_id').value);
    const quantity_demanded = parseFloat(document.getElementById('offer_quantity').value);
    const offered_price_per_unit = parseFloat(document.getElementById('offer_price').value);
    const delivery_location = document.getElementById('offer_location').value.trim();
    const message = document.getElementById('offer_message').value.trim();

    try {
        const res = await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                produce_id, quantity_demanded, offered_price_per_unit,
                delivery_location, message
            })
        });
        const data = await res.json();
        if (res.ok) {
            closeBuyOfferModal();
            showToast('🤝 Direct purchase offer sent to the farmer!');
            loadDeals();
            switchTab('deals');
        } else {
            alert(data.error || 'Failed to submit offer');
        }
    } catch (err) {
        console.error('Error submitting offer:', err);
    }
}


// ==========================================
// 6. LIVE MANDI RATES & CHART.JS
// ==========================================

async function loadMandiPrices() {
    try {
        const res = await fetch('/api/mandi_prices');
        const data = await res.json();
        mandiPrices = data.mandi_prices || [];
        renderMandiTable();
    } catch (err) {
        console.error('Error loading mandi prices:', err);
    }
}

function renderMandiTable() {
    const tbody = document.getElementById('mandiTableBody');
    if (!tbody) return;

    tbody.innerHTML = mandiPrices.map(m => {
        const isUp = m.change_trend === 'up';
        const isDown = m.change_trend === 'down';
        const trendBadge = isUp ? 
            `<span class="text-emerald-700 font-bold bg-emerald-100 px-2 py-0.5 rounded">▲ +${m.change_percent}%</span>` :
            (isDown ? `<span class="text-red-700 font-bold bg-red-100 px-2 py-0.5 rounded">▼ ${m.change_percent}%</span>` :
            `<span class="text-slate-700 font-bold bg-gray-100 px-2 py-0.5 rounded">● Stable</span>`);

        return `
            <tr class="hover:bg-kisan-50/50 transition">
                <td class="p-3 font-bold text-slate-900">${m.crop_name}</td>
                <td class="p-3 text-slate-700">${m.market_name}</td>
                <td class="p-3 text-slate-600">${m.state}</td>
                <td class="p-3 text-slate-600">₹${m.min_price}</td>
                <td class="p-3 text-slate-600">₹${m.max_price}</td>
                <td class="p-3 font-extrabold text-kisan-800 text-sm">₹${m.modal_price}</td>
                <td class="p-3">${trendBadge}</td>
            </tr>
        `;
    }).join('');
}

function renderMandiChart() {
    const ctx = document.getElementById('mandiPriceChart');
    if (!ctx) return;

    const selectEl = document.getElementById('mandiChartCropSelect');
    const selectedCrop = selectEl ? selectEl.value : 'Basmati Paddy (बासमती धान)';

    const cropObj = mandiPrices.find(m => m.crop_name === selectedCrop) || mandiPrices[0];
    if (!cropObj) return;

    const history = cropObj.historical_prices || [];
    const labels = history.map(h => h.date);
    const dataPoints = history.map(h => h.price);

    if (mandiChartInstance) {
        mandiChartInstance.destroy();
    }

    mandiChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${cropObj.crop_name} Modal Rate (₹/Quintal)`,
                data: dataPoints,
                borderColor: '#16a34a',
                backgroundColor: 'rgba(22, 163, 74, 0.1)',
                fill: true,
                tension: 0.35,
                pointBackgroundColor: '#14532d',
                pointRadius: 5,
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { font: { family: '"Plus Jakarta Sans"', weight: 'bold' } }
                }
            },
            scales: {
                y: {
                    grid: { color: '#f1f5f9' },
                    ticks: { callback: val => '₹' + val }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

function updateMandiChart() {
    renderMandiChart();
}


// ==========================================
// 7. WEATHER & CROP ADVISORIES
// ==========================================

async function loadAdvisories() {
    try {
        const res = await fetch('/api/advisories');
        const data = await res.json();

        // Populate Weather
        if (data.weather) {
            const w = data.weather;
            document.getElementById('weatherCurrentTemp').textContent = w.current_temp;
            document.getElementById('weatherCondition').textContent = `${w.condition} • ${w.location}`;
            document.getElementById('weatherHumidity').textContent = w.humidity;
            document.getElementById('weatherRainChance').textContent = `${w.rainfall_chance} (Low Risk)`;
            document.getElementById('weatherWind').textContent = w.wind_speed;

            const fGrid = document.getElementById('weatherForecastGrid');
            if (fGrid && w.forecast) {
                fGrid.innerHTML = w.forecast.map(f => `
                    <div class="bg-black/25 p-2.5 rounded-xl border border-teal-600/30 text-center">
                        <div class="font-bold text-teal-200 text-xs">${f.day}</div>
                        <div class="text-sm font-extrabold text-white my-1">${f.temp}</div>
                        <div class="text-[10px] text-teal-100">${f.condition}</div>
                    </div>
                `).join('');
            }
        }

        // Populate Crop Advisories
        const aGrid = document.getElementById('cropAdvisoryGrid');
        if (aGrid && data.crop_advisories) {
            aGrid.innerHTML = data.crop_advisories.map(a => `
                <div class="bg-white rounded-3xl p-5 border border-kisan-200 shadow-sm space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-full">${a.badge}</span>
                        <span class="text-xs text-slate-500 font-semibold">${a.season} Season</span>
                    </div>
                    <div>
                        <h4 class="text-base font-extrabold text-slate-900">${a.crop_name}</h4>
                        <p class="text-xs text-slate-500">Soil: ${a.soil_type}</p>
                    </div>

                    <div class="bg-kisan-50 p-3 rounded-2xl border border-kisan-200 text-xs space-y-1">
                        <strong class="text-kisan-900">🌾 Sowing & Irrigation Tips:</strong>
                        <p class="text-slate-700 text-[11px]">${a.watering_tips}</p>
                    </div>

                    <div class="bg-amber-50 p-3 rounded-2xl border border-amber-200 text-xs space-y-1">
                        <strong class="text-amber-900">🛡️ Pest & Disease Protection:</strong>
                        <p class="text-slate-700 text-[11px]">${a.pest_control_tips}</p>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error('Error loading advisories:', err);
    }
}


// ==========================================
// 8. MY DEALS & NEGOTIATIONS
// ==========================================

async function loadDeals() {
    try {
        const res = await fetch('/api/orders');
        const data = await res.json();
        const orders = data.orders || [];

        const badge = document.getElementById('dealsBadge');
        if (badge) {
            if (orders.length > 0) {
                badge.textContent = orders.length;
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }
        }

        const container = document.getElementById('dealsContainer');
        if (!container) return;

        if (orders.length === 0) {
            container.innerHTML = `
                <div class="py-12 text-center space-y-2 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
                    <span class="text-3xl">🤝</span>
                    <h4 class="text-sm font-bold text-slate-700">No active offers or deals yet</h4>
                    <p class="text-xs text-slate-500">
                        ${currentUser?.role === 'farmer' ? 'Incoming purchase offers from buyers will appear here.' : 'Explore the marketplace and make a direct offer on any crop.'}
                    </p>
                </div>
            `;
            return;
        }

        container.innerHTML = orders.map(o => {
            const isPending = o.status === 'pending';
            const isAccepted = o.status === 'accepted';
            const cleanPhone = (currentUser?.role === 'farmer' ? o.buyer_phone : o.farmer_phone).replace(/[^0-9]/g, '');

            return `
                <div class="p-5 rounded-2xl bg-white border border-kisan-200 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div class="space-y-1">
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-bold ${isPending ? 'bg-amber-100 text-amber-900' : (isAccepted ? 'bg-emerald-100 text-emerald-900' : 'bg-gray-100 text-slate-800')} px-2.5 py-0.5 rounded-full uppercase">
                                ${o.status}
                            </span>
                            <span class="text-xs text-slate-400">${o.created_at}</span>
                        </div>
                        <h4 class="text-base font-extrabold text-slate-900">${o.produce_name}</h4>
                        <p class="text-xs text-slate-600">
                            <strong>${o.quantity_demanded} ${o.produce_unit}</strong> @ ₹${o.offered_price_per_unit}/${o.produce_unit} = <strong class="text-kisan-800">₹${o.total_amount.toLocaleString('en-IN')}</strong>
                        </p>
                        <p class="text-xs text-slate-500 italic">"${o.message}"</p>
                        <div class="text-[11px] text-slate-600">
                            ${currentUser?.role === 'farmer' ? `Buyer: <strong>${o.buyer_name}</strong>` : `Farmer: <strong>${o.farmer_name}</strong>`}
                        </div>
                    </div>

                    <div class="flex flex-wrap items-center gap-2 w-full sm:w-auto">
                        ${currentUser?.role === 'farmer' && isPending ? `
                            <button onclick="updateDealStatus(${o.id}, 'accepted')" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow-sm transition">
                                ✓ Accept Deal
                            </button>
                            <button onclick="updateDealStatus(${o.id}, 'rejected')" class="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-slate-700 text-xs font-bold rounded-xl transition">
                                Decline
                            </button>
                        ` : ''}

                        <a href="https://wa.me/${cleanPhone}?text=Namaste,%20regarding%20our%20KisanMitra%20deal%20for%20${encodeURIComponent(o.produce_name)}..." target="_blank" class="px-4 py-2 bg-emerald-100 hover:bg-emerald-200 text-emerald-900 text-xs font-bold rounded-xl transition flex items-center gap-1">
                            <span>💬 WhatsApp Connect</span>
                        </a>
                    </div>
                </div>
            `;
        }).join('');
    } catch (err) {
        console.error('Error loading deals:', err);
    }
}

async function updateDealStatus(orderId, status) {
    try {
        const res = await fetch(`/api/orders/${orderId}/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });
        if (res.ok) {
            showToast(`Deal marked as ${status}!`);
            loadDeals();
        }
    } catch (err) {
        console.error('Error updating deal status:', err);
    }
}


// ==========================================
// 9. KISAN AI ASSISTANT
// ==========================================

function openKisanAIAssistant() {
    document.getElementById('kisanAIModal').classList.remove('hidden');
    if (window.lucide) lucide.createIcons();
}

function closeKisanAIModal() {
    document.getElementById('kisanAIModal').classList.add('hidden');
}

async function submitAIChat(e) {
    e.preventDefault();
    const input = document.getElementById('aiUserInput');
    const query = input.value.trim();
    if (!query) return;

    const container = document.getElementById('aiChatContainer');

    // Append User Message
    container.innerHTML += `
        <div class="flex gap-2.5 items-start justify-end">
            <div class="bg-kisan-700 text-white p-3 rounded-2xl rounded-tr-none shadow-sm max-w-[85%] text-xs">
                ${query}
            </div>
            <div class="w-7 h-7 rounded-full bg-slate-800 text-white flex items-center justify-center shrink-0 text-xs">👤</div>
        </div>
    `;

    input.value = '';
    container.scrollTop = container.scrollHeight;

    try {
        const res = await fetch('/api/kisan_assistant', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const data = await res.json();

        container.innerHTML += `
            <div class="flex gap-2.5 items-start">
                <div class="w-7 h-7 rounded-full bg-kisan-600 text-white flex items-center justify-center shrink-0 text-xs">🌾</div>
                <div class="bg-white p-3 rounded-2xl rounded-tl-none border border-kisan-200 shadow-sm max-w-[85%] text-slate-800 leading-relaxed text-xs">
                    ${data.response.replace(/\n/g, '<br>')}
                </div>
            </div>
        `;
        container.scrollTop = container.scrollHeight;
    } catch (err) {
        console.error('Error in Kisan AI Assistant:', err);
    }
}


// ==========================================
// 10. USER REGISTRATION MODAL
// ==========================================

function openRegisterModal() {
    document.getElementById('registerModal').classList.remove('hidden');
    toggleUserDropdown();
}

function closeRegisterModal() {
    document.getElementById('registerModal').classList.add('hidden');
}

async function submitRegistration(e) {
    e.preventDefault();
    const role = document.querySelector('input[name="reg_role"]:checked').value;
    const name = document.getElementById('reg_name').value.trim();
    const phone = document.getElementById('reg_phone').value.trim();
    const email_or_phone = document.getElementById('reg_email').value.trim();
    const state = document.getElementById('reg_state').value.trim();
    const district = document.getElementById('reg_district').value.trim();

    try {
        const res = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role, name, phone, email_or_phone, state, district })
        });
        const data = await res.json();
        if (res.ok && data.user) {
            currentUser = data.user;
            updateUserUI();
            closeRegisterModal();
            loadProduce();
            loadDeals();
            showToast(`Welcome ${name}! Registered as ${role.toUpperCase()}`);
        } else {
            alert(data.error || 'Registration failed');
        }
    } catch (err) {
        console.error('Error in registration:', err);
    }
}
