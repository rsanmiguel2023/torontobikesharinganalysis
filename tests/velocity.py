import plotly.express as px

data = {
    "Sprint": ["Sprint 1", "Sprint 2"],
    "Points": [25, 26]
}

fig = px.bar(
    data,
    x="Sprint",
    y="Points",
    text="Points",
    title="Velocity Chart"
)

fig.update_layout(
    width=1000,
    height=500,
    margin=dict(l=50, r=50, t=80, b=80),
    font=dict(size=14)
)

fig.update_traces(
    textposition='outside',
    width=0.45
)

fig.show()
