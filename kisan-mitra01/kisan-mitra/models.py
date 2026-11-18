from datetime import datetime, timezone
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email_or_phone = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='farmer')  # 'farmer' or 'buyer'
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(100), default='Uttar Pradesh')
    district = db.Column(db.String(100), default='Varanasi')
    village_or_city = db.Column(db.String(100), default='Rampur')
    avatar_icon = db.Column(db.String(50), default='seedling')
    verified = db.Column(db.Boolean, default=True)
    bio = db.Column(db.String(300), default='')
    rating = db.Column(db.Float, default=4.8)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    produce_listings = db.relationship('Produce', backref='farmer', lazy=True, cascade="all, delete-orphan")
    offers_made = db.relationship('OrderOffer', foreign_keys='OrderOffer.buyer_id', backref='buyer', lazy=True)
    offers_received = db.relationship('OrderOffer', foreign_keys='OrderOffer.farmer_id', backref='farmer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email_or_phone': self.email_or_phone,
            'role': self.role,
            'phone': self.phone,
            'state': self.state,
            'district': self.district,
            'village_or_city': self.village_or_city,
            'avatar_icon': self.avatar_icon,
            'verified': self.verified,
            'bio': self.bio,
            'rating': self.rating,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else ''
        }


class Produce(db.Model):
    __tablename__ = 'produce'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_name = db.Column(db.String(120), nullable=False)
    hindi_name = db.Column(db.String(120), default='')
    category = db.Column(db.String(50), nullable=False)  # Grains, Vegetables, Fruits, Pulses, Oilseeds, Spices, Organic, Dairy/Honey
    variety = db.Column(db.String(100), default='Standard')
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='Quintal')  # Quintal, kg, Ton, Box
    price_per_unit = db.Column(db.Float, nullable=False)  # Price in INR
    mandi_benchmark_price = db.Column(db.Float, default=0.0)  # Reference APMC Mandi price
    expected_harvest_date = db.Column(db.String(50), default='Fresh Harvest Ready')
    state = db.Column(db.String(100), default='Uttar Pradesh')
    district = db.Column(db.String(100), default='Varanasi')
    location_text = db.Column(db.String(200), default='')
    organic_certified = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, default='')
    image_url = db.Column(db.String(300), default='')
    status = db.Column(db.String(30), default='available')  # available, in_deal, sold
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    offers = db.relationship('OrderOffer', backref='produce', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        farmer_data = self.farmer.to_dict() if self.farmer else None
        # Calculate middleman savings comparison
        # Usually middlemen take 15-25% margin. Here farmer gets full price and buyer saves ~15%.
        est_market_retail = round(self.price_per_unit * 1.25, 2)
        middleman_margin = round(self.price_per_unit * 0.20, 2)

        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farmer_name': farmer_data['name'] if farmer_data else 'Kisan Brother',
            'farmer_phone': farmer_data['phone'] if farmer_data else '',
            'farmer_verified': farmer_data['verified'] if farmer_data else True,
            'farmer_rating': farmer_data['rating'] if farmer_data else 4.8,
            'crop_name': self.crop_name,
            'hindi_name': self.hindi_name,
            'category': self.category,
            'variety': self.variety,
            'quantity': self.quantity,
            'unit': self.unit,
            'price_per_unit': self.price_per_unit,
            'mandi_benchmark_price': self.mandi_benchmark_price or round(self.price_per_unit * 0.85, 2),
            'est_market_retail': est_market_retail,
            'middleman_saving': middleman_margin,
            'expected_harvest_date': self.expected_harvest_date,
            'state': self.state,
            'district': self.district,
            'location_text': self.location_text or f"{self.district}, {self.state}",
            'organic_certified': self.organic_certified,
            'description': self.description,
            'image_url': self.image_url,
            'status': self.status,
            'views': self.views,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else ''
        }


class Scheme(db.Model):
    __tablename__ = 'schemes'

    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_hi = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # financial_subsidy, crop_insurance, solar_energy, irrigation, credit_loan, organic_farming, machinery_tools, pension_welfare
    organizing_body = db.Column(db.String(150), default='Ministry of Agriculture & Farmers Welfare, Govt of India')
    description_en = db.Column(db.Text, nullable=False)
    description_hi = db.Column(db.Text, nullable=False)
    subsidy_amount_text = db.Column(db.String(150), default='Direct Financial Benefit')
    max_benefit_amount = db.Column(db.Float, default=0.0)
    subsidy_percentage = db.Column(db.String(50), default='Up to 50-80%')
    eligible_land_type = db.Column(db.String(50), default='all')  # all, marginal_small, medium, large
    min_land_hectares = db.Column(db.Float, default=0.0)
    max_land_hectares = db.Column(db.Float, default=100.0)
    eligible_crops = db.Column(db.String(250), default='All Agricultural & Horticultural Crops')
    eligible_states = db.Column(db.String(250), default='All States & UTs across India')
    irrigation_required = db.Column(db.String(50), default='any')  # any, rainfed, irrigated
    documents_required = db.Column(db.Text, default='[]')  # JSON Array of strings
    application_steps = db.Column(db.Text, default='[]')  # JSON Array of strings
    official_url = db.Column(db.String(300), default='https://agricoop.nic.in')
    helpline_number = db.Column(db.String(50), default='155261 / 1800-115-526')
    deadline_info = db.Column(db.String(100), default='Open Round the Year')
    badge_color = db.Column(db.String(30), default='emerald')
    icon_name = db.Column(db.String(50), default='award')

    def get_documents_list(self):
        try:
            return json.loads(self.documents_required)
        except Exception:
            return []

    def get_application_steps_list(self):
        try:
            return json.loads(self.application_steps)
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'title_en': self.title_en,
            'title_hi': self.title_hi,
            'category': self.category,
            'organizing_body': self.organizing_body,
            'description_en': self.description_en,
            'description_hi': self.description_hi,
            'subsidy_amount_text': self.subsidy_amount_text,
            'max_benefit_amount': self.max_benefit_amount,
            'subsidy_percentage': self.subsidy_percentage,
            'eligible_land_type': self.eligible_land_type,
            'min_land_hectares': self.min_land_hectares,
            'max_land_hectares': self.max_land_hectares,
            'eligible_crops': self.eligible_crops,
            'eligible_states': self.eligible_states,
            'irrigation_required': self.irrigation_required,
            'documents_required': self.get_documents_list(),
            'application_steps': self.get_application_steps_list(),
            'official_url': self.official_url,
            'helpline_number': self.helpline_number,
            'deadline_info': self.deadline_info,
            'badge_color': self.badge_color,
            'icon_name': self.icon_name
        }


class OrderOffer(db.Model):
    __tablename__ = 'order_offers'

    id = db.Column(db.Integer, primary_key=True)
    produce_id = db.Column(db.Integer, db.ForeignKey('produce.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity_demanded = db.Column(db.Float, nullable=False)
    offered_price_per_unit = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    delivery_location = db.Column(db.String(200), default='')
    message = db.Column(db.Text, default='')
    status = db.Column(db.String(30), default='pending')  # pending, accepted, rejected, completed
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        buyer_data = self.buyer.to_dict() if self.buyer else None
        farmer_data = self.farmer.to_dict() if self.farmer else None
        produce_data = self.produce.to_dict() if self.produce else None

        return {
            'id': self.id,
            'produce_id': self.produce_id,
            'produce_name': produce_data['crop_name'] if produce_data else 'Crop Produce',
            'produce_unit': produce_data['unit'] if produce_data else 'kg',
            'buyer_id': self.buyer_id,
            'buyer_name': buyer_data['name'] if buyer_data else 'Direct Buyer',
            'buyer_phone': buyer_data['phone'] if buyer_data else '',
            'farmer_id': self.farmer_id,
            'farmer_name': farmer_data['name'] if farmer_data else 'Kisan Brother',
            'farmer_phone': farmer_data['phone'] if farmer_data else '',
            'quantity_demanded': self.quantity_demanded,
            'offered_price_per_unit': self.offered_price_per_unit,
            'total_amount': self.total_amount,
            'delivery_location': self.delivery_location,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class MandiPrice(db.Model):
    __tablename__ = 'mandi_prices'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    hindi_name = db.Column(db.String(100), default='')
    category = db.Column(db.String(50), default='Grains')
    market_name = db.Column(db.String(120), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    min_price = db.Column(db.Float, nullable=False)  # INR per Quintal
    max_price = db.Column(db.Float, nullable=False)
    modal_price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='₹/Quintal')
    change_trend = db.Column(db.String(20), default='up')  # 'up', 'down', 'stable'
    change_percent = db.Column(db.Float, default=+2.5)
    historical_prices_json = db.Column(db.Text, default='[]')
    updated_date = db.Column(db.String(50), default='Today')

    def get_history(self):
        try:
            return json.loads(self.historical_prices_json)
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'hindi_name': self.hindi_name,
            'category': self.category,
            'market_name': self.market_name,
            'district': self.district,
            'state': self.state,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'modal_price': self.modal_price,
            'unit': self.unit,
            'change_trend': self.change_trend,
            'change_percent': self.change_percent,
            'historical_prices': self.get_history(),
            'updated_date': self.updated_date
        }


class CropAdvisory(db.Model):
    __tablename__ = 'crop_advisories'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    hindi_name = db.Column(db.String(100), default='')
    season = db.Column(db.String(50), default='Kharif')  # Kharif, Rabi, Zaid
    soil_type = db.Column(db.String(100), default='Loamy to Clayey')
    sowing_window = db.Column(db.String(100), default='June - July')
    harvesting_window = db.Column(db.String(100), default='October - November')
    watering_tips = db.Column(db.Text, default='')
    pest_control_tips = db.Column(db.Text, default='')
    fertilizer_tips = db.Column(db.Text, default='')
    weather_alert = db.Column(db.String(250), default='')
    badge = db.Column(db.String(50), default='Recommended Sowing')

    def to_dict(self):
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'hindi_name': self.hindi_name,
            'season': self.season,
            'soil_type': self.soil_type,
            'sowing_window': self.sowing_window,
            'harvesting_window': self.harvesting_window,
            'watering_tips': self.watering_tips,
            'pest_control_tips': self.pest_control_tips,
            'fertilizer_tips': self.fertilizer_tips,
            'weather_alert': self.weather_alert,
            'badge': self.badge
        }
