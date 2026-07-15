import unittest
from bson import ObjectId
from datetime import datetime, timedelta
import app
from pymongo import MongoClient

class HotelManagementTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Override MongoDB connection in app to isolate tests
        cls.test_client = MongoClient("mongodb://localhost:27017/")
        cls.test_db = cls.test_client["hotel_management_test"]
        
        # Override the app's db reference
        app.db = cls.test_db

    def setUp(self):
        self.flask_client = app.app.test_client()
        # Clear collections before each test to ensure clean state
        self.test_db.users.delete_many({})
        self.test_db.rooms.delete_many({})
        self.test_db.bookings.delete_many({})
        self.test_db.allbookings.delete_many({})
        self.test_db.freq_booking_collection.delete_many({})
        self.test_db.admins.delete_many({})

        # Setup base room types for test purposes
        self.room_types = [
            {'room_type': 'Standard Room - Single Bed', 'room_number': 'SSB-TEST-1', 'status': 'available', 'user_token': None, 'price_per_day': 1000, 'free_date': None},
            {'room_type': 'Standard Room - Double Bed', 'room_number': 'SDB-TEST-1', 'status': 'available', 'user_token': None, 'price_per_day': 1500, 'free_date': None}
        ]
        self.test_db.rooms.insert_many(self.room_types)

        # Setup admin account
        # admin password is 'admin123'
        self.admin_pass_hash = app.generate_password_hash("admin123")
        self.admin_doc = {
            'username': 'admin',
            'password': self.admin_pass_hash
        }
        self.test_db.admins.insert_one(self.admin_doc)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # Drop test database completely after testing finishes
        cls.test_client.drop_database("hotel_management_test")

    # ==========================================
    # USER FUNCTIONALITY TESTS
    # ==========================================

    def test_user_registration_success(self):
        # Test registering a new user with valid inputs
        data = {
            'name': 'Test User',
            'email': 'testuser@gmail.com',
            'phone': '1234567890',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }
        resp = self.flask_client.post('/register', data=data)
        # Should redirect to login on success (302)
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login', resp.location)

        # Check DB entries
        user = self.test_db.users.find_one({'email': 'testuser@gmail.com'})
        self.assertIsNotNone(user)
        self.assertEqual(user['name'], 'Test User')
        self.assertTrue(app.check_password_hash(user['password'], 'Password123!'))
        self.assertIsNotNone(user['user_token'])
        
        # Verify secondary table registration (frequency booking track)
        freq_record = self.test_db.freq_booking_collection.find_one({'user_token': user['user_token']})
        self.assertIsNotNone(freq_record)
        self.assertEqual(freq_record['ssb_count'], 0)
        self.assertEqual(freq_record['sdb_count'], 0)

    def test_user_registration_mismatch_passwords(self):
        # Test registering with mismatching passwords
        data = {
            'name': 'Test Mismatch',
            'email': 'mismatch@gmail.com',
            'phone': '1234567890',
            'password': 'Password123!',
            'confirm_password': 'Different123!'
        }
        resp = self.flask_client.post('/register', data=data)
        # Should render registration page again (redirects to /register or returns status 302/200 depending on flask route)
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/register', resp.location)
        
        # Verify user was NOT created
        user = self.test_db.users.find_one({'email': 'mismatch@gmail.com'})
        self.assertIsNone(user)

    def test_user_registration_duplicate_email(self):
        # Setup existing user
        self.test_db.users.insert_one({
            'name': 'Existing User',
            'email': 'duplicate@gmail.com',
            'phone': '0987654321',
            'password': self.admin_pass_hash,
            'user_token': 'LUX-EXIST-1111',
            'created_at': datetime.utcnow()
        })

        data = {
            'name': 'New User',
            'email': 'duplicate@gmail.com',
            'phone': '1234567890',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }
        resp = self.flask_client.post('/register', data=data)
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/register', resp.location)

    def test_user_login_success(self):
        # Setup user
        pwd_hash = app.generate_password_hash("password123")
        user_doc = {
            'name': 'Abi User',
            'email': 'abi@gmail.com',
            'phone': '1234567890',
            'password': pwd_hash,
            'user_token': 'LUX-ABI-1234',
            'created_at': datetime.utcnow()
        }
        self.test_db.users.insert_one(user_doc)

        # Login request
        resp = self.flask_client.post('/login', data={'email': 'abi@gmail.com', 'password': 'password123'})
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/', resp.location) # redirects to home

        # Verify session variables
        with self.flask_client.session_transaction() as sess:
            self.assertEqual(sess['user_name'], 'Abi User')
            self.assertEqual(sess['user_token'], 'LUX-ABI-1234')
            self.assertIsNotNone(sess['user_id'])

    def test_user_login_fail(self):
        resp = self.flask_client.post('/login', data={'email': 'nonexistent@gmail.com', 'password': 'wrongpassword'})
        # Should return 200 OK rendering login page again
        self.assertEqual(resp.status_code, 200)
        with self.flask_client.session_transaction() as sess:
            self.assertNotIn('user_id', sess)

    def test_user_logout(self):
        with self.flask_client.session_transaction() as sess:
            sess['user_id'] = 'some-user-id'
            sess['user_name'] = 'testuser'
            sess['user_token'] = 'LUX-TEST'

        resp = self.flask_client.get('/logout')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login', resp.location)

        with self.flask_client.session_transaction() as sess:
            self.assertNotIn('user_id', sess)
            self.assertNotIn('user_token', sess)

    def test_room_booking_flow_and_validation(self):
        # Register a mock user session
        user_id = str(ObjectId())
        with self.flask_client.session_transaction() as sess:
            sess['user_id'] = user_id
            sess['user_name'] = 'Abi User'
            sess['user_token'] = 'LUX-ABI-1234'

        # Insert user document matching session ID
        self.test_db.users.insert_one({
            '_id': ObjectId(user_id),
            'name': 'Abi User',
            'email': 'abi@gmail.com',
            'phone': '1234567890',
            'password': 'hashedpwd',
            'user_token': 'LUX-ABI-1234'
        })

        # Scenario A: Invalid Dates range (checkout <= checkin)
        booking_data_invalid = {
            'room_number': 'SSB-TEST-1',
            'check_in': '2026-08-10',
            'check_out': '2026-08-10',  # checkout == checkin
            'num_persons': '2'
        }
        resp = self.flask_client.post('/rooms', data=booking_data_invalid)
        # Should fail date validations and redirect back to rooms view (302)
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/rooms', resp.location)
        self.assertEqual(self.test_db.bookings.count_documents({}), 0)

        # Scenario A2: Past Check-in Date
        booking_data_past = {
            'room_number': 'SSB-TEST-1',
            'check_in': '2020-01-01',  # past check-in
            'check_out': '2026-08-12',
            'num_persons': '2'
        }
        resp_past = self.flask_client.post('/rooms', data=booking_data_past)
        self.assertEqual(resp_past.status_code, 302)
        self.assertIn('/rooms', resp_past.location)
        self.assertEqual(self.test_db.bookings.count_documents({}), 0)

        # Scenario B: Valid Date Range
        booking_data_valid = {
            'room_number': 'SSB-TEST-1',
            'check_in': '2026-08-10',
            'check_out': '2026-08-12', # 2 days stay
            'num_persons': '2'
        }
        resp_valid = self.flask_client.post('/rooms', data=booking_data_valid)
        self.assertEqual(resp_valid.status_code, 200) # Renders booking_confirmation.html
        
        # Verify DB updates
        booking = self.test_db.bookings.find_one({'room_number': 'SSB-TEST-1'})
        self.assertIsNotNone(booking)
        self.assertEqual(booking['user_token'], 'LUX-ABI-1234')
        self.assertEqual(booking['num_persons'], '2')
        self.assertEqual(booking['check_in'], datetime(2026, 8, 10))
        self.assertEqual(booking['check_out'], datetime(2026, 8, 12))

        # Check room status updated to booked
        room = self.test_db.rooms.find_one({'room_number': 'SSB-TEST-1'})
        self.assertEqual(room['status'], 'booked')
        self.assertEqual(room['user_token'], 'LUX-ABI-1234')
        self.assertEqual(room['free_date'], datetime(2026, 8, 12))

    # ==========================================
    # ADMIN FUNCTIONALITY TESTS
    # ==========================================

    def test_admin_dashboard_protection(self):
        # 1. Access without authorization
        resp = self.flask_client.get('/admin/dashboard')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/admin/login', resp.location)

        # 2. Access with valid admin session
        admin_doc = self.test_db.admins.find_one({'username': 'admin'})
        with self.flask_client.session_transaction() as sess:
            sess['admin_id'] = str(admin_doc['_id'])

        resp_auth = self.flask_client.get('/admin/dashboard')
        self.assertEqual(resp_auth.status_code, 200)

    def test_admin_booking_approval_and_rejection(self):
        admin_doc = self.test_db.admins.find_one({'username': 'admin'})
        with self.flask_client.session_transaction() as sess:
            sess['admin_id'] = str(admin_doc['_id'])

        # Setup a pending booking doc
        user_token = "LUX-ABI-1234"
        room_num = "SDB-TEST-1"
        self.test_db.rooms.update_one({'room_number': room_num}, {'$set': {'status': 'booked', 'user_token': user_token}})
        
        booking_doc = {
            'user_id': 'some-id',
            'user_name': 'Abi',
            'user_email': 'abi@gmail.com',
            'user_phone': '1234567890',
            'user_token': user_token,
            'room_number': room_num,
            'room_type': 'Standard Room - Double Bed',
            'num_persons': '2',
            'check_in': datetime.utcnow(),
            'check_out': datetime.utcnow() + timedelta(days=2),
            'booking_date': datetime.utcnow(),
            'status': 'Pending'
        }
        self.test_db.bookings.insert_one(booking_doc)
        booking_id = str(booking_doc['_id'])

        # 1. Approve Booking
        resp_app = self.flask_client.get(f'/approve_booking/{booking_id}')
        self.assertEqual(resp_app.status_code, 302)
        
        # Verify approval in active bookings and allbookings list
        app_booking = self.test_db.bookings.find_one({'_id': ObjectId(booking_id)})
        self.assertEqual(app_booking['status'], 'Approved')
        
        archived_booking = self.test_db.allbookings.find_one({'_id': ObjectId(booking_id)})
        self.assertIsNotNone(archived_booking)
        self.assertEqual(archived_booking['status'], 'Approved')

        # 2. Setup a second pending booking to test Reject
        self.test_db.rooms.update_one({'room_number': room_num}, {'$set': {'status': 'booked', 'user_token': user_token}})
        booking_doc_2 = {
            'user_id': 'some-id',
            'user_name': 'Abi',
            'user_email': 'abi@gmail.com',
            'user_phone': '1234567890',
            'user_token': user_token,
            'room_number': room_num,
            'room_type': 'Standard Room - Double Bed',
            'num_persons': '2',
            'check_in': datetime.utcnow(),
            'check_out': datetime.utcnow() + timedelta(days=2),
            'booking_date': datetime.utcnow(),
            'status': 'Pending'
        }
        self.test_db.bookings.insert_one(booking_doc_2)
        booking_id_2 = str(booking_doc_2['_id'])

        # Reject the second pending booking
        resp_rej = self.flask_client.get(f'/reject_booking/{booking_id_2}')
        self.assertEqual(resp_rej.status_code, 302)
        
        # Check bookings is deleted, room released, but FIRST booking in allbookings remains!
        self.assertIsNone(self.test_db.bookings.find_one({'_id': ObjectId(booking_id_2)}))
        self.assertIsNone(self.test_db.allbookings.find_one({'_id': ObjectId(booking_id_2)}))
        
        # Confirm historical booking is untouched
        self.assertIsNotNone(self.test_db.allbookings.find_one({'_id': ObjectId(booking_id)}))
        
        released_room = self.test_db.rooms.find_one({'room_number': room_num})
        self.assertEqual(released_room['status'], 'available')
        self.assertIsNone(released_room['user_token'])

    def test_admin_lock_and_release_room(self):
        admin_doc = self.test_db.admins.find_one({'username': 'admin'})
        with self.flask_client.session_transaction() as sess:
            sess['admin_id'] = str(admin_doc['_id'])

        room_num = "SSB-TEST-1"
        free_date_str = "2026-12-25"

        # 1. Lock room
        resp = self.flask_client.post(f'/lock_room/{room_num}', data={'free_date': free_date_str})
        self.assertEqual(resp.status_code, 302)
        
        # Verify Locked status
        room = self.test_db.rooms.find_one({'room_number': room_num})
        self.assertEqual(room['status'], 'locked')
        self.assertEqual(room['free_date'], datetime(2026, 12, 25))

        # Test Case: Try locking with a date in the past
        past_date_str = "2020-01-01"
        resp_past = self.flask_client.post(f'/lock_room/{room_num}', data={'free_date': past_date_str})
        self.assertEqual(resp_past.status_code, 400) # Rejects past date

        # 2. Release room
        resp_rel = self.flask_client.post(f'/release_room/{room_num}')
        self.assertEqual(resp_rel.status_code, 302)
        
        room_rel = self.test_db.rooms.find_one({'room_number': room_num})
        self.assertEqual(room_rel['status'], 'available')
        self.assertIsNone(room_rel['free_date'])

    def test_admin_dynamic_pricing_prediction(self):
        admin_doc = self.test_db.admins.find_one({'username': 'admin'})
        with self.flask_client.session_transaction() as sess:
            sess['admin_id'] = str(admin_doc['_id'])

        # Create mock check-ins in allbookings to simulate historical usage data
        booking_mock = {
            'room_type': 'Standard Room - Single Bed',
            'check_in': datetime(2026, 1, 1),
            'check_out': datetime(2026, 1, 5) # 4 days stayed
        }
        self.test_db.allbookings.insert_one(booking_mock)

        resp = self.flask_client.get('/predict')
        # Expecting successful rendering after scikit-learn dependency is verified
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')
        self.assertIn("Standard Room - Single Bed", html)

    def test_user_rewards_cycle_calculations(self):
        # Register a mock user session
        user_id = str(ObjectId())
        with self.flask_client.session_transaction() as sess:
            sess['user_id'] = user_id
            sess['user_name'] = 'Reward User'
            sess['user_token'] = 'LUX-REWARD-1234'

        # Insert user document matching session ID
        self.test_db.users.insert_one({
            '_id': ObjectId(user_id),
            'name': 'Reward User',
            'email': 'reward@gmail.com',
            'phone': '1234567890',
            'password': 'hashedpwd',
            'user_token': 'LUX-REWARD-1234'
        })

        # Test Case 1: 0 stays (ssb_progress = 0, earned = 0, needed = 5)
        resp1 = self.flask_client.get('/rewards')
        self.assertEqual(resp1.status_code, 200)
        html1 = resp1.data.decode('utf-8')
        self.assertIn("0 / 5", html1)
        self.assertIn("5", html1) # needs 5 more SSB stays

        # Insert 5 approved bookings for SSB (so ssb_progress will be 5, next stays free)
        mock_bookings = []
        for i in range(5):
            mock_bookings.append({
                'user_token': 'LUX-REWARD-1234',
                'room_type': 'Standard Room - Single Bed',
                'status': 'Approved',
                'check_in': datetime.utcnow(),
                'check_out': datetime.utcnow() + timedelta(days=1)
            })
        self.test_db.allbookings.insert_many(mock_bookings)

        # Test Case 2: 5 stays (ssb_progress = 5, next stay free!)
        resp2 = self.flask_client.get('/rewards')
        self.assertEqual(resp2.status_code, 200)
        html2 = resp2.data.decode('utf-8')
        self.assertIn("5 / 5", html2)
        self.assertIn("Congratulations! Your next (6th) SSB booking will be FREE!", html2)

        # Insert 1 more stay (total 6 stays, so ssb_progress resets to 0, ssb_earned_free becomes 1)
        self.test_db.allbookings.insert_one({
            'user_token': 'LUX-REWARD-1234',
            'room_type': 'Standard Room - Single Bed',
            'status': 'Approved',
            'check_in': datetime.utcnow(),
            'check_out': datetime.utcnow() + timedelta(days=1)
        })

        # Test Case 3: 6 stays (ssb_progress resets to 0, earned = 1, needed = 5)
        resp3 = self.flask_client.get('/rewards')
        self.assertEqual(resp3.status_code, 200)
        html3 = resp3.data.decode('utf-8')
        self.assertIn("0 / 5", html3)
        self.assertIn("1", html3) # Earned 1 free rooms
        self.assertIn("5", html3) # needs 5 more SSB stays

if __name__ == "__main__":
    unittest.main()
