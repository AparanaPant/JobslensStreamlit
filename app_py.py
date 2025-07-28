import streamlit as st
import pandas as pd
import plotly.express as px

# Load clustered data
df = pd.read_csv("clustered_jobs.csv")

st.title("JobLens: Explore Skills by Job Title")

# --- Step 1: Autocomplete Job Title ---
job_title = st.selectbox("Search by Job Title", sorted(df['title'].unique()))

# --- Step 2: Find Cluster ---
selected_cluster = df[df['title'] == job_title]['cluster'].values[0]
st.markdown(f"### 🔍 This role belongs to Cluster: `{selected_cluster}`")

# --- Step 3: Top Skills in This Cluster ---
cluster_df = df[df['cluster'] == selected_cluster]
all_words = ','.join(cluster_df['keywords']).split(',')
top_skills = pd.Series([w.strip() for w in all_words]).value_counts().head(10)

st.subheader("🔑 Top Skills in This Cluster")
for skill in top_skills.index:
    st.markdown(f"- {skill}")

# --- Step 4: Other Job Titles in This Cluster ---
st.subheader("📌 Other Job Titles in the Same Cluster")
st.write(cluster_df['title'].value_counts().head(10))

# --- Step 5: UMAP Visualization ---
st.subheader("📊 UMAP Plot of All Jobs")
fig = px.scatter(
    df, x='x', y='y',
    color='cluster',
    hover_data=['title', 'keywords'],
    title="UMAP Projection of Job Role Clusters",
    width=900, height=600
)

# Highlight selected job
selected = df[df['title'] == job_title].iloc[0]
fig.add_scatter(
    x=[selected['x']], y=[selected['y']],
    mode='markers+text',
    marker=dict(size=12, color='black'),
    text=[job_title],
    textposition='top center',
    name='Selected Job'
)

st.plotly_chart(fig)
