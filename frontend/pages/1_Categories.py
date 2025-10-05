import streamlit as st
import sys, os
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.logic import CategoryLogic

st.set_page_config(page_title="Categories", page_icon="📂", layout="wide")
st.title("📂 Category Management")

category_logic = CategoryLogic()

# ----- Add New Category -----
st.subheader("➕ Add Category")
name = st.text_input("Category Name")
if st.button("Add Category"):
    if not name:
        st.warning("Please enter a category name.")
    else:
        res = category_logic.create_category(name)
        if res["Success"]:
            st.success("✅ Category added successfully!")
        else:
            st.error(res["message"])

st.divider()

# ----- View All Categories -----
st.subheader("📋 View All Categories")
categories = category_logic.fetch_all_categories()
if categories["Success"] and categories["data"]:
    for c in categories["data"]:
        st.write(f"**ID:** {c['id']} | **Name:** {c['name']}")
else:
    st.info("No categories found.")

st.divider()

# ----- Update Category -----
st.subheader("✏️ Update Category")
categories = category_logic.fetch_all_categories()
if categories["Success"] and categories["data"]:
    cat_names = [c["name"] for c in categories["data"]]
    selected = st.selectbox("Select Category", cat_names)
    new_name = st.text_input("New Category Name", value=selected)
    if st.button("Update Category"):
        cat_id = next(c["id"] for c in categories["data"] if c["name"] == selected)
        res = category_logic.modify_category(cat_id, new_name)
        if res["Success"]:
            st.success("✅ Category updated successfully!")
        else:
            st.error(res["message"])
else:
    st.warning("No categories available to update.")

st.divider()

# ----- Delete Category -----
st.subheader("🗑️ Delete Category")
if categories["Success"] and categories["data"]:
    del_cat = st.selectbox("Select Category to Delete", [c["name"] for c in categories["data"]])
    if st.button("Delete Category"):
        cat_id = next(c["id"] for c in categories["data"] if c["name"] == del_cat)
        res = category_logic.remove_category(cat_id)
        if res["Success"]:
            st.success("✅ Category deleted successfully!")
        else:
            st.error(res["message"])
else:
    st.info("No categories available to delete.")
