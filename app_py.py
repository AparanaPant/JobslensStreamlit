import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data ---
try:
    df = pd.read_csv("clustered_jobs.csv", encoding='utf-8')
except Exception as e:
    st.error(f"❌ Failed to load CSV: {e}")
    st.stop()

# Confirm expected columns exist
expected_cols = {'title', 'description', 'keywords', 'cluster', 'x', 'y'}
if not expected_cols.issubset(df.columns):
    st.error("❌ CSV is missing required columns.")
    st.stop()

st.title("💼 JobLens: Explore Skills by Job Title")

# --- Step 1: Autocomplete Job Title ---
job_title = st.selectbox("🔍 Search by Job Title", sorted(df['title'].dropna().unique()))

# --- Step 2: Find Cluster ---
selected_row = df[df['title'] == job_title].iloc[0]
selected_cluster = selected_row['cluster']
st.markdown(f"### 🧠 This role belongs to Cluster: `{selected_cluster}`")

# --- Step 3: Top Skills in This Cluster ---
cluster_df = df[df['cluster'] == selected_cluster]
all_words = ','.join(cluster_df['keywords'].dropna()).split(',')
top_skills = pd.Series([w.strip() for w in all_words if w.strip() != ""]).value_counts().head(10)

st.subheader("🔑 Top Skills in This Cluster")
for skill in top_skills.index:
    st.markdown(f"- {skill}")

# --- Step 4: Other Job Titles in the Same Cluster ---
st.subheader("📌 Other Job Titles in This Cluster")
similar_jobs = cluster_df['title'].value_counts().head(10)
st.write(similar_jobs)

# --- Step 5: UMAP Visualization ---
st.subheader("📊 UMAP Plot of Job Clusters")
fig = px.scatter(
    df, x='x', y='y',
    color=df['cluster'].astype(str),  # ensure cluster is treated as category
    hover_data=['title', 'keywords'],
    title="UMAP Projection of Job Role Clusters",
    width=900, height=600
)

# Highlight selected job
fig.add_scatter(
    x=[selected_row['x']],
    y=[selected_row['y']],
    mode='markers+text',
    marker=dict(size=12, color='black'),
    text=[job_title],
    textposition='top center',
    name='Selected Job'
)

st.plotly_chart(fig)
