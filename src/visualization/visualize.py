import folium
from folium.plugins import HeatMap, Fullscreen
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_feature_importance(model, feature_names):
    # Note: VotingClassifier doesn't have direct feature_importances_
    # We usually visualize the underlying RF or XGB, or skip for Ensemble
    pass

def generate_map(elite_df, output_path="reports/final_project_report/maps/Enhanced_EV_Map.html"):
    print("Generating Interactive Map...")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    center = [elite_df['latitude_x'].mean(), elite_df['longitude_x'].mean()]
    m = folium.Map(location=center, zoom_start=11, tiles='cartodbdark_matter')
    Fullscreen(position='topright').add_to(m)

    # Heatmap Layer
    heat_data = [[r['latitude_x'], r['longitude_x'], r['AI_Demand_Prob']] for i, r in elite_df.iterrows()]
    HeatMap(heat_data, radius=12, blur=15, name="AI Demand Heatmap").add_to(m)

    # Add Markers for Top Sites
    for idx, row in elite_df.head(100).iterrows():
        popup_html = f"""
        <b>Rank:</b> {idx+1}<br>
        <b>MCDM Score:</b> {row['MCDM_Score']:.2f}<br>
        <b>Demand Prob:</b> {row['AI_Demand_Prob']:.2%}
        """
        folium.Marker(
            location=[row['latitude_x'], row['longitude_x']],
            popup=folium.Popup(popup_html, max_width=200),
            icon=folium.Icon(color='green', icon='flash')
        ).add_to(m)

    m.save(output_path)
    print(f"Map saved to {output_path}")
