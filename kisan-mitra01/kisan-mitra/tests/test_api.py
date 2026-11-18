import unittest
import json
from app import app, db
from models import User, Produce, Scheme, OrderOffer, MandiPrice

class KisanMitraTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            from seed_data import seed_database
            seed_database()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_homepage_render(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'KisanMitra', response.data)

    def test_current_user_and_switch_demo(self):
        # Default user
        res = self.client.get('/api/auth/current_user')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['user']['role'], 'farmer')

        # Switch to Buyer
        res = self.client.post('/api/auth/switch_demo', json={'role': 'buyer'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['user']['role'], 'buyer')

    def test_schemes_and_eligibility(self):
        # Fetch all schemes
        res = self.client.get('/api/schemes')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['schemes']), 5)

        # Check eligibility for small organic farmer in UP
        payload = {
            'land_size': 1.5,
            'state': 'Uttar Pradesh',
            'crop_type': 'wheat_paddy',
            'irrigation': 'borewell',
            'is_organic': True
        }
        res = self.client.post('/api/schemes/check_eligibility', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(data['total_matched'], 3)
        self.assertTrue(any('PM-Kisan' in s['title_en'] for s in data['results']))

    def test_produce_marketplace_and_orders(self):
        # Fetch produce listings
        res = self.client.get('/api/produce')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['produce']), 3)

        produce_item = data['produce'][0]
        farmer_id = produce_item['farmer_id']

        # Login as buyer and create direct purchase offer
        self.client.post('/api/auth/switch_demo', json={'role': 'buyer'})
        offer_payload = {
            'produce_id': produce_item['id'],
            'quantity_demanded': 5.0,
            'offered_price_per_unit': produce_item['price_per_unit'],
            'delivery_location': 'South Delhi Hub',
            'message': 'Need 5 quintals of organic harvest delivered.'
        }
        res = self.client.post('/api/orders', json=offer_payload)
        self.assertEqual(res.status_code, 201)
        order_data = json.loads(res.data)
        self.assertIn('whatsapp_url', order_data)
        self.assertEqual(order_data['order']['quantity_demanded'], 5.0)

        # Set session to the specific farmer who owns this produce
        with self.client.session_transaction() as sess:
            sess['user_id'] = farmer_id

        res = self.client.get('/api/orders')
        self.assertEqual(res.status_code, 200)
        orders = json.loads(res.data)['orders']
        self.assertGreaterEqual(len(orders), 1)

        # Farmer accepts offer
        order_id = orders[0]['id']
        res = self.client.post(f'/api/orders/{order_id}/status', json={'status': 'accepted'})
        self.assertEqual(res.status_code, 200)
        updated_order = json.loads(res.data)['order']
        self.assertEqual(updated_order['status'], 'accepted')

    def test_mandi_prices_and_advisories(self):
        # Mandi prices
        res = self.client.get('/api/mandi_prices')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data['mandi_prices']), 3)

        # Advisories
        res = self.client.get('/api/advisories')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('weather', data)
        self.assertIn('crop_advisories', data)

    def test_login_page_and_credentials(self):
        # 1. Test GET /login page
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Farmer Portal', res.data)
        self.assertIn(b'Buyer Portal', res.data)

        # 2. Test Farmer credential login
        res = self.client.post('/api/auth/login', json={
            'email_or_phone': 'farmer@kisanmitra.in',
            'password': 'farmer123'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['user']['role'], 'farmer')

        # 3. Test Buyer credential login
        res = self.client.post('/api/auth/login', json={
            'email_or_phone': 'buyer@kisanmitra.in',
            'password': 'buyer123'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['user']['role'], 'buyer')

        # 4. Test Logout
        res = self.client.get('/logout')
        self.assertEqual(res.status_code, 302)  # Redirects to /login

if __name__ == '__main__':
    unittest.main()
