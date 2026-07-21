import streamlit as st
from supabase import create_client, Client
import re

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="iHome",
    page_icon="🏠",
    layout="wide"
)


# ==========================================================
# SUPABASE CONNECTION
# ==========================================================

SUPABASE_URL = "https://xbdlzzjparnvrsvsjfca.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhiZGx6empwYXJudnJzdnNqZmNhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5MzQ0NDYsImV4cCI6MjA5MzUxMDQ0Nn0.h0AxxjVJZWpTCkywH-Et30TCn4nKQwGXfvmPbVmgZJo"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def valid_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email)

# ==========================================================
# TITLE
# ==========================================================

st.title("🏠 iHome")
st.caption(
    "A modular platform for tasks, goods, space, services, and activities of a home."
)


# ==========================================================
# DATABASE INSERT
# ==========================================================

def save_post(
    layer,
    module,
    purpose,
    title,
    description,
    location,
    price,
    email
):

    data = {
        "layer": layer,
        "module": module,
        "purpose": purpose,
        "title": title,
        "description": description,
        "location": location,
        "price": price,
        "email": email
    }

    supabase.table(
        "ihome_posts"
    ).insert(
        data
    ).execute()


# ==========================================================
# DISPLAY POSTS
# ==========================================================

def show_posts(layer, module):

    st.subheader(
        f"📋 {module} Listings"
    )

    response = (
        supabase
        .table("ihome_posts")
        .select("*")
        .eq("layer", layer)
        .eq("module", module)
        .execute()
    )

    posts = response.data

    if posts:

        for post in posts:

            with st.container():

                st.write(
                    "### " + post["title"]
                )

                st.write(
                    "Type:",
                    post["purpose"]
                )

                st.write(
                    post["description"]
                )

                st.write(
                    "📍",
                    post["location"]
                )

                st.write(
                    "💰 $",
                    post["price"]
                )

                st.divider()

    else:

        st.info(
            "No listings yet."
        )
        
# ==========================================================
# COMMON FORM
# ==========================================================

def post_form(layer, module, purpose):

    st.subheader(
        f"{purpose}: {module}"
    )

    title = st.text_input(
        "Title",
        key=f"{layer}_{module}_{purpose}_title"
    )

    description = st.text_area(
        "Description",
        key=f"{layer}_{module}_{purpose}_description"
    )

    location = st.text_input(
        "City",
        key=f"{layer}_{module}_{purpose}_location"
    )

    email = st.text_input(
    "Email",
    key=f"{layer}_{module}_{purpose}_email"
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        step=5.0,
        key=f"{layer}_{module}_{purpose}_price"
    )

    image = st.file_uploader(
        "Photo",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key=f"{layer}_{module}_{purpose}_image"
    )


    if st.button(
        "Post",
        key=f"{layer}_{module}_{purpose}_submit"
    ):

        if not valid_email(email):

            st.error(
                "Please enter a valid email address."
            )

        return

        save_post(
            layer,
            module,
            purpose,
            title,
            description,
            location,
            price,
            email
        )

        st.success(
            "Post created successfully!"
        )


# ==========================================================
# OFFERING / WANTED BUTTONS
# ==========================================================

def choose_purpose(
    layer,
    module
):

    col1, col2 = st.columns(2)

    if "purpose" not in st.session_state:
        st.session_state.purpose = None


    with col1:
        if st.button(
            "🔵 Offering",
            key=f"{layer}_{module}_offer"
        ):
            st.session_state.purpose = "Offering"


    with col2:
        if st.button(
            "🟢 Wanted",
            key=f"{layer}_{module}_wanted"
        ):
            st.session_state.purpose = "Wanted"


    if st.session_state.purpose:

        action = st.radio(
            "Choose Action",
            [
                "Post",
                "View Listings"
            ],
            key=f"{layer}_{module}_action"
        )

        if action == "Post":

            post_form(
                layer,
                module,
                st.session_state.purpose
            )

        else:

            show_posts(
                layer,
                module
            )


# ==========================================================
# TABS
# ==========================================================

tasks, goods, space, services, activities = st.tabs(
    [
        "🗂️ Tasks",
        "🛍️ Goods",
        "📦 Space",
        "🧹 Services",
        "📚 Activities"
    ]
)


# ==========================================================
# TASKS LAYER
# ==========================================================

with tasks:

    st.header(
        "🗂️ Tasks Layer"
    )

    module = st.selectbox(
        "Choose Module",
        [
            "Bins",
            "iMove",
            "iShop"
        ],
        key="tasks_module"
    )

    choose_purpose(
        "Tasks",
        module
    )


# ==========================================================
# GOODS LAYER
# ==========================================================

with goods:

    st.header(
        "🛍️ Goods Layer"
    )

    choose_purpose(
        "Goods",
        "iSale"
    )


# ==========================================================
# SPACE LAYER
# ==========================================================

with space:

    st.header(
        "📦 Space Layer"
    )

    choose_purpose(
        "Space",
        "iStorage"
    )


# ==========================================================
# SERVICE LAYER
# ==========================================================

with services:

    st.header(
        "🧹 Service Layer"
    )

    module = st.selectbox(
        "Choose Service",
        [
            "iWash",
            "iClean"
        ],
        key="service_module"
    )

    choose_purpose(
        "Service",
        module
    )


# ==========================================================
# ACTIVITY LAYER
# ==========================================================

with activities:

    st.header(
        "📚 Activity Layer"
    )

    choose_purpose(
        "Activity",
        "iTutor"
    )
