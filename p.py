import streamlit as st
import pandas as pd
import numpy as np
import time

# Apply custom CSS for font styling
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: white;
            text-align: center;
            font-family: Times New Roman;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for navigation and prediction tracking
if "page" not in st.session_state:
    st.session_state.page = "Upload"
if "total_predictions" not in st.session_state:
    st.session_state.total_predictions = 0
if "failure_count" not in st.session_state:
    st.session_state.failure_count = 0
if "no_failure_count" not in st.session_state:
    st.session_state.no_failure_count = 0

# Function to change page
def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Sidebar Navigation
st.sidebar.title("🔄 Navigation")
if st.sidebar.button("📂 Upload"):
    switch_page("Upload")
if st.sidebar.button("📊 Train Page"):
    switch_page("Train")
if st.sidebar.button("📈 Analyse Page"):
    switch_page("Analyse")
if st.sidebar.button("📉 Visualize Trends"):
    switch_page("Visualize")
if st.sidebar.button("🤖 Prediction Page"):
    switch_page("Predict")


# ------------------- 📂 UPLOAD PAGE ------------------- #
if st.session_state.page == "Upload":
    st.markdown('<p class="title">🚀 Time Series Failure Prediction</p>', unsafe_allow_html=True)
    st.write("Upload a dataset to begin.")

    uploaded_file = st.file_uploader("📂 Upload CSV File", type="csv")

    if uploaded_file is not None:
        st.session_state["data"] = pd.read_csv(uploaded_file)  # Store data
    if "data" in st.session_state:
         df = st.session_state["data"]
         st.write("### 🔍 Data Preview:")
         st.write(df.head())
         if st.button("Train Model"):
             switch_page("Train")
   

# ------------------- 📊 TRAIN PAGE ------------------- #
elif st.session_state.page == "Train":
    st.markdown('<p class="title">📊 Training Model</p>', unsafe_allow_html=True)

    if "data" in st.session_state:
        st.write("### ⚙️ Model Training in Progress... Please wait.")

        # Training Progress Bar
        progress_bar = st.progress(0)
        for percent_complete in range(0, 101, 20):
            time.sleep(1)  # Simulating training delay
            progress_bar.progress(percent_complete)

        st.success("✅ Training Completed!")

        # Display Training Metrics (Simulated)
        st.write("### 📊 Model Performance:")
        training_accuracy = round(np.random.uniform(85, 95), 2)  # Simulated accuracy
        training_loss = round(np.random.uniform(0.2, 0.5), 2)    # Simulated loss

        st.write(f"🔢 **Training Accuracy:** {training_accuracy}%")
        st.write(f"📉 **Training Loss:** {training_loss}")

        # Model Summary (Replace with actual summary)
        st.write("### 🏗 Model Summary:")
        st.text("""
        - Input Layer: LSTM (64 units)
        - Hidden Layer: LSTM (128 units)
        - Output Layer: Dense (1 neuron, sigmoid activation)
        - Optimizer: Adam
        - Loss Function: Binary Crossentropy
        """)

        # Proceed to Analysis
        if st.button("Analyse "):
            switch_page("Analyse")

    else:
        st.warning("⚠️ No data uploaded yet.")


# ------------------- 📈 ANALYSE PAGE ------------------- #
elif st.session_state.page == "Analyse":
    st.markdown('<p class="title">📊 Data Analysis</p>', unsafe_allow_html=True)

    if "data" in st.session_state:
        df = st.session_state["data"]

        # Show Dataset Info
        st.write("### 📌 Dataset Information:")
        st.write(f"📝 Number of Rows: {df.shape[0]}")
        st.write(f"📌 Number of Columns: {df.shape[1]}")
        st.write(f"🔢 Numeric Columns: {df.select_dtypes(include=[np.number]).columns.tolist()}")

        # Detect Missing Values
        missing_values = df.isnull().sum().sum()
        if missing_values > 0:
            st.warning(f"⚠️ Missing Values Found: {missing_values}")
        else:
            st.success("✅ No Missing Values!")

        if st.button("Visualize Page"):
            switch_page("Visualize")
    else:
        st.warning("⚠️ No data uploaded yet.")

# ------------------- 📉 VISUALIZE TRENDS PAGE ------------------- #
elif st.session_state.page == "Visualize":
    st.markdown('<p class="title">📉 Visualizing Trends</p>', unsafe_allow_html=True)

    if "data" in st.session_state:
        df = st.session_state["data"]

        st.write("### 📊 Sample Data:")
        st.write(df.head())

        st.success("📈 Trends Visualized Successfully!")

        if st.button("Prediction"):
            switch_page("Predict")
    else:
        st.warning("⚠️ No data uploaded yet.")

# ------------------- 🤖 PREDICTION PAGE ------------------- #
elif st.session_state.page == "Predict":
    st.markdown('<p class="title">🤖 Make a Prediction</p>', unsafe_allow_html=True)

    if "data" in st.session_state:
        df = st.session_state["data"]

        st.write("Enter values below to predict:")

        # Dynamically generate input fields based on dataset columns
        input_data = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

        if numeric_columns:
            for col in numeric_columns:
                input_data[col] = st.number_input(f"Enter {col}", value=float(df[col].mean()))

            # Simulate prediction (replace with actual model)
            if st.button("🔮 Predict"):
                prediction = np.random.choice(["Failure", "No Failure"])  # Random placeholder
                st.success(f" Prediction: **{prediction}**")

                # Update counts
                st.session_state.total_predictions += 1
                if prediction == "Failure":
                    st.session_state.failure_count += 1
                else:
                    st.session_state.no_failure_count += 1

        else:
            st.warning("⚠️ No numeric columns found for prediction.")

        # Show prediction statistics
        st.write("### 📊 Prediction Statistics:")
        st.write(f"🔢 **Total Predictions Made:** {st.session_state.total_predictions}")
        st.write(f"❌ **Failures Predicted:** {st.session_state.failure_count}")
        st.write(f"✅ **No Failures Predicted:** {st.session_state.no_failure_count}")

        # Reset counters
        if st.button("🔄 Reset Stats"):
            st.session_state.total_predictions = 0
            st.session_state.failure_count = 0
            st.session_state.no_failure_count = 0
            st.rerun()

        if st.button("🏠 Back to Upload"):
            switch_page("Upload")
            
    else:
        st.warning("⚠️ No data uploaded yet.")
