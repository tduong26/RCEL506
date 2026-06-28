import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np

# Streamlit Title and Setup
st.set_page_config(layout="wide")
st.title("Interactive Vehicle Fleet Electrification Dashboard")
st.write("Explore how different adoption scenarios shift the balance from gasoline to electric fleets.")

# 1. INTERACTIVE SIDEBAR CONTROLS
st.sidebar.header("Simulation Settings")
ev_marker_size = st.sidebar.slider("Vehicle Icon Size", min_value=50, max_value=200, value=90, step=10)
ev_color = st.sidebar.color_picker("Pick Electric Vehicle Color", value="#4CAF50")
gas_color = st.sidebar.color_picker("Pick Gasoline Vehicle Color", value="#DCDCDC")

# Core layout constants updated exactly to 8 columns and 49 rows
num_columns = 4
cars_per_col_x = 8
cars_per_col_y = 49
total_cars_per_plot = cars_per_col_x * cars_per_col_y

def create_horizontal_car_marker():
    verts = [
        (0.0, 0.2), (0.0, 0.8), (0.6, 0.8), (0.65, 0.9), (0.7, 0.8),
        (0.95, 0.75), (0.95, 0.25), (0.7, 0.2), (0.65, 0.1), (0.6, 0.2),
        (0.0, 0.2)
    ]
    codes = [
        mpath.Path.MOVETO, mpath.Path.LINETO, mpath.Path.LINETO, mpath.Path.LINETO,
        mpath.Path.LINETO, mpath.Path.LINETO, mpath.Path.LINETO, mpath.Path.LINETO,
        mpath.Path.LINETO, mpath.Path.LINETO, mpath.Path.CLOSEPOLY
    ]
    return mpath.Path(verts, codes)

car_marker_horizontal = create_horizontal_car_marker()

# Generate proportional mappings for the new 392-car grid structure
np.random.seed(42)
col0_ev_indices = np.random.choice(total_cars_per_plot, 4, replace=False)
col1_ev_indices = np.random.choice(total_cars_per_plot, 48, replace=False)
col2_ev_indices = np.random.choice(total_cars_per_plot, 156, replace=False)
col3_gas_indices = np.random.choice(total_cars_per_plot, 15, replace=False)

col0_colors = np.zeros(total_cars_per_plot)
col0_colors[col0_ev_indices] = 1

col1_colors = np.zeros(total_cars_per_plot)
col1_colors[col1_ev_indices] = 1

col2_colors = np.zeros(total_cars_per_plot)
col2_colors[col2_ev_indices] = 1

col3_colors = np.ones(total_cars_per_plot)
col3_colors[col3_gas_indices] = 0

all_colors = [col0_colors, col1_colors, col2_colors, col3_colors]

titles = [
    "Vehicles on the road today",
    "Projected on the road in 2035",
    "Projected on the road in 2050",
    "In 2050, if all new sales are electric by 2035"
]

descriptions = [
    "These vehicles represent the 250 million cars, S.U.V.s, vans and pickup trucks on America's roads today. The vast majority run on gasoline.",
    "Automakers are now shifting to electric vehicles, which could make up a quarter of new sales by 2035, analysts project.",
    "Even in 2050, when electric vehicles are projected to make up 60 percent of new sales, **the majority of vehicles on the road would still run on gasoline.**",
    "Theoretical aggressive adoption curve showing full turnover consequence if sales shift entirely to electric within 10 years."
]

# 2. GENERATING AND RENDERING MATPLOTLIB FIG TO STREAMLIT
fig, axes = plt.subplots(1, 4, figsize=(16, 12), facecolor='white')

for i in range(num_columns):
    ax = axes[i]
    ax.set_xlim(-0.5, cars_per_col_x - 0.5)
    ax.set_ylim(-1, cars_per_col_y + 1)
    ax.axis('off')
    
    ax.text(0, cars_per_col_y, titles[i], fontsize=10, fontweight='bold', va='bottom')
    
    color_map = all_colors[i]
    idx = 0
    for y in range(cars_per_col_y):
        for x in range(cars_per_col_x):
            car_color = ev_color if color_map[idx] == 1 else gas_color
            ax.scatter(x, y, marker=car_marker_horizontal, s=ev_marker_size, color=car_color)
            idx += 1

plt.tight_layout()
st.pyplot(fig)

# 3. LAYOUT DOWNSTREAM DESCRIPTION BLOCKS
st.markdown("---")
cols = st.columns(4)
for i in range(num_columns):
    with cols[i]:
        st.subheader(titles[i])
        # Removed the st.error() line from here so the red table banner disappears
        st.markdown(descriptions[i])
