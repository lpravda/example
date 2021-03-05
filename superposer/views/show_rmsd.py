import json
import os
from pathlib import Path

import pandas as pd
import plotly.express as ex
import streamlit as st
import superposer

root = Path(superposer.__file__).parent

with open(os.path.join(root, "data/rmsd.json"), "r") as fp:
    data = json.load(fp)

df = pd.DataFrame(data, columns=["RMSD"])

st.title("Example histogram of RMSDs")

fig = ex.histogram(df, ["RMSD"], nbins=30)
st.plotly_chart(fig, use_container_width=True)
