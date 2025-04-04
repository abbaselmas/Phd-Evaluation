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
    fig = go.Figure()
    fig = make_subplots(rows=2, cols=2, subplot_titles=["<span style='font-size: 20px;'><b>Intensity changing I+b</b></span>", "<span style='font-size: 20px;'><b>Intensity changing Ixc</b></span>", "<span style='font-size: 20px;'><b>Scale changing</b></span>", "<span style='font-size: 20px;'><b>Rotation changing</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    sett_axis = dict(range=[-0.01, 1.01])
    fig.update_layout( template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=60, b=20), yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis,
                        xaxis=dict(tickmode="array", tickvals=val_b), xaxis2=dict(tickmode="array", tickvals=val_c), xaxis3=dict(tickmode="array", tickvals=scale), xaxis4=dict(tickmode="array", tickvals=rot))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1 = [
                        Rate_intensity[:len(val_b), m, c3, i, j, 13], 
                        Rate_intensity[:len(val_b), m, c3, i, j, 12], 
                        Rate_intensity[:len(val_b), m, c3, i, j, 14], 
                        Rate_intensity[:len(val_b), m, c3, i, j, 15], 
                        Rate_intensity[:len(val_b), m, c3, i, j,  9], 
                        Rate_intensity[:len(val_b), m, c3, i, j, 10], 
                        1 - nonlinear_normalize(Exec_time_intensity[:len(val_b), m, c3, i, j, 6], Exec_time_intensity[:len(val_b), :, :, :, :, 6]),
                        1 - nonlinear_normalize(Exec_time_intensity[:len(val_b), m, c3, i, j, 7], Exec_time_intensity[:len(val_b), :, :, :, :, 7])]
                    Rate2_I2 = [
                        Rate_intensity[len(val_c):, m, c3, i, j, 13], 
                        Rate_intensity[len(val_c):, m, c3, i, j, 12], 
                        Rate_intensity[len(val_c):, m, c3, i, j, 14], 
                        Rate_intensity[len(val_c):, m, c3, i, j, 15], 
                        Rate_intensity[len(val_c):, m, c3, i, j,  9], 
                        Rate_intensity[len(val_c):, m, c3, i, j, 10],
                        1 - nonlinear_normalize(Exec_time_intensity[len(val_c):, m, c3, i, j, 6], Exec_time_intensity[len(val_c):, :, :, :, :, 6]),
                        1 - nonlinear_normalize(Exec_time_intensity[len(val_c):, m, c3, i, j, 7], Exec_time_intensity[len(val_c):, :, :, :, :, 7])]
                    Rate2_S  = [
                        Rate_scale[:, m, c3, i, j, 13], 
                        Rate_scale[:, m, c3, i, j, 12], 
                        Rate_scale[:, m, c3, i, j, 14], 
                        Rate_scale[:, m, c3, i, j, 15], 
                        Rate_scale[:, m, c3, i, j,  9], 
                        Rate_scale[:, m, c3, i, j, 10],
                        1 - nonlinear_normalize(Exec_time_scale[:, m, c3, i, j, 6], Exec_time_scale[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(Exec_time_scale[:, m, c3, i, j, 7], Exec_time_scale[:, :, :, :, :, 7])]
                    Rate2_R  = [
                        Rate_rot[:, m, c3, i, j, 13], 
                        Rate_rot[:, m, c3, i, j, 12], 
                        Rate_rot[:, m, c3, i, j, 14], 
                        Rate_rot[:, m, c3, i, j, 15], 
                        Rate_rot[:, m, c3, i, j,  9], 
                        Rate_rot[:, m, c3, i, j, 10],
                        1 - nonlinear_normalize(Exec_time_rot[:, m, c3, i, j, 6], Exec_time_rot[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(Exec_time_rot[:, m, c3, i, j, 7], Exec_time_rot[:, :, :, :, :, 7])]
                    legend_groupfig = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig, legendgroup=legend_groupfig, showlegend=True, hovertemplate="<b>%{y:.3f}</b>")
                    if not (np.isnan(Rate2_I1).any() or np.isnan(Rate2_I2).any() or np.isnan(Rate2_S).any() or np.isnan(Rate2_R).any()):
                    # if not np.isnan(Rate2_I1).any():
                        traces.append(go.Scatter(x=val_b, y=Rate2_I1,    arg=sett))
                        fig.add_trace(go.Scatter(x=val_b, y=Rate2_I1[0], arg=sett), row=1, col=1)
                    # if not np.isnan(Rate2_I2).any():
                        traces.append(go.Scatter(x=val_c, y=Rate2_I2,    arg=sett))
                        fig.add_trace(go.Scatter(x=val_c, y=Rate2_I2[0], arg=sett), row=1, col=2)
                    # if not np.isnan(Rate2_S).any():
                        traces.append(go.Scatter(x=scale, y=Rate2_S,     arg=sett))
                        fig.add_trace(go.Scatter(x=scale, y=Rate2_S[0],  arg=sett), row=2, col=1)
                    # if not np.isnan(Rate2_R).any():
                        traces.append(go.Scatter(x=rot,   y=Rate2_R,     arg=sett))
                        fig.add_trace(go.Scatter(x=rot,   y=Rate2_R[0],  arg=sett), row=2, col=2)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=f"y: {y}", method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis3.title": f"<span style='font-size: 22px;'><b>{y}</b></span>"}]))    
    fig.update_layout(updatemenus=[ dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1, yanchor="bottom")]) 
    fig.write_html(f"./html/synthetic/syntheticAll4.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/syntheticAll4.html", "a") as f:
        f.write(custom_html)

def synthetic4():
    fig = go.Figure()
    fig = make_subplots(rows=2, cols=2, subplot_titles=["<span style='font-size: 20px;'><b>Intensity changing I+b</b></span>", "<span style='font-size: 20px;'><b>Intensity changing Ixc</b></span>", "<span style='font-size: 20px;'><b>Scale changing</b></span>", "<span style='font-size: 20px;'><b>Rotation changing</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    sett_axis = dict(range=[-0.01, 1.01])
    fig.update_layout( template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=70, b=20),
                        xaxis=sett_axis, xaxis2=sett_axis, xaxis3=sett_axis, xaxis4=sett_axis,
                        yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis)
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
                        1 - nonlinear_normalize(np.nanmean(Exec_time_intensity[:len(val_b), m, c3, i, j, 6]), Exec_time_intensity[:len(val_b), :, :, :, :, 6]), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time_intensity[:len(val_b), m, c3, i, j, 7]), Exec_time_intensity[:len(val_b), :, :, :, :, 7])  # 1K feature Inlier Time
                    ]
                    xydata_Intensity2 = [
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 15]),       # F1 Score
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j,  9]),       # Inliers
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 10]),       # Matches
                        1 - nonlinear_normalize(np.nanmean(Exec_time_intensity[len(val_c):, m, c3, i, j, 6]), Exec_time_intensity[len(val_c):, :, :, :, :, 6]), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time_intensity[len(val_c):, m, c3, i, j, 7]), Exec_time_intensity[len(val_c):, :, :, :, :, 7])  # 1K feature Inlier Time
                    ]
                    xydata_Scale = [
                        np.nanmean(Rate_scale[:, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_scale[:, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_scale[:, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_scale[:, m, c3, i, j, 15]),       # F1 Score
                        np.nanmean(Rate_scale[:, m, c3, i, j,  9]),       # Inliers
                        np.nanmean(Rate_scale[:, m, c3, i, j, 10]),       # Matches
                        1 - nonlinear_normalize(np.nanmean(Exec_time_scale[:, m, c3, i, j, 6]), Exec_time_scale[:, :, :, :, :, 6]), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time_scale[:, m, c3, i, j, 7]), Exec_time_scale[:, :, :, :, :, 7])  # 1K feature Inlier Time
                    ]
                    xydata_Rotation = [
                        np.nanmean(Rate_rot[:, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_rot[:, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_rot[:, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_rot[:, m, c3, i, j, 15]),       # F1 Score
                        np.nanmean(Rate_rot[:, m, c3, i, j,  9]),       # Inliers
                        np.nanmean(Rate_rot[:, m, c3, i, j, 10]),       # Matches
                        1 - nonlinear_normalize(np.nanmean(Exec_time_rot[:, m, c3, i, j, 6]), Exec_time_rot[:, :, :, :, :, 6]), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time_rot[:, m, c3, i, j, 7]), Exec_time_rot[:, :, :, :, :, 7])  # 1K feature Inlier Time
                    ]
                    legend_groupfig = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                name=legend_groupfig, legendgroup=legend_groupfig, showlegend=True,
                                hovertemplate="x: <b>%{x:.2f}</b> | y: <b>%{y:.2f}</b>")
                    if not (np.isnan(xydata_Intensity1).any() or np.isnan(xydata_Intensity2).any() or np.isnan(xydata_Scale).any() or np.isnan(xydata_Rotation).any()):
                    # if not np.isnan(xydata_Intensity1).any():
                        traces.append(go.Scatter( x=xydata_Intensity1,      y=xydata_Intensity1,      arg=sett, marker_size=xydata_Intensity1))
                        fig.add_trace(go.Scatter(x=[xydata_Intensity1[0]], y=[xydata_Intensity1[1]], arg=sett), row=1, col=1)
                    # if not np.isnan(xydata_Intensity2).any():
                        traces.append(go.Scatter( x=xydata_Intensity2,      y=xydata_Intensity2,      arg=sett, marker_size=xydata_Intensity2))
                        fig.add_trace(go.Scatter(x=[xydata_Intensity2[0]], y=[xydata_Intensity2[1]], arg=sett), row=1, col=2)
                    # if not np.isnan(xydata_Scale).any():
                        traces.append(go.Scatter( x=xydata_Scale,           y=xydata_Scale,           arg=sett, marker_size=xydata_Scale))
                        fig.add_trace(go.Scatter(x=[xydata_Scale[0]],      y=[xydata_Scale[1]],      arg=sett), row=2, col=1)
                    # if not np.isnan(xydata_Rotation).any():
                        traces.append(go.Scatter( x=xydata_Rotation,        y=xydata_Rotation,        arg=sett, marker_size=xydata_Rotation))
                        fig.add_trace(go.Scatter(x=[xydata_Rotation[0]],   y=[xydata_Rotation[1]],   arg=sett), row=2, col=2)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_listx = []
    button_listy = []
    button_listz = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict(label=f"x: {axis}", method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis3.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict(label=f"y: {axis}", method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis3.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listz.append(dict(label=f"z: {axis}", method="update", args=[{"marker.size": [((trace.marker.size[idx]*40+10)%50) for trace in traces]}]))
    fig.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listy, direction="down", x=0,  xanchor="left",  y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listx, direction="up",   x=1,  xanchor="right", y=0, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=5, buttons=button_listz, direction="down", x=0,  xanchor="left",  y=1)])
    fig.write_html(f"./html/synthetic/synthetic4.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic4.html", "a") as f:
        f.write(custom_html)

def synthetic():
    fig = go.Figure()
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=50, b=20), xaxis=dict(range=[-0.01, 1.01]), yaxis=dict(range=[-0.01, 1.01]))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    xydata = [
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 13], Rate_scale[:, m, c3, i, j, 13], Rate_rot[:, m, c3, i, j, 13]), axis=0)),                 # Precision
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 12], Rate_scale[:, m, c3, i, j, 12], Rate_rot[:, m, c3, i, j, 12]), axis=0)),                 # Recall
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 14], Rate_scale[:, m, c3, i, j, 14], Rate_rot[:, m, c3, i, j, 14]), axis=0)),                 # Repeatibility
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 15], Rate_scale[:, m, c3, i, j, 15], Rate_rot[:, m, c3, i, j, 15]), axis=0)),                 # F1 Score
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j,  9], Rate_scale[:, m, c3, i, j,  9], Rate_rot[:, m, c3, i, j,  9]), axis=0)),                 # Inliers
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 10], Rate_scale[:, m, c3, i, j, 10], Rate_rot[:, m, c3, i, j, 10]), axis=0)),                 # Matches
                        1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 6], Exec_time_scale[:, m, c3, i, j, 6], Exec_time_rot[:, m, c3, i, j, 6]), axis=0)), np.concatenate((Exec_time_intensity[:, :, :, :, :, 6], Exec_time_scale[:, :, :, :, :, 6], Exec_time_rot[:, :, :, :, :, 6]), axis=0)),  # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 7], Exec_time_scale[:, m, c3, i, j, 7], Exec_time_rot[:, m, c3, i, j, 7]), axis=0)), np.concatenate((Exec_time_intensity[:, :, :, :, :, 7], Exec_time_scale[:, :, :, :, :, 7], Exec_time_rot[:, :, :, :, :, 7]), axis=0))]  # 1K feature Inlier Time
                    if not np.isnan(xydata).any():
                        traces.append(go.Scatter(   x=xydata,       y=xydata,       mode="markers", marker=dict(color=colors[color_index], size=xydata, symbol=marker_symbols[symbol_index]),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                        fig.add_trace(go.Scatter(   x=[xydata[0]],  y=[xydata[1]],  mode="markers", marker=dict(color=colors[color_index], size=xydata, symbol=marker_symbols[symbol_index]),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_listx = []
    button_listy = []
    button_listz = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict(label=f"x: {axis}", method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict(label=f"y: {axis}", method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listz.append(dict(label=f"z: {axis}", method="update", args=[{"marker.size": [((trace.marker.size[idx]*40+10)%50) for trace in traces]}]))
    fig.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listy, direction="down", x=0,  xanchor="left",  y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listx, direction="up",   x=1,  xanchor="right", y=0, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=5, buttons=button_listz, direction="down", x=0,  xanchor="left",  y=1)])
    fig.write_html(f"./html/synthetic/synthetic.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic.html", "a") as f:
        f.write(custom_html)

def syntheticTiming():
    fig = go.Figure()
    fig = make_subplots(rows=6, cols=2, subplot_titles=["<span style='font-size: 22px;'>Total time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Total time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>Detect time</span>","<span style='font-size: 22px;'>Describe time</span>",
                                                        "<span style='font-size: 22px;'>All Timings</span>"],
                        specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.06)
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset Timings for Average 1k</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), height=2500, margin=dict(l=20, r=20, t=80, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 6],         Exec_time_scale[:, m, :, i, j, 6],          Exec_time_rot[:, m, :, i, j, 6]),           axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 7],         Exec_time_scale[:, m, :, i, j, 7],          Exec_time_rot[:, m, :, i, j, 7]),           axis=0))
                if not np.isnan(result3) and result3 > 0 and not np.isnan(result4) and result4 > 0:
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_match_synt_result3,  row=1, col=1) if m == 0 else fig.add_trace(trace_match_synt_result3, row=2, col=1)
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_match_synt_result4,  row=3, col=1) if m == 0 else fig.add_trace(trace_match_synt_result4, row=4, col=1)
                    # All timings
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-total']], y=[result3],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                            text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=6, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-inlier']], y=[result4],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                            text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=6, col=1 )
            color_index = (color_index + 14) % num_combinations
        result  = np.nanmean(np.concatenate((Exec_time_intensity       [:, :, :, i, :, 4], Exec_time_scale       [:, :, :, i, :, 4], Exec_time_rot       [:, :, :, i, :, 4]), axis=0))
        result2 = np.nanmean(np.concatenate((Exec_time_intensity       [:, :, :, :, i, 5], Exec_time_scale       [:, :, :, :, i, 5], Exec_time_rot       [:, :, :, :, i, 5]), axis=0))
        if not np.isnan(result) and result > 0:
            trace_detect_synt  = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=f".{DetectorsLegend[i]}-p",   showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            fig.add_trace(trace_detect_synt, row=5, col=1)
        if not np.isnan(result2) and result2 > 0:
            trace_descr_synt  = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=f"-{DescriptorsLegend[i]}-p", showlegend=True, text=[f"{result2:.3f}"], marker=dict(color = colors[14*i]))
            fig.add_trace(trace_descr_synt,  row=5, col=2)
    # for i in range(1, 7):
    #     fig.update_xaxes(tickangle=90, row=i, col=1)
    # fig.update_xaxes(tickangle=90, row=5, col=2)
    fig.update_layout(updatemenus=[ dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear", "yaxis7.type": "linear"}]),
                                                                    dict(label="Log",             method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log", "yaxis7.type": "linear"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html("./html/synthetic/syntheticTiming.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open("./html/synthetic/syntheticTiming.html", "a") as f:
        f.write(custom_html)

def syntheticTimingMobile():
    fig = go.Figure()
    fig = make_subplots(rows=9, cols=1, subplot_titles=["<span style='font-size: 22px;'>Total time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Total time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'><b>Mobile</b> Total time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'><b>Mobile</b> Total time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'><b>Mobile</b> Inlier time <b>BF</b></span>","<span style='font-size: 22px;'><b>Mobile</b> Inlier time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>All Timings</span>"],horizontal_spacing=0.05, vertical_spacing=0.05)
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset Timings for Average 1k</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), barmode="stack", height=3000, margin=dict(l=20, r=20, t=80, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 6],         Exec_time_scale[:, m, :, i, j, 6],          Exec_time_rot[:, m, :, i, j, 6]),           axis=0))
                result3m= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, m, :, i, j, 6], Exec_time_scale_mobile[:, m, :, i, j, 6], Exec_time_rot_mobile[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 7],         Exec_time_scale[:, m, :, i, j, 7],          Exec_time_rot[:, m, :, i, j, 7]),           axis=0))
                result4m= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, m, :, i, j, 7], Exec_time_scale_mobile[:, m, :, i, j, 7], Exec_time_rot_mobile[:, m, :, i, j, 7]), axis=0))
                if not np.isnan(result3) and result3 > 0 and not np.isnan(result4) and result4 > 0 and not np.isnan(result3m) and result3m > 0 and not np.isnan(result4m) and result4m > 0:
                    trace_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-p",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result3,  row=1, col=1) if m == 0 else fig.add_trace(trace_result3, row=2, col=1)
                    trace_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-p",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result4,  row=3, col=1) if m == 0 else fig.add_trace(trace_result4, row=4, col=1)
                    # Mobile timings
                    trace_result3m= go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m",
                                                        text=[f"{result3m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result3m, row=1+4, col=1) if m == 0 else fig.add_trace(trace_result3m, row=2+4, col=1)
                    trace_result4m = go.Bar( x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m",
                                                        text=[f"{result4m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result4m, row=3+4, col=1) if m == 0 else fig.add_trace(trace_result4m, row=4+4, col=1)                    
                    # All timings
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-total-p']], y=[result3],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-p",
                                            text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=9, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-total-m']], y=[result3m],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m",
                                            text=[f"{result3m:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=9, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-inlier-p']], y=[result4],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-p",
                                            text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=9, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-inlier-m']], y=[result4m],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m",
                                            text=[f"{result4m:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=9, col=1 )
            color_index = (color_index + 14) % num_combinations
    # for i in range(1, 10):
    #     fig.update_xaxes(tickangle=90, row=i, col=1)
    fig.update_layout(updatemenus=[ dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear","yaxis7.type": "linear","yaxis8.type": "linear", "yaxis9.type": "linear"}]),
                                                                    dict(label="Log",             method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log","yaxis7.type": "log","yaxis8.type": "log", "yaxis9.type": "log"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html("./html/synthetic/syntheticTimingMobile.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open("./html/synthetic/syntheticTimingMobile.html", "a") as f:
        f.write(custom_html)

def syntheticEfficiency():
    fig = go.Figure()
    fig.update_layout(  template="ggplot2", font_size=16, margin=dict(l=20, r=20, t=80, b=20),
                        title=dict(text=f"<span style='font-size: 26px;'><b>Synthetic Efficiency</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        xaxis_tickangle=90, yaxis=dict(range=[-0.01, 1.01], autorange=False))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    eff_score = (
                        0.12 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 13], Rate_scale[:, m, c3, i, j, 13], Rate_rot[:, m, c3, i, j, 13]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 13], Rate_scale[:, :, :, :, :, 13], Rate_rot[:, :, :, :, :, 13]), axis=0)) + # Precision
                        0.05 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 12], Rate_scale[:, m, c3, i, j, 12], Rate_rot[:, m, c3, i, j, 12]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 12], Rate_scale[:, :, :, :, :, 12], Rate_rot[:, :, :, :, :, 12]), axis=0)) + # Recall
                        0.05 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 14], Rate_scale[:, m, c3, i, j, 14], Rate_rot[:, m, c3, i, j, 14]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 14], Rate_scale[:, :, :, :, :, 14], Rate_rot[:, :, :, :, :, 14]), axis=0)) + # Repeatibility
                        0.15 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 15], Rate_scale[:, m, c3, i, j, 15], Rate_rot[:, m, c3, i, j, 15]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 15], Rate_scale[:, :, :, :, :, 15], Rate_rot[:, :, :, :, :, 15]), axis=0)) + # F1 Score
                        0.08 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j,  9], Rate_scale[:, m, c3, i, j,  9], Rate_rot[:, m, c3, i, j,  9]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :,  9], Rate_scale[:, :, :, :, :,  9], Rate_rot[:, :, :, :, :,  9]), axis=0)) + # Inliers
                        0.05 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 10], Rate_scale[:, m, c3, i, j, 10], Rate_rot[:, m, c3, i, j, 10]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 10], Rate_scale[:, :, :, :, :, 10], Rate_rot[:, :, :, :, :, 10]), axis=0)) + # Matches
                        0.10 * (1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 6], Exec_time_scale[:, m, c3, i, j, 6], Exec_time_rot[:, m, c3, i, j, 6]), axis=0)), np.concatenate((Exec_time_intensity[:, :, :, :, :, 6], Exec_time_scale[:, :, :, :, :, 6], Exec_time_rot[:, :, :, :, :, 6]), axis=0))) + # 1K Total Time
                        0.15 * (1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 7], Exec_time_scale[:, m, c3, i, j, 7], Exec_time_rot[:, m, c3, i, j, 7]), axis=0)), np.concatenate((Exec_time_intensity[:, :, :, :, :, 7], Exec_time_scale[:, :, :, :, :, 7], Exec_time_rot[:, :, :, :, :, 7]), axis=0)))   # 1K feature Inlier Time
                    ) * 4 / 3
                    if not (eff_score == 0 or np.isnan(eff_score)):
                        fig.add_trace(go.Scatter(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[eff_score], text=[f"{eff_score:.3f}"],
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}", mode="markers",
                                                    marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]), showlegend=True,
                                                    legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    fig.update_layout(updatemenus=[ dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear"}]),
                                                                    dict(label="Log",             method="relayout", args=[{"yaxis.type": "log"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html(f"./html/synthetic/synthetic_Efficiency.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic_Efficiency.html", "a") as f:
        f.write(custom_html)

def syntheticHeatmap():
    fig = make_subplots(rows=2, cols=2, subplot_titles=[f"<span style='font-size: 22px;'>L2-BruteForce</span>", "<span style='font-size: 22px;'>L2-Flann</span>", "<span style='font-size: 22px;'>Hamming-BruteForce</span>", "<span style='font-size: 22px;'>Hamming-Flann</span>"], horizontal_spacing=0.07, vertical_spacing=0.08)
    scores = np.full((len(DetectorsLegend), len(DescriptorsLegend), 2, 2), np.nan)
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    scores[i, j, c3, m] = (
                        0.15 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 13], Rate_scale[:, m, c3, i, j, 13], Rate_rot[:, m, c3, i, j, 13]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 13], Rate_scale[:, :, :, :, :, 13], Rate_rot[:, :, :, :, :, 13]), axis=0)) +
                        0.10 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 12], Rate_scale[:, m, c3, i, j, 12], Rate_rot[:, m, c3, i, j, 12]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 12], Rate_scale[:, :, :, :, :, 12], Rate_rot[:, :, :, :, :, 12]), axis=0)) +
                        0.08 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 14], Rate_scale[:, m, c3, i, j, 14], Rate_rot[:, m, c3, i, j, 14]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 14], Rate_scale[:, :, :, :, :, 14], Rate_rot[:, :, :, :, :, 14]), axis=0)) +
                        0.10 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 15], Rate_scale[:, m, c3, i, j, 15], Rate_rot[:, m, c3, i, j, 15]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 15], Rate_scale[:, :, :, :, :, 15], Rate_rot[:, :, :, :, :, 15]), axis=0)) +
                        0.10 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j,  9], Rate_scale[:, m, c3, i, j,  9], Rate_rot[:, m, c3, i, j,  9]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :,  9], Rate_scale[:, :, :, :, :,  9], Rate_rot[:, :, :, :, :,  9]), axis=0)) +
                        0.07 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 10], Rate_scale[:, m, c3, i, j, 10], Rate_rot[:, m, c3, i, j, 10]), axis=0)), np.concatenate((Rate_intensity[:, :, :, :, :, 10], Rate_scale[:, :, :, :, :, 10], Rate_rot[:, :, :, :, :, 10]), axis=0)) +
                        0.05 * (1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 6], Exec_time_scale[:, m, c3, i, j, 6], Exec_time_rot[:, m, c3, i, j, 6]), axis=0)), np.concatenate((Exec_time_intensity[:, :, :, :, :, 6], Exec_time_scale[:, :, :, :, :, 6], Exec_time_rot[:, :, :, :, :, 6]), axis=0))) +
                        0.10 * (1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 7], Exec_time_scale[:, m, c3, i, j, 7], Exec_time_rot[:, m, c3, i, j, 7]), axis=0)), np.concatenate((Exec_time_intensity[:, :, :, :, :, 7], Exec_time_scale[:, :, :, :, :, 7], Exec_time_rot[:, :, :, :, :, 7]), axis=0)))
                    ) * 4 / 3
    for c3 in range(2):
        for m in range(2):
            fig.add_trace(go.Heatmap( z=scores[:,:,c3,m], x=DescriptorsLegend, y=DetectorsLegend, colorscale="matter", hoverongaps=False, hovertemplate="Detector: %{y}<br>Descriptor: %{x}<br>Score: %{z:.3f}"), row=c3+1, col=m+1)
    fig.update_layout(template="ggplot2", title=dict(text=f"<span style='font-size: 26px;'><b>Synthetic Efficiency Heatmaps</b></span>", x=0.5, xanchor="center", yanchor="middle"), font_size=20, margin=dict(l=20, r=20, t=50, b=20))
    fig.write_html(f"./html/synthetic/synthetic_Heatmap.html", include_plotlyjs="cdn", full_html=True, config=config)

def syntheticCorrelationHeatmap():
    
    metrics = {
        "Precision":            np.concatenate((Rate_intensity[:, :, :, :, :, 13].flatten(), Rate_scale[:, :, :, :, :, 13].flatten(), Rate_rot[:, :, :, :, :, 13].flatten())),
        "Recall":               np.concatenate((Rate_intensity[:, :, :, :, :, 12].flatten(), Rate_scale[:, :, :, :, :, 12].flatten(), Rate_rot[:, :, :, :, :, 12].flatten())),
        "Repeatibility":        np.concatenate((Rate_intensity[:, :, :, :, :, 14].flatten(), Rate_scale[:, :, :, :, :, 14].flatten(), Rate_rot[:, :, :, :, :, 14].flatten())),
        "F1 Score":             np.concatenate((Rate_intensity[:, :, :, :, :, 15].flatten(), Rate_scale[:, :, :, :, :, 15].flatten(), Rate_rot[:, :, :, :, :, 15].flatten())),
        "Inliers":              np.concatenate((Rate_intensity[:, :, :, :, :,  9].flatten(), Rate_scale[:, :, :, :, :,  9].flatten(), Rate_rot[:, :, :, :, :,  9].flatten())),
        "Matches":              np.concatenate((Rate_intensity[:, :, :, :, :, 10].flatten(), Rate_scale[:, :, :, :, :, 10].flatten(), Rate_rot[:, :, :, :, :, 10].flatten())),
        "1K Total Time":   np.concatenate((Exec_time_intensity[:, :, :, :, :,  6].flatten(), Exec_time_scale[:, :, :, :, :,  6].flatten(), Exec_time_rot[:, :, :, :, :,  6].flatten())),
        "1K Inlier Time":  np.concatenate((Exec_time_intensity[:, :, :, :, :,  7].flatten(), Exec_time_scale[:, :, :, :, :,  7].flatten(), Exec_time_rot[:, :, :, :, :,  7].flatten()))
    }
    metric_names = list(metrics.keys())
    corr_matrix = np.zeros((len(metric_names), len(metric_names)))
    for i, name1 in enumerate(metric_names):
        for j, name2 in enumerate(metric_names):
            data1 = metrics[name1]
            data2 = metrics[name2]
            mask = ~(np.isnan(data1) | np.isnan(data2) | np.isinf(data1) | np.isinf(data2))
            if np.sum(mask) > 1:
                corr_matrix[i,j] = np.corrcoef(data1[mask], data2[mask])[0,1]
            else:
                corr_matrix[i,j] = 0
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=corr_matrix, x=metric_names, y=metric_names, colorscale='RdBu', zmid=0, text=np.round(corr_matrix, 3), texttemplate='%{text}', hoverongaps=False, hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>'))
    fig.update_layout(template="ggplot2", font_size=20, title=dict(text=f"<span style='font-size: 26px;'><b>Synthetic Dataset Metric Correlations</b></span>", x=0.5, xanchor="center", yanchor="middle"), margin=dict(l=20, r=20, t=50, b=20))
    fig.write_html(f"./html/synthetic/synthetic_Correlation.html", include_plotlyjs="cdn", full_html=True, config=config)

def syntheticViolin():
    fig = go.Figure()
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):  # Normalization Type
                for m in range(2):  # Matcher Type
                    xydata = [
                        np.concatenate((Rate_intensity[:, m, c3, i, j, 13], Rate_scale[:, m, c3, i, j, 13], Rate_rot[:, m, c3, i, j, 13]), axis=0),  # Precision
                        np.concatenate((Rate_intensity[:, m, c3, i, j, 12], Rate_scale[:, m, c3, i, j, 12], Rate_rot[:, m, c3, i, j, 12]), axis=0),  # Recall
                        np.concatenate((Rate_intensity[:, m, c3, i, j, 14], Rate_scale[:, m, c3, i, j, 14], Rate_rot[:, m, c3, i, j, 14]), axis=0),  # Repeatibility
                        np.concatenate((Rate_intensity[:, m, c3, i, j, 15], Rate_scale[:, m, c3, i, j, 15], Rate_rot[:, m, c3, i, j, 15]), axis=0),  # F1 Score
                        np.concatenate((Rate_intensity[:, m, c3, i, j,  9], Rate_scale[:, m, c3, i, j,  9], Rate_rot[:, m, c3, i, j,  9]), axis=0),  # Inliers
                        np.concatenate((Rate_intensity[:, m, c3, i, j, 10], Rate_scale[:, m, c3, i, j, 10], Rate_rot[:, m, c3, i, j, 10]), axis=0),  # Matches
                        np.concatenate((Exec_time_intensity[:, m, c3, i, j, 6], Exec_time_scale[:, m, c3, i, j, 6], Exec_time_rot[:, m, c3, i, j, 6]), axis=0),  # 1K Total Time
                        np.concatenate((Exec_time_intensity[:, m, c3, i, j, 7], Exec_time_scale[:, m, c3, i, j, 7], Exec_time_rot[:, m, c3, i, j, 7]), axis=0)   # 1K Inlier Time
                    ]
                    if not np.isnan(xydata).any():
                        traces.append(go.Violin(
                                x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]]*len(xydata[0]), [Norm[c3]]*len(xydata[0])], y=xydata,
                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                box_visible=True, meanline_visible=True))
                        fig.add_trace(go.Violin(
                                x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]]*len(xydata[0]), [Norm[c3]]*len(xydata[0])], y=xydata[0],
                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                box_visible=True, meanline_visible=True))
    dropdown_axis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_list = []
    for idx, axis in enumerate(dropdown_axis):
        button_list.append(dict(label=f"y: {axis}", method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}])
    )
    fig.update_layout(  template="ggplot2", font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>Synthetic - Violin Plots</b></span>", x=0.5, xanchor="center", yanchor="middle"), margin=dict(l=20, r=20, t=50, b=20), hovermode="x unified", 
                        updatemenus=[   dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                        dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1, yanchor="bottom")])
    
    fig.write_html(f"./html/synthetic/synthetic_Violin.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic_Violin.html", "a") as f:
        f.write(custom_html)

################
# MARK: - Oxford
################
def oxfordAll9():
    fig = go.Figure()
    fig = make_subplots(rows=3, cols=3, subplot_titles=["<span style='font-size: 18px;'><b>Graf(Viewpoint)</b></span>", "<span style='font-size: 18px;'><b>Bikes(Blur)</b></span>", "<span style='font-size: 18px;'><b>Boat(Zoom + Rotation)</b></span>", 
                                                        "<span style='font-size: 18px;'><b>Leuven(Light)</b></span>", "<span style='font-size: 18px;'><b>Wall(Viewpoint)</b></span>", "<span style='font-size: 18px;'><b>Trees(Blur)</b></span>", 
                                                        "<span style='font-size: 18px;'><b>Bark(Zoom + Rotation)</b></span>", "<span style='font-size: 18px;'><b>UBC(JPEG)", "<span style='font-size: 18px;'><b>Overall</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    xvals = ["Img2", "Img3", "Img4", "Img5", "Img6"]
    sett_axis = dict(range=[-0.01, 1.01])
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Affine Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                                                hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=70, b=20), yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis, yaxis5=sett_axis, yaxis6=sett_axis, yaxis7=sett_axis, yaxis8=sett_axis, yaxis9=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_Graf  = [Rate_graf  [:, m, c3, i, j, 13], Rate_graf  [:, m, c3, i, j, 12], Rate_graf  [:, m, c3, i, j, 14], Rate_graf  [:, m, c3, i, j, 15], Rate_graf  [:, m, c3, i, j, 9], Rate_graf  [:, m, c3, i, j, 10], 1 - nonlinear_normalize(Exec_time_graf  [:, m, c3, i, j, 6], Exec_time_graf  [:, :, :, :, :, 6]), 1 - nonlinear_normalize(Exec_time_graf  [:, m, c3, i, j, 7], Exec_time_graf  [:, :, :, :, :, 7])]
                    Rate_Bikes = [Rate_bikes [:, m, c3, i, j, 13], Rate_bikes [:, m, c3, i, j, 12], Rate_bikes [:, m, c3, i, j, 14], Rate_bikes [:, m, c3, i, j, 15], Rate_bikes [:, m, c3, i, j, 9], Rate_bikes [:, m, c3, i, j, 10], 1 - nonlinear_normalize(Exec_time_bikes [:, m, c3, i, j, 6], Exec_time_bikes [:, :, :, :, :, 6]), 1 - nonlinear_normalize(Exec_time_bikes [:, m, c3, i, j, 7], Exec_time_bikes [:, :, :, :, :, 7])]
                    Rate_Boat  = [Rate_boat  [:, m, c3, i, j, 13], Rate_boat  [:, m, c3, i, j, 12], Rate_boat  [:, m, c3, i, j, 14], Rate_boat  [:, m, c3, i, j, 15], Rate_boat  [:, m, c3, i, j, 9], Rate_boat  [:, m, c3, i, j, 10], 1 - nonlinear_normalize(Exec_time_boat  [:, m, c3, i, j, 6], Exec_time_boat  [:, :, :, :, :, 6]), 1 - nonlinear_normalize(Exec_time_boat  [:, m, c3, i, j, 7], Exec_time_boat  [:, :, :, :, :, 7])]
                    Rate_Leuven= [Rate_leuven[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 9], Rate_leuven[:, m, c3, i, j, 10], 1 - nonlinear_normalize(Exec_time_leuven[:, m, c3, i, j, 6], Exec_time_leuven[:, :, :, :, :, 6]), 1 - nonlinear_normalize(Exec_time_leuven[:, m, c3, i, j, 7], Exec_time_leuven[:, :, :, :, :, 7])]
                    Rate_Wall  = [Rate_wall  [:, m, c3, i, j, 13], Rate_wall  [:, m, c3, i, j, 12], Rate_wall  [:, m, c3, i, j, 14], Rate_wall  [:, m, c3, i, j, 15], Rate_wall  [:, m, c3, i, j, 9], Rate_wall  [:, m, c3, i, j, 10], 1 - nonlinear_normalize(Exec_time_wall  [:, m, c3, i, j, 6], Exec_time_wall  [:, :, :, :, :, 6]), 1 - nonlinear_normalize(Exec_time_wall  [:, m, c3, i, j, 7], Exec_time_wall  [:, :, :, :, :, 7])]
                    Rate_Trees = [Rate_trees [:, m, c3, i, j, 13], Rate_trees [:, m, c3, i, j, 12], Rate_trees [:, m, c3, i, j, 14], Rate_trees [:, m, c3, i, j, 15], Rate_trees [:, m, c3, i, j, 9], Rate_trees [:, m, c3, i, j, 10], 1 - nonlinear_normalize(Exec_time_trees [:, m, c3, i, j, 6], Exec_time_trees [:, :, :, :, :, 6]), 1 - nonlinear_normalize(Exec_time_trees [:, m, c3, i, j, 7], Exec_time_trees [:, :, :, :, :, 7])]
                    Rate_Bark  = [Rate_bark  [:, m, c3, i, j, 13], Rate_bark  [:, m, c3, i, j, 12], Rate_bark  [:, m, c3, i, j, 14], Rate_bark  [:, m, c3, i, j, 15], Rate_bark  [:, m, c3, i, j, 9], Rate_bark  [:, m, c3, i, j, 10], 1 - nonlinear_normalize(Exec_time_bark  [:, m, c3, i, j, 6], Exec_time_bark  [:, :, :, :, :, 6]), 1 - nonlinear_normalize(Exec_time_bark  [:, m, c3, i, j, 7], Exec_time_bark  [:, :, :, :, :, 7])]
                    Rate_Ubc   = [Rate_ubc   [:, m, c3, i, j, 13], Rate_ubc   [:, m, c3, i, j, 12], Rate_ubc   [:, m, c3, i, j, 14], Rate_ubc   [:, m, c3, i, j, 15], Rate_ubc   [:, m, c3, i, j, 9], Rate_ubc   [:, m, c3, i, j, 10], 1 - nonlinear_normalize(Exec_time_ubc   [:, m, c3, i, j, 6], Exec_time_ubc   [:, :, :, :, :, 6]), 1 - nonlinear_normalize(Exec_time_ubc   [:, m, c3, i, j, 7], Exec_time_ubc   [:, :, :, :, :, 7])]
                    Overall    = np.nanmean([Rate_Graf, Rate_Bikes, Rate_Boat, Rate_Leuven, Rate_Wall, Rate_Trees, Rate_Bark, Rate_Ubc], axis=0)
                    legend_groupfig = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig, legendgroup=legend_groupfig, showlegend=True, hovertemplate="<b>%{y:.3f}</b>")
                    # Check for each trace individually and only add if it doesn't contain NaN values
                    if not (np.isnan(Rate_Graf).any() or np.isnan(Rate_Bikes).any() or np.isnan(Rate_Boat).any() or np.isnan(Rate_Leuven).any() or np.isnan(Rate_Wall).any() or np.isnan(Rate_Trees).any() or np.isnan(Rate_Bark).any() or np.isnan(Rate_Ubc).any() or np.isnan(Overall).any()):
                    # if not np.isnan(Rate_Graf).any():
                        traces.append(go.Scatter(x = xvals, y=Rate_Graf,       arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Rate_Graf[0],    arg=sett), row=1, col=1)
                    # if not np.isnan(Rate_Bikes).any():
                        traces.append(go.Scatter(x = xvals, y=Rate_Bikes,      arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Rate_Bikes[0],   arg=sett), row=1, col=2)
                    # if not np.isnan(Rate_Boat).any():
                        traces.append(go.Scatter(x = xvals, y=Rate_Boat,       arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Rate_Boat[0],    arg=sett), row=1, col=3)
                    # if not np.isnan(Rate_Leuven).any():
                        traces.append(go.Scatter(x = xvals, y=Rate_Leuven,     arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Rate_Leuven[0],  arg=sett), row=2, col=1)
                    # if not np.isnan(Rate_Wall).any():
                        traces.append(go.Scatter(x = xvals, y=Rate_Wall,       arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Rate_Wall[0],    arg=sett), row=2, col=2)
                    # if not np.isnan(Rate_Trees).any():
                        traces.append(go.Scatter(x = xvals, y=Rate_Trees,      arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Rate_Trees[0],   arg=sett), row=2, col=3)
                    # if not np.isnan(Rate_Bark).any():
                        traces.append(go.Scatter(x = xvals, y=Rate_Bark,       arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Rate_Bark[0],    arg=sett), row=3, col=1)
                    # if not np.isnan(Rate_Ubc).any():
                        traces.append(go.Scatter(x = xvals, y=Rate_Ubc,        arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Rate_Ubc[0],     arg=sett), row=3, col=2)
                    # if not np.isnan(Overall).any():
                        traces.append(go.Scatter(x = xvals, y=Overall,         arg=sett))
                        fig.add_trace(go.Scatter(x = xvals, y=Overall[0],      arg=sett), row=3, col=3)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=f"y: {y}", method="update", 
                                args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis4.title": f"<span style='font-size: 22px;'><b>{y}</b></span>"}]))
    fig.update_layout(updatemenus=[ dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=-0.04, xanchor="left", y=1, yanchor="bottom")]) 
    fig.write_html(f"./html/oxford/oxfordAll9.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxfordAll9.html", "a") as f:
        f.write(custom_html)

def oxford9():
    fig = go.Figure()
    fig = make_subplots(rows=3, cols=3,subplot_titles=["<span style='font-size: 20px;'><b>Graf(Viewpoint)</b></span>", "<span style='font-size: 20px;'><b>Bikes(Blur)</b></span>", "<span style='font-size: 20px;'><b>Boat(Zoom + Rotation)</b></span>", 
                                                        "<span style='font-size: 20px;'><b>Leuven(Light)</b></span>", "<span style='font-size: 20px;'><b>Wall(Viewpoint)</b></span>", "<span style='font-size: 20px;'><b>Trees(Blur)</b></span>", 
                                                        "<span style='font-size: 20px;'><b>Bark(Zoom + Rotation)</b></span>","<span style='font-size: 20px;'><b>UBC(JPEG)</b></span>", "<span style='font-size: 20px;'><b>Overall</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    sett_axis = dict(range=[-0.01, 1.01])
    fig.update_layout( template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Affine Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"),
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=70, b=20),
                        xaxis=sett_axis, xaxis2=sett_axis, xaxis3=sett_axis, xaxis4=sett_axis, xaxis5=sett_axis, xaxis6=sett_axis, xaxis7=sett_axis, xaxis8=sett_axis, xaxis9=sett_axis,
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
                        1 - nonlinear_normalize(np.nanmean(Exec_time_graf[:, m, c3, i, j, 6]), Exec_time_graf[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_graf[:, m, c3, i, j, 7]), Exec_time_graf[:, :, :, :, :, 7])
                    ]
                    xydata_Bikes = [
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 10]), 
                        1 - nonlinear_normalize(np.nanmean(Exec_time_bikes[:, m, c3, i, j, 6]), Exec_time_bikes[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_bikes[:, m, c3, i, j, 7]), Exec_time_bikes[:, :, :, :, :, 7])
                    ]
                    xydata_Boat = [
                        np.nanmean(Rate_boat[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 10]), 
                        1 - nonlinear_normalize(np.nanmean(Exec_time_boat[:, m, c3, i, j, 6]), Exec_time_boat[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_boat[:, m, c3, i, j, 7]), Exec_time_boat[:, :, :, :, :, 7])
                    ]
                    xydata_Leuven = [
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 10]), 
                        1 - nonlinear_normalize(np.nanmean(Exec_time_leuven[:, m, c3, i, j, 6]), Exec_time_leuven[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_leuven[:, m, c3, i, j, 7]), Exec_time_leuven[:, :, :, :, :, 7])
                    ]
                    xydata_Wall = [
                        np.nanmean(Rate_wall[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 10]), 
                        1 - nonlinear_normalize(np.nanmean(Exec_time_wall[:, m, c3, i, j, 6]), Exec_time_wall[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_wall[:, m, c3, i, j, 7]), Exec_time_wall[:, :, :, :, :, 7])
                    ]
                    xydata_Trees = [
                        np.nanmean(Rate_trees[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 10]), 
                        1 - nonlinear_normalize(np.nanmean(Exec_time_trees[:, m, c3, i, j, 6]), Exec_time_trees[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_trees[:, m, c3, i, j, 7]), Exec_time_trees[:, :, :, :, :, 7])
                    ]
                    xydata_Bark = [
                        np.nanmean(Rate_bark[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 10]), 
                        1 - nonlinear_normalize(np.nanmean(Exec_time_bark[:, m, c3, i, j, 6]), Exec_time_bark[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_bark[:, m, c3, i, j, 7]), Exec_time_bark[:, :, :, :, :, 7])
                    ]
                    xydata_Ubc = [
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 15]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 9]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 10]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_ubc[:, m, c3, i, j, 6]), Exec_time_ubc[:, :, :, :, :, 6]),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_ubc[:, m, c3, i, j, 7]), Exec_time_ubc[:, :, :, :, :, 7])
                    ]
                    Overall = np.nanmean([xydata_Graf, xydata_Bikes, xydata_Boat, xydata_Leuven, xydata_Wall, xydata_Trees, xydata_Bark, xydata_Ubc], axis=0)
                    legend_groupfig = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                name=legend_groupfig, legendgroup=legend_groupfig, showlegend=True,
                                hovertemplate="x: <b>%{x:.2f}</b> | y: <b>%{y:.2f}</b>")
                    if not (np.isnan(xydata_Graf).any() or np.isnan(xydata_Bikes).any() or np.isnan(xydata_Boat).any() or np.isnan(xydata_Leuven).any() or np.isnan(xydata_Wall).any() or np.isnan(xydata_Trees).any() or np.isnan(xydata_Bark).any() or np.isnan(xydata_Ubc).any() or np.isnan(Overall).any()):
                    # if not np.isnan(xydata_Graf).any():
                        traces.append(go.Scatter(x=xydata_Graf,        y=xydata_Graf,       arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Graf[0]],   y=[xydata_Graf[1]],  arg=sett), row=1, col=1)
                    # if not np.isnan(xydata_Bikes).any():
                        traces.append(go.Scatter(x=xydata_Bikes,       y=xydata_Bikes,      arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Bikes[0]],  y=[xydata_Bikes[1]], arg=sett), row=1, col=2)
                    # if not np.isnan(xydata_Boat).any():
                        traces.append(go.Scatter(x=xydata_Boat,        y=xydata_Boat,       arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Boat[0]],   y=[xydata_Boat[1]],  arg=sett), row=1, col=3)
                    # if not np.isnan(xydata_Leuven).any():
                        traces.append(go.Scatter(x=xydata_Leuven,      y=xydata_Leuven,     arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Leuven[0]], y=[xydata_Leuven[1]],arg=sett), row=2, col=1)
                    # if not np.isnan(xydata_Wall).any():
                        traces.append(go.Scatter(x=xydata_Wall,        y=xydata_Wall,       arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Wall[0]],   y=[xydata_Wall[1]],  arg=sett), row=2, col=2)
                    # if not np.isnan(xydata_Trees).any():
                        traces.append(go.Scatter(x=xydata_Trees,       y=xydata_Trees,      arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Trees[0]],  y=[xydata_Trees[1]], arg=sett), row=2, col=3)
                    # if not np.isnan(xydata_Bark).any():
                        traces.append(go.Scatter(x=xydata_Bark,        y=xydata_Bark,       arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Bark[0]],   y=[xydata_Bark[1]],  arg=sett), row=3, col=1)
                    # if not np.isnan(xydata_Ubc).any():
                        traces.append(go.Scatter(x=xydata_Ubc,         y=xydata_Ubc,        arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Ubc[0]],    y=[xydata_Ubc[1]],   arg=sett), row=3, col=2)
                    # if not np.isnan(Overall).any():
                        traces.append(go.Scatter(x=Overall,            y=Overall,           arg=sett))
                        fig.add_trace(go.Scatter(x=[Overall[0]],       y=[Overall[1]],      arg=sett), row=3, col=3)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_listx = []
    button_listy = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict(label=f"x: {axis}", method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis8.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict(label=f"y: {axis}", method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis4.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listy, direction="down", x=0,  xanchor="left",  y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listx, direction="up",   x=1,  xanchor="right", y=0, yanchor="bottom")])
    fig.write_html(f"./html/oxford/oxford9.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford9.html", "a") as f:
        f.write(custom_html)

def oxford():
    fig = go.Figure()
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Affine Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        hovermode="x", hoverdistance=900, margin=dict(l=20, r=20, t=50, b=20), xaxis=dict(range=[-0.01, 1.01]), yaxis=dict(range=[-0.01, 1.01]))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    xydata = [
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 13], Rate_bikes[:, m, c3, i, j, 13], Rate_boat[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 13], Rate_wall[:, m, c3, i, j, 13], Rate_trees[:, m, c3, i, j, 13], Rate_bark[:, m, c3, i, j, 13], Rate_ubc[:, m, c3, i, j, 13]), axis=0)),                                    # Precision
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 12], Rate_bikes[:, m, c3, i, j, 12], Rate_boat[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 12], Rate_wall[:, m, c3, i, j, 12], Rate_trees[:, m, c3, i, j, 12], Rate_bark[:, m, c3, i, j, 12], Rate_ubc[:, m, c3, i, j, 12]), axis=0)),                                    # Recall
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 14], Rate_bikes[:, m, c3, i, j, 14], Rate_boat[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 14], Rate_wall[:, m, c3, i, j, 14], Rate_trees[:, m, c3, i, j, 14], Rate_bark[:, m, c3, i, j, 14], Rate_ubc[:, m, c3, i, j, 14]), axis=0)),                                    # Repeatibility
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 15], Rate_bikes[:, m, c3, i, j, 15], Rate_boat[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 15], Rate_wall[:, m, c3, i, j, 15], Rate_trees[:, m, c3, i, j, 15], Rate_bark[:, m, c3, i, j, 15], Rate_ubc[:, m, c3, i, j, 15]), axis=0)),                                    # F1Score
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 9],  Rate_bikes[:, m, c3, i, j, 9],  Rate_boat[:, m, c3, i, j, 9],  Rate_leuven[:, m, c3, i, j, 9],  Rate_wall[:, m, c3, i, j, 9],  Rate_trees[:, m, c3, i, j, 9],  Rate_bark[:, m, c3, i, j, 9],  Rate_ubc[:, m, c3, i, j, 9]), axis=0)),                                     # Inliers
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 10], Rate_bikes[:, m, c3, i, j, 10], Rate_boat[:, m, c3, i, j, 10], Rate_leuven[:, m, c3, i, j, 10], Rate_wall[:, m, c3, i, j, 10], Rate_trees[:, m, c3, i, j, 10], Rate_bark[:, m, c3, i, j, 10], Rate_ubc[:, m, c3, i, j, 10]), axis=0)),                                    # Matches
                        1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 6], Exec_time_bikes[:, m, c3, i, j, 6], Exec_time_boat[:, m, c3, i, j, 6], Exec_time_leuven[:, m, c3, i, j, 6], Exec_time_wall[:, m, c3, i, j, 6], Exec_time_trees[:, m, c3, i, j, 6], Exec_time_bark[:, m, c3, i, j, 6], Exec_time_ubc[:, m, c3, i, j, 6]), axis=0)),  # Total Time
                                                        np.concatenate((Exec_time_graf[:, :, :, :, :, 6],  Exec_time_bikes[:, :, :, :, :, 6],  Exec_time_boat[:, :, :, :, :, 6],  Exec_time_leuven[:, :, :, :, :, 6],  Exec_time_wall[:, :, :, :, :, 6],  Exec_time_trees[:, :, :, :, :, 6],  Exec_time_bark[:, :, :, :, :, 6],  Exec_time_ubc[:, :, :, :, :, 6]),  axis=0)),  # Total Time
                        1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 7], Exec_time_bikes[:, m, c3, i, j, 7], Exec_time_boat[:, m, c3, i, j, 7], Exec_time_leuven[:, m, c3, i, j, 7], Exec_time_wall[:, m, c3, i, j, 7], Exec_time_trees[:, m, c3, i, j, 7], Exec_time_bark[:, m, c3, i, j, 7], Exec_time_ubc[:, m, c3, i, j, 7]), axis=0)),  # Inlier Time
                                                        np.concatenate((Exec_time_graf[:, :, :, :, :, 7],  Exec_time_bikes[:, :, :, :, :, 7],  Exec_time_boat[:, :, :, :, :, 7],  Exec_time_leuven[:, :, :, :, :, 7],  Exec_time_wall[:, :, :, :, :, 7],  Exec_time_trees[:, :, :, :, :, 7],  Exec_time_bark[:, :, :, :, :, 7],  Exec_time_ubc[:, :, :, :, :, 7]),  axis=0))   # Inlier Time
                    ]
                    if not np.isnan(xydata).any():
                        traces.append(  go.Scatter( x=xydata,       y=xydata,       mode="markers", marker=dict(color=colors[color_index], size=xydata, symbol=marker_symbols[symbol_index]),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                        fig.add_trace(go.Scatter( x=[xydata[0]],  y=[xydata[1]],  mode="markers", marker=dict(color=colors[color_index], size=xydata, symbol=marker_symbols[symbol_index]),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_listx = []
    button_listy = []
    button_listz = []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict(label=f"x: {axis}", method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict(label=f"y: {axis}", method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listz.append(dict(label=f"z: {axis}", method="update", args=[{"marker.size": [((trace.marker.size[idx]*40+10)%50) for trace in traces]}]))
    fig.update_layout(updatemenus=[ dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listy, direction="down", x=0,  xanchor="left",  y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listx, direction="up",   x=1,  xanchor="right", y=0, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=5, buttons=button_listz, direction="down", x=0,  xanchor="left",  y=1)])
    fig.write_html(f"./html/oxford/oxford.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford.html", "a") as f:
        f.write(custom_html)

def oxfordTiming():
    fig = go.Figure()
    fig = make_subplots(rows=6, cols=2, subplot_titles=["<span style='font-size: 22px;'>Total time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Total time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>Detect time</span>","<span style='font-size: 22px;'>Describe time</span>",
                                                        "<span style='font-size: 22px;'>All Timings</span>"],
                        specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.06)
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Dataset Timings for Average 1k</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), height=2500, margin=dict(l=20, r=20, t=80, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 6],          Exec_time_wall[:, m, :, i, j, 6],           Exec_time_trees[:, m, :, i, j, 6],          Exec_time_bikes[:, m, :, i, j, 6],          Exec_time_bark[:, m, :, i, j, 6],           Exec_time_boat[:, m, :, i, j, 6],           Exec_time_leuven[:, m, :, i, j, 6],         Exec_time_ubc[:, m, :, i, j, 6]),           axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 7],          Exec_time_wall[:, m, :, i, j, 7],           Exec_time_trees[:, m, :, i, j, 7],          Exec_time_bikes[:, m, :, i, j, 7],          Exec_time_bark[:, m, :, i, j, 7],           Exec_time_boat[:, m, :, i, j, 7],           Exec_time_leuven[:, m, :, i, j, 7],         Exec_time_ubc[:, m, :, i, j, 7]),           axis=0))
                if not np.isnan(result3) and result3 > 0 and not np.isnan(result4) and result4 > 0:
                    trace_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result3,  row=1, col=1) if m == 0 else fig.add_trace(trace_result3, row=2, col=1)                    
                    trace_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result4,  row=3, col=1) if m == 0 else fig.add_trace(trace_result4, row=4, col=1)
                    # All Data Timings
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-total']], y=[result3],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                            text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=6, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-inlier']], y=[result4],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                            text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=6, col=1 )
            color_index = (color_index + 14) % num_combinations            
        result  = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, i, :, 4], Exec_time_wall[:, :, :, i, :, 4], Exec_time_trees[:, :, :, i, :, 4], Exec_time_bikes[:, :, :, i, :, 4], Exec_time_bark[:, :, :, i, :, 4], Exec_time_boat[:, :, :, i, :, 4], Exec_time_leuven[:, :, :, i, :, 4], Exec_time_ubc[:, :, :, i, :, 4]), axis=0))
        result2 = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, :, i, 5], Exec_time_wall[:, :, :, :, i, 5], Exec_time_trees[:, :, :, :, i, 5], Exec_time_bikes[:, :, :, :, i, 5], Exec_time_bark[:, :, :, :, i, 5], Exec_time_boat[:, :, :, :, i, 5], Exec_time_leuven[:, :, :, :, i, 5], Exec_time_ubc[:, :, :, :, i, 5]), axis=0))
        if not np.isnan(result) and result > 0:
            trace_detect_oxford = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=f".{DetectorsLegend[i]}",   showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            fig.add_trace(trace_detect_oxford, row=5, col=1)
        if not np.isnan(result2) and result2 > 0:
            trace_descr_oxford = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=f"-{DescriptorsLegend[i]}", showlegend=True, text=[f"{result2:.3f}"], marker=dict(color = colors[14*i]))
            fig.add_trace(trace_descr_oxford,  row=5, col=2)
    # for i in range(1, 7):
    #     fig.update_xaxes(tickangle=90, row=i, col=1)
    # fig.update_xaxes(tickangle=90, row=5, col=2)
    fig.update_layout(updatemenus=[ dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear"}]),
                                                                    dict(label="Log",             method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html("./html/oxford/oxfordTiming.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxfordTiming.html", "a") as f:
        f.write(custom_html)

def oxfordTimingMobile():
    fig = go.Figure()
    fig = make_subplots(rows=9, cols=1, subplot_titles=["<span style='font-size: 22px;'>Total time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Total time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'><b>Mobile</b> Total time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'><b>Mobile</b> Total time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'><b>Mobile</b> Inlier time <b>BF</b></span>","<span style='font-size: 22px;'><b>Mobile</b> Inlier time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>All Timings</span>"],horizontal_spacing=0.05, vertical_spacing=0.05)
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text="<span style='font-size: 26px;'><b>Oxford Dataset Timings for Average 1k</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), barmode="stack", height=3000, margin=dict(l=20, r=20, t=80, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 6],          Exec_time_wall[:, m, :, i, j, 6],           Exec_time_trees[:, m, :, i, j, 6],          Exec_time_bikes[:, m, :, i, j, 6],          Exec_time_bark[:, m, :, i, j, 6],           Exec_time_boat[:, m, :, i, j, 6],           Exec_time_leuven[:, m, :, i, j, 6],         Exec_time_ubc[:, m, :, i, j, 6]),           axis=0))
                result3m= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, m, :, i, j, 6],   Exec_time_wall_mobile[:, m, :, i, j, 6],    Exec_time_trees_mobile[:, m, :, i, j, 6],   Exec_time_bikes_mobile[:, m, :, i, j, 6],   Exec_time_bark_mobile[:, m, :, i, j, 6],    Exec_time_boat_mobile[:, m, :, i, j, 6],    Exec_time_leuven_mobile[:, m, :, i, j, 6],  Exec_time_ubc_mobile[:, m, :, i, j, 6]),    axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 7],          Exec_time_wall[:, m, :, i, j, 7],           Exec_time_trees[:, m, :, i, j, 7],          Exec_time_bikes[:, m, :, i, j, 7],          Exec_time_bark[:, m, :, i, j, 7],           Exec_time_boat[:, m, :, i, j, 7],           Exec_time_leuven[:, m, :, i, j, 7],         Exec_time_ubc[:, m, :, i, j, 7]),           axis=0))
                result4m= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, m, :, i, j, 7],   Exec_time_wall_mobile[:, m, :, i, j, 7],    Exec_time_trees_mobile[:, m, :, i, j, 7],   Exec_time_bikes_mobile[:, m, :, i, j, 7],   Exec_time_bark_mobile[:, m, :, i, j, 7],    Exec_time_boat_mobile[:, m, :, i, j, 7],    Exec_time_leuven_mobile[:, m, :, i, j, 7],  Exec_time_ubc_mobile[:, m, :, i, j, 7]),    axis=0))
                if not np.isnan(result3) and result3 > 0 and not np.isnan(result4) and result4 > 0 and not np.isnan(result3m) and result3m > 0 and not np.isnan(result4m) and result4m > 0:
                    trace_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-p",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result3,  row=1, col=1) if m == 0 else fig.add_trace(trace_result3, row=2, col=1)
                    trace_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-p",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result4,  row=3, col=1) if m == 0 else fig.add_trace(trace_result4, row=4, col=1)
                    #mobile
                    trace_result3m= go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m",
                                                        text=[f"{result3m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result3m, row=1+4, col=1) if m == 0 else fig.add_trace(trace_result3m, row=2+4, col=1)
                    trace_result4m = go.Bar( x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m",
                                                        text=[f"{result4m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_result4m, row=3+4, col=1) if m == 0 else fig.add_trace(trace_result4m, row=4+4, col=1)
                    # All Data Timings
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-total-p']], y=[result3],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-p",
                                            text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=9, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-total-m']], y=[result3m],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m",
                                            text=[f"{result3m:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=9, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-inlier-p']], y=[result4],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-p",
                                            text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=9, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-inlier-m']], y=[result4m],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m",
                                            text=[f"{result4m:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=9, col=1 )
            color_index = (color_index + 14) % num_combinations
    # for i in range(1, 10):
    #     fig.update_xaxes(tickangle=90, row=i, col=1)
    fig.update_layout(updatemenus=[ dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear","yaxis7.type": "linear","yaxis8.type": "linear", "yaxis9.type": "linear"}]),
                                                                    dict(label="Log",             method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log","yaxis7.type": "log","yaxis8.type": "log", "yaxis9.type": "log"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html("./html/oxford/oxfordTimingMobile.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxfordTimingMobile.html", "a") as f:
        f.write(custom_html)

def oxfordEfficiency():
    fig = go.Figure()
    fig.update_layout(  template="ggplot2", font_size=16, margin=dict(l=20, r=20, t=80, b=20),
                        title=dict(text=f"<span style='font-size: 26px;'><b>Oxford Efficiency</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        xaxis_tickangle=90, yaxis=dict(range=[-0.01, 1.01], autorange=False))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    eff_score = (
                        0.12 * nonlinear_normalize(np.nanmean( np.concatenate((Rate_graf[:, m, c3, i, j, 13], Rate_bikes[:, m, c3, i, j, 13], Rate_boat[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 13], Rate_wall[:, m, c3, i, j, 13], Rate_trees[:, m, c3, i, j, 13], Rate_bark[:, m, c3, i, j, 13], Rate_ubc[:, m, c3, i, j, 13]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 13],  Rate_bikes[:, :, :, :, :, 13],  Rate_boat[:, :, :, :, :, 13],  Rate_leuven[:, :, :, :, :, 13],  Rate_wall[:, :, :, :, :, 13],  Rate_trees[:, :, :, :, :, 13],  Rate_bark[:, :, :, :, :, 13],  Rate_ubc[:, :, :, :, :, 13]),  axis=0))+
                        0.05 * nonlinear_normalize(np.nanmean( np.concatenate((Rate_graf[:, m, c3, i, j, 12], Rate_bikes[:, m, c3, i, j, 12], Rate_boat[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 12], Rate_wall[:, m, c3, i, j, 12], Rate_trees[:, m, c3, i, j, 12], Rate_bark[:, m, c3, i, j, 12], Rate_ubc[:, m, c3, i, j, 12]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 12],  Rate_bikes[:, :, :, :, :, 12],  Rate_boat[:, :, :, :, :, 12],  Rate_leuven[:, :, :, :, :, 12],  Rate_wall[:, :, :, :, :, 12],  Rate_trees[:, :, :, :, :, 12],  Rate_bark[:, :, :, :, :, 12],  Rate_ubc[:, :, :, :, :, 12]),  axis=0))+
                        0.05 * nonlinear_normalize(np.nanmean( np.concatenate((Rate_graf[:, m, c3, i, j, 14], Rate_bikes[:, m, c3, i, j, 14], Rate_boat[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 14], Rate_wall[:, m, c3, i, j, 14], Rate_trees[:, m, c3, i, j, 14], Rate_bark[:, m, c3, i, j, 14], Rate_ubc[:, m, c3, i, j, 14]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 14],  Rate_bikes[:, :, :, :, :, 14],  Rate_boat[:, :, :, :, :, 14],  Rate_leuven[:, :, :, :, :, 14],  Rate_wall[:, :, :, :, :, 14],  Rate_trees[:, :, :, :, :, 14],  Rate_bark[:, :, :, :, :, 14],  Rate_ubc[:, :, :, :, :, 14]),  axis=0))+
                        0.15 * nonlinear_normalize(np.nanmean( np.concatenate((Rate_graf[:, m, c3, i, j, 15], Rate_bikes[:, m, c3, i, j, 15], Rate_boat[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 15], Rate_wall[:, m, c3, i, j, 15], Rate_trees[:, m, c3, i, j, 15], Rate_bark[:, m, c3, i, j, 15], Rate_ubc[:, m, c3, i, j, 15]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 15],  Rate_bikes[:, :, :, :, :, 15],  Rate_boat[:, :, :, :, :, 15],  Rate_leuven[:, :, :, :, :, 15],  Rate_wall[:, :, :, :, :, 15],  Rate_trees[:, :, :, :, :, 15],  Rate_bark[:, :, :, :, :, 15],  Rate_ubc[:, :, :, :, :, 15]),  axis=0))+
                        0.08 * nonlinear_normalize(np.nanmean( np.concatenate((Rate_graf[:, m, c3, i, j,  9], Rate_bikes[:, m, c3, i, j,  9], Rate_boat[:, m, c3, i, j,  9], Rate_leuven[:, m, c3, i, j,  9], Rate_wall[:, m, c3, i, j,  9], Rate_trees[:, m, c3, i, j,  9], Rate_bark[:, m, c3, i, j,  9], Rate_ubc[:, m, c3, i, j,  9]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :,  9],  Rate_bikes[:, :, :, :, :,  9],  Rate_boat[:, :, :, :, :,  9],  Rate_leuven[:, :, :, :, :,  9],  Rate_wall[:, :, :, :, :,  9],  Rate_trees[:, :, :, :, :,  9],  Rate_bark[:, :, :, :, :,  9],  Rate_ubc[:, :, :, :, :,  9]),  axis=0))+
                        0.05 * nonlinear_normalize(np.nanmean( np.concatenate((Rate_graf[:, m, c3, i, j, 10], Rate_bikes[:, m, c3, i, j, 10], Rate_boat[:, m, c3, i, j, 10], Rate_leuven[:, m, c3, i, j, 10], Rate_wall[:, m, c3, i, j, 10], Rate_trees[:, m, c3, i, j, 10], Rate_bark[:, m, c3, i, j, 10], Rate_ubc[:, m, c3, i, j, 10]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 10],  Rate_bikes[:, :, :, :, :, 10],  Rate_boat[:, :, :, :, :, 10],  Rate_leuven[:, :, :, :, :, 10],  Rate_wall[:, :, :, :, :, 10],  Rate_trees[:, :, :, :, :, 10],  Rate_bark[:, :, :, :, :, 10],  Rate_ubc[:, :, :, :, :, 10]),  axis=0))+
                        0.10 * (1-nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 6], Exec_time_bikes[:, m, c3, i, j, 6], Exec_time_boat[:, m, c3, i, j, 6], Exec_time_leuven[:, m, c3, i, j, 6], Exec_time_wall[:, m, c3, i, j, 6], Exec_time_trees[:, m, c3, i, j, 6], Exec_time_bark[:, m, c3, i, j, 6], Exec_time_ubc[:, m, c3, i, j, 6]), axis=0)),np.concatenate((Exec_time_graf[:, :, :, :, :, 6],  Exec_time_bikes[:, :, :, :, :, 6],  Exec_time_boat[:, :, :, :, :, 6],  Exec_time_leuven[:, :, :, :, :, 6],  Exec_time_wall[:, :, :, :, :, 6],  Exec_time_trees[:, :, :, :, :, 6],  Exec_time_bark[:, :, :, :, :, 6],  Exec_time_ubc[:, :, :, :, :, 6]),  axis=0)))+
                        0.15 * (1-nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 7], Exec_time_bikes[:, m, c3, i, j, 7], Exec_time_boat[:, m, c3, i, j, 7], Exec_time_leuven[:, m, c3, i, j, 7], Exec_time_wall[:, m, c3, i, j, 7], Exec_time_trees[:, m, c3, i, j, 7], Exec_time_bark[:, m, c3, i, j, 7], Exec_time_ubc[:, m, c3, i, j, 7]), axis=0)),np.concatenate((Exec_time_graf[:, :, :, :, :, 7],  Exec_time_bikes[:, :, :, :, :, 7],  Exec_time_boat[:, :, :, :, :, 7],  Exec_time_leuven[:, :, :, :, :, 7],  Exec_time_wall[:, :, :, :, :, 7],  Exec_time_trees[:, :, :, :, :, 7],  Exec_time_bark[:, :, :, :, :, 7],  Exec_time_ubc[:, :, :, :, :, 7]),  axis=0)))
                    ) * 4 / 3
                    if not (eff_score == 0 or np.isnan(eff_score)):
                        fig.add_trace(go.Scatter(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[eff_score], text=[f"{eff_score:.3f}"],
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}", mode="markers",
                                                    marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]), showlegend=True,
                                                    legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    fig.update_layout(updatemenus=[ dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear"}]),
                                                                    dict(label="Log",             method="relayout", args=[{"yaxis.type": "log"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html(f"./html/oxford/oxford_Efficiency.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford_Efficiency.html", "a") as f:
        f.write(custom_html)

def oxfordHeatmap():
    fig = make_subplots(rows=2, cols=2, subplot_titles=[f"<span style='font-size: 22px;'>L2-BruteForce</span>", "<span style='font-size: 22px;'>L2-Flann</span>", "<span style='font-size: 22px;'>Hamming-BruteForce</span>", "<span style='font-size: 22px;'>Hamming-Flann</span>"], horizontal_spacing=0.07, vertical_spacing=0.08)
    scores = np.full((len(DetectorsLegend), len(DescriptorsLegend), 2, 2), np.nan)
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    scores[i, j, c3, m] = (
                        0.15 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 13], Rate_bikes[:, m, c3, i, j, 13], Rate_boat[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 13], Rate_wall[:, m, c3, i, j, 13], Rate_trees[:, m, c3, i, j, 13], Rate_bark[:, m, c3, i, j, 13], Rate_ubc[:, m, c3, i, j, 13]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 13], Rate_bikes[:, :, :, :, :, 13], Rate_boat[:, :, :, :, :, 13], Rate_leuven[:, :, :, :, :, 13], Rate_wall[:, :, :, :, :, 13], Rate_trees[:, :, :, :, :, 13], Rate_bark[:, :, :, :, :, 13], Rate_ubc[:, :, :, :, :, 13]), axis=0))+
                        0.10 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 12], Rate_bikes[:, m, c3, i, j, 12], Rate_boat[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 12], Rate_wall[:, m, c3, i, j, 12], Rate_trees[:, m, c3, i, j, 12], Rate_bark[:, m, c3, i, j, 12], Rate_ubc[:, m, c3, i, j, 12]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 12], Rate_bikes[:, :, :, :, :, 12], Rate_boat[:, :, :, :, :, 12], Rate_leuven[:, :, :, :, :, 12], Rate_wall[:, :, :, :, :, 12], Rate_trees[:, :, :, :, :, 12], Rate_bark[:, :, :, :, :, 12], Rate_ubc[:, :, :, :, :, 12]), axis=0))+
                        0.08 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 14], Rate_bikes[:, m, c3, i, j, 14], Rate_boat[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 14], Rate_wall[:, m, c3, i, j, 14], Rate_trees[:, m, c3, i, j, 14], Rate_bark[:, m, c3, i, j, 14], Rate_ubc[:, m, c3, i, j, 14]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 14], Rate_bikes[:, :, :, :, :, 14], Rate_boat[:, :, :, :, :, 14], Rate_leuven[:, :, :, :, :, 14], Rate_wall[:, :, :, :, :, 14], Rate_trees[:, :, :, :, :, 14], Rate_bark[:, :, :, :, :, 14], Rate_ubc[:, :, :, :, :, 14]), axis=0))+
                        0.10 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 15], Rate_bikes[:, m, c3, i, j, 15], Rate_boat[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 15], Rate_wall[:, m, c3, i, j, 15], Rate_trees[:, m, c3, i, j, 15], Rate_bark[:, m, c3, i, j, 15], Rate_ubc[:, m, c3, i, j, 15]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 15], Rate_bikes[:, :, :, :, :, 15], Rate_boat[:, :, :, :, :, 15], Rate_leuven[:, :, :, :, :, 15], Rate_wall[:, :, :, :, :, 15], Rate_trees[:, :, :, :, :, 15], Rate_bark[:, :, :, :, :, 15], Rate_ubc[:, :, :, :, :, 15]), axis=0))+
                        0.10 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j,  9], Rate_bikes[:, m, c3, i, j,  9], Rate_boat[:, m, c3, i, j,  9], Rate_leuven[:, m, c3, i, j,  9], Rate_wall[:, m, c3, i, j,  9], Rate_trees[:, m, c3, i, j,  9], Rate_bark[:, m, c3, i, j,  9], Rate_ubc[:, m, c3, i, j,  9]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :,  9], Rate_bikes[:, :, :, :, :,  9], Rate_boat[:, :, :, :, :,  9], Rate_leuven[:, :, :, :, :,  9], Rate_wall[:, :, :, :, :,  9], Rate_trees[:, :, :, :, :,  9], Rate_bark[:, :, :, :, :,  9], Rate_ubc[:, :, :, :, :,  9]), axis=0))+
                        0.07 * nonlinear_normalize(np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 10], Rate_bikes[:, m, c3, i, j, 10], Rate_boat[:, m, c3, i, j, 10], Rate_leuven[:, m, c3, i, j, 10], Rate_wall[:, m, c3, i, j, 10], Rate_trees[:, m, c3, i, j, 10], Rate_bark[:, m, c3, i, j, 10], Rate_ubc[:, m, c3, i, j, 10]), axis=0)),np.concatenate((Rate_graf[:, :, :, :, :, 10], Rate_bikes[:, :, :, :, :, 10], Rate_boat[:, :, :, :, :, 10], Rate_leuven[:, :, :, :, :, 10], Rate_wall[:, :, :, :, :, 10], Rate_trees[:, :, :, :, :, 10], Rate_bark[:, :, :, :, :, 10], Rate_ubc[:, :, :, :, :, 10]), axis=0))+
                        0.05 * (1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 6], Exec_time_bikes[:, m, c3, i, j, 6], Exec_time_boat[:, m, c3, i, j, 6], Exec_time_leuven[:, m, c3, i, j, 6], Exec_time_wall[:, m, c3, i, j, 6], Exec_time_trees[:, m, c3, i, j, 6], Exec_time_bark[:, m, c3, i, j, 6], Exec_time_ubc[:, m, c3, i, j, 6]), axis=0)),np.concatenate((Exec_time_graf[:, :, :, :, :, 6], Exec_time_bikes[:, :, :, :, :, 6], Exec_time_boat[:, :, :, :, :, 6], Exec_time_leuven[:, :, :, :, :, 6], Exec_time_wall[:, :, :, :, :, 6], Exec_time_trees[:, :, :, :, :, 6], Exec_time_bark[:, :, :, :, :, 6], Exec_time_ubc[:, :, :, :, :, 6]), axis=0)))+
                        0.10 * (1 - nonlinear_normalize(np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 7], Exec_time_bikes[:, m, c3, i, j, 7], Exec_time_boat[:, m, c3, i, j, 7], Exec_time_leuven[:, m, c3, i, j, 7], Exec_time_wall[:, m, c3, i, j, 7], Exec_time_trees[:, m, c3, i, j, 7], Exec_time_bark[:, m, c3, i, j, 7], Exec_time_ubc[:, m, c3, i, j, 7]), axis=0)),np.concatenate((Exec_time_graf[:, :, :, :, :, 7], Exec_time_bikes[:, :, :, :, :, 7], Exec_time_boat[:, :, :, :, :, 7], Exec_time_leuven[:, :, :, :, :, 7], Exec_time_wall[:, :, :, :, :, 7], Exec_time_trees[:, :, :, :, :, 7], Exec_time_bark[:, :, :, :, :, 7], Exec_time_ubc[:, :, :, :, :, 7]), axis=0)))
                    ) * 4 / 3
    for c3 in range(2):
        for m in range(2):
            fig.add_trace(go.Heatmap( z=scores[:,:,c3,m], x=DescriptorsLegend, y=DetectorsLegend, colorscale="matter", hoverongaps=False, hovertemplate="Detector: %{y}<br>Descriptor: %{x}<br>Score: %{z:.3f}"), row=c3+1, col=m+1)
    fig.update_layout(template="ggplot2", title=dict(text=f"<span style='font-size: 26px;'><b>Oxford Efficiency Heatmaps</b></span>", x=0.5, xanchor="center", yanchor="middle"), font_size=20, margin=dict(l=20, r=20, t=50, b=20))
    fig.write_html(f"./html/oxford/oxford_Heatmap.html", include_plotlyjs="cdn", full_html=True, config=config)

def oxfordCorrelationHeatmap():
    metrics = {
        "Precision":            np.concatenate((Rate_graf[:, :, :, :, :, 13], Rate_bikes[:, :, :, :, :, 13], Rate_boat[:, :, :, :, :, 13], Rate_leuven[:, :, :, :, :, 13], Rate_wall[:, :, :, :, :, 13], Rate_trees[:, :, :, :, :, 13], Rate_bark[:, :, :, :, :, 13], Rate_ubc[:, :, :, :, :, 13]), axis=0).flatten(),
        "Recall":               np.concatenate((Rate_graf[:, :, :, :, :, 12], Rate_bikes[:, :, :, :, :, 12], Rate_boat[:, :, :, :, :, 12], Rate_leuven[:, :, :, :, :, 12], Rate_wall[:, :, :, :, :, 12], Rate_trees[:, :, :, :, :, 12], Rate_bark[:, :, :, :, :, 12], Rate_ubc[:, :, :, :, :, 12]), axis=0).flatten(),
        "Repeatibility":        np.concatenate((Rate_graf[:, :, :, :, :, 14], Rate_bikes[:, :, :, :, :, 14], Rate_boat[:, :, :, :, :, 14], Rate_leuven[:, :, :, :, :, 14], Rate_wall[:, :, :, :, :, 14], Rate_trees[:, :, :, :, :, 14], Rate_bark[:, :, :, :, :, 14], Rate_ubc[:, :, :, :, :, 14]), axis=0).flatten(),
        "F1 Score":             np.concatenate((Rate_graf[:, :, :, :, :, 15], Rate_bikes[:, :, :, :, :, 15], Rate_boat[:, :, :, :, :, 15], Rate_leuven[:, :, :, :, :, 15], Rate_wall[:, :, :, :, :, 15], Rate_trees[:, :, :, :, :, 15], Rate_bark[:, :, :, :, :, 15], Rate_ubc[:, :, :, :, :, 15]), axis=0).flatten(),
        "Inliers":              np.concatenate((Rate_graf[:, :, :, :, :,  9], Rate_bikes[:, :, :, :, :,  9], Rate_boat[:, :, :, :, :,  9], Rate_leuven[:, :, :, :, :,  9], Rate_wall[:, :, :, :, :,  9], Rate_trees[:, :, :, :, :,  9], Rate_bark[:, :, :, :, :,  9], Rate_ubc[:, :, :, :, :,  9]), axis=0).flatten(),
        "Matches":              np.concatenate((Rate_graf[:, :, :, :, :, 10], Rate_bikes[:, :, :, :, :, 10], Rate_boat[:, :, :, :, :, 10], Rate_leuven[:, :, :, :, :, 10], Rate_wall[:, :, :, :, :, 10], Rate_trees[:, :, :, :, :, 10], Rate_bark[:, :, :, :, :, 10], Rate_ubc[:, :, :, :, :, 10]), axis=0).flatten(),
        "1K Total Time":        np.concatenate((Exec_time_graf[:, :, :, :, :, 6], Exec_time_bikes[:, :, :, :, :, 6], Exec_time_boat[:, :, :, :, :, 6], Exec_time_leuven[:, :, :, :, :, 6], Exec_time_wall[:, :, :, :, :, 6], Exec_time_trees[:, :, :, :, :, 6], Exec_time_bark[:, :, :, :, :, 6], Exec_time_ubc[:, :, :, :, :, 6]), axis=0).flatten(),
        "1K Inlier Time":       np.concatenate((Exec_time_graf[:, :, :, :, :, 7], Exec_time_bikes[:, :, :, :, :, 7], Exec_time_boat[:, :, :, :, :, 7], Exec_time_leuven[:, :, :, :, :, 7], Exec_time_wall[:, :, :, :, :, 7], Exec_time_trees[:, :, :, :, :, 7], Exec_time_bark[:, :, :, :, :, 7], Exec_time_ubc[:, :, :, :, :, 7]), axis=0).flatten()
    }
    
    metric_names = list(metrics.keys())
    corr_matrix = np.zeros((len(metric_names), len(metric_names)))
    
    for i, name1 in enumerate(metric_names):
        for j, name2 in enumerate(metric_names):
            data1 = metrics[name1]
            data2 = metrics[name2]
            mask = ~(np.isnan(data1) | np.isnan(data2) | np.isinf(data1) | np.isinf(data2))
            if np.sum(mask) > 1:
                corr_matrix[i,j] = np.corrcoef(data1[mask], data2[mask])[0,1]
            else:
                corr_matrix[i,j] = 0
    
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=corr_matrix, x=metric_names, y=metric_names, colorscale='RdBu',zmid=0, text=np.round(corr_matrix, 3), texttemplate='%{text}', hoverongaps=False, hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>'))
    fig.update_layout(template="ggplot2", font_size=20, title=dict(text="<span style='font-size: 26px;'><b>Oxford Dataset Metric Correlations</b></span>", x=0.5,xanchor="center", yanchor="middle"), margin=dict(l=20, r=20, t=50, b=20))
    fig.write_html(f"./html/oxford/oxford_Correlation.html", include_plotlyjs="cdn", full_html=True, config=config)

def oxfordViolin():
    fig = go.Figure()
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):  # Normalization Type
                for m in range(2):  # Matcher Type
                    xydata = [
                        np.concatenate((Rate_graf[:, m, c3, i, j, 13], Rate_bikes[:, m, c3, i, j, 13], Rate_boat[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 13], Rate_wall[:, m, c3, i, j, 13], Rate_trees[:, m, c3, i, j, 13], Rate_bark[:, m, c3, i, j, 13], Rate_ubc[:, m, c3, i, j, 13]), axis=0),
                        np.concatenate((Rate_graf[:, m, c3, i, j, 12], Rate_bikes[:, m, c3, i, j, 12], Rate_boat[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 12], Rate_wall[:, m, c3, i, j, 12], Rate_trees[:, m, c3, i, j, 12], Rate_bark[:, m, c3, i, j, 12], Rate_ubc[:, m, c3, i, j, 12]), axis=0),
                        np.concatenate((Rate_graf[:, m, c3, i, j, 14], Rate_bikes[:, m, c3, i, j, 14], Rate_boat[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 14], Rate_wall[:, m, c3, i, j, 14], Rate_trees[:, m, c3, i, j, 14], Rate_bark[:, m, c3, i, j, 14], Rate_ubc[:, m, c3, i, j, 14]), axis=0),
                        np.concatenate((Rate_graf[:, m, c3, i, j, 15], Rate_bikes[:, m, c3, i, j, 15], Rate_boat[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 15], Rate_wall[:, m, c3, i, j, 15], Rate_trees[:, m, c3, i, j, 15], Rate_bark[:, m, c3, i, j, 15], Rate_ubc[:, m, c3, i, j, 15]), axis=0),
                        np.concatenate((Rate_graf[:, m, c3, i, j,  9], Rate_bikes[:, m, c3, i, j,  9], Rate_boat[:, m, c3, i, j,  9], Rate_leuven[:, m, c3, i, j,  9], Rate_wall[:, m, c3, i, j,  9], Rate_trees[:, m, c3, i, j,  9], Rate_bark[:, m, c3, i, j,  9], Rate_ubc[:, m, c3, i, j,  9]), axis=0),
                        np.concatenate((Rate_graf[:, m, c3, i, j, 10], Rate_bikes[:, m, c3, i, j, 10], Rate_boat[:, m, c3, i, j, 10], Rate_leuven[:, m, c3, i, j, 10], Rate_wall[:, m, c3, i, j, 10], Rate_trees[:, m, c3, i, j, 10], Rate_bark[:, m, c3, i, j, 10], Rate_ubc[:, m, c3, i, j, 10]), axis=0),
                        np.concatenate((Exec_time_graf[:, m, c3, i, j, 6], Exec_time_bikes[:, m, c3, i, j, 6], Exec_time_boat[:, m, c3, i, j, 6], Exec_time_leuven[:, m, c3, i, j, 6], Exec_time_wall[:, m, c3, i, j, 6], Exec_time_trees[:, m, c3, i, j, 6], Exec_time_bark[:, m, c3, i, j, 6], Exec_time_ubc[:, m, c3, i, j, 6]), axis=0),
                        np.concatenate((Exec_time_graf[:, m, c3, i, j, 7], Exec_time_bikes[:, m, c3, i, j, 7], Exec_time_boat[:, m, c3, i, j, 7], Exec_time_leuven[:, m, c3, i, j, 7], Exec_time_wall[:, m, c3, i, j, 7], Exec_time_trees[:, m, c3, i, j, 7], Exec_time_bark[:, m, c3, i, j, 7], Exec_time_ubc[:, m, c3, i, j, 7]), axis=0)
                    ]
                    if not np.isnan(xydata).any():
                        traces.append(go.Violin(
                                x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]]*len(xydata[0]), [Norm[c3]]*len(xydata[0])], y=xydata,
                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                box_visible=True, meanline_visible=True))
                        fig.add_trace(go.Violin(
                                x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]]*len(xydata[0]), [Norm[c3]]*len(xydata[0])], y=xydata[0],
                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                box_visible=True, meanline_visible=True))
    dropdown_axis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_list = []
    for idx, axis in enumerate(dropdown_axis):
        button_list.append(dict(label=f"y: {axis}", method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig.update_layout(  template="ggplot2", font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>Oxford - Violin Plots</b></span>", x=0.5, xanchor="center", yanchor="middle"), margin=dict(l=20, r=20, t=50, b=20), hovermode="x unified", 
                        updatemenus=[   dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                        dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1, yanchor="bottom")])
    
    fig.write_html(f"./html/oxford/oxford_Violin.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford_Violin.html", "a") as f:
        f.write(custom_html)
########################################
# MARK: - Single Data (Drone-UAV-AirSim)
########################################
def singleAll(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig = go.Figure()
    xvals = [f"Img{i}" for i in range(153, 188)] if data == "drone" else (
        ["Bahamas", "Office", "Suburban", "Building", "Construction", "Dominica", "Cadastre", "Rivaz", "Urban", "Belleview"] if data == "uav" else 
        [f"Img{i}" for i in range(653, 774, 5)])
    fig.update_layout( template="ggplot2", font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()} Data</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
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
                        1 - nonlinear_normalize(Exec_time[:, m, c3, i, j, 6], Exec_time[:, :, :, :, :, 6]),# 1K Total Time
                        1 - nonlinear_normalize(Exec_time[:, m, c3, i, j, 7], Exec_time[:, :, :, :, :, 7]) # 1K feature Inlier Time
                    ]
                    if not np.isnan(y_data).any():
                        traces.append(go.Scatter(   x=xvals, y=y_data, mode="markers+lines",
                                                    marker=dict(symbol=marker_symbols[symbol_index], color=colors[color_index], size=16),
                                                    line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="<b>%{y:.3f}</b>"))
                        fig.add_trace(go.Scatter(   x=xvals, y=y_data[0], mode="markers+lines",
                                                    marker=dict(symbol=marker_symbols[symbol_index], color=colors[color_index], size=16),
                                                    line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="<b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=f"y: {y}", method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{y}</b></span>"}]))
    
    fig.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1, yanchor="bottom")]) 
    fig.write_html(f"./html/{data}/{data}All.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}All.html", "a") as f:
        f.write(custom_html)

def single(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig = go.Figure()
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()}</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"),
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
                        1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 6]), Exec_time[:, :, :, :, :, 6]), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 7]), Exec_time[:, :, :, :, :, 7]), # 1K feature Inlier Time
                    ]
                    if data == "drone":
                        xydata.append(1 - nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 11]), Rate[:, :, :, :, :, 11])) # Reprojection Error
                        xydata.append(np.nanmean(Rate[:, m, c3, i, j, 16])) # 3D Points Count
                        xydata.append(1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 8]) / np.nanmean(Rate[:, m, c3, i, j, 16]) * 1000, 
                                                               (Exec_time[:, :, :, :, :, 8] / Rate[:, :, :, :, :, 16] * 1000).flatten())) # 1K 3D Point Reconstruction Time
                    if not np.isnan(xydata).any():
                        traces.append(  go.Scatter( x=xydata,       y=xydata,       mode="markers", 
                                                    marker=dict(color=colors[color_index], size=xydata, symbol=marker_symbols[symbol_index]),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="x: <b>%{x:.2f}</b> | y: <b>%{y:.2f}</b>"))
                        fig.add_trace(go.Scatter( x=[xydata[0]],  y=[xydata[1]],  mode="markers", 
                                                    marker=dict(color=colors[color_index], size=[(xydata[4]*40+10)%50], symbol=marker_symbols[symbol_index]),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="x: <b>%{x:.2f}</b> | y: <b>%{y:.2f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."] + (["Reproj. Err", "3D-Points", "3D Time"] if data == "drone" else [])
    button_listx = []
    button_listy = []
    button_listz = []
        
    for idx, axis in enumerate(dropdown_axis):
        if idx < len(dropdown_axis):  # Ensure we don't go out of bounds
            button_listx.append(dict(label=f"x: {axis}", method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
            button_listy.append(dict(label=f"y: {axis}", method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
            button_listz.append(dict(label=f"z: {axis}", method="update", args=[{"marker.size": [((trace.marker.size[idx]*40+10)%50) for trace in traces]}]))
    fig.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listy, direction="down", x=0,  xanchor="left",  y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listx, direction="up",   x=1,  xanchor="right", y=0, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=5, buttons=button_listz, direction="down", x=0,  xanchor="left",  y=1)])
    fig.write_html(f"./html/{data}/{data}.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}.html", "a") as f:
        f.write(custom_html)

def singleTiming(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    fig = go.Figure()
    fig = make_subplots(rows=6, cols=2, subplot_titles=["<span style='font-size: 22px;'>Total time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Total time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>BF</b></span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>Flann</b></span>",
                                                        "<span style='font-size: 22px;'>Detect time</span>","<span style='font-size: 22px;'>Describe time</span>",
                                                        "<span style='font-size: 22px;'>All Timings</span>"],
                        specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.06)
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()} Dataset Timings for Average 1k</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), height=2500, margin=dict(l=20, r=20, t=80, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(Exec_time[:, m, :, i, j, 6])
                result4 = np.nanmean(Exec_time[:, m, :, i, j, 7])
                if not np.isnan(result3) and result3 > 0 and not np.isnan(result4) and result4 > 0:
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                        text=[f"{result3:.3f}"], marker=dict(color = colors[color_index]),
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_match_synt_result3, row=1, col=1) if m == 0 else fig.add_trace(trace_match_synt_result3, row=2, col=1)
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                        text=[f"{result4:.3f}"], marker=dict(color = colors[color_index]),
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig.add_trace(trace_match_synt_result4, row=3, col=1) if m == 0 else fig.add_trace(trace_match_synt_result4, row=4, col=1)
                    #All Timings
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-total']], y=[result3],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                            text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=6, col=1 )
                    fig.add_trace(go.Bar(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j] + '-' + Matcher[m] + '-inlier']], y=[result4],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                            text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"),  row=6, col=1 )
            color_index = (color_index + 14) % num_combinations
        result  = np.nanmean(Exec_time[:, :, :, i, :, 4])
        if not np.isnan(result) and result > 0:
            trace_detect = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=f".{DetectorsLegend[i]}",  showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            fig.add_trace(trace_detect, row=5, col=1)
        result2 = np.nanmean(Exec_time[:, :, :, :, i, 5])
        if not np.isnan(result2) and result2 > 0:
            trace_descr = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=f"-{DescriptorsLegend[i]}",showlegend=True, text=[f"{result2:.3f}"], marker=dict(color = colors[14*i]))
            fig.add_trace(trace_descr, row=5, col=2)
    # for i in range(1, 5):
    #     fig.update_xaxes(tickangle=90, row=i, col=1)
    # fig.update_xaxes(tickangle=90, row=5, col=2)
    fig.update_layout(updatemenus=[ dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear", "yaxis7.type": "linear"}]),
                                                                    dict(label="Log",             method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log", "yaxis7.type": "linear"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html(f"./html/{data}/{data}Timing.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}Timing.html", "a") as f:
        f.write(custom_html)

def singleEfficiency(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig = go.Figure()
    fig.update_layout(  template="ggplot2", font_size=16, margin=dict(l=20, r=20, t=80, b=20),
                        title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()} Efficiency</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        xaxis_tickangle=90, yaxis=dict(range=[-0.01, 1.01], autorange=False))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    eff_score = (
                        0.12 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 13]), Rate[:, :, :, :, :, 13].flatten()) +  # Precision
                        0.05 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 12]), Rate[:, :, :, :, :, 12].flatten()) +  # Recall
                        0.05 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 14]), Rate[:, :, :, :, :, 14].flatten()) +  # Repeatability
                        0.15 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 15]), Rate[:, :, :, :, :, 15].flatten()) +  # F1 Score
                        0.08 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j,  9]), Rate[:, :, :, :, :,  9].flatten()) +  # Inliers
                        0.05 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 10]), Rate[:, :, :, :, :, 10].flatten()) +  # Matches
                        0.10 * (1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 6]), Exec_time[:, :, :, :, :, 6].flatten())) +    # 1K Total Time
                        0.15 * (1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 7]), Exec_time[:, :, :, :, :, 7].flatten()))      # 1K Inlier Time
                    )
                    if data == "drone":
                        eff_score += (
                            0.08 * (1 - nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 11]), Rate[:, :, :, :, :, 11].flatten())) +  # Reprojection Error
                            0.10 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 16]), Rate[:, :, :, :, :, 16].flatten()) +        # 3D Points Count
                            0.07 * (1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 8]) / np.nanmean(Rate[:, m, c3, i, j, 16]) * 1000, (Exec_time[:, :, :, :, :, 8] / Rate[:, :, :, :, :, 16] * 1000).flatten()))  # 1K 3D Point Reconstruction Time
                        )
                    else:
                        eff_score = eff_score * 4 / 3
                    if not (eff_score == 0 or np.isnan(eff_score)):
                        fig.add_trace(go.Scatter(   x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[eff_score], text=[f"{eff_score:.3f}"],
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}", mode="markers",
                                                    marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]), showlegend=True,
                                                    legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
        color_index = (color_index + 14) % num_combinations
    fig.update_layout(updatemenus=[ dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear"}]),
                                                                    dict(label="Log",             method="relayout", args=[{"yaxis.type": "log"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html(f"./html/{data}/{data}_Efficiency.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}_Efficiency.html", "a") as f:
        f.write(custom_html)

def heatmap(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")  
    fig = make_subplots(rows=2, cols=2, subplot_titles=[f"<span style='font-size: 22px;'>L2-BruteForce</span>", "<span style='font-size: 22px;'>L2-Flann</span>", "<span style='font-size: 22px;'>Hamming-BruteForce</span>", "<span style='font-size: 22px;'>Hamming-Flann</span>"], horizontal_spacing=0.07, vertical_spacing=0.08)
    scores = np.full((len(DetectorsLegend), len(DescriptorsLegend), 2, 2), np.nan)
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    scores[i, j, c3, m] = (
                        0.15 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 13]), Rate[:, :, :, :, :, 13].flatten()) +  # Precision
                        0.10 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 12]), Rate[:, :, :, :, :, 12].flatten()) +  # Recall
                        0.08 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 14]), Rate[:, :, :, :, :, 14].flatten()) +  # Repeatability
                        0.10 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 15]), Rate[:, :, :, :, :, 15].flatten()) +  # F1 Score
                        0.10 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j,  9]), Rate[:, :, :, :, :, 9].flatten()) +   # Inliers
                        0.07 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 10]), Rate[:, :, :, :, :, 10].flatten()) +  # Matches
                        0.05 * (1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 6]), Exec_time[:, :, :, :, :, 6].flatten())) + # 1K Total Time
                        0.10 * (1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 7]), Exec_time[:, :, :, :, :, 7].flatten()))   # 1K Inlier Time
                    )
                    if data == "drone":
                        scores[i, j, c3, m] += (
                            0.05 * (1 - nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 11]), Rate[:, :, :, :, :, 11].flatten())) +  # Reprojection Error
                            0.10 * nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 16]), Rate[:, :, :, :, :, 16].flatten()) +        # 3D Points Count
                            0.10 * (1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 8]) / np.nanmean(Rate[:, m, c3, i, j, 16]) * 1000, (Exec_time[:, :, :, :, :, 8] / Rate[:, :, :, :, :, 16] * 1000).flatten()))  # 1K 3D Point Reconstruction Time
                        )
                    else:
                        scores[i, j, c3, m] = scores[i, j, c3, m] * 4 / 3
    for c3 in range(2):
        for m in range(2):            
            fig.add_trace(go.Heatmap(z=scores[:, :, c3, m],x=DescriptorsLegend, y=DetectorsLegend, colorscale="matter",hovertemplate='Detector: %{y}<br>Descriptor: %{x}<br>Score: %{z:.3f}'), row=c3+1, col=m+1)
    fig.update_layout(template="ggplot2", title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()} Efficiency Heatmaps</b></span>", x=0.5, xanchor="center", yanchor="middle"), font_size=20, margin=dict(l=20, r=20, t=50, b=20))
    fig.write_html(f"./html/{data}/{data}_Heatmap.html", include_plotlyjs="cdn", full_html=True, config=config)

def correlationHeatmap(data="drone"):
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")    
    
    metrics = {
        "Precision":            Rate[:, :, :, :, :, 13].flatten(),
        "Recall":               Rate[:, :, :, :, :, 12].flatten(),
        "Repeatibility":        Rate[:, :, :, :, :, 14].flatten(),
        "F1 Score":             Rate[:, :, :, :, :, 15].flatten(),
        "Inliers":              Rate[:, :, :, :, :,  9].flatten(),
        "Matches":              Rate[:, :, :, :, :, 10].flatten(),
        "1K Total Time":   Exec_time[:, :, :, :, :,  6].flatten(),
        "1K Inlier Time":  Exec_time[:, :, :, :, :,  7].flatten(),
    }
    
    if data == "drone":
        metrics.update({
            "Reprojection Error": Rate[:, :, :, :, :, 11].flatten(),
            "3D Points Count":    Rate[:, :, :, :, :, 16].flatten()
        })
    
    metric_names = list(metrics.keys())
    corr_matrix = np.zeros((len(metric_names), len(metric_names)))
    for i, name1 in enumerate(metric_names):
        for j, name2 in enumerate(metric_names):
            data1 = metrics[name1]
            data2 = metrics[name2]
            mask = ~(np.isnan(data1) | np.isnan(data2) | np.isinf(data1) | np.isinf(data2))
            if np.sum(mask) > 1:
                corr_matrix[i,j] = np.corrcoef(data1[mask], data2[mask])[0,1]
            else:
                corr_matrix[i,j] = 0
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=corr_matrix, x=metric_names, y=metric_names, colorscale='RdBu', zmid=0, text=np.round(corr_matrix, 3), texttemplate='%{text}', hoverongaps=False, hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>'))
    fig.update_layout(template="ggplot2", font_size=20, title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()} Metric Correlations</b></span>", x=0.5, xanchor="center", yanchor="middle"), margin=dict(l=20, r=20, t=50, b=20))
    fig.write_html(f"./html/{data}/{data}_Correlation.html", include_plotlyjs="cdn", full_html=True, config=config)

def violinPlot(data="drone"):
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    fig = go.Figure()
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):  # Normalization Type
                for m in range(2):  # Matcher Type
                    xydata = [
                        Rate[:, m, c3, i, j, 13], # Precision
                        Rate[:, m, c3, i, j, 12], # Recall
                        Rate[:, m, c3, i, j, 14], # Repeatibility
                        Rate[:, m, c3, i, j, 15], # F1 Score
                        Rate[:, m, c3, i, j,  9], # Inliers
                        Rate[:, m, c3, i, j, 10], # Matches
                        Exec_time[:, m, c3, i, j, 6],  # 1K Total Time
                        Exec_time[:, m, c3, i, j, 7]   # 1K Inlier Time
                    ]
                    if not np.isnan(xydata).any():
                        traces.append(go.Violin(
                                x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]]*len(xydata[0]), [Norm[c3]]*len(xydata[0])], y=xydata,
                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                box_visible=True, meanline_visible=True))
                        fig.add_trace(go.Violin(
                                x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]]*len(xydata[0]), [Norm[c3]]*len(xydata[0])], y=xydata[0],
                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                box_visible=True, meanline_visible=True))
    dropdown_axis = ["Precision", "Recall", "Repeat.", "F1Score", "Inliers", "Matches", "Time", "Inlier T."]
    button_list = []
    for idx, axis in enumerate(dropdown_axis):
        button_list.append(dict(label=f"y: {axis}", method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}])
    )
    fig.update_layout(  template="ggplot2", font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>{data.upper()} Violin Plots</b></span>", x=0.5, xanchor="center", yanchor="middle"), margin=dict(l=20, r=20, t=50, b=20), hovermode="x unified", 
                        updatemenus=[   dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                        dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1, yanchor="bottom")])
    
    fig.write_html(f"./html/{data}/{data}_Violin.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}_Violin.html", "a") as f:
        f.write(custom_html)
