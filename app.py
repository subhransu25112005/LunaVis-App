import streamlit as st
from datetime import datetime, timedelta
from moon_phase import get_moon_phase
from PIL import Image, ImageDraw, ImageEnhance
import os, random
import matplotlib.pyplot as plt

# ----------------- Paths -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOON_IMAGE_PATH = os.path.join(BASE_DIR, "moon_images")

# ----------------- Select Moon Image -----------------
def get_moon_image(illumination, waxing=True):
    if illumination < 1:
        phase_file = "new_moon.png"
    elif illumination < 50:
        phase_file = "waxing_crescent.png" if waxing else "waning_crescent.png"
    elif illumination == 50:
        phase_file = "first_quarter.png" if waxing else "last_quarter.png"
    elif illumination < 99:
        phase_file = "waxing_gibbous.png" if waxing else "waning_gibbous.png"
    else:
        phase_file = "full_moon.png"
    return os.path.join(MOON_IMAGE_PATH, phase_file)

# ----------------- Waxing or Waning -----------------
def waxing_or_waning(date, lat, lon):
    today_phase = get_moon_phase(date, lat, lon)
    tomorrow = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow_phase = get_moon_phase(tomorrow, lat, lon)
    return tomorrow_phase >= today_phase

# ----------------- Starry Sky with Moon -----------------
def generate_starry_sky_with_moon(moon_img_path, width=600, height=400, num_stars=150):
    sky = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(sky)

    for _ in range(num_stars):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        color = random.choice(["white", "#a9cfff", "#dbe9ff"])  # Twinkling tones
        draw.ellipse((x, y, x+size, y+size), fill=color)

    moon = Image.open(moon_img_path).convert("RGBA")
    moon = moon.resize((150, 150), Image.LANCZOS)  # ✅ Fixed resizing method
    moon = ImageEnhance.Brightness(moon).enhance(1.2)

    moon_position = ((width - moon.width) // 2, (height - moon.height) // 2)
    sky.paste(moon, moon_position, moon)

    return sky

# ----------------- Streamlit GUI -----------------
st.set_page_config(page_title="Moon Phase Visualizer", page_icon="🌙", layout="centered")
st.title("🌌 Moon Phase Visualizer")
st.sidebar.markdown("© 2025 Subhranshu Nanda")

# Inputs
date = st.date_input("Select Date", datetime.utcnow())
lat = st.number_input("Latitude", value=20.2961, format="%.4f")
lon = st.number_input("Longitude", value=85.8245, format="%.4f")

if st.button("Show Moon Phase"):
    try:
        phase = get_moon_phase(date.strftime("%Y-%m-%d"), lat, lon)
        waxing = waxing_or_waning(date.strftime("%Y-%m-%d"), lat, lon)

        st.subheader(f"Illumination: {phase:.2f}% ({'Waxing' if waxing else 'Waning'})")

        img_path = get_moon_image(phase, waxing)
        sky_with_moon = generate_starry_sky_with_moon(img_path)
        st.image(sky_with_moon, caption="Moon Phase", use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching moon phase: {e}")

# Plot for 30 days
if st.button("Plot Next 30 Days"):
    with st.spinner("Calculating moon phases..."):
        phases, dates = [], []
        base_date = datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d")
        for i in range(30):
            d = base_date + timedelta(days=i)
            phase = get_moon_phase(d.strftime("%Y-%m-%d"), lat, lon)
            phases.append(phase)
            dates.append(d.strftime("%d-%b"))

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(dates, phases, marker="o", color="orange")
        ax.set_title("Moon Phase Over 30 Days")
        ax.set_ylabel("Illumination (%)")
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45)
        st.pyplot(fig)

st.markdown("Created by *Subhransu Nanda*")