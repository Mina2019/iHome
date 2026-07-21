import streamlit as st
from supabase import create_client, Client


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

SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================================
# TITLE
# ==========================================================

st.title("🏠 iHome")
st.caption(
    "A modular platform for tasks, goods, space, services, and activities."
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
    price
):

    data = {
        "layer": layer,
        "module": module,
        "purpose": purpose,
        "title": title,
        "description": description,
        "location": location,
        "price": price
    }

    supabase.table(
        "ihome_posts"
    ).insert(
        data
    ).execute()


# ==========================================================
# COMMON FORM
# ==========================================================

def post_form(layer, module, purpose):

    st.subheader(
        f"{purpose}: {module}"
    )

    title = st.text_input(
        "Title"
    )

    description = st.text_area(
        "Description"
    )

    location = st.text_input(
        "City"
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        step=5.0
    )

    image = st.file_uploader(
        "Photo",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )


    if st.button(
        "Post",
        key=f"{layer}_{module}_{purpose}"
    ):

        save_post(
            layer,
            module,
            purpose,
            title,
            description,
            location,
            price
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

        post_form(
            layer,
            module,
            st.session_state.purpose
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
