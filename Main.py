import os
from order_manager import OrderManager
from barcode_handler import BarcodeHandler
from qr_handler import QRHandler

def display_menu(manager):
    print("\n" + "="*60)
    print("📱 COFFEE SHOP MENU")
    print("="*60)
    
    # Define the display order and Persian names for categories
    category_names = {
        'hot_drinks': '☕ Hot Drinks (Espresso & Brew)',
        'cold_drinks': '🧊 Cold Drinks (Iced Coffee & Detox)',
        'desserts': '🍰 Desserts, Cakes & Ice Cream',
        'breakfast': '🍳 Breakfast & Snacks'
    }
    
    for category, display_name in category_names.items():
        if category in manager.menu:
            print(f"\n{display_name}:")
            for item in manager.menu[category]:
                print(f"  {item['id']}. {item['name']} - {item['price']:,} IRR")
        else:
            print(f"\n⚠️ Warning: Category '{category}' not found in menu file.")

def main():
    manager = OrderManager()
    barcode_handler = BarcodeHandler()
    
    while True:
        print("\n" + "="*50)
        print("🎯 Order Management System")
        print("1️⃣ Create New Order")
        print("2️⃣ Scan QR Code (Track Order)")
        print("3️⃣ Scan Barcode (Product)")
        print("4️⃣ Update Order Status (Logistics)")
        print("5️⃣ Track Order by Code")
        print("6️⃣ Generate Barcode for New Product")
        print("7️⃣ Exit")
        
        choice = input("\nYour choice: ").strip()
        
        if choice == '1':
            display_menu(manager)
            items = []
            while True:
                try:
                    prod_id = int(input("Product ID (0 to finish): "))
                    if prod_id == 0:
                        break
                    
                    found = None
                    for category in manager.menu.values():
                        for item in category:
                            if item['id'] == prod_id:
                                found = item
                                break
                        if found:
                            break
                    
                    if found:
                        qty = int(input("Quantity: "))
                        items.append({
                            "name": found['name'],
                            "price": found['price'],
                            "quantity": qty
                        })
                        print(f"✅ {found['name']} added")
                    else:
                        print("❌ Invalid product!")
                
                except ValueError:
                    print("❌ Invalid input!")
            
            if items:
                cust_name = input("Customer name (default: Guest): ") or "Guest"
                order_code, qr_file = manager.create_order(items, cust_name)
                print(f"\n🎉 Order created! Code: {order_code}")
                print(f"📱 QR Code saved: {qr_file}")
                print("🔍 Scan QR code to track your order")
            else:
                print("⚠️ No items selected!")
        
        elif choice == '2':
            print("🔍 Scan your order QR code...")
            qr_data = QRHandler.scan_qr_from_camera()
            if qr_data and 'order_code' in qr_data:
                manager.track_order(qr_data['order_code'])
            else:
                print("❌ Invalid QR code!")
        
        elif choice == '3':
            print("📦 Scan product barcode...")
            barcode = barcode_handler.scan_barcode_from_camera()
            if barcode:
                product = manager.db.get_product_by_barcode(barcode)
                if product:
                    print(f"✅ Product: {product[1]} - Price: {product[2]:,} IRR")
                else:
                    print("⚠️ Product not found!")
            else:
                print("❌ No barcode scanned!")
        
        elif choice == '4':
            code = input("Order code: ").upper()
            print("Status options: pending, preparing, ready, delivered, cancelled")
            status = input("New status: ").strip().lower()
            location = input("Location (shop/warehouse/delivery): ")
            manager.update_order_status(code, status, location)
        
        elif choice == '5':
            code = input("Order code: ").upper()
            manager.track_order(code)
        
        elif choice == '6':
            prod_name = input("Product name: ")
            prod_price = float(input("Price: "))
            prod_category = input("Category: ")
            barcode_file = barcode_handler.generate_barcode(prod_name[:12])
            print(f"✅ Barcode generated: {barcode_file}")
            manager.db.add_product(prod_name, prod_price, prod_category, barcode_file)
        
        elif choice == '7':
            print("🙏 Goodbye!")
            break

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    os.makedirs("orders", exist_ok=True)
    main()
