import streamlit as st
import pandas as pd

# Sample product data
products = pd.DataFrame({
    "Product_Id": [f"P{str(i).zfill(3)}" for i in range(1, 11)],
    "Product_Name": [
        "Apple", "Banana", "Carrot", "Donut", "Eggplant",
        "Fish", "Grapes", "Honey", "Ice Cream", "Juice"
    ],
    "Product_Price": [120, 40, 50, 70, 90, 300, 200, 400, 150, 60],
    "Image_Link": [
        "https://via.placeholder.com/150?text=Apple",
        "https://via.placeholder.com/150?text=Banana",
        "https://via.placeholder.com/150?text=Carrot",
        "https://via.placeholder.com/150?text=Donut",
        "https://via.placeholder.com/150?text=Eggplant",
        "https://via.placeholder.com/150?text=Fish",
        "https://via.placeholder.com/150?text=Grapes",
        "https://via.placeholder.com/150?text=Honey",
        "https://via.placeholder.com/150?text=Ice+Cream",
        "https://via.placeholder.com/150?text=Juice",
    ],
})

# Initialize session state for cart, orders, and active tab
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "orders" not in st.session_state:
    st.session_state.orders = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Cart"
if "payment_stage" not in st.session_state:
    st.session_state.payment_stage = False

# Function to add items to the cart
def add_to_cart(product_id):
    product = products[products["Product_Id"] == product_id].iloc[0]
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id]["quantity"] += 1
    else:
        st.session_state.cart[product_id] = {
            "Product_Name": product["Product_Name"],
            "Product_Price": product["Product_Price"],
            "quantity": 1,
        }
    st.success(f"Added {product['Product_Name']} to cart!")

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["Product Details", "Cart", "Orders"])

# Tab 1: Product Details
with tab1:
    if st.session_state.active_tab != "Cart":
        st.session_state.active_tab = "Product Details"
    st.title("Product Details")
    for _, row in products.iterrows():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(row["Image_Link"], width=100)
        with col2:
            st.write(f"**{row['Product_Name']}** - ₹{row['Product_Price']}")
            st.button(
                "Add to Cart", 
                key=f"add_{row['Product_Id']}", 
                on_click=add_to_cart, 
                args=(row["Product_Id"],)
            )

# Tab 2: Cart
with tab2:
    st.session_state.active_tab = "Cart"
    st.title("Your Cart")
    if st.session_state.cart:
        cart_items = [
            {
                "Product_Name": item["Product_Name"],
                "Product_Price": item["Product_Price"],
                "Quantity": item["quantity"],
                "Total": item["Product_Price"] * item["quantity"]
            }
            for item in st.session_state.cart.values()
        ]
        cart_df = pd.DataFrame(cart_items)
        st.table(cart_df)
        total = sum(item["Total"] for item in cart_items)
        st.write(f"**Total Amount: ₹{total}**")
        
        if st.button("Proceed to Payment"):
            st.session_state.payment_stage = True

    else:
        st.info("Your cart is empty.")

    # Payment Section (simulated as a pop-up)
    if st.session_state.payment_stage:
        with st.expander("Payment Options", expanded=True):
            st.subheader("Payment")
            payment_method = st.radio("Select Payment Method", ["Cash", "Online", "Card"])
            if st.button("Finalize Order"):
                total = sum(item["Product_Price"] * item["quantity"] for item in st.session_state.cart.values())
                st.session_state.orders.append({
                    "items": st.session_state.cart,
                    "total": total,
                    "payment_method": payment_method,
                })
                st.session_state.cart = {}  # Clear cart
                st.session_state.payment_stage = False
                # Do not change active tab, keep it in Cart
                st.success("Order placed successfully!")

# Tab 3: Orders
with tab3:
    st.session_state.active_tab = "Orders"
    st.title("Your Orders")
    if st.session_state.orders:
        for i, order in enumerate(st.session_state.orders, start=1):
            st.write(f"**Order {i}:**")
            order_items = [
                {
                    "Product_Name": item["Product_Name"],
                    "Product_Price": item["Product_Price"],
                    "Quantity": item["quantity"],
                    "Total": item["Product_Price"] * item["quantity"]
                }
                for item in order["items"].values()
            ]
            order_df = pd.DataFrame(order_items)
            st.table(order_df)
            st.write(f"**Total: ₹{order['total']}** | **Payment Method: {order['payment_method']}**")
    else:
        st.info("No orders placed yet.")
