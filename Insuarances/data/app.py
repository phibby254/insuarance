import pandas as pd
import streamlit as st
import os
from fpdf import FPDF
import tempfile

DATA_FILE = os.path.join("data", "insurance_data.csv")

# -------------------------------
# Load or initialize dataframe
# -------------------------------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "Name", "Mobile", "Email", "Age", "Income", "Employment", "Dependents",
        "Dependents_Info", "Covers", "Insurance_Type", "Monthly_Cost_EUR", "Yearly_Cost_EUR",
        "Health Issues", "Cost"
    ])

pdf_bytes = None

# -------------------------------
# Layout with Tabs
# -------------------------------
tab1, tab2 = st.tabs(["📝 Insurance Application", "💊 Health Insurance Quick Form"])

# -------------------------------
# TAB 1: Full Insurance Form
# -------------------------------
with tab1:
    st.header("📝 Insurance Application Form")

    with st.form("insurance_form"):
        st.subheader("Contributor Information")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=18, max_value=120, step=1)
        mobile = st.text_input("Mobile Number")
        email = st.text_input("Email Address")
        employment = st.text_input("Employment Status (e.g. Employed, Self-employed, Unemployed)")
        income = st.number_input("Monthly Income (€)", min_value=0, step=100)

        st.markdown("---")
        st.subheader("Dependents (0-18 years)")
        num_dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, step=1)
        dependents_info = []
        for i in range(int(num_dependents)):
            with st.expander(f"Dependent #{i+1}", expanded=False):
                dep_name = st.text_input(f"Dependent {i+1} Name", key=f"dep_name_input_{i}")
                dep_age = st.number_input(f"Dependent {i+1} Age", min_value=0, max_value=18, step=1, key=f"dep_age_input_{i}")
                dependents_info.append({"name": dep_name, "age": dep_age})

        st.markdown("---")
        st.subheader("Cover Options")
        cover_options = [
            ("Accidental", 20),
            ("Tooth", 15),
            ("Pregnancy", 30),
            ("Terminal Illnesses", 50)
        ]
        selected_covers = st.multiselect(
            "Select Cover Options (cost per cover shown)",
            [f"{c_name} (+€{cost}/month)" for c_name, cost in cover_options]
        )

        # Calculate costs
        cover_cost = sum([cost for (c_name, cost) in cover_options if any(c_name in sel for sel in selected_covers)])
        children_cover_cost = 40 * int(num_dependents) if num_dependents > 0 else 0
        insurance_type = "Private" if income > 2500 else "Governmental"

        base_cost = 100
        monthly_cost = base_cost + cover_cost + children_cover_cost
        yearly_cost = monthly_cost * 12

        st.markdown(f"**Insurance Type:** {insurance_type}")
        st.markdown(f"**Estimated Monthly Cost:** €{monthly_cost}")
        st.markdown(f"**Estimated Yearly Cost:** €{yearly_cost}")

        submitted = st.form_submit_button("Save Application")

    if submitted:
        if name and employment and mobile and email:
            new_entry = dict(
                Name=name,
                Mobile=mobile,
                Email=email,
                Age=age,
                Income=income,
                Employment=employment,
                Dependents=num_dependents,
                Dependents_Info=str(dependents_info),
                Covers=", ".join(selected_covers),
                Insurance_Type=insurance_type,
                Monthly_Cost_EUR=monthly_cost,
                Yearly_Cost_EUR=yearly_cost,
                Health_Issues="",
                Cost=""
            )

            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Data saved successfully!")

            # -------------------------------
            # Generate PDF with DejaVu Unicode font
            # -------------------------------
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Insurance Application Summary", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(0, 10, f"Name: {name}", ln=True)
            pdf.cell(0, 10, f"Mobile: {mobile}", ln=True)
            pdf.cell(0, 10, f"Email: {email}", ln=True)
            pdf.cell(0, 10, f"Age: {age}", ln=True)
            pdf.cell(0, 10, f"Income: {income} EUR", ln=True)
            pdf.cell(0, 10, f"Employment: {employment}", ln=True)
            pdf.cell(0, 10, f"Insurance Type: {insurance_type}", ln=True)
            pdf.cell(0, 10, f"Monthly Cost: {monthly_cost} EUR", ln=True)
            pdf.cell(0, 10, f"Yearly Cost: {yearly_cost} EUR", ln=True)
            pdf.cell(0, 10, f"Covers: {', '.join(selected_covers)}", ln=True)
            pdf.cell(0, 10, f"Number of Dependents: {num_dependents}", ln=True)
            for idx, dep in enumerate(dependents_info):
                dep_name_ascii = dep['name']
                pdf.cell(0, 10, f"Dependent {idx+1}: {dep_name_ascii} (Age: {dep['age']})", ln=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                pdf.output(tmpfile.name)
                tmpfile.seek(0)
                pdf_bytes = tmpfile.read()

            st.download_button(
                label="📄 Download PDF Summary",
                data=pdf_bytes,
                file_name="insurance_summary.pdf",
                mime="application/pdf"
            )

        else:
            st.warning("⚠️ Please fill in all required fields (Name, Mobile, Email, Employment).")


# -------------------------------
# TAB 2: Health Insurance Quick Form
# -------------------------------
with tab2:
    st.header("💊 Health Insurance Quick Form")

    name2 = st.text_input("Full Name", key="health_name")
    age2 = st.number_input("Age", min_value=0, max_value=120, step=1, key="health_age")
    health_issues = st.multiselect(
        "Known Health Issues",
        ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "None"]
    )
    employment2 = st.text_input("Employment Status", key="health_employment")
    dependents2 = st.number_input("Number of Dependents under 18", min_value=0, max_value=10, step=1, key="health_dependents")

    # Simple cost calculation
    base_cost = 1000
    cost = base_cost + (age2 * 10) + (len(health_issues) * 200) + (dependents2 * 150)

    if st.button("Save Health Application"):
        if name2 and employment2:
            new_entry = {
                "Name": name2,
                "Mobile": "",
                "Email": "",
                "Age": age2,
                "Income": "",
                "Employment": employment2,
                "Dependents": dependents2,
                "Dependents_Info": "",
                "Covers": "",
                "Insurance_Type": "",
                "Monthly_Cost_EUR": "",
                "Yearly_Cost_EUR": "",
                "Health Issues": ", ".join(health_issues),
                "Cost": cost,
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Health Insurance Application saved successfully!")

            # -------------------------------
            # Generate PDF for Health Quick Form
            # -------------------------------
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", size=12)

            pdf.cell(200, 10, txt="Health Insurance Application Summary", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(0, 10, f"Name: {name2}", ln=True)
            pdf.cell(0, 10, f"Age: {age2}", ln=True)
            pdf.cell(0, 10, f"Employment: {employment2}", ln=True)
            pdf.cell(0, 10, f"Dependents: {dependents2}", ln=True)
            pdf.cell(0, 10, f"Health Issues: {', '.join(health_issues)}", ln=True)
            pdf.cell(0, 10, f"Estimated Cost: {cost} €", ln=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                pdf.output(tmpfile.name)
                tmpfile.seek(0)
                pdf_bytes = tmpfile.read()

            st.download_button(
                label="📄 Download Health PDF Summary",
                data=pdf_bytes,
                file_name="health_insurance_summary.pdf",
                mime="application/pdf"
            )

        else:
            st.warning("⚠️ Please fill in all required fields (Name and Employment).")


# -------------------------------
# Show All Records
# -------------------------------
st.header("📊 Insurance Records")
st.dataframe(df)
