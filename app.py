import gradio as gr
import joblib
import pandas as pd

# 1. Load the saved machine learning files
model = joblib.load("laptop_model.pkl")
scaler = joblib.load("laptop_scaler.pkl")
columns = joblib.load("laptop_columns.pkl")

# 2. Define the prediction function
def predict_price(brand, processor, ram, storage):
    # Create a dictionary with the user's input
    input_data = {
        'Brand': brand,
        'Processor': processor,
        'RAM': ram,
        'Storage': storage
    }

    # Convert to DataFrame and apply One-Hot Encoding
    data = pd.DataFrame([input_data])
    data = pd.get_dummies(data)
    
    # Match the exact columns the model was trained on
    data = data.reindex(columns=columns, fill_value=0)
    
    # Scale the numbers using your saved scaler
    data_scaled = scaler.transform(data)
    
    # Make the prediction
    price = model.predict(data_scaled)[0]
    
    # Return the formatted price
    return f"Estimated Price: ₹ {int(price):,}"

# 3. Build the User Interface
app = gr.Interface(
    fn=predict_price,
    inputs=[
        gr.Dropdown(["Dell", "HP", "Lenovo", "Asus", "Acer", "Apple", "MSI"], label="Brand", value="Dell"),
        gr.Dropdown(["Intel Core i3", "Intel Core i5", "Intel Core i7", "AMD Ryzen 5", "AMD Ryzen 7", "Apple M1"], label="Processor", value="Intel Core i5"),
        gr.Slider(4, 64, step=4, label="RAM (GB)", value=8),
        gr.Dropdown(["256GB SSD", "512GB SSD", "1TB HDD", "1TB SSD"], label="Storage", value="512GB SSD")
    ],
    outputs=gr.Textbox(label="Predicted Price"),
    title="Laptop Price Predictor",
    description="Select the laptop specifications to estimate its price."
)

# 4. Launch the app
app.launch()