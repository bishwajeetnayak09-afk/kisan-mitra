import os
from flask import Flask, render_template, request, jsonify, session, redirect
from models import db, User, Produce, Scheme, OrderOffer, MandiPrice, CropAdvisory
from seed_data import seed_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kisan-mitra-secret-key-2026'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'kisanmitra.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    seed_database()


def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        if user:
            return user
    # Fallback to default demo farmer
    default_farmer = User.query.filter_by(role='farmer').first()
    if default_farmer:
        session['user_id'] = default_farmer.id
        return default_farmer
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ==========================================
# AUTH & PERSONA SWITCHING ENDPOINTS
# ==========================================

@app.route('/api/auth/current_user', methods=['GET'])
def current_user():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user found'}), 404
    return jsonify({'user': user.to_dict()})


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email_or_phone = data.get('email_or_phone', '').strip()
    password = data.get('password', '').strip()

    if not email_or_phone:
        return jsonify({'error': 'Please provide email or phone number'}), 400

    user = User.query.filter(
        (User.email_or_phone == email_or_phone) | (User.phone == email_or_phone)
    ).first()

    if not user or not user.check_password(password):
        # If demo credentials or testing, find user with role
        return jsonify({'error': 'Invalid credentials. For demo, use quick persona switch or registered account.'}), 401

    session['user_id'] = user.id
    return jsonify({'message': 'Logged in successfully', 'user': user.to_dict()})


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email_or_phone = data.get('email_or_phone', '').strip()
    role = data.get('role', 'farmer').strip().lower()
    phone = data.get('phone', '').strip()
    password = data.get('password', 'kisan123').strip()
    state = data.get('state', 'Uttar Pradesh').strip()
    district = data.get('district', '').strip()
    village_or_city = data.get('village_or_city', '').strip()
    bio = data.get('bio', '').strip()

    if not name or not email_or_phone or not phone:
        return jsonify({'error': 'Name, Phone, and Email/ID are required'}), 400

    existing_user = User.query.filter_by(email_or_phone=email_or_phone).first()
    if existing_user:
        session['user_id'] = existing_user.id
        return jsonify({'message': 'User exists, logged in', 'user': existing_user.to_dict()})

    avatar_icon = 'tractor' if role == 'farmer' else 'shopping-bag'
    new_user = User(
        name=name,
        email_or_phone=email_or_phone,
        role=role,
        phone=phone,
        state=state,
        district=district or ('Varanasi' if role == 'farmer' else 'New Delhi'),
        village_or_city=village_or_city or ('Kisan Colony' if role == 'farmer' else 'City Center'),
        avatar_icon=avatar_icon,
        bio=bio or ('Registered verified farmer on KisanMitra' if role == 'farmer' else 'Verified direct produce buyer'),
        verified=True
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    return jsonify({'message': 'Registration successful', 'user': new_user.to_dict()}), 201


@app.route('/api/auth/switch_demo', methods=['POST'])
def switch_demo():
    data = request.get_json() or {}
    target_role = data.get('role', 'farmer').lower()

    target_user = User.query.filter_by(role=target_role).first()
    if not target_user:
        return jsonify({'error': f'No demo user found for role: {target_role}'}), 404

    session['user_id'] = target_user.id
    return jsonify({
        'message': f'Switched to {target_role.capitalize()} Persona ({target_user.name})',
        'user': target_user.to_dict()
    })


# ==========================================
# GOVERNMENT SCHEMES & ELIGIBILITY ENDPOINTS
# ==========================================

@app.route('/api/schemes', methods=['GET'])
def get_schemes():
    category = request.args.get('category', '').strip()
    search = request.args.get('search', '').strip().lower()

    query = Scheme.query
    if category and category != 'all':
        query = query.filter_by(category=category)

    schemes = query.all()

    if search:
        schemes = [
            s for s in schemes
            if search in s.title_en.lower()
            or search in s.title_hi.lower()
            or search in s.description_en.lower()
            or search in s.eligible_crops.lower()
        ]

    return jsonify({'schemes': [s.to_dict() for s in schemes]})


@app.route('/api/schemes/<int:scheme_id>', methods=['GET'])
def get_scheme_detail(scheme_id):
    scheme = Scheme.query.get_or_404(scheme_id)
    return jsonify({'scheme': scheme.to_dict()})


@app.route('/api/schemes/check_eligibility', methods=['POST'])
def check_eligibility():
    data = request.get_json() or {}
    land_size = float(data.get('land_size', 1.0))
    state = data.get('state', '').strip()
    crop_type = data.get('crop_type', '').strip().lower()
    irrigation = data.get('irrigation', 'any').strip().lower()
    is_organic = bool(data.get('is_organic', False))

    all_schemes = Scheme.query.all()
    matched_schemes = []

    for s in all_schemes:
        match_score = 100
        reasons = []

        # Check land size bounds
        if land_size < s.min_land_hectares:
            match_score -= 30
        elif land_size > s.max_land_hectares:
            match_score -= 20
        else:
            reasons.append(f'Land holding ({land_size} ha) fits scheme limits')

        # Organic bonus
        if is_organic and s.category == 'organic_farming':
            match_score = min(100, match_score + 15)
            reasons.append('Organic cultivator preference applied (+₹50,000 grant eligibility)')

        # Irrigation alignment
        if s.category == 'irrigation' and (irrigation == 'rainfed' or irrigation == 'borewell'):
            reasons.append('Qualifies for high-priority micro-irrigation 55% subsidy')

        # Solar pump alignment
        if s.category == 'solar_energy' and land_size >= 0.5:
            reasons.append('Eligible for PM-KUSUM 60-90% solar pump capital grant')

        if match_score >= 60:
            scheme_dict = s.to_dict()
            scheme_dict['match_score'] = match_score
            scheme_dict['match_reasons'] = reasons
            matched_schemes.append(scheme_dict)

    # Sort by match score descending
    matched_schemes.sort(key=lambda x: x['match_score'], reverse=True)

    return jsonify({
        'total_matched': len(matched_schemes),
        'results': matched_schemes
    })


# ==========================================
# DIRECT PRODUCE MARKETPLACE ENDPOINTS
# ==========================================

@app.route('/api/produce', methods=['GET'])
def get_produce():
    category = request.args.get('category', '').strip()
    search = request.args.get('search', '').strip().lower()
    state = request.args.get('state', '').strip()
    organic_only = request.args.get('organic_only', 'false').lower() == 'true'
    farmer_id = request.args.get('farmer_id', type=int)

    query = Produce.query.order_by(Produce.created_at.desc())

    if farmer_id:
        query = query.filter_by(farmer_id=farmer_id)
    if category and category != 'all':
        query = query.filter_by(category=category)
    if state and state != 'all':
        query = query.filter_by(state=state)
    if organic_only:
        query = query.filter_by(organic_certified=True)

    produce_list = query.all()

    if search:
        produce_list = [
            p for p in produce_list
            if search in p.crop_name.lower()
            or search in p.hindi_name.lower()
            or search in p.variety.lower()
            or search in p.state.lower()
            or search in p.district.lower()
        ]

    return jsonify({'produce': [p.to_dict() for p in produce_list]})


@app.route('/api/produce', methods=['POST'])
def create_produce():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Please log in'}), 401

    data = request.get_json() or {}
    crop_name = data.get('crop_name', '').strip()
    if not crop_name:
        return jsonify({'error': 'Crop name is required'}), 400

    hindi_name = data.get('hindi_name', crop_name)
    category = data.get('category', 'Grains')
    variety = data.get('variety', 'Standard Local')
    quantity = float(data.get('quantity', 10.0))
    unit = data.get('unit', 'Quintal')
    price_per_unit = float(data.get('price_per_unit', 1000.0))
    expected_harvest_date = data.get('expected_harvest_date', 'Ready in Stock')
    state = data.get('state', user.state)
    district = data.get('district', user.district)
    location_text = data.get('location_text', f"{district}, {state}")
    organic_certified = bool(data.get('organic_certified', False))
    description = data.get('description', '')
    image_url = data.get('image_url', '').strip()

    # Preset images based on category if none provided
    if not image_url:
        presets = {
            'Grains': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=600&q=80',
            'Vegetables': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=600&q=80',
            'Fruits': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?auto=format&fit=crop&w=600&q=80',
            'Pulses': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80',
            'Oilseeds': 'https://images.unsplash.com/photo-1508873696983-2df5703bc20d?auto=format&fit=crop&w=600&q=80',
            'Organic Special': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=600&q=80',
            'Spices': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=600&q=80'
        }
        image_url = presets.get(category, presets['Grains'])

    new_produce = Produce(
        farmer_id=user.id,
        crop_name=crop_name,
        hindi_name=hindi_name,
        category=category,
        variety=variety,
        quantity=quantity,
        unit=unit,
        price_per_unit=price_per_unit,
        mandi_benchmark_price=round(price_per_unit * 0.85, 2),
        expected_harvest_date=expected_harvest_date,
        state=state,
        district=district,
        location_text=location_text,
        organic_certified=organic_certified,
        description=description,
        image_url=image_url,
        status='available'
    )
    db.session.add(new_produce)
    db.session.commit()

    return jsonify({'message': 'Harvest listing created successfully', 'produce': new_produce.to_dict()}), 201


@app.route('/api/produce/<int:produce_id>', methods=['PUT'])
def update_produce(produce_id):
    user = get_current_user()
    produce = Produce.query.get_or_404(produce_id)

    if produce.farmer_id != user.id and user.role != 'admin':
        return jsonify({'error': 'Unauthorized to modify this listing'}), 403

    data = request.get_json() or {}
    if 'price_per_unit' in data:
        produce.price_per_unit = float(data['price_per_unit'])
    if 'quantity' in data:
        produce.quantity = float(data['quantity'])
    if 'status' in data:
        produce.status = data['status']
    if 'description' in data:
        produce.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Listing updated', 'produce': produce.to_dict()})


@app.route('/api/produce/<int:produce_id>', methods=['DELETE'])
def delete_produce(produce_id):
    user = get_current_user()
    produce = Produce.query.get_or_404(produce_id)

    if produce.farmer_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(produce)
    db.session.commit()
    return jsonify({'message': 'Listing deleted'})


# ==========================================
# DIRECT DEALS & OFFERS ENDPOINTS
# ==========================================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    user = get_current_user()
    if not user:
        return jsonify({'orders': []})

    if user.role == 'farmer':
        orders = OrderOffer.query.filter_by(farmer_id=user.id).order_by(OrderOffer.created_at.desc()).all()
    else:
        orders = OrderOffer.query.filter_by(buyer_id=user.id).order_by(OrderOffer.created_at.desc()).all()

    return jsonify({'orders': [o.to_dict() for o in orders]})


@app.route('/api/orders', methods=['POST'])
def create_order_offer():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Please log in to make an offer'}), 401

    data = request.get_json() or {}
    produce_id = data.get('produce_id')
    if not produce_id:
        return jsonify({'error': 'Produce ID is required'}), 400

    produce = Produce.query.get_or_404(produce_id)
    quantity = float(data.get('quantity_demanded', 1.0))
    offered_price = float(data.get('offered_price_per_unit', produce.price_per_unit))
    total_amount = round(quantity * offered_price, 2)
    delivery_location = data.get('delivery_location', user.district or 'Direct Pickup')
    message = data.get('message', 'Interested in purchasing fresh harvest directly.')

    new_offer = OrderOffer(
        produce_id=produce.id,
        buyer_id=user.id,
        farmer_id=produce.farmer_id,
        quantity_demanded=quantity,
        offered_price_per_unit=offered_price,
        total_amount=total_amount,
        delivery_location=delivery_location,
        message=message,
        status='pending'
    )
    db.session.add(new_offer)
    db.session.commit()

    # Form direct WhatsApp negotiation URL
    farmer_phone_clean = "".join(filter(str.isdigit, produce.farmer.phone))
    wa_text = f"Namaste {produce.farmer.name} ji, I saw your listing for {produce.crop_name} on KisanMitra. I am offering ₹{offered_price}/{produce.unit} for {quantity} {produce.unit} (Total: ₹{total_amount}). Please connect!"
    whatsapp_url = f"https://wa.me/{farmer_phone_clean}?text={wa_text}"

    return jsonify({
        'message': 'Direct offer submitted to farmer successfully!',
        'order': new_offer.to_dict(),
        'whatsapp_url': whatsapp_url
    }), 201


@app.route('/api/orders/<int:order_id>/status', methods=['POST'])
def update_order_status(order_id):
    user = get_current_user()
    order = OrderOffer.query.get_or_404(order_id)

    if order.farmer_id != user.id and order.buyer_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}
    new_status = data.get('status', 'accepted')
    if new_status in ['pending', 'accepted', 'rejected', 'completed']:
        order.status = new_status
        db.session.commit()
        return jsonify({'message': f'Order status updated to {new_status}', 'order': order.to_dict()})

    return jsonify({'error': 'Invalid status'}), 400


# ==========================================
# LIVE MANDI PRICES & ADVISORIES ENDPOINTS
# ==========================================

@app.route('/api/mandi_prices', methods=['GET'])
def get_mandi_prices():
    crop = request.args.get('crop', '').strip()
    state = request.args.get('state', '').strip()

    query = MandiPrice.query
    if crop and crop != 'all':
        query = query.filter(MandiPrice.crop_name.ilike(f"%{crop}%"))
    if state and state != 'all':
        query = query.filter_by(state=state)

    prices = query.all()
    return jsonify({'mandi_prices': [p.to_dict() for p in prices]})


@app.route('/api/advisories', methods=['GET'])
def get_advisories():
    advisories = CropAdvisory.query.all()
    weather_data = {
        'location': 'North & Central India Agro Zone',
        'current_temp': '29°C',
        'condition': 'Partly Sunny & Favorable',
        'humidity': '62%',
        'rainfall_chance': '15%',
        'wind_speed': '11 km/h',
        'forecast': [
            {'day': 'Wed', 'temp': '30°C', 'icon': 'sun', 'condition': 'Sunny - Ideal for Sowing & Weeding'},
            {'day': 'Thu', 'temp': '29°C', 'icon': 'cloud-sun', 'condition': 'Mild Breeze - Good for Spraying'},
            {'day': 'Fri', 'temp': '28°C', 'icon': 'cloud-rain', 'condition': 'Light Showers (20%) - Delay Irrigation'},
            {'day': 'Sat', 'temp': '31°C', 'icon': 'sun', 'condition': 'Clear Sunshine - Good for Sun-Drying'},
            {'day': 'Sun', 'temp': '30°C', 'icon': 'sun', 'condition': 'Warm & Clear - Harvest Window'}
        ]
    }
    return jsonify({
        'weather': weather_data,
        'crop_advisories': [a.to_dict() for a in advisories]
    })


# ==========================================
# KISAN MITRA AI SMART ASSISTANT
# ==========================================

@app.route('/api/kisan_assistant', methods=['POST'])
def kisan_assistant():
    data = request.get_json() or {}
    user_query = data.get('query', '').strip().lower()

    if not user_query:
        return jsonify({'response': 'Namaste Kisan Brother! How can I assist you with government schemes, fair crop pricing, or pest management today?'})

    # Intelligent intent recognition for agricultural knowledge
    if any(k in user_query for k in ['solar', 'kusum', 'pump', 'बिजली', 'सोलर']):
        resp = "Under the **PM-KUSUM Scheme**, farmers receive a **60% to 90% subsidy** for installing solar agricultural water pumps (3HP to 10HP). You only need to pay 10-40% of the cost. You can apply on `pmkusum.mnre.gov.in` with your Aadhaar, land Khatauni, and borewell details. Would you like to view the full scheme checklist?"
    elif any(k in user_query for k in ['pm-kisan', '6000', 'kisan samman', 'किस्त', 'पैसा']):
        resp = "Under the **PM-Kisan Samman Nidhi**, eligible landholding farmers receive **₹6,000 annually** in three ₹2,000 installments. Ensure your bank account has e-KYC completed and Aadhaar NPCI seeding activated at `pmkisan.gov.in`."
    elif any(k in user_query for k in ['insurance', 'fasal bima', 'crop loss', 'बीमा', 'नुकसान', 'ओले']):
        resp = "Under **PM Fasal Bima Yojana (PMFBY)**, you pay only **2% premium for Kharif crops** and **1.5% for Rabi crops**. In case of crop damage from hail, flood, or drought, file a claim within **72 hours** via the Crop Insurance App or helpline **14447** for fast claim settlement."
    elif any(k in user_query for k in ['organic', 'jaivik', 'जैविक', 'pkvy', 'khad', 'खाद']):
        resp = "Under **PKVY (Paramparagat Krishi Vikas Yojana)**, farmer groups receive **₹50,000 per hectare** over 3 years for organic inputs, PGS certification, and packaging. You can also list certified organic produce directly on KisanMitra to get 20-40% premium rates from consumers!"
    elif any(k in user_query for k in ['sell', 'buyer', 'direct', 'बेचना', 'ग्राहक', 'दाम', 'rate']):
        resp = "On KisanMitra, you can list your crop produce directly using the **'Sell Produce'** tab. Direct buyers contact you over WhatsApp or in-app offer. This eliminates the 15-20% middleman cut, so you earn top dollar and buyers get farm-fresh produce!"
    elif any(k in user_query for k in ['tractor', 'machine', 'smam', 'यंत्र', 'ट्रैक्टर', 'rotavator']):
        resp = "Under the **SMAM (Sub-Mission on Agricultural Mechanization)**, farmers get **50% to 80% subsidy** on Tractors, Rotavators, Harvesters, and Super Seeders. Register on `agrimachinery.nic.in` with dealer proforma invoice."
    else:
        resp = f"Namaste! For '{data.get('query')}', I recommend exploring our **Government Schemes tab** for active subsidies or the **Direct Marketplace** to sell your harvest at zero commission. You can also check our Live Mandi rates to set competitive prices!"

    return jsonify({'response': resp})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
