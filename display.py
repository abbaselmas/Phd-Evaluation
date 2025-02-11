import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from define import *

custom_html = """
<div style="position: fixed; top: 2px; left: 2px;">
    <span>
        <input type="text" id="filterInput" size="15" onchange="applyFilters()" placeholder="and/or .sift -sift bf">
        <input type="number" id="minYValueInput" min="0" max="99" step="0.05" onchange="applyFilters()" placeholder="min y">
        <input type="number" id="maxYValueInput" min="0" max="99" step="0.05" onchange="applyFilters()" placeholder="max y">
        <input type="number" id="minXValueInput" min="0" max="99" step="0.05" onchange="applyFilters()" placeholder="min x">
        <input type="number" id="maxXValueInput" min="0" max="99" step="0.05" onchange="applyFilters()" placeholder="max x">
        <input type="radio" name="filterMode" value="all" onchange="applyFilters()" checked>All
        <input type="radio" name="filterMode" value="any" onchange="applyFilters()" >Any
    </span>
    <span id="trace-count">Total Traces: 0</span>
</div>
<script>
let selectedPoints = new Set();
let textFilteredTraces = new Set();
var plot = document.querySelectorAll(".js-plotly-plot")[0];

function applyFilters() {
    var filter = document.getElementById("filterInput").value.toUpperCase();
    var minYThreshold = parseFloat(document.getElementById("minYValueInput").value) || -Infinity;
    var maxYThreshold = parseFloat(document.getElementById("maxYValueInput").value) ||  Infinity;
    var minXThreshold = parseFloat(document.getElementById("minXValueInput").value) || -Infinity;
    var maxXThreshold = parseFloat(document.getElementById("maxXValueInput").value) ||  Infinity;
    var data = plot.data;
    var visibleTraceCount = 0;
    var filterParts = filter.split(" ");
    var logicKeyword = filterParts.shift() || "";
    var filterWords = filterParts;
    var filterFunction = word => {
        if (logicKeyword === "AND")
            return filterWords.every(filterWord => word.includes(filterWord));
        else if (logicKeyword === "OR")
            return filterWords.some(filterWord => word.includes(filterWord));
        else
            return true;
    };
    var filterMode = document.querySelector('input[name="filterMode"]:checked').value;
    textFilteredTraces.clear();
    let uniqueLegendNames = new Set();
    let visibleTraces = [];

    for (let i = 0; i < data.length; i++) {
        var traceName = data[i].name || "";
        var yValues = data[i].y;
        var xValues = data[i].x;
        var showTrace = false;
        if (filterFunction(traceName.toUpperCase())) {
            const matchFunc = filterMode === "all" ? yValues.every : yValues.some;
            const isValueInRange = (y, i) => {
                const x = xValues[i];
                return y >= minYThreshold && y <= maxYThreshold &&
                    (isNaN(x) || (x >= minXThreshold && x <= maxXThreshold));
            };
            if (matchFunc.call(yValues, isValueInRange)) {
                showTrace = true;
                textFilteredTraces.add(i);
                visibleTraceCount++;
                visibleTraces.push({ index: i, name: traceName });
            }
        }
    }
    let update = { visible: [], showlegend: [] };
    let legendSet = new Set();
    data.forEach((trace, index) => {
        if (textFilteredTraces.has(index)) {
            if (selectedPoints.size === 0 || selectedPoints.has(index)) {
                update.visible.push(true);
                if (!legendSet.has(trace.name)) {
                    update.showlegend.push(true);
                    legendSet.add(trace.name);
                } else {
                    update.showlegend.push(false);
                }
            } else {
                update.visible.push("legendonly");
                update.showlegend.push(false);
            }
        } else {
            update.visible.push(false);
            update.showlegend.push(false);
        }
    });
    document.getElementById('trace-count').innerText = "Total Traces: " + visibleTraceCount;
    Plotly.restyle(plot, update);
}

document.addEventListener("DOMContentLoaded", function() {
    applyFilters();
    plot.on('plotly_selected', function(eventData) {
        selectedPoints.clear();
        if (eventData && eventData.points) {
            eventData.points.forEach(point => {
                if (textFilteredTraces.has(point.curveNumber)) {
                    selectedPoints.add(point.curveNumber);
                }
            });
        }
        applyFilters();
    });    
    plot.on('plotly_deselect', function() {
        selectedPoints.clear();
        Plotly.relayout(plot, {
            'dragmode': 'lasso',
            'selectedpoints': null
        });
        applyFilters();
    });
});
</script>
"""

config = {
        "toImageButtonOptions":     {"format": "svg"},
        "modeBarButtonsToRemove":   ["zoomIn2d", "zoomOut2d"],
        "modeBarButtonsToAdd":      ["v1hovermode", "hoverclosest", "toggleSpikeLines", "zoom", "pan", "select", "lasso2d"],
        "displaylogo":              False,
        "editable":                 False
}

Rate_intensity              = np.load("./arrays/Rate_intensity.npy")
Rate_scale                  = np.load("./arrays/Rate_scale.npy")
Rate_rot                    = np.load("./arrays/Rate_rot.npy")
Rate_graf                   = np.load("./arrays/Rate_graf.npy")
Rate_bikes                  = np.load("./arrays/Rate_bikes.npy")
Rate_boat                   = np.load("./arrays/Rate_boat.npy")
Rate_leuven                 = np.load("./arrays/Rate_leuven.npy")
Rate_wall                   = np.load("./arrays/Rate_wall.npy")
Rate_trees                  = np.load("./arrays/Rate_trees.npy")
Rate_bark                   = np.load("./arrays/Rate_bark.npy")
Rate_ubc                    = np.load("./arrays/Rate_ubc.npy")
Rate_airsim                 = np.load("./arrays/Rate_airsim.npy")
Exec_time_intensity         = np.load("./arrays/Exec_time_intensity.npy")
Exec_time_scale             = np.load("./arrays/Exec_time_scale.npy")
Exec_time_rot               = np.load("./arrays/Exec_time_rot.npy")
Exec_time_graf              = np.load("./arrays/Exec_time_graf.npy")
Exec_time_bikes             = np.load("./arrays/Exec_time_bikes.npy")
Exec_time_boat              = np.load("./arrays/Exec_time_boat.npy")
Exec_time_leuven            = np.load("./arrays/Exec_time_leuven.npy")
Exec_time_wall              = np.load("./arrays/Exec_time_wall.npy")
Exec_time_trees             = np.load("./arrays/Exec_time_trees.npy")
Exec_time_bark              = np.load("./arrays/Exec_time_bark.npy")
Exec_time_ubc               = np.load("./arrays/Exec_time_ubc.npy")
Exec_time_intensity_mobile  = np.load("./arrays/Exec_time_intensity_mobile.npy")
Exec_time_scale_mobile      = np.load("./arrays/Exec_time_scale_mobile.npy")
Exec_time_rot_mobile        = np.load("./arrays/Exec_time_rot_mobile.npy")
Exec_time_graf_mobile       = np.load("./arrays/Exec_time_graf_mobile.npy")
Exec_time_bikes_mobile      = np.load("./arrays/Exec_time_bikes_mobile.npy")
Exec_time_boat_mobile       = np.load("./arrays/Exec_time_boat_mobile.npy")
Exec_time_leuven_mobile     = np.load("./arrays/Exec_time_leuven_mobile.npy")
Exec_time_wall_mobile       = np.load("./arrays/Exec_time_wall_mobile.npy")
Exec_time_trees_mobile      = np.load("./arrays/Exec_time_trees_mobile.npy")
Exec_time_bark_mobile       = np.load("./arrays/Exec_time_bark_mobile.npy")
Exec_time_ubc_mobile        = np.load("./arrays/Exec_time_ubc_mobile.npy")
Exec_time_airsim            = np.load("./arrays/Exec_time_airsim.npy")

########################
# MARK: - Synthetic Data
########################
def syntheticAll4():
    fig1 = go.Figure()
    fig1 = make_subplots(rows=2, cols=2, subplot_titles=["<span style='font-size: 20px;'><b>Intensity changing I+b</b></span>", "<span style='font-size: 20px;'><b>Intensity changing Ixc</b></span>", "<span style='font-size: 20px;'><b>Scale changing</b></span>", "<span style='font-size: 20px;'><b>Rotation changing</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    sett_axis = dict(range=[-0.01, 1.01])
    fig1.update_layout( font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=60, b=20), yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis,
                        xaxis=dict(tickmode="array", tickvals=val_b), xaxis2=dict(tickmode="array", tickvals=val_c), xaxis3=dict(tickmode="array", tickvals=scale), xaxis4=dict(tickmode="array", tickvals=rot))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1 = [Rate_intensity[:len(val_b), m, c3, i, j, 13], Rate_intensity[:len(val_b), m, c3, i, j, 12], Rate_intensity[:len(val_b), m, c3, i, j, 14], Rate_intensity[:len(val_b), m, c3, i, j, 15], Rate_intensity[:len(val_b), m, c3, i, j, 9], Rate_intensity[:len(val_b), m, c3, i, j, 10], Exec_time_intensity[:len(val_b), m, c3, i, j, 6], Exec_time_intensity[:len(val_b), m, c3, i, j, 7]]
                    Rate2_I2 = [Rate_intensity[len(val_c):, m, c3, i, j, 13], Rate_intensity[len(val_c):, m, c3, i, j, 12], Rate_intensity[len(val_c):, m, c3, i, j, 14], Rate_intensity[len(val_c):, m, c3, i, j, 15], Rate_intensity[len(val_c):, m, c3, i, j, 9], Rate_intensity[len(val_c):, m, c3, i, j, 10], Exec_time_intensity[len(val_c):, m, c3, i, j, 6], Exec_time_intensity[len(val_c):, m, c3, i, j, 7]]
                    Rate2_S  = [Rate_scale    [          :, m, c3, i, j, 13], Rate_scale    [          :, m, c3, i, j, 12], Rate_scale    [          :, m, c3, i, j, 14], Rate_scale    [          :, m, c3, i, j, 15], Rate_scale    [          :, m, c3, i, j, 9], Rate_scale    [          :, m, c3, i, j, 10], Exec_time_scale    [          :, m, c3, i, j, 6], Exec_time_scale    [          :, m, c3, i, j, 7]]
                    Rate2_R  = [Rate_rot      [          :, m, c3, i, j, 13], Rate_rot      [          :, m, c3, i, j, 12], Rate_rot      [          :, m, c3, i, j, 14], Rate_rot      [          :, m, c3, i, j, 15], Rate_rot      [          :, m, c3, i, j, 9], Rate_rot      [          :, m, c3, i, j, 10], Exec_time_rot      [          :, m, c3, i, j, 6], Exec_time_rot      [          :, m, c3, i, j, 7]]
                    legend_groupfig1 = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig1, legendgroup=legend_groupfig1, showlegend=True, hovertemplate="<b>%{y:.3f}</b>")
                    # Intensity changing I+b
                    if not (np.isnan(Rate2_I1).any):
                        traces.append (go.Scatter(x=val_b, y=Rate2_I1,    arg=sett))
                        fig1.add_trace(go.Scatter(x=val_b, y=Rate2_I1[0], arg=sett), row=1, col=1)
                    # Intensity changing Ixc
                    if not (np.isnan(Rate2_I2).any):
                        traces.append (go.Scatter(x=val_c, y=Rate2_I2,    arg=sett))
                        fig1.add_trace(go.Scatter(x=val_c, y=Rate2_I2[0], arg=sett), row=1, col=2)
                    # Scale changing
                    if not (np.isnan(Rate2_S).any):
                        traces.append (go.Scatter(x=scale, y=Rate2_S,     arg=sett))
                        fig1.add_trace(go.Scatter(x=scale, y=Rate2_S[0],  arg=sett), row=2, col=1)
                    # Rotation changing
                    if not (np.isnan(Rate2_R).any):
                        traces.append (go.Scatter(x=rot,   y=Rate2_R,     arg=sett))
                        fig1.add_trace(go.Scatter(x=rot,   y=Rate2_R[0],  arg=sett), row=2, col=2)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches", "Total Time(1K)", "Inlier Time(1K)"]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=y, method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis3.title": f"<span style='font-size: 22px;'><b>{y}</b></span>"}]))    
    fig1.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1)]) 
    fig1.write_html(f"./html/synthetic/syntheticAll4.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/syntheticAll4.html", "a") as f:
        f.write(custom_html)

def synthetic4():
    fig2 = go.Figure()
    fig2 = make_subplots(rows=2, cols=2, subplot_titles=["<span style='font-size: 20px;'><b>Intensity changing I+b</b></span>", "<span style='font-size: 20px;'><b>Intensity changing Ixc</b></span>", "<span style='font-size: 20px;'><b>Scale changing</b></span>", "<span style='font-size: 20px;'><b>Rotation changing</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    sett_axis = dict(range=[-0.01, 1.01])
    fig2.update_layout( font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=50, b=20), xaxis=sett_axis, xaxis2=sett_axis, xaxis3=sett_axis, xaxis4=sett_axis, yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    xydata_Intensity1 = [
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 15]),       # F1 Score
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j,  9]),       # Inliers
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 10]),       # Matches
                        np.nanmean(Exec_time_intensity[:len(val_b), m, c3, i, j, 6]),   # 1K Total Time
                        np.nanmean(Exec_time_intensity[:len(val_b), m, c3, i, j, 7])    # 1K feature Inlier Time
                    ]
                    xydata_Intensity2 = [
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 15]),       # F1 Score
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j,  9]),       # Inliers
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 10]),       # Matches
                        np.nanmean(Exec_time_intensity[len(val_c):, m, c3, i, j, 6]),   # 1K Total Time
                        np.nanmean(Exec_time_intensity[len(val_c):, m, c3, i, j, 7])    # 1K feature Inlier Time
                    ]
                    xydata_Scale = [
                        np.nanmean(Rate_scale[:, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_scale[:, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_scale[:, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_scale[:, m, c3, i, j, 15]),       # F1 Score
                        np.nanmean(Rate_scale[:, m, c3, i, j,  9]),       # Inliers
                        np.nanmean(Rate_scale[:, m, c3, i, j, 10]),       # Matches
                        np.nanmean(Exec_time_scale[:, m, c3, i, j, 6]),   # 1K Total Time
                        np.nanmean(Exec_time_scale[:, m, c3, i, j, 7])    # 1K feature Inlier Time
                    ]
                    xydata_Rotation = [
                        np.nanmean(Rate_rot[:, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_rot[:, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_rot[:, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_rot[:, m, c3, i, j, 15]),       # F1 Score
                        np.nanmean(Rate_rot[:, m, c3, i, j,  9]),       # Inliers
                        np.nanmean(Rate_rot[:, m, c3, i, j, 10]),       # Matches
                        np.nanmean(Exec_time_rot[:, m, c3, i, j, 6]),   # 1K Total Time
                        np.nanmean(Exec_time_rot[:, m, c3, i, j, 7])    # 1K feature Inlier Time
                    ]
                    legend_groupfig2 = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=True,
                                hovertemplate="x: <b>%{x:.2f}</b> | y: <b>%{y:.2f}</b>")
                    # Intensity changing I+b
                    if not (np.isnan(xydata_Intensity1).any):
                        traces.append(go.Scatter( x=xydata_Intensity1,      y=xydata_Intensity1, arg=sett))
                        fig2.add_trace(go.Scatter(x=[xydata_Intensity1[0]], y=[xydata_Intensity1[1]], arg=sett), row=1, col=1)
                    # Intensity changing Ixc
                    if not (np.isnan(xydata_Intensity2).any):
                        traces.append(go.Scatter( x=xydata_Intensity2,      y=xydata_Intensity2, arg=sett))
                        fig2.add_trace(go.Scatter(x=[xydata_Intensity2[0]], y=[xydata_Intensity2[1]], arg=sett), row=1, col=2)
                    # Scale changing
                    if not (np.isnan(xydata_Scale).any):
                        traces.append(go.Scatter( x=xydata_Scale,           y=xydata_Scale,      arg=sett))
                        fig2.add_trace(go.Scatter(x=[xydata_Scale[0]],      y=[xydata_Scale[1]],      arg=sett), row=2, col=1)
                    # Rotation changing
                    if not (np.isnan(xydata_Rotation).any):
                        traces.append(go.Scatter( x=xydata_Rotation,        y=xydata_Rotation,   arg=sett))
                        fig2.add_trace(go.Scatter(x=[xydata_Rotation[0]],   y=[xydata_Rotation[1]],   arg=sett), row=2, col=2)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches", "Total Time(1K)", "Inlier Time(1K)"]
    button_listx = []
    button_listy = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict( label=axis, method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis3.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict( label=axis, method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis3.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig2.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listx, direction="down", x=0,    xanchor="left", y=1),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listy, direction="down", x=0.14, xanchor="left", y=1)])
    fig2.write_html(f"./html/synthetic/synthetic4.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic4.html", "a") as f:
        f.write(custom_html)

def synthetic():
    fig15 = go.Figure()
    fig15.update_layout(font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=50, b=20), xaxis=dict(range=[-0.01, 1.01]), yaxis=dict(range=[-0.01, 1.01]))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    xydata = [
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 13], Rate_scale[:, m, c3, i, j, 13], Rate_rot[:, m, c3, i, j, 13]), axis=0)), # Precision
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 12], Rate_scale[:, m, c3, i, j, 12], Rate_rot[:, m, c3, i, j, 12]), axis=0)), # Recall
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 14], Rate_scale[:, m, c3, i, j, 14], Rate_rot[:, m, c3, i, j, 14]), axis=0)), # Repeatibility
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 15], Rate_scale[:, m, c3, i, j, 15], Rate_rot[:, m, c3, i, j, 15]), axis=0)), # F1 Score
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j,  9], Rate_scale[:, m, c3, i, j,  9], Rate_rot[:, m, c3, i, j,  9]), axis=0)), # Inliers
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 10], Rate_scale[:, m, c3, i, j, 10], Rate_rot[:, m, c3, i, j, 10]), axis=0)), # Matches
                        np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 6], Exec_time_scale[:, m, c3, i, j, 6], Exec_time_rot[:, m, c3, i, j, 6]), axis=0)), # 1K Total Time
                        np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 7], Exec_time_scale[:, m, c3, i, j, 7], Exec_time_rot[:, m, c3, i, j, 7]), axis=0))  # 1K feature Inlier Time
                    ]
                    if not (np.isnan(xydata).any):
                        traces.append(go.Scatter( x=xydata, y=xydata, mode="markers", marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                    fig15.add_trace(go.Scatter( x=[xydata[0]], y=[xydata[1]], mode="markers", marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                        showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches", "Total Time(1K)", "Inlier Time(1K)"]
    button_listx = []
    button_listy = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict( label=axis, method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict( label=axis, method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig15.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listx, direction="down", x=0,    xanchor="left", y=1),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listy, direction="down", x=0.14, xanchor="left", y=1)])
    fig15.write_html(f"./html/synthetic/synthetic.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic.html", "a") as f:
        f.write(custom_html)

def syntheticTiming():
    fig15 = go.Figure()
    fig15 = make_subplots(  rows=5, cols=2, subplot_titles=["<span style='font-size: 22px;'>Total & Inlier time (Detect + Descript + Match(BF) | MAGSAC++)</span>", "<span style='font-size: 22px;'>Total & Inlier time (Detect + Descript + Match(Flann) | MAGSAC++)</span>",
                                                            "<span style='font-size: 22px;'>Total time (Detect + Descript + Match(BF+Flann))</span>", "<span style='font-size: 22px;'>Inlier time (Detect + Descript + Match(BF+Flann) + MAGSAC++)</span>",
                                                            "<span style='font-size: 22px;'>Detect time</span>", "<span style='font-size: 22px;'>Describe time</span>"],
                            specs=[[{"colspan": 2}, None], [{"colspan": 2}, None],[{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}]], horizontal_spacing=0.05, vertical_spacing=0.05)
    fig15.update_layout(font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset Timings for Average 1k</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), barmode="stack", height=2000, margin=dict(l=20, r=20, t=80, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 6],         Exec_time_scale[:, m, :, i, j, 6],          Exec_time_rot[:, m, :, i, j, 6]),           axis=0))
                result3m= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, m, :, i, j, 6],  Exec_time_scale_mobile[:, m, :, i, j, 6],   Exec_time_rot_mobile[:, m, :, i, j, 6]),    axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 7],         Exec_time_scale[:, m, :, i, j, 7],          Exec_time_rot[:, m, :, i, j, 7]),           axis=0))
                result4m= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, m, :, i, j, 7],  Exec_time_scale_mobile[:, m, :, i, j, 7],   Exec_time_rot_mobile[:, m, :, i, j, 7]),    axis=0))
                if not (result3 == 0 or np.isnan(result3).any or result3m == 0 or np.isnan(result3m).any):
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["pc"]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-p",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig15.add_trace(trace_match_synt_result3,  row=1, col=1) if m == 0 else fig15.add_trace(trace_match_synt_result3, row=2, col=1)
                    trace_match_synt_result3m= go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["mobile"]], y=[result3m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m",
                                                        text=[f"{result3m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig15.add_trace(trace_match_synt_result3m, row=1, col=1) if m == 0 else fig15.add_trace(trace_match_synt_result3m, row=2, col=1)
                    trace_match_synt_result3.showlegend = False
                    fig15.add_trace(trace_match_synt_result3,  row=3, col=1)
                    trace_match_synt_result3m.showlegend = False
                    fig15.add_trace(trace_match_synt_result3m, row=3, col=1)
                if not (result4 == 0 or np.isnan(result4).any or result4m == 0 or np.isnan(result4m).any):
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["pc"]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-p",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig15.add_trace(trace_match_synt_result4,  row=1, col=1) if m == 0 else fig15.add_trace(trace_match_synt_result4, row=2, col=1)
                    trace_match_synt_result4m= go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["mobile"]], y=[result4m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m",
                                                        text=[f"{result4m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig15.add_trace(trace_match_synt_result4m, row=1, col=1) if m == 0 else fig15.add_trace(trace_match_synt_result4m, row=2, col=1)
                    trace_match_synt_result4.showlegend = False
                    fig15.add_trace(trace_match_synt_result4,  row=4, col=1)
                    trace_match_synt_result4m.showlegend = False
                    fig15.add_trace(trace_match_synt_result4m, row=4, col=1)
            color_index = (color_index + 14) % num_combinations
        result = np.nanmean(np.concatenate((Exec_time_intensity       [:, :, :, i, :, 4], Exec_time_scale       [:, :, :, i, :, 4], Exec_time_rot       [:, :, :, i, :, 4]), axis=0))
        resultm= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, :, :, i, :, 4], Exec_time_scale_mobile[:, :, :, i, :, 4], Exec_time_rot_mobile[:, :, :, i, :, 4]), axis=0))
        if not (result == 0 or np.isnan(result).any or resultm == 0 or np.isnan(resultm).any):
            trace_detect_synt  = go.Bar(x=[[DetectorsLegend[i]],["pc"]],     y=[result],  name=f".{DetectorsLegend[i]}-p", showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            trace_detect_syntm = go.Bar(x=[[DetectorsLegend[i]],["mobile"]], y=[resultm], name=f".{DetectorsLegend[i]}-m", showlegend=True, text=[f"{resultm:.3f}"], marker=dict(color = colors[14*i]))
            fig15.add_trace(trace_detect_synt,  row=5, col=1)
            fig15.add_trace(trace_detect_syntm, row=5, col=1)
        result2 = np.nanmean(np.concatenate((Exec_time_intensity       [:, :, :, :, i, 5], Exec_time_scale       [:, :, :, :, i, 5], Exec_time_rot       [:, :, :, :, i, 5]), axis=0))
        result2m= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, :, :, :, i, 5], Exec_time_scale_mobile[:, :, :, :, i, 5], Exec_time_rot_mobile[:, :, :, :, i, 5]), axis=0))
        if not (result2 == 0 or np.isnan(result2).any or result2m == 0 or np.isnan(result2m).any):
            trace_descr_synt  = go.Bar(x=[[DescriptorsLegend[i]],["pc"]],     y=[result2],  name=f"-{DescriptorsLegend[i]}-p", showlegend=True, text=[f"{result2:.3f}"],  marker=dict(color = colors[14*i]))
            trace_descr_syntm = go.Bar(x=[[DescriptorsLegend[i]],["mobile"]], y=[result2m], name=f"-{DescriptorsLegend[i]}-m", showlegend=True, text=[f"{result2m:.3f}"], marker=dict(color = colors[14*i]))
            fig15.add_trace(trace_descr_synt,  row=5, col=2)
            fig15.add_trace(trace_descr_syntm, row=5, col=2)
    fig15.update_layout(updatemenus=[   dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                        dict(type="dropdown", buttons=[ dict(label="Linear",   method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear"}]),
                                                                        dict(label="Log",      method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log"}])], x=0, xanchor="left", y=1)])
    fig15.write_html("./html/synthetic/syntheticTiming.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open("./html/synthetic/syntheticTiming.html", "a") as f:
        f.write(custom_html)

################
# MARK: - Oxford
################
def oxfordAll9():
    fig4 = go.Figure()
    fig4 = make_subplots(rows=3, cols=3, subplot_titles=[   "<span style='font-size: 20px;'><b>Graf(Viewpoint)</b></span>", "<span style='font-size: 20px;'><b>Bikes(Blur)</b></span>", "<span style='font-size: 20px;'><b>Boat(Zoom + Rotation)</b></span>", 
                                                            "<span style='font-size: 20px;'><b>Leuven(Light)</b></span>", "<span style='font-size: 20px;'><b>Wall(Viewpoint)</b></span>", "<span style='font-size: 20px;'><b>Trees(Blur)</b></span>", 
                                                            "<span style='font-size: 20px;'><b>Bark(Zoom + Rotation)</b></span>", "<span style='font-size: 20px;'><b>UBC(JPEG)", "<span style='font-size: 20px;'><b>Overall</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    xvals = ["Img2", "Img3", "Img4", "Img5", "Img6"]
    sett_axis = dict(range=[-0.01, 1.01])
    fig4.update_layout(font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Affine Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                                                hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=70, b=20), yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis, yaxis5=sett_axis, yaxis6=sett_axis, yaxis7=sett_axis, yaxis8=sett_axis, yaxis9=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_Graf  = [Rate_graf  [:, m, c3, i, j, 13], Rate_graf  [:, m, c3, i, j, 12], Rate_graf  [:, m, c3, i, j, 14], Rate_graf  [:, m, c3, i, j, 15], Rate_graf  [:, m, c3, i, j, 9], Rate_graf  [:, m, c3, i, j, 10], Exec_time_graf  [:, m, c3, i, j, 6], Exec_time_graf  [:, m, c3, i, j, 7]]
                    Rate_Bikes = [Rate_bikes [:, m, c3, i, j, 13], Rate_bikes [:, m, c3, i, j, 12], Rate_bikes [:, m, c3, i, j, 14], Rate_bikes [:, m, c3, i, j, 15], Rate_bikes [:, m, c3, i, j, 9], Rate_bikes [:, m, c3, i, j, 10], Exec_time_bikes [:, m, c3, i, j, 6], Exec_time_bikes [:, m, c3, i, j, 7]]
                    Rate_Boat  = [Rate_boat  [:, m, c3, i, j, 13], Rate_boat  [:, m, c3, i, j, 12], Rate_boat  [:, m, c3, i, j, 14], Rate_boat  [:, m, c3, i, j, 15], Rate_boat  [:, m, c3, i, j, 9], Rate_boat  [:, m, c3, i, j, 10], Exec_time_boat  [:, m, c3, i, j, 6], Exec_time_boat  [:, m, c3, i, j, 7]]
                    Rate_Leuven= [Rate_leuven[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 9], Rate_leuven[:, m, c3, i, j, 10], Exec_time_leuven[:, m, c3, i, j, 6], Exec_time_leuven[:, m, c3, i, j, 7]]
                    Rate_Wall  = [Rate_wall  [:, m, c3, i, j, 13], Rate_wall  [:, m, c3, i, j, 12], Rate_wall  [:, m, c3, i, j, 14], Rate_wall  [:, m, c3, i, j, 15], Rate_wall  [:, m, c3, i, j, 9], Rate_wall  [:, m, c3, i, j, 10], Exec_time_wall  [:, m, c3, i, j, 6], Exec_time_wall  [:, m, c3, i, j, 7]]
                    Rate_Trees = [Rate_trees [:, m, c3, i, j, 13], Rate_trees [:, m, c3, i, j, 12], Rate_trees [:, m, c3, i, j, 14], Rate_trees [:, m, c3, i, j, 15], Rate_trees [:, m, c3, i, j, 9], Rate_trees [:, m, c3, i, j, 10], Exec_time_trees [:, m, c3, i, j, 6], Exec_time_trees [:, m, c3, i, j, 7]]
                    Rate_Bark  = [Rate_bark  [:, m, c3, i, j, 13], Rate_bark  [:, m, c3, i, j, 12], Rate_bark  [:, m, c3, i, j, 14], Rate_bark  [:, m, c3, i, j, 15], Rate_bark  [:, m, c3, i, j, 9], Rate_bark  [:, m, c3, i, j, 10], Exec_time_bark  [:, m, c3, i, j, 6], Exec_time_bark  [:, m, c3, i, j, 7]]
                    Rate_Ubc   = [Rate_ubc   [:, m, c3, i, j, 13], Rate_ubc   [:, m, c3, i, j, 12], Rate_ubc   [:, m, c3, i, j, 14], Rate_ubc   [:, m, c3, i, j, 15], Rate_ubc   [:, m, c3, i, j, 9], Rate_ubc   [:, m, c3, i, j, 10], Exec_time_ubc   [:, m, c3, i, j, 6], Exec_time_ubc   [:, m, c3, i, j, 7]]
                    legend_groupfig4 = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=True, hovertemplate="<b>%{y:.3f}</b>")
                    # Graf(Viewpoint)
                    if not (np.isnan(Rate_Graf).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Graf,       arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Graf[0],    arg=sett), row=1, col=1)
                        # Bikes(Blur)
                    if not (np.isnan(Rate_Bikes).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Bikes,      arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Bikes[0],   arg=sett), row=1, col=2)
                        # Boat(Zoom + Rotation)
                    if not (np.isnan(Rate_Boat).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Boat,       arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Boat[0],    arg=sett), row=1, col=3)
                        # Leuven(Light)
                    if not (np.isnan(Rate_Leuven).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Leuven,     arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Leuven[0],  arg=sett), row=2, col=1)
                        # Wall(Viewpoint)
                    if not (np.isnan(Rate_Wall).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Wall,       arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Wall[0],    arg=sett), row=2, col=2)
                        # Trees(Blur)
                    if not (np.isnan(Rate_Trees).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Trees,      arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Trees[0],   arg=sett), row=2, col=3)
                        # Bark(Zoom + Rotation)
                    if not (np.isnan(Rate_Bark).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Bark,       arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Bark[0],    arg=sett), row=3, col=1)
                        # UBC(JPEG)
                    if not (np.isnan(Rate_Ubc).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Ubc,        arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Ubc[0],     arg=sett), row=3, col=2)
                        # Overall
                    yval = np.nanmean([Rate_Graf, Rate_Bikes, Rate_Boat, Rate_Leuven, Rate_Wall, Rate_Trees, Rate_Bark, Rate_Ubc], axis=0)
                    if not (np.isnan(yval).any()):
                        traces.append (go.Scatter(x = xvals, y=yval, arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=np.nanmean([Rate_Graf[0], Rate_Bikes[0], Rate_Boat[0], Rate_Leuven[0], Rate_Wall[0], Rate_Trees[0], Rate_Bark[0], Rate_Ubc[0]], axis=0), arg=sett), row=3, col=3)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches", "Total Time(1K)", "Inlier Time(1K)"]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=y, method="update", 
                                args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis4.title": f"<span style='font-size: 22px;'><b>{y}</b></span>"}]))
    fig4.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1)])        
    fig4.write_html(f"./html/oxford/oxfordAll9.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxfordAll9.html", "a") as f:
        f.write(custom_html)

def oxford9():
    fig5 = go.Figure()
    fig5 = make_subplots(rows=3, cols=3,subplot_titles=["<span style='font-size: 20px;'><b>Graf(Viewpoint)</b></span>", "<span style='font-size: 20px;'><b>Bikes(Blur)</b></span>", "<span style='font-size: 20px;'><b>Boat(Zoom + Rotation)</b></span>", 
                                                        "<span style='font-size: 20px;'><b>Leuven(Light)</b></span>", "<span style='font-size: 20px;'><b>Wall(Viewpoint)</b></span>", "<span style='font-size: 20px;'><b>Trees(Blur)</b></span>", 
                                                        "<span style='font-size: 20px;'><b>Bark(Zoom + Rotation)</b></span>","<span style='font-size: 20px;'><b>UBC(JPEG)</b></span>", "<span style='font-size: 20px;'><b>Overall</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    fig5.update_layout(font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Affine Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=70, b=20))
    sett_axis = dict(range=[-0.01, 1.01])
    fig5.update_layout( xaxis=sett_axis, xaxis2=sett_axis, xaxis3=sett_axis, xaxis4=sett_axis, xaxis5=sett_axis, xaxis6=sett_axis, xaxis7=sett_axis, xaxis8=sett_axis, xaxis9=sett_axis,
                        yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis, yaxis5=sett_axis, yaxis6=sett_axis, yaxis7=sett_axis, yaxis8=sett_axis, yaxis9=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    xydata_Graf = [
                        np.nanmean(Rate_graf[:, m, c3, i, j, 13]),
                        np.nanmean(Rate_graf[:, m, c3, i, j, 12]),
                        np.nanmean(Rate_graf[:, m, c3, i, j, 14]),
                        np.nanmean(Rate_graf[:, m, c3, i, j, 15]),
                        np.nanmean(Rate_graf[:, m, c3, i, j, 9]),
                        np.nanmean(Rate_graf[:, m, c3, i, j, 10]),
                        np.nanmean(Exec_time_graf[:, m, c3, i, j, 6]),
                        np.nanmean(Exec_time_graf[:, m, c3, i, j, 7])
                    ]
                    xydata_Bikes = [
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 10]), 
                        np.nanmean(Exec_time_bikes[:, m, c3, i, j, 6]), 
                        np.nanmean(Exec_time_bikes[:, m, c3, i, j, 7])
                    ]
                    xydata_Boat = [
                        np.nanmean(Rate_boat[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 10]), 
                        np.nanmean(Exec_time_boat[:, m, c3, i, j, 6]), 
                        np.nanmean(Exec_time_boat[:, m, c3, i, j, 7])
                    ]
                    xydata_Leuven = [
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 10]), 
                        np.nanmean(Exec_time_leuven[:, m, c3, i, j, 6]), 
                        np.nanmean(Exec_time_leuven[:, m, c3, i, j, 7])
                    ]
                    xydata_Wall = [
                        np.nanmean(Rate_wall[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 10]), 
                        np.nanmean(Exec_time_wall[:, m, c3, i, j, 6]), 
                        np.nanmean(Exec_time_wall[:, m, c3, i, j, 7])
                    ]
                    xydata_Trees = [
                        np.nanmean(Rate_trees[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 10]), 
                        np.nanmean(Exec_time_trees[:, m, c3, i, j, 6]), 
                        np.nanmean(Exec_time_trees[:, m, c3, i, j, 7])
                    ]
                    xydata_Bark = [
                        np.nanmean(Rate_bark[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 10]), 
                        np.nanmean(Exec_time_bark[:, m, c3, i, j, 6]), 
                        np.nanmean(Exec_time_bark[:, m, c3, i, j, 7])
                    ]
                    xydata_Ubc = [
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 10]),
                        np.nanmean(Exec_time_ubc[:, m, c3, i, j, 6]), 
                        np.nanmean(Exec_time_ubc[:, m, c3, i, j, 7])
                    ]
                    legend_groupfig5 = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False,
                                hovertemplate="x: <b>%{x:.2f}</b> | y: <b>%{y:.2f}</b>")
                    # Graf(Viewpoint)
                    if not (np.isnan(xydata_Graf).any()):
                        traces.append(go.Scatter( x=xydata_Graf,        y=xydata_Graf,       arg=sett))
                        fig5.add_trace(go.Scatter(x=[xydata_Graf[0]],   y=[xydata_Graf[1]],  arg=sett), row=1, col=1)
                    # Bikes(Blur)
                    if not (np.isnan(xydata_Bikes).any()):
                        traces.append(go.Scatter( x=xydata_Bikes,       y=xydata_Bikes,      arg=sett))
                        fig5.add_trace(go.Scatter(x=[xydata_Bikes[0]],  y=[xydata_Bikes[1]], arg=sett), row=1, col=2)
                    # Boat(Zoom + Rotation)
                    if not (np.isnan(xydata_Boat).any()):
                        traces.append(go.Scatter( x=xydata_Boat,        y=xydata_Boat,       arg=sett))
                        fig5.add_trace(go.Scatter(x=[xydata_Boat[0]],   y=[xydata_Boat[1]],  arg=sett), row=1, col=3)
                    # Leuven(Light)
                    if not (np.isnan(xydata_Leuven).any()):
                        traces.append(go.Scatter( x=xydata_Leuven,      y=xydata_Leuven,     arg=sett))
                        fig5.add_trace(go.Scatter(x=[xydata_Leuven[0]], y=[xydata_Leuven[1]],arg=sett), row=2, col=1)
                    # Wall(Viewpoint)
                    if not (np.isnan(xydata_Wall).any()):
                        traces.append(go.Scatter( x=xydata_Wall,        y=xydata_Wall,       arg=sett))
                        fig5.add_trace(go.Scatter(x=[xydata_Wall[0]],   y=[xydata_Wall[1]],  arg=sett), row=2, col=2)
                    # Trees(Blur)
                    if not (np.isnan(xydata_Trees).any()):
                        traces.append(go.Scatter( x=xydata_Trees,       y=xydata_Trees,      arg=sett))
                        fig5.add_trace(go.Scatter(x=[xydata_Trees[0]],  y=[xydata_Trees[1]], arg=sett), row=2, col=3)
                    # Bark(Zoom + Rotation)
                    if not (np.isnan(xydata_Bark).any()):
                        traces.append(go.Scatter( x=xydata_Bark,        y=xydata_Bark,       arg=sett))
                        fig5.add_trace(go.Scatter(x=[xydata_Bark[0]],   y=[xydata_Bark[1]],  arg=sett), row=3, col=1)
                    # UBC(JPEG)
                    if not (np.isnan(xydata_Ubc).any()):
                        traces.append(go.Scatter( x=xydata_Ubc,         y=xydata_Ubc,        arg=sett))
                        fig5.add_trace(go.Scatter(x=[xydata_Ubc[0]],    y=[xydata_Ubc[1]],   arg=sett), row=3, col=2)
                    # Overall
                    yval = np.nanmean([xydata_Graf, xydata_Bikes, xydata_Boat, xydata_Leuven, xydata_Wall, xydata_Trees, xydata_Bark, xydata_Ubc], axis=0)
                    if not (np.isnan(yval).any()):
                        traces.append(go.Scatter( x=yval,       y=yval,      arg=sett))
                        fig5.add_trace(go.Scatter(x=[yval[0]],  y=[yval[1]], arg=sett), row=3, col=3)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches", "Total Time(1K)", "Inlier Time(1K)"]
    button_listx = []
    button_listy = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict(label=axis, method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis8.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict(label=axis, method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis4.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig5.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listx, direction="down", x=0,    xanchor="left", y=1),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listy, direction="down", x=0.14, xanchor="left", y=1)])
    fig5.write_html(f"./html/oxford/oxford9.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford9.html", "a") as f:
        f.write(custom_html)

def oxford():
    fig14 = go.Figure()
    fig14.update_layout(font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Data Timings</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=50, b=20), xaxis=dict(range=[-0.01, 1.01]), yaxis=dict(range=[-0.01, 1.01]))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    xydata = [
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 13], Rate_bikes[:, m, c3, i, j, 13], Rate_boat[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 13], Rate_wall[:, m, c3, i, j, 13], Rate_trees[:, m, c3, i, j, 13], Rate_bark[:, m, c3, i, j, 13], Rate_ubc[:, m, c3, i, j, 13]), axis=0)),  # Precision
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 12], Rate_bikes[:, m, c3, i, j, 12], Rate_boat[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 12], Rate_wall[:, m, c3, i, j, 12], Rate_trees[:, m, c3, i, j, 12], Rate_bark[:, m, c3, i, j, 12], Rate_ubc[:, m, c3, i, j, 12]), axis=0)),  # Recall
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 14], Rate_bikes[:, m, c3, i, j, 14], Rate_boat[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 14], Rate_wall[:, m, c3, i, j, 14], Rate_trees[:, m, c3, i, j, 14], Rate_bark[:, m, c3, i, j, 14], Rate_ubc[:, m, c3, i, j, 14]), axis=0)),  # Repeatibility
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 15], Rate_bikes[:, m, c3, i, j, 15], Rate_boat[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 15], Rate_wall[:, m, c3, i, j, 15], Rate_trees[:, m, c3, i, j, 15], Rate_bark[:, m, c3, i, j, 15], Rate_ubc[:, m, c3, i, j, 15]), axis=0)),  # F1 Score
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 9],  Rate_bikes[:, m, c3, i, j, 9],  Rate_boat[:, m, c3, i, j, 9],  Rate_leuven[:, m, c3, i, j, 9],  Rate_wall[:, m, c3, i, j, 9],  Rate_trees[:, m, c3, i, j, 9],  Rate_bark[:, m, c3, i, j, 9],  Rate_ubc[:, m, c3, i, j, 9]), axis=0)),   # Inliers
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 10], Rate_bikes[:, m, c3, i, j, 10], Rate_boat[:, m, c3, i, j, 10], Rate_leuven[:, m, c3, i, j, 10], Rate_wall[:, m, c3, i, j, 10], Rate_trees[:, m, c3, i, j, 10], Rate_bark[:, m, c3, i, j, 10], Rate_ubc[:, m, c3, i, j, 10]), axis=0)),   # Matches
                        np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 6], Exec_time_bikes[:, m, c3, i, j, 6], Exec_time_boat[:, m, c3, i, j, 6], Exec_time_leuven[:, m, c3, i, j, 6], Exec_time_wall[:, m, c3, i, j, 6], Exec_time_trees[:, m, c3, i, j, 6], Exec_time_bark[:, m, c3, i, j, 6], Exec_time_ubc[:, m, c3, i, j, 6]), axis=0)),  # Total Time
                        np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 7], Exec_time_bikes[:, m, c3, i, j, 7], Exec_time_boat[:, m, c3, i, j, 7], Exec_time_leuven[:, m, c3, i, j, 7], Exec_time_wall[:, m, c3, i, j, 7], Exec_time_trees[:, m, c3, i, j, 7], Exec_time_bark[:, m, c3, i, j, 7], Exec_time_ubc[:, m, c3, i, j, 7]), axis=0))   # Inlier Time
                    ]
                    if not (np.isnan(xydata).any()):
                        traces.append(  go.Scatter( x=xydata, y=xydata, mode="markers", marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                    fig14.add_trace(go.Scatter( x=[xydata[0]], y=[xydata[1]], mode="markers", marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                        showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches", "Total Time(1K)", "Inlier Time(1K)"]
    button_listx = []
    button_listy = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict( label=axis, method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict( label=axis, method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig14.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listx, direction="down", x=0,    xanchor="left", y=1),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listy, direction="down", x=0.14, xanchor="left", y=1)])
    fig14.write_html(f"./html/oxford/oxford.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford.html", "a") as f:
        f.write(custom_html)

def oxfordTiming():
    fig6 = go.Figure()
    fig6 = make_subplots(   rows=5, cols=2, subplot_titles=["<span style='font-size: 22px;'>Total & Inlier time (Detect + Descript + Match(BF) | MAGSAC++)</span>", "<span style='font-size: 22px;'>Total & Inlier time (Detect + Descript + Match(Flann) | MAGSAC++)</span>",
                                                            "<span style='font-size: 22px;'>Total time (Detect + Descript + Match(BF+Flann))</span>", "<span style='font-size: 22px;'>Inlier time (Detect + Descript + Match(BF+Flann) + MAGSAC++)</span>",
                                                            "<span style='font-size: 22px;'>Detect time</span>", "<span style='font-size: 22px;'>Describe time</span>"],
                            specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}]], horizontal_spacing=0.05, vertical_spacing=0.05)
    fig6.update_layout(font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Affine Dataset Timings for Average 1k</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), barmode="stack", height=2000, margin=dict(l=20, r=20, t=80, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 6],          Exec_time_wall[:, m, :, i, j, 6],           Exec_time_trees[:, m, :, i, j, 6],          Exec_time_bikes[:, m, :, i, j, 6],          Exec_time_bark[:, m, :, i, j, 6],           Exec_time_boat[:, m, :, i, j, 6],           Exec_time_leuven[:, m, :, i, j, 6],         Exec_time_ubc[:, m, :, i, j, 6]),           axis=0))
                result3m= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, m, :, i, j, 6],   Exec_time_wall_mobile[:, m, :, i, j, 6],    Exec_time_trees_mobile[:, m, :, i, j, 6],   Exec_time_bikes_mobile[:, m, :, i, j, 6],   Exec_time_bark_mobile[:, m, :, i, j, 6],    Exec_time_boat_mobile[:, m, :, i, j, 6],    Exec_time_leuven_mobile[:, m, :, i, j, 6],  Exec_time_ubc_mobile[:, m, :, i, j, 6]),    axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 7],          Exec_time_wall[:, m, :, i, j, 7],           Exec_time_trees[:, m, :, i, j, 7],          Exec_time_bikes[:, m, :, i, j, 7],          Exec_time_bark[:, m, :, i, j, 7],           Exec_time_boat[:, m, :, i, j, 7],           Exec_time_leuven[:, m, :, i, j, 7],         Exec_time_ubc[:, m, :, i, j, 7]),           axis=0))
                result4m= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, m, :, i, j, 7],   Exec_time_wall_mobile[:, m, :, i, j, 7],    Exec_time_trees_mobile[:, m, :, i, j, 7],   Exec_time_bikes_mobile[:, m, :, i, j, 7],   Exec_time_bark_mobile[:, m, :, i, j, 7],    Exec_time_boat_mobile[:, m, :, i, j, 7],    Exec_time_leuven_mobile[:, m, :, i, j, 7],  Exec_time_ubc_mobile[:, m, :, i, j, 7]),    axis=0))
                if not (result3 == 0 or np.isnan(result3).any or result3m == 0 or np.isnan(result3m).any):
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["pc"]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-p",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig6.add_trace(trace_match_synt_result3,  row=1, col=1) if m == 0 else fig6.add_trace(trace_match_synt_result3, row=2, col=1)
                    trace_match_synt_result3m= go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["mobile"]], y=[result3m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m",
                                                        text=[f"{result3m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig6.add_trace(trace_match_synt_result3m, row=1, col=1) if m == 0 else fig6.add_trace(trace_match_synt_result3m, row=2, col=1)
                    trace_match_synt_result3.showlegend  = False
                    fig6.add_trace(trace_match_synt_result3,  row=3, col=1)
                    trace_match_synt_result3m.showlegend = False
                    fig6.add_trace(trace_match_synt_result3m, row=3, col=1)
                if not (result4 == 0 or np.isnan(result4).any or result4m == 0 or np.isnan(result4m).any):
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["pc"]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-p",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig6.add_trace(trace_match_synt_result4,  row=1, col=1) if m == 0 else fig6.add_trace(trace_match_synt_result4, row=2, col=1)
                    trace_match_synt_result4m = go.Bar( x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["mobile"]], y=[result4m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m",
                                                        text=[f"{result4m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig6.add_trace(trace_match_synt_result4m, row=1, col=1) if m == 0 else fig6.add_trace(trace_match_synt_result4m, row=2, col=1)
                    trace_match_synt_result4.showlegend  = False
                    fig6.add_trace(trace_match_synt_result4,  row=4, col=1)
                    trace_match_synt_result4m.showlegend = False
                    fig6.add_trace(trace_match_synt_result4m, row=4, col=1)
            color_index = (color_index + 14) % num_combinations            
        result = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, i, :, 4], Exec_time_wall[:, :, :, i, :, 4], Exec_time_trees[:, :, :, i, :, 4], Exec_time_bikes[:, :, :, i, :, 4], Exec_time_bark[:, :, :, i, :, 4], Exec_time_boat[:, :, :, i, :, 4], Exec_time_leuven[:, :, :, i, :, 4], Exec_time_ubc[:, :, :, i, :, 4]), axis=0))
        resultm= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, :, :, i, :, 4], Exec_time_wall_mobile[:, :, :, i, :, 4], Exec_time_trees_mobile[:, :, :, i, :, 4], Exec_time_bikes_mobile[:, :, :, i, :, 4], Exec_time_bark_mobile[:, :, :, i, :, 4], Exec_time_boat_mobile[:, :, :, i, :, 4], Exec_time_leuven_mobile[:, :, :, i, :, 4], Exec_time_ubc_mobile[:, :, :, i, :, 4]), axis=0))
        if not (result == 0 or np.isnan(result).any or resultm == 0 or np.isnan(resultm).any):
            trace_detect_oxford = go.Bar(x=[[DetectorsLegend[i]],["pc"]],     y=[result],  name=f".{DetectorsLegend[i]}-p", showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            trace_detect_oxfordm= go.Bar(x=[[DetectorsLegend[i]],["mobile"]], y=[resultm], name=f".{DetectorsLegend[i]}-m", showlegend=True, text=[f"{resultm:.3f}"], marker=dict(color = colors[14*i]))
            fig6.add_trace(trace_detect_oxford,  row=5, col=1)
            fig6.add_trace(trace_detect_oxfordm, row=5, col=1)
        
        result2 = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, :, i, 5], Exec_time_wall[:, :, :, :, i, 5], Exec_time_trees[:, :, :, :, i, 5], Exec_time_bikes[:, :, :, :, i, 5], Exec_time_bark[:, :, :, :, i, 5], Exec_time_boat[:, :, :, :, i, 5], Exec_time_leuven[:, :, :, :, i, 5], Exec_time_ubc[:, :, :, :, i, 5]), axis=0))
        result2m= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, :, :, :, i, 5], Exec_time_wall_mobile[:, :, :, :, i, 5], Exec_time_trees_mobile[:, :, :, :, i, 5], Exec_time_bikes_mobile[:, :, :, :, i, 5], Exec_time_bark_mobile[:, :, :, :, i, 5], Exec_time_boat_mobile[:, :, :, :, i, 5], Exec_time_leuven_mobile[:, :, :, :, i, 5], Exec_time_ubc_mobile[:, :, :, :, i, 5]), axis=0))
        if not (result2 == 0 or np.isnan(result2).any or result2m == 0 or np.isnan(result2m).any):
            trace_descr_oxford = go.Bar(x=[[DescriptorsLegend[i]],["pc"]],     y=[result2],  name=f"-{DescriptorsLegend[i]}-p", showlegend=True, text=[f"{result2:.3f}"],  marker=dict(color = colors[14*i]))
            trace_descr_oxfordm= go.Bar(x=[[DescriptorsLegend[i]],["mobile"]], y=[result2m], name=f"-{DescriptorsLegend[i]}-m", showlegend=True, text=[f"{result2m:.3f}"], marker=dict(color = colors[14*i]))
            fig6.add_trace(trace_descr_oxford,  row=5, col=2)
            fig6.add_trace(trace_descr_oxfordm, row=5, col=2)
        
    fig6.update_layout(updatemenus=[dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",   method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear"}]),
                                                                    dict(label="Log",      method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log"}])], x=0, xanchor="left", y=1)])
    fig6.write_html("./html/oxford/oxfordTiming.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxfordTiming.html", "a") as f:
        f.write(custom_html)

########################################
# MARK: - Single Data (Drone-UAV-AirSim)
########################################
def singleAll(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig7 = go.Figure()
    xvals = [f"Img{i}" for i in range(153, 188)] if data == "drone" else (
        ["Bahamas", "Office", "Suburban", "Building", "Construction", "Dominica", "Cadastre", "Rivaz", "Urban", "Belleview"] if data == "uav" else 
        [f"Img{i}" for i in range(653, 774, 5)])
    fig7.update_layout( font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()} Data</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=50, b=20), yaxis=dict(range=[-0.01, 1.01]))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    y_data = [
                        Rate[:, m, c3, i, j, 13],       # Precision
                        Rate[:, m, c3, i, j, 12],       # Recall
                        Rate[:, m, c3, i, j, 14],       # Repeatibility
                        Rate[:, m, c3, i, j, 15],       # F1 Score
                        Rate[:, m, c3, i, j,  9],       # Inliers
                        Rate[:, m, c3, i, j, 10],       # Matches
                        Exec_time[:, m, c3, i, j, 6],   # 1K Total Time
                        Exec_time[:, m, c3, i, j, 7],   # 1K feature Inlier Time
                    ]
                    if not (np.isnan(y_data).any()):
                        traces.append(go.Scatter(x=xvals, y=y_data, mode="markers+lines",
                                                marker=dict(symbol=marker_symbols[symbol_index], color=colors[color_index], size=16),
                                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                showlegend=True, hovertemplate="<b>%{y:.3f}</b>"))
                    fig7.add_trace(go.Scatter(  x=xvals, y=y_data[0], mode="markers+lines",
                                            marker=dict(symbol=marker_symbols[symbol_index], color=colors[color_index], size=16),
                                            line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="<b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches", "Total Time(1K)", "Inlier Time(1K)"]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=y, method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{y}</b></span>"}]))
    
    fig7.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1)]) 
    fig7.write_html(f"./html/{data}/{data}All.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}All.html", "a") as f:
        f.write(custom_html)

def single(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig13 = go.Figure()
    fig13.update_layout(font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()}</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"),
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=50, b=20), xaxis=dict(range=[-0.01, 1.01]), yaxis=dict(range=[-0.01, 1.01]))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    xydata = [
                        np.nanmean(Rate[:, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate[:, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate[:, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate[:, m, c3, i, j, 15]),       # F1 Score
                        np.nanmean(Rate[:, m, c3, i, j,  9]),       # Inliers
                        np.nanmean(Rate[:, m, c3, i, j, 10]),       # Matches
                        np.nanmean(Rate[:, m, c3, i, j, 11]),       # Reprojection Error
                        np.nanmean(Exec_time[:, m, c3, i, j, 6]),   # 1K Total Time
                        np.nanmean(Exec_time[:, m, c3, i, j, 7]),   # 1K feature Inlier Time
                        np.nanmean(Rate[:, m, c3, i, j, 16])]       # 3D Points Count
                    if not (np.isnan(xydata).any()):
                        traces.append(  go.Scatter(x=xydata, y=xydata, mode="markers", 
                                            marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.2f}</b> | y: <b>%{y:.2f}</b>"))
                    fig13.add_trace(go.Scatter(x=[xydata[0]], y=[xydata[1]], mode="markers", 
                                        marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                        showlegend=True, hovertemplate="x: <b>%{x:.2f}</b> | y: <b>%{y:.2f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches", "Reprojection Error(pixel)", "Total Time(1K)", "Inlier Time(1K)", "3D Points Count"]
    button_listx = []
    button_listy = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict( label=axis, method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict( label=axis, method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig13.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listx, direction="down", x=0,    xanchor="left", y=1),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listy, direction="down", x=0.14, xanchor="left", y=1)])
    fig13.write_html(f"./html/{data}/{data}.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}.html", "a") as f:
        f.write(custom_html)

def singleTiming(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    fig12 = go.Figure()
    fig12 = make_subplots(  rows=5, cols=2, subplot_titles=["<span style='font-size: 22px;'>Total & Inlier time (Detect + Descript + Match(BF) | MAGSAC++)</span>", "<span style='font-size: 22px;'>Total & Inlier time (Detect + Descript + Match(Flann) | MAGSAC++)</span>",
                                                            "<span style='font-size: 22px;'>Total time (Detect + Descript + Match(BF+Flann))</span>", "<span style='font-size: 22px;'>Inlier time (Detect + Descript + Match(BF+Flann) + MAGSAC++)</span>",
                                                            "<span style='font-size: 22px;'>Detect time</span>", "<span style='font-size: 22px;'>Describe time</span>"],
                            specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}]],horizontal_spacing=0.05, vertical_spacing=0.05)
    fig12.update_layout(font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()} Timings for Average 1k</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), barmode="stack", height=2000, margin=dict(l=20, r=20, t=80, b=20), hovermode="x unified")
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(Exec_time[:, m, :, i, j, 6])
                result4 = np.nanmean(Exec_time[:, m, :, i, j, 7])
                if not (result3 == 0 or np.isnan(result3).any):
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                        text=[f"{result3:.3f}"], marker=dict(color = colors[color_index]),
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig12.add_trace(trace_match_synt_result3, row=1, col=1) if m == 0 else fig12.add_trace(trace_match_synt_result3, row=2, col=1)
                    trace_match_synt_result3.showlegend = False
                    fig12.add_trace(trace_match_synt_result3, row=3, col=1)
                if not (result4 == 0 or np.isnan(result4).any):
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                        text=[f"{result4:.3f}"], marker=dict(color = colors[color_index]),
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig12.add_trace(trace_match_synt_result4, row=1, col=1) if m == 0 else fig12.add_trace(trace_match_synt_result4, row=2, col=1)
                    trace_match_synt_result4.showlegend = False
                    fig12.add_trace(trace_match_synt_result4, row=4, col=1)
                symbol_index = (symbol_index + 1) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
        result = np.nanmean(Exec_time[:, :, :, i, :, 4])
        if not (result == 0 or np.isnan(result).any):
            trace_detect = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=f".{DetectorsLegend[i]}",  showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            fig12.add_trace(trace_detect, row=5, col=1)
        result2 = np.nanmean(Exec_time[:, :, :, :, i, 5])
        if not (result2 == 0 or np.isnan(result2).any):
            trace_descr = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=f"-{DescriptorsLegend[i]}",showlegend=True, text=[f"{result2:.3f}"], marker=dict(color = colors[14*i]))
            fig12.add_trace(trace_descr, row=5, col=2)
        
    fig12.update_layout(updatemenus=[   dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1),
                                        dict(type="dropdown", buttons=[ dict(label="Linear",   method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear"}]),
                                                                        dict(label="Log",      method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log"}])], x=0, xanchor="left", y=1)])
    fig12.write_html(f"./html/{data}/{data}Timing.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}Timing.html", "a") as f:
        f.write(custom_html)