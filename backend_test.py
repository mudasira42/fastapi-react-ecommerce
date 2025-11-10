import requests
import sys
import json
from datetime import datetime

class ECommerceAPITester:
    def __init__(self, base_url="https://webshop-stack.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, params=data)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if not success:
                try:
                    error_data = response.json()
                    details += f", Response: {error_data}"
                except:
                    details += f", Response: {response.text[:200]}"
            
            self.log_test(name, success, details)
            
            if success:
                try:
                    return response.json()
                except:
                    return {}
            return None

        except Exception as e:
            self.log_test(name, False, f"Exception: {str(e)}")
            return None

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_user_registration(self):
        """Test user registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        user_data = {
            "name": f"Test User {timestamp}",
            "email": f"test{timestamp}@example.com",
            "password": "TestPass123!"
        }
        
        response = self.run_test("User Registration", "POST", "auth/register", 200, user_data)
        if response:
            self.token = response.get('access_token')
            self.user_id = response.get('user', {}).get('id')
            return True
        return False

    def test_user_login(self):
        """Test user login with existing credentials"""
        # First register a user
        timestamp = datetime.now().strftime('%H%M%S')
        user_data = {
            "name": f"Login Test User {timestamp}",
            "email": f"logintest{timestamp}@example.com",
            "password": "TestPass123!"
        }
        
        # Register
        reg_response = self.run_test("Pre-Login Registration", "POST", "auth/register", 200, user_data)
        if not reg_response:
            return False
        
        # Now test login
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        response = self.run_test("User Login", "POST", "auth/login", 200, login_data)
        if response:
            self.token = response.get('access_token')
            self.user_id = response.get('user', {}).get('id')
            return True
        return False

    def test_get_user_profile(self):
        """Test getting current user profile"""
        if not self.token:
            self.log_test("Get User Profile", False, "No token available")
            return False
        
        response = self.run_test("Get User Profile", "GET", "auth/me", 200)
        return response is not None

    def test_get_products(self):
        """Test getting all products"""
        response = self.run_test("Get All Products", "GET", "products", 200)
        if response and isinstance(response, list):
            print(f"   Found {len(response)} products")
            return len(response) > 0
        return False

    def test_search_products(self):
        """Test product search functionality"""
        # Test search by name
        response = self.run_test("Search Products by Name", "GET", "products", 200, {"search": "laptop"})
        if response is not None:
            print(f"   Search 'laptop' returned {len(response)} products")
        
        # Test filter by category
        response = self.run_test("Filter Products by Category", "GET", "products", 200, {"category": "Electronics"})
        if response is not None:
            print(f"   Category 'Electronics' returned {len(response)} products")
            return True
        return False

    def test_get_single_product(self):
        """Test getting a single product"""
        # First get all products to get a valid ID
        products = self.run_test("Get Products for Single Test", "GET", "products", 200)
        if not products or len(products) == 0:
            self.log_test("Get Single Product", False, "No products available")
            return False
        
        product_id = products[0]['id']
        response = self.run_test("Get Single Product", "GET", f"products/{product_id}", 200)
        return response is not None

    def test_cart_operations(self):
        """Test cart CRUD operations"""
        if not self.token:
            self.log_test("Cart Operations", False, "No authentication token")
            return False
        
        # Get products first
        products = self.run_test("Get Products for Cart Test", "GET", "products", 200)
        if not products or len(products) == 0:
            self.log_test("Cart Operations", False, "No products available")
            return False
        
        product_id = products[0]['id']
        
        # Test getting empty cart
        cart = self.run_test("Get Empty Cart", "GET", "cart", 200)
        if cart is None:
            return False
        
        # Test adding to cart
        add_data = {"product_id": product_id, "quantity": 2}
        cart_item = self.run_test("Add to Cart", "POST", "cart", 200, add_data)
        if not cart_item:
            return False
        
        cart_item_id = cart_item.get('id')
        if not cart_item_id:
            self.log_test("Cart Operations", False, "No cart item ID returned")
            return False
        
        # Test updating cart item
        update_data = {"quantity": 3}
        updated_item = self.run_test("Update Cart Item", "PATCH", f"cart/{cart_item_id}", 200, update_data)
        if not updated_item:
            return False
        
        # Test getting cart with items
        cart_with_items = self.run_test("Get Cart with Items", "GET", "cart", 200)
        if not cart_with_items or len(cart_with_items) == 0:
            self.log_test("Cart Operations", False, "Cart should have items")
            return False
        
        # Test removing from cart
        self.run_test("Remove from Cart", "DELETE", f"cart/{cart_item_id}", 200)
        
        return True

    def test_cart_sync(self):
        """Test guest cart sync functionality"""
        if not self.token:
            self.log_test("Cart Sync", False, "No authentication token")
            return False
        
        # Get products first
        products = self.run_test("Get Products for Sync Test", "GET", "products", 200)
        if not products or len(products) >= 2:
            product_ids = [products[0]['id'], products[1]['id']] if len(products) >= 2 else [products[0]['id']]
        else:
            self.log_test("Cart Sync", False, "Need at least 1 product")
            return False
        
        # Simulate guest cart data
        guest_cart = [
            {"product_id": product_ids[0], "quantity": 1}
        ]
        
        if len(product_ids) > 1:
            guest_cart.append({"product_id": product_ids[1], "quantity": 2})
        
        response = self.run_test("Sync Guest Cart", "POST", "cart/sync", 200, guest_cart)
        return response is not None

    def test_invalid_endpoints(self):
        """Test error handling for invalid requests"""
        # Test invalid product ID
        self.run_test("Invalid Product ID", "GET", "products/invalid-id", 404)
        
        # Test invalid cart item ID (requires auth)
        if self.token:
            self.run_test("Invalid Cart Item ID", "DELETE", "cart/invalid-id", 404)
        
        # Test invalid login
        invalid_login = {"email": "nonexistent@example.com", "password": "wrongpass"}
        self.run_test("Invalid Login", "POST", "auth/login", 401, invalid_login)
        
        return True

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting E-Commerce API Tests...")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Basic API tests
        self.test_root_endpoint()
        
        # Product tests (no auth required)
        self.test_get_products()
        self.test_search_products()
        self.test_get_single_product()
        
        # Auth tests
        if self.test_user_registration():
            self.test_get_user_profile()
        
        # Login test (separate user)
        self.test_user_login()
        
        # Cart tests (requires auth)
        if self.token:
            self.test_cart_operations()
            self.test_cart_sync()
        
        # Error handling tests
        self.test_invalid_endpoints()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print("❌ Some tests failed!")
            failed_tests = [r for r in self.test_results if not r['success']]
            print("\nFailed tests:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['details']}")
            return 1

def main():
    tester = ECommerceAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())