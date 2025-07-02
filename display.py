import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from define import *
from sklearn.decomposition import PCA

custom_html = """
    <div style="position: fixed; top: 2px; left: 2px;">
        <span>
            <input type="text" id="filterInput" onchange="applyFilters()" placeholder="and/or/not .sift -sift bf pc">
            <input type="number" id="minYValueInput" step="0.05" onchange="applyFilters()" placeholder="min y">
            <input type="number" id="maxYValueInput" step="0.05" onchange="applyFilters()" placeholder="max y">
            <input type="number" id="minXValueInput" step="0.05" onchange="applyFilters()" placeholder="min x">
            <input type="number" id="maxXValueInput" step="0.05" onchange="applyFilters()" placeholder="max x">
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
            else if (logicKeyword === "NOT") {
                if (filterWords.length === 0) return true;
                return !filterWords.some(filterWord => word.includes(filterWord));
            }
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
                const matchFunc = filterMode === "all" ? Array.prototype.every : Array.prototype.some;
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

# *Synthetic Dataset
Rate_intensity              = np.load("./arrays/Rate_intensity.npy")
Rate_scale                  = np.load("./arrays/Rate_scale.npy")
Rate_rot                    = np.load("./arrays/Rate_rot.npy")
Exec_time_intensity         = np.load("./arrays/Exec_time_intensity.npy")
Exec_time_scale             = np.load("./arrays/Exec_time_scale.npy")
Exec_time_rot               = np.load("./arrays/Exec_time_rot.npy")
# # *mobile 1 Mediatek Dimensity 7200 Ultra
# Rate_intensity_mobile       = np.load("./arrays/Rate_intensity_mobile.npy")
# Rate_scale_mobile           = np.load("./arrays/Rate_scale_mobile.npy")
# Rate_rot_mobile             = np.load("./arrays/Rate_rot_mobile.npy")
Exec_time_intensity_mobile  = np.load("./arrays/Exec_time_intensity_mobile.npy")
Exec_time_scale_mobile      = np.load("./arrays/Exec_time_scale_mobile.npy")
Exec_time_rot_mobile        = np.load("./arrays/Exec_time_rot_mobile.npy")
# # *mobile 2 Snapdragon 855
# Rate_intensity_mobile2      = np.load("./arrays/Rate_intensity_mobile2.npy")
# Rate_scale_mobile2          = np.load("./arrays/Rate_scale_mobile2.npy")
# Rate_rot_mobile2            = np.load("./arrays/Rate_rot_mobile2.npy")
Exec_time_intensity_mobile2 = np.load("./arrays/Exec_time_intensity_mobile2.npy")
Exec_time_scale_mobile2     = np.load("./arrays/Exec_time_scale_mobile2.npy")
Exec_time_rot_mobile2       = np.load("./arrays/Exec_time_rot_mobile2.npy")

# *Oxford Dataset
Rate_graf                   = np.load("./arrays/Rate_graf.npy")
Rate_bikes                  = np.load("./arrays/Rate_bikes.npy")
Rate_boat                   = np.load("./arrays/Rate_boat.npy")
Rate_leuven                 = np.load("./arrays/Rate_leuven.npy")
Rate_wall                   = np.load("./arrays/Rate_wall.npy")
Rate_trees                  = np.load("./arrays/Rate_trees.npy")
Rate_bark                   = np.load("./arrays/Rate_bark.npy")
Rate_ubc                    = np.load("./arrays/Rate_ubc.npy")
Exec_time_graf              = np.load("./arrays/Exec_time_graf.npy")
Exec_time_bikes             = np.load("./arrays/Exec_time_bikes.npy")
Exec_time_boat              = np.load("./arrays/Exec_time_boat.npy")
Exec_time_leuven            = np.load("./arrays/Exec_time_leuven.npy")
Exec_time_wall              = np.load("./arrays/Exec_time_wall.npy")
Exec_time_trees             = np.load("./arrays/Exec_time_trees.npy")
Exec_time_bark              = np.load("./arrays/Exec_time_bark.npy")
Exec_time_ubc               = np.load("./arrays/Exec_time_ubc.npy")
# *mobile 1 Mediatek Dimensity 7200 Ultra
# Rate_graf_mobile            = np.load("./arrays/Rate_graf_mobile.npy")
# Rate_bikes_mobile           = np.load("./arrays/Rate_bikes_mobile.npy")
# Rate_boat_mobile            = np.load("./arrays/Rate_boat_mobile.npy")
# Rate_leuven_mobile          = np.load("./arrays/Rate_leuven_mobile.npy")
# Rate_wall_mobile            = np.load("./arrays/Rate_wall_mobile.npy")
# Rate_trees_mobile           = np.load("./arrays/Rate_trees_mobile.npy")
# Rate_bark_mobile            = np.load("./arrays/Rate_bark_mobile.npy")
# Rate_ubc_mobile             = np.load("./arrays/Rate_ubc_mobile.npy")
Exec_time_graf_mobile       = np.load("./arrays/Exec_time_graf_mobile.npy")
Exec_time_bikes_mobile      = np.load("./arrays/Exec_time_bikes_mobile.npy")
Exec_time_boat_mobile       = np.load("./arrays/Exec_time_boat_mobile.npy")
Exec_time_leuven_mobile     = np.load("./arrays/Exec_time_leuven_mobile.npy")
Exec_time_wall_mobile       = np.load("./arrays/Exec_time_wall_mobile.npy")
Exec_time_trees_mobile      = np.load("./arrays/Exec_time_trees_mobile.npy")
Exec_time_bark_mobile       = np.load("./arrays/Exec_time_bark_mobile.npy")
Exec_time_ubc_mobile        = np.load("./arrays/Exec_time_ubc_mobile.npy")
# # *mobile 2 Snapdragon 855
# Rate_graf_mobile2           = np.load("./arrays/Rate_graf_mobile2.npy")
# Rate_bikes_mobile2          = np.load("./arrays/Rate_bikes_mobile2.npy")
# Rate_boat_mobile2           = np.load("./arrays/Rate_boat_mobile2.npy")
# Rate_leuven_mobile2         = np.load("./arrays/Rate_leuven_mobile2.npy")
# Rate_wall_mobile2           = np.load("./arrays/Rate_wall_mobile2.npy")
# Rate_trees_mobile2          = np.load("./arrays/Rate_trees_mobile2.npy")
# Rate_bark_mobile2           = np.load("./arrays/Rate_bark_mobile2.npy")
# Rate_ubc_mobile2            = np.load("./arrays/Rate_ubc_mobile2.npy")
Exec_time_graf_mobile2      = np.load("./arrays/Exec_time_graf_mobile2.npy")
Exec_time_bikes_mobile2     = np.load("./arrays/Exec_time_bikes_mobile2.npy")
Exec_time_boat_mobile2      = np.load("./arrays/Exec_time_boat_mobile2.npy")
Exec_time_leuven_mobile2    = np.load("./arrays/Exec_time_leuven_mobile2.npy")
Exec_time_wall_mobile2      = np.load("./arrays/Exec_time_wall_mobile2.npy")
Exec_time_trees_mobile2     = np.load("./arrays/Exec_time_trees_mobile2.npy")
Exec_time_bark_mobile2      = np.load("./arrays/Exec_time_bark_mobile2.npy")
Exec_time_ubc_mobile2       = np.load("./arrays/Exec_time_ubc_mobile2.npy")


def syntheticAll4():
    fig = go.Figure()
    fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.05, vertical_spacing=0.08,
                        subplot_titles=["<span style='font-size: 20px;'><b>Intensity changing I+b</b></span>",
                                        "<span style='font-size: 20px;'><b>Intensity changing Ixc</b></span>",
                                        "<span style='font-size: 20px;'><b>Scale changing</b></span>",
                                        "<span style='font-size: 20px;'><b>Rotation changing</b></span>"])
    sett_axis = dict(range=[-0.01, 1.01], autorange=False)
    fig.update_layout(  template="ggplot2", font_size=16, hovermode="closest", margin=dict(l=20, r=20, t=70, b=20),
                        title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis,
                        xaxis=dict(tickmode="array", tickvals=val_b), xaxis2=dict(tickmode="array", tickvals=val_c), xaxis3=dict(tickmode="array", tickvals=scale), xaxis4=dict(tickmode="array", tickvals=rot))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1 = np.array([
                        Rate_intensity[:len(val_b), m, c3, i, j, 13], 
                        Rate_intensity[:len(val_b), m, c3, i, j, 12], 
                        Rate_intensity[:len(val_b), m, c3, i, j, 14], 
                        Rate_intensity[:len(val_b), m, c3, i, j, 15], 
                        Rate_intensity[:len(val_b), m, c3, i, j,  9], 
                        Rate_intensity[:len(val_b), m, c3, i, j, 10], 
                        Exec_time_intensity[:len(val_b), m, c3, i, j, 6],
                        Exec_time_intensity[:len(val_b), m, c3, i, j, 7]
                    ])
                    Rate2_I2 = np.array([
                        Rate_intensity[len(val_c):, m, c3, i, j, 13], 
                        Rate_intensity[len(val_c):, m, c3, i, j, 12], 
                        Rate_intensity[len(val_c):, m, c3, i, j, 14], 
                        Rate_intensity[len(val_c):, m, c3, i, j, 15], 
                        Rate_intensity[len(val_c):, m, c3, i, j,  9], 
                        Rate_intensity[len(val_c):, m, c3, i, j, 10],
                        Exec_time_intensity[len(val_c):, m, c3, i, j, 6],
                        Exec_time_intensity[len(val_c):, m, c3, i, j, 7]
                    ])
                    Rate2_S  = np.array([
                        Rate_scale[:, m, c3, i, j, 13], 
                        Rate_scale[:, m, c3, i, j, 12], 
                        Rate_scale[:, m, c3, i, j, 14], 
                        Rate_scale[:, m, c3, i, j, 15], 
                        Rate_scale[:, m, c3, i, j,  9], 
                        Rate_scale[:, m, c3, i, j, 10],
                        Exec_time_scale[:, m, c3, i, j, 6],
                        Exec_time_scale[:, m, c3, i, j, 7]
                    ])
                    Rate2_R  = np.array([
                        Rate_rot[:, m, c3, i, j, 13], 
                        Rate_rot[:, m, c3, i, j, 12], 
                        Rate_rot[:, m, c3, i, j, 14], 
                        Rate_rot[:, m, c3, i, j, 15], 
                        Rate_rot[:, m, c3, i, j,  9], 
                        Rate_rot[:, m, c3, i, j, 10],
                        Exec_time_rot[:, m, c3, i, j, 6],
                        Exec_time_rot[:, m, c3, i, j, 7]
                    ])
                    legend_groupfig = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig, legendgroup=legend_groupfig, showlegend=True, hovertemplate="<b>%{y:.3f}</b>")
                    if not np.isnan(Rate2_I1).all():
                        traces.append(go.Scatter(x=val_b, y=Rate2_I1,    arg=sett))
                        fig.add_trace(go.Scatter(x=val_b, y=Rate2_I1[0], arg=sett), row=1, col=1)
                    if not np.isnan(Rate2_I2).all():
                        traces.append(go.Scatter(x=val_c, y=Rate2_I2,    arg=sett))
                        fig.add_trace(go.Scatter(x=val_c, y=Rate2_I2[0], arg=sett), row=1, col=2)
                    if not np.isnan(Rate2_S).all():
                        traces.append(go.Scatter(x=scale, y=Rate2_S,     arg=sett))
                        fig.add_trace(go.Scatter(x=scale, y=Rate2_S[0],  arg=sett), row=2, col=1)
                    if not np.isnan(Rate2_R).all():
                        traces.append(go.Scatter(x=rot,   y=Rate2_R,     arg=sett))
                        fig.add_trace(go.Scatter(x=rot,   y=Rate2_R[0],  arg=sett), row=2, col=2)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeatability", "F1-Score", "Inliers", "Matches", "1k Match Time", "1k Inlier Time"]
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
    fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.05, vertical_spacing=0.08,
                        subplot_titles=["<span style='font-size: 20px;'><b>Intensity changing I+b</b></span>",
                                        "<span style='font-size: 20px;'><b>Intensity changing Ixc</b></span>",
                                        "<span style='font-size: 20px;'><b>Scale changing</b></span>",
                                        "<span style='font-size: 20px;'><b>Rotation changing</b></span>"])
    sett_axis = dict(range=[-0.01, 1.01], autorange=False)
    fig.update_layout(  template="ggplot2", font_size=16, hovermode="closest", margin=dict(l=20, r=20, t=70, b=20),
                        title=dict(text="<span style='font-size: 26px;'><b>Synthetic Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        xaxis=sett_axis, xaxis2=sett_axis, xaxis3=sett_axis, xaxis4=sett_axis,
                        yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    xydata_Intensity1 = np.array([
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 15]),       # F1 Score
                        nonlinear_normalize(np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j,  9]), Rate_intensity[:len(val_b), :, :, :, :, 9],               alpha=0.2), # Inliers
                        nonlinear_normalize(np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, 10]), Rate_intensity[:len(val_b), :, :, :, :, 10],              alpha=0.3), # Matches
                        1 - nonlinear_normalize(np.nanmean(Exec_time_intensity[:len(val_b), m, c3, i, j, 6]), Exec_time_intensity[:len(val_b), :, :, :, :, 6],  alpha=0.2), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time_intensity[:len(val_b), m, c3, i, j, 7]), Exec_time_intensity[:len(val_b), :, :, :, :, 7],  alpha=0.2)  # 1K feature Inlier Time
                    ])
                    xydata_Intensity2 = np.array([
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 15]),       # F1 Score
                        nonlinear_normalize(np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j,  9]), Rate_intensity[len(val_c):, :, :, :, :, 9],               alpha=0.2), # Inliers
                        nonlinear_normalize(np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, 10]), Rate_intensity[len(val_c):, :, :, :, :, 10],              alpha=0.3), # Matches
                        1 - nonlinear_normalize(np.nanmean(Exec_time_intensity[len(val_c):, m, c3, i, j, 6]), Exec_time_intensity[len(val_c):, :, :, :, :, 6],  alpha=0.2), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time_intensity[len(val_c):, m, c3, i, j, 7]), Exec_time_intensity[len(val_c):, :, :, :, :, 7],  alpha=0.2)  # 1K feature Inlier Time
                    ])
                    xydata_Scale      = np.array([
                        np.nanmean(Rate_scale[:, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_scale[:, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_scale[:, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_scale[:, m, c3, i, j, 15]),       # F1 Score
                        nonlinear_normalize(np.nanmean(Rate_scale[:, m, c3, i, j,  9]), Rate_scale[:, :, :, :, :, 9],               alpha=0.2), # Inliers
                        nonlinear_normalize(np.nanmean(Rate_scale[:, m, c3, i, j, 10]), Rate_scale[:, :, :, :, :, 10],              alpha=0.3), # Matches
                        1 - nonlinear_normalize(np.nanmean(Exec_time_scale[:, m, c3, i, j, 6]), Exec_time_scale[:, :, :, :, :, 6],  alpha=0.2), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time_scale[:, m, c3, i, j, 7]), Exec_time_scale[:, :, :, :, :, 7],  alpha=0.2)  # 1K feature Inlier Time
                    ])
                    xydata_Rotation   = np.array([
                        np.nanmean(Rate_rot[:, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate_rot[:, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate_rot[:, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate_rot[:, m, c3, i, j, 15]),       # F1 Score
                        nonlinear_normalize(np.nanmean(Rate_rot[:, m, c3, i, j,  9]), Rate_rot[:, :, :, :, :, 9],               alpha=0.2), # Inliers
                        nonlinear_normalize(np.nanmean(Rate_rot[:, m, c3, i, j, 10]), Rate_rot[:, :, :, :, :, 10],              alpha=0.3), # Matches
                        1 - nonlinear_normalize(np.nanmean(Exec_time_rot[:, m, c3, i, j, 6]), Exec_time_rot[:, :, :, :, :, 6],  alpha=0.2), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time_rot[:, m, c3, i, j, 7]), Exec_time_rot[:, :, :, :, :, 7],  alpha=0.2)  # 1K feature Inlier Time
                    ])
                    legend_groupfig = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                name=legend_groupfig, legendgroup=legend_groupfig, showlegend=True,
                                hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>")
                    if not np.isnan(xydata_Intensity1).all():
                        traces.append(go.Scatter(x=xydata_Intensity1,      y=xydata_Intensity1,      arg=sett,  marker_size=np.where(np.isnan(xydata_Intensity1), epsilon, xydata_Intensity1)))
                        fig.add_trace(go.Scatter(x=[xydata_Intensity1[0]], y=[xydata_Intensity1[1]], arg=sett), row=1, col=1)
                    if not np.isnan(xydata_Intensity2).all():
                        traces.append(go.Scatter(x=xydata_Intensity2,      y=xydata_Intensity2,      arg=sett,  marker_size=np.where(np.isnan(xydata_Intensity2), epsilon, xydata_Intensity2)))
                        fig.add_trace(go.Scatter(x=[xydata_Intensity2[0]], y=[xydata_Intensity2[1]], arg=sett), row=1, col=2)
                    if not np.isnan(xydata_Scale).all():
                        traces.append(go.Scatter(x=xydata_Scale,           y=xydata_Scale,           arg=sett,  marker_size=np.where(np.isnan(xydata_Scale), epsilon, xydata_Scale)))
                        fig.add_trace(go.Scatter(x=[xydata_Scale[0]],      y=[xydata_Scale[1]],      arg=sett), row=2, col=1)
                    if not np.isnan(xydata_Rotation).all():
                        traces.append(go.Scatter(x=xydata_Rotation,        y=xydata_Rotation,        arg=sett,  marker_size=np.where(np.isnan(xydata_Rotation), epsilon, xydata_Rotation)))
                        fig.add_trace(go.Scatter(x=[xydata_Rotation[0]],   y=[xydata_Rotation[1]],   arg=sett), row=2, col=2)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatability", "F1-Score", "Inliers", "Matches", "1k Match Time", "1k Inlier Time"]
    button_listx, button_listy, button_listz = [], [], []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict(label=f"x: {axis}", method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis3.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict(label=f"y: {axis}", method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis3.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listz.append(dict(label=f"z: {axis}", method="update", args=[{"marker.size": [(trace.marker.size[idx]*50) for trace in traces]}]))
    fig.update_layout(updatemenus=[ dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listy, direction="down", x=0,  xanchor="left",  y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listx, direction="up",   x=1,  xanchor="right", y=0, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=3, buttons=button_listz, direction="down", x=0,  xanchor="left",  y=1)])
    fig.write_html(f"./html/synthetic/synthetic4.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic4.html", "a") as f:
        f.write(custom_html)

def oxfordAll9():
    fig = go.Figure()
    fig = make_subplots(rows=3, cols=3, horizontal_spacing=0.05, vertical_spacing=0.08,
                        subplot_titles=["<span style='font-size: 18px;'><b>Graf(Viewpoint)</b></span>", "<span style='font-size: 18px;'><b>Bikes(Blur)</b></span>", "<span style='font-size: 18px;'><b>Boat(Zoom + Rotation)</b></span>", 
                                        "<span style='font-size: 18px;'><b>Leuven(Light)</b></span>", "<span style='font-size: 18px;'><b>Wall(Viewpoint)</b></span>", "<span style='font-size: 18px;'><b>Trees(Blur)</b></span>", 
                                        "<span style='font-size: 18px;'><b>Bark(Zoom + Rotation)</b></span>", "<span style='font-size: 18px;'><b>UBC(JPEG)", "<span style='font-size: 18px;'><b>Overall</b></span>"])
    xvals = ["Img2", "Img3", "Img4", "Img5", "Img6"]
    sett_axis = dict(range=[-0.01, 1.01], autorange=False)
    fig.update_layout(  template="ggplot2", font_size=16, hovermode="closest", margin=dict(l=20, r=20, t=70, b=20),
                        title=dict(text="<span style='font-size: 26px;'><b>Oxford Affine Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis, yaxis5=sett_axis, yaxis6=sett_axis, yaxis7=sett_axis, yaxis8=sett_axis, yaxis9=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_Graf  = np.array([Rate_graf  [:, m, c3, i, j, 13], Rate_graf  [:, m, c3, i, j, 12], Rate_graf  [:, m, c3, i, j, 14], Rate_graf  [:, m, c3, i, j, 15], Rate_graf  [:, m, c3, i, j, 9], Rate_graf  [:, m, c3, i, j, 10], Exec_time_graf  [:, m, c3, i, j, 6], Exec_time_graf  [:, m, c3, i, j, 7]])
                    Rate_Bikes = np.array([Rate_bikes [:, m, c3, i, j, 13], Rate_bikes [:, m, c3, i, j, 12], Rate_bikes [:, m, c3, i, j, 14], Rate_bikes [:, m, c3, i, j, 15], Rate_bikes [:, m, c3, i, j, 9], Rate_bikes [:, m, c3, i, j, 10], Exec_time_bikes [:, m, c3, i, j, 6], Exec_time_bikes [:, m, c3, i, j, 7]])
                    Rate_Boat  = np.array([Rate_boat  [:, m, c3, i, j, 13], Rate_boat  [:, m, c3, i, j, 12], Rate_boat  [:, m, c3, i, j, 14], Rate_boat  [:, m, c3, i, j, 15], Rate_boat  [:, m, c3, i, j, 9], Rate_boat  [:, m, c3, i, j, 10], Exec_time_boat  [:, m, c3, i, j, 6], Exec_time_boat  [:, m, c3, i, j, 7]])
                    Rate_Leuven= np.array([Rate_leuven[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 9], Rate_leuven[:, m, c3, i, j, 10], Exec_time_leuven[:, m, c3, i, j, 6], Exec_time_leuven[:, m, c3, i, j, 7]])
                    Rate_Wall  = np.array([Rate_wall  [:, m, c3, i, j, 13], Rate_wall  [:, m, c3, i, j, 12], Rate_wall  [:, m, c3, i, j, 14], Rate_wall  [:, m, c3, i, j, 15], Rate_wall  [:, m, c3, i, j, 9], Rate_wall  [:, m, c3, i, j, 10], Exec_time_wall  [:, m, c3, i, j, 6], Exec_time_wall  [:, m, c3, i, j, 7]])
                    Rate_Trees = np.array([Rate_trees [:, m, c3, i, j, 13], Rate_trees [:, m, c3, i, j, 12], Rate_trees [:, m, c3, i, j, 14], Rate_trees [:, m, c3, i, j, 15], Rate_trees [:, m, c3, i, j, 9], Rate_trees [:, m, c3, i, j, 10], Exec_time_trees [:, m, c3, i, j, 6], Exec_time_trees [:, m, c3, i, j, 7]])
                    Rate_Bark  = np.array([Rate_bark  [:, m, c3, i, j, 13], Rate_bark  [:, m, c3, i, j, 12], Rate_bark  [:, m, c3, i, j, 14], Rate_bark  [:, m, c3, i, j, 15], Rate_bark  [:, m, c3, i, j, 9], Rate_bark  [:, m, c3, i, j, 10], Exec_time_bark  [:, m, c3, i, j, 6], Exec_time_bark  [:, m, c3, i, j, 7]])
                    Rate_Ubc   = np.array([Rate_ubc   [:, m, c3, i, j, 13], Rate_ubc   [:, m, c3, i, j, 12], Rate_ubc   [:, m, c3, i, j, 14], Rate_ubc   [:, m, c3, i, j, 15], Rate_ubc   [:, m, c3, i, j, 9], Rate_ubc   [:, m, c3, i, j, 10], Exec_time_ubc   [:, m, c3, i, j, 6], Exec_time_ubc   [:, m, c3, i, j, 7]])
                    Overall    = np.nanmean([Rate_Graf, Rate_Bikes, Rate_Boat, Rate_Leuven, Rate_Wall, Rate_Trees, Rate_Bark, Rate_Ubc], axis=0)
                    legend_groupfig = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker=dict(color=colors[color_index], size=16, symbol=marker_symbols[symbol_index]),
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig, legendgroup=legend_groupfig, showlegend=True, hovertemplate="<b>%{y:.3f}</b>")
                    traces.append(go.Scatter(x = xvals, y=Rate_Graf,       arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Rate_Graf[0],    arg=sett), row=1, col=1)
                    traces.append(go.Scatter(x = xvals, y=Rate_Bikes,      arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Rate_Bikes[0],   arg=sett), row=1, col=2)
                    traces.append(go.Scatter(x = xvals, y=Rate_Boat,       arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Rate_Boat[0],    arg=sett), row=1, col=3)
                    traces.append(go.Scatter(x = xvals, y=Rate_Leuven,     arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Rate_Leuven[0],  arg=sett), row=2, col=1)
                    traces.append(go.Scatter(x = xvals, y=Rate_Wall,       arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Rate_Wall[0],    arg=sett), row=2, col=2)
                    traces.append(go.Scatter(x = xvals, y=Rate_Trees,      arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Rate_Trees[0],   arg=sett), row=2, col=3)
                    traces.append(go.Scatter(x = xvals, y=Rate_Bark,       arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Rate_Bark[0],    arg=sett), row=3, col=1)
                    traces.append(go.Scatter(x = xvals, y=Rate_Ubc,        arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Rate_Ubc[0],     arg=sett), row=3, col=2)
                    traces.append(go.Scatter(x = xvals, y=Overall,         arg=sett))
                    fig.add_trace(go.Scatter(x = xvals, y=Overall[0],      arg=sett), row=3, col=3)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeatability", "F1-Score", "Inliers", "Matches", "1k Match Time", "1k Inlier Time"]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=f"y: {y}", method="update", 
                                args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis4.title": f"<span style='font-size: 22px;'><b>{y}</b></span>"}]))
    fig.update_layout(updatemenus=[ dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1, yanchor="bottom")]) 
    fig.write_html(f"./html/oxford/oxfordAll9.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxfordAll9.html", "a") as f:
        f.write(custom_html)

def oxford9():
    fig = go.Figure()
    fig = make_subplots(rows=3, cols=3,subplot_titles=["<span style='font-size: 20px;'><b>Graf(Viewpoint)</b></span>", "<span style='font-size: 20px;'><b>Bikes(Blur)</b></span>", "<span style='font-size: 20px;'><b>Boat(Zoom + Rotation)</b></span>", 
                                                        "<span style='font-size: 20px;'><b>Leuven(Light)</b></span>", "<span style='font-size: 20px;'><b>Wall(Viewpoint)</b></span>", "<span style='font-size: 20px;'><b>Trees(Blur)</b></span>", 
                                                        "<span style='font-size: 20px;'><b>Bark(Zoom + Rotation)</b></span>","<span style='font-size: 20px;'><b>UBC(JPEG)</b></span>", "<span style='font-size: 20px;'><b>Overall</b></span>"], horizontal_spacing=0.05, vertical_spacing=0.08)
    sett_axis = dict(range=[-0.01, 1.01], autorange=False)
    fig.update_layout(  template="ggplot2", font_size=16, hovermode="closest", margin=dict(l=20, r=20, t=70, b=20),
                        title=dict(text="<span style='font-size: 26px;'><b>Oxford Affine Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"),
                        xaxis=sett_axis, xaxis2=sett_axis, xaxis3=sett_axis, xaxis4=sett_axis, xaxis5=sett_axis, xaxis6=sett_axis, xaxis7=sett_axis, xaxis8=sett_axis, xaxis9=sett_axis,
                        yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis, yaxis5=sett_axis, yaxis6=sett_axis, yaxis7=sett_axis, yaxis8=sett_axis, yaxis9=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    xydata_Graf = np.array([
                        np.nanmean(Rate_graf[:, m, c3, i, j, 13]),
                        np.nanmean(Rate_graf[:, m, c3, i, j, 12]),
                        np.nanmean(Rate_graf[:, m, c3, i, j, 14]),
                        np.nanmean(Rate_graf[:, m, c3, i, j, 15]),
                        nonlinear_normalize(np.nanmean(Rate_graf[:, m, c3, i, j, 9]), Rate_graf[:, :, :, :, :, 9], alpha=0.2),
                        nonlinear_normalize(np.nanmean(Rate_graf[:, m, c3, i, j, 10]), Rate_graf[:, :, :, :, :, 10], alpha=0.3),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_graf[:, m, c3, i, j, 6]), Exec_time_graf[:, :, :, :, :, 6], alpha=0.2),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_graf[:, m, c3, i, j, 7]), Exec_time_graf[:, :, :, :, :, 7], alpha=0.2)
                    ])
                    xydata_Bikes = np.array([
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_bikes[:, m, c3, i, j, 15]),
                        nonlinear_normalize(np.nanmean(Rate_bikes[:, m, c3, i, j, 9]), Rate_bikes[:, :, :, :, :, 9], alpha=0.2),
                        nonlinear_normalize(np.nanmean(Rate_bikes[:, m, c3, i, j, 10]), Rate_bikes[:, :, :, :, :, 10], alpha=0.3),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_bikes[:, m, c3, i, j, 6]), Exec_time_bikes[:, :, :, :, :, 6], alpha=0.2),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_bikes[:, m, c3, i, j, 7]), Exec_time_bikes[:, :, :, :, :, 7], alpha=0.2)
                    ])
                    xydata_Boat = np.array([
                        np.nanmean(Rate_boat[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_boat[:, m, c3, i, j, 15]), 
                        nonlinear_normalize(np.nanmean(Rate_boat[:, m, c3, i, j, 9]), Rate_boat[:, :, :, :, :, 9], alpha=0.2),
                        nonlinear_normalize(np.nanmean(Rate_boat[:, m, c3, i, j, 10]), Rate_boat[:, :, :, :, :, 10], alpha=0.3),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_boat[:, m, c3, i, j, 6]), Exec_time_boat[:, :, :, :, :, 6], alpha=0.2),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_boat[:, m, c3, i, j, 7]), Exec_time_boat[:, :, :, :, :, 7], alpha=0.2)
                    ])
                    xydata_Leuven = np.array([
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_leuven[:, m, c3, i, j, 15]), 
                        nonlinear_normalize(np.nanmean(Rate_leuven[:, m, c3, i, j, 9]), Rate_leuven[:, :, :, :, :, 9], alpha=0.2),
                        nonlinear_normalize(np.nanmean(Rate_leuven[:, m, c3, i, j, 10]), Rate_leuven[:, :, :, :, :, 10], alpha=0.3),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_leuven[:, m, c3, i, j, 6]), Exec_time_leuven[:, :, :, :, :, 6], alpha=0.2),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_leuven[:, m, c3, i, j, 7]), Exec_time_leuven[:, :, :, :, :, 7], alpha=0.2)
                    ])
                    xydata_Wall = np.array([
                        np.nanmean(Rate_wall[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_wall[:, m, c3, i, j, 15]),
                        nonlinear_normalize(np.nanmean(Rate_wall[:, m, c3, i, j, 9]), Rate_wall[:, :, :, :, :, 9], alpha=0.2),
                        nonlinear_normalize(np.nanmean(Rate_wall[:, m, c3, i, j, 10]), Rate_wall[:, :, :, :, :, 10], alpha=0.3),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_wall[:, m, c3, i, j, 6]), Exec_time_wall[:, :, :, :, :, 6], alpha=0.2),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_wall[:, m, c3, i, j, 7]), Exec_time_wall[:, :, :, :, :, 7], alpha=0.2)
                    ])
                    xydata_Trees = np.array([
                        np.nanmean(Rate_trees[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_trees[:, m, c3, i, j, 15]), 
                        nonlinear_normalize(np.nanmean(Rate_trees[:, m, c3, i, j, 9]), Rate_trees[:, :, :, :, :, 9], alpha=0.2),
                        nonlinear_normalize(np.nanmean(Rate_trees[:, m, c3, i, j, 10]), Rate_trees[:, :, :, :, :, 10], alpha=0.3),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_trees[:, m, c3, i, j, 6]), Exec_time_trees[:, :, :, :, :, 6], alpha=0.2),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_trees[:, m, c3, i, j, 7]), Exec_time_trees[:, :, :, :, :, 7], alpha=0.2)
                    ])
                    xydata_Bark = np.array([
                        np.nanmean(Rate_bark[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_bark[:, m, c3, i, j, 15]), 
                        nonlinear_normalize(np.nanmean(Rate_bark[:, m, c3, i, j, 9]), Rate_bark[:, :, :, :, :, 9], alpha=0.2),
                        nonlinear_normalize(np.nanmean(Rate_bark[:, m, c3, i, j, 10]), Rate_bark[:, :, :, :, :, 10], alpha=0.3),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_bark[:, m, c3, i, j, 6]), Exec_time_bark[:, :, :, :, :, 6], alpha=0.2),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_bark[:, m, c3, i, j, 7]), Exec_time_bark[:, :, :, :, :, 7], alpha=0.2)
                    ])
                    xydata_Ubc = np.array([
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 13]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 12]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 14]), 
                        np.nanmean(Rate_ubc[:, m, c3, i, j, 15]), 
                        nonlinear_normalize(np.nanmean(Rate_ubc[:, m, c3, i, j, 9]), Rate_ubc[:, :, :, :, :, 9], alpha=0.2),
                        nonlinear_normalize(np.nanmean(Rate_ubc[:, m, c3, i, j, 10]), Rate_ubc[:, :, :, :, :, 10], alpha=0.3),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_ubc[:, m, c3, i, j, 6]), Exec_time_ubc[:, :, :, :, :, 6], alpha=0.2),
                        1 - nonlinear_normalize(np.nanmean(Exec_time_ubc[:, m, c3, i, j, 7]), Exec_time_ubc[:, :, :, :, :, 7], alpha=0.2)
                    ])
                    Overall = np.nanmean([xydata_Graf, xydata_Bikes, xydata_Boat, xydata_Leuven, xydata_Wall, xydata_Trees, xydata_Bark, xydata_Ubc], axis=0)
                    legend_groupfig = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers", marker=dict(symbol=marker_symbols[symbol_index], size=16, color=colors[color_index]),
                                name=legend_groupfig, legendgroup=legend_groupfig, showlegend=True,
                                hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>")
                    if not np.isnan(xydata_Graf).all():
                        traces.append(go.Scatter(x=xydata_Graf,        y=xydata_Graf,       arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Graf[0]],   y=[xydata_Graf[1]],  arg=sett), row=1, col=1)
                    if not np.isnan(xydata_Bikes).all():
                        traces.append(go.Scatter(x=xydata_Bikes,       y=xydata_Bikes,      arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Bikes[0]],  y=[xydata_Bikes[1]], arg=sett), row=1, col=2)
                    if not np.isnan(xydata_Boat).all():
                        traces.append(go.Scatter(x=xydata_Boat,        y=xydata_Boat,       arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Boat[0]],   y=[xydata_Boat[1]],  arg=sett), row=1, col=3)
                    if not np.isnan(xydata_Leuven).all():
                        traces.append(go.Scatter(x=xydata_Leuven,      y=xydata_Leuven,     arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Leuven[0]], y=[xydata_Leuven[1]],arg=sett), row=2, col=1)
                    if not np.isnan(xydata_Wall).all():
                        traces.append(go.Scatter(x=xydata_Wall,        y=xydata_Wall,       arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Wall[0]],   y=[xydata_Wall[1]],  arg=sett), row=2, col=2)
                    if not np.isnan(xydata_Trees).all():
                        traces.append(go.Scatter(x=xydata_Trees,       y=xydata_Trees,      arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Trees[0]],  y=[xydata_Trees[1]], arg=sett), row=2, col=3)
                    if not np.isnan(xydata_Bark).all():
                        traces.append(go.Scatter(x=xydata_Bark,        y=xydata_Bark,       arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Bark[0]],   y=[xydata_Bark[1]],  arg=sett), row=3, col=1)
                    if not np.isnan(xydata_Ubc).all():
                        traces.append(go.Scatter(x=xydata_Ubc,         y=xydata_Ubc,        arg=sett))
                        fig.add_trace(go.Scatter(x=[xydata_Ubc[0]],    y=[xydata_Ubc[1]],   arg=sett), row=3, col=2)
                    if not np.isnan(Overall).all():
                        traces.append(go.Scatter(x=Overall,            y=Overall,           arg=sett))
                        fig.add_trace(go.Scatter(x=[Overall[0]],       y=[Overall[1]],      arg=sett), row=3, col=3)
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatability", "F1-Score", "Inliers", "Matches", "1k Match Time", "1k Inlier Time"]
    button_listx, button_listy = [], []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict(label=f"x: {axis}", method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis8.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict(label=f"y: {axis}", method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis4.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig.update_layout(updatemenus=[ dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listy, direction="down", x=0,  xanchor="left",  y=1, yanchor="top"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listx, direction="up",   x=1,  xanchor="right", y=0, yanchor="bottom")])
    fig.write_html(f"./html/oxford/oxford9.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford9.html", "a") as f:
        f.write(custom_html)

def singleAll(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig = go.Figure()
    xvals = [f"Img{i}" for i in range(153, 188)] if data == "drone" else (
        ["Bahamas", "Office", "Suburban", "Building", "Construction", "Dominica", "Cadastre", "Rivaz", "Urban", "Belleview"] if data == "uav" else 
        [f"Img{i}" for i in range(653, 774, 5)])
    fig.update_layout(  template="ggplot2", font_size=16, hovermode="closest", margin=dict(l=20, r=20, t=50, b=20), yaxis=dict(range=[-0.01, 1.01], autorange=False),
                        title=dict(text=f"<span style='font-size: 26px;'><b>{data.capitalize()} Data</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    y_data = np.array([
                        Rate[:, m, c3, i, j, 13],       # Precision
                        Rate[:, m, c3, i, j, 12],       # Recall
                        Rate[:, m, c3, i, j, 14],       # Repeatibility
                        Rate[:, m, c3, i, j, 15],       # F1 Score
                        Rate[:, m, c3, i, j,  9],       # Inliers
                        Rate[:, m, c3, i, j, 10],       # Matches
                        Exec_time[:, m, c3, i, j, 6],   # 1K Total Time
                        Exec_time[:, m, c3, i, j, 7]    # 1K feature Inlier Time
                    ])
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
    dropdown_yaxis = ["Precision", "Recall", "Repeatability", "F1-Score", "Inliers", "Matches", "1k Match Time", "1k Inlier Time"]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=f"y: {y}", method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{y}</b></span>"}]))
    
    fig.update_layout(updatemenus=[ dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1, yanchor="bottom")]) 
    fig.write_html(f"./html/{data}/{data}All.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}All.html", "a") as f:
        f.write(custom_html)

def single(data="drone"):
    if data == "synthetic":
        Rate = np.concatenate((Rate_intensity, Rate_scale, Rate_rot), axis=0)
        Exec_time = np.concatenate((Exec_time_intensity, Exec_time_scale, Exec_time_rot), axis=0)
    elif data == "oxford":
        Rate = np.concatenate((Rate_graf, Rate_bikes, Rate_boat, Rate_leuven, Rate_wall, Rate_trees, Rate_bark, Rate_ubc), axis=0)
        Exec_time = np.concatenate((Exec_time_graf, Exec_time_bikes, Exec_time_boat, Exec_time_leuven, Exec_time_wall, Exec_time_trees, Exec_time_bark, Exec_time_ubc), axis=0)
    else:
        Rate = np.load(f"./arrays/Rate_{data}.npy")
        Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    fig = go.Figure()
    fig.update_layout(template="ggplot2", font_size=16, title=dict(text=f"<span style='font-size: 26px;'><b>{data.capitalize()} Dataset</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"),
                        hovermode="closest", margin=dict(l=20, r=20, t=70, b=20), xaxis=dict(range=[-0.01, 1.01], autorange=False), yaxis=dict(range=[-0.01, 1.01], autorange=False))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    xydata = np.array([
                        np.nanmean(Rate[:, m, c3, i, j, 13]),       # Precision
                        np.nanmean(Rate[:, m, c3, i, j, 12]),       # Recall
                        np.nanmean(Rate[:, m, c3, i, j, 14]),       # Repeatibility
                        np.nanmean(Rate[:, m, c3, i, j, 15]),       # F1 Score
                        nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j,  9]), Rate[:, :, :, :, :,  9], alpha=0.3),             # Inliers
                        nonlinear_normalize(np.nanmean(Rate[:, m, c3, i, j, 10]), Rate[:, :, :, :, :, 10], alpha=0.3),             # Matches
                        1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 6]), Exec_time[:, :, :, :, :, 6], alpha=0.2), # 1K Total Time
                        1 - nonlinear_normalize(np.nanmean(Exec_time[:, m, c3, i, j, 7]), Exec_time[:, :, :, :, :, 7], alpha=0.2), # 1K Inlier Time
                    ])
                    if data == "drone":
                        xydata = np.append(xydata, 1 - nonlinear_normalize(np.nanmean(Rate      [:, m, c3, i, j, 11]), Rate      [:, :, :, :, :, 11], alpha=0.4)) # Reprojection Error
                        xydata = np.append(xydata,     nonlinear_normalize(np.nanmean(Rate      [:, m, c3, i, j, 16]), Rate      [:, :, :, :, :, 16], alpha=0.2)) # 3D Points Count
                        xydata = np.append(xydata, 1 - nonlinear_normalize(np.nanmean(Exec_time [:, m, c3, i, j,  8]), Exec_time [:, :, :, :, :,  8], alpha=0.2)) # 3D Point Reconstruction Time
                        # xydata = np.append(xydata, 1 - nonlinear_normalize((np.nanmean(Exec_time[:, m, c3, i, j, 8]) / np.nanmean(Rate[:, m, c3, i, j, 16]) * 1000), (Exec_time[:, :, :, :, :, 8] / Rate[:, :, :, :, :, 16] * 1000).flatten(), alpha=0.2)) # 1K 3D Point Reconstruction Time
                    if not (np.isnan(xydata).any() or np.any(xydata == 0)):
                        traces.append(  go.Scatter( x=xydata,       y=xydata,       mode="markers", 
                                                    marker=dict(color=colors[color_index], size=xydata, symbol=marker_symbols[symbol_index]),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                        fig.add_trace(go.Scatter( x=[xydata[0]],  y=[xydata[1]],  mode="markers", 
                                                    marker=dict(color=colors[color_index], size=[xydata[3]*50], symbol=marker_symbols[symbol_index]),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatability", "F1-Score", "Inliers", "Matches", "1k Match Time", "1k Inlier Time"] + (["Reprojection Error", "3D Points", "Reconstruction Time"] if data == "drone" else [])
    button_listx, button_listy, button_listz = [], [], []
    for idx, axis in enumerate(dropdown_axis):
        button_listx.append(dict(label=f"x: {axis}", method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}, {"xaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listy.append(dict(label=f"y: {axis}", method="update", args=[{"y": [[trace.y[idx]] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
        button_listz.append(dict(label=f"z: {axis}", method="update", args=[{"marker.size": [(trace.marker.size[idx]*50) for trace in traces]}]))
    fig.update_layout(updatemenus=[ dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=1, buttons=button_listy, direction="down", x=0,  xanchor="left",  y=1, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=0, buttons=button_listx, direction="up",   x=1,  xanchor="right", y=0, yanchor="bottom"),
                                    dict(type="dropdown", showactive=True, active=3, buttons=button_listz, direction="down", x=0,  xanchor="left",  y=1)])
    fig.write_html(f"./html/{data}/{data}.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}.html", "a") as f:
        f.write(custom_html)

def timing(data="drone", mobile=""):
    if data == "synthetic":
        Exec_time = np.concatenate((Exec_time_intensity, Exec_time_scale, Exec_time_rot), axis=0)
        if mobile:
            Exec_time_mobile = np.concatenate((Exec_time_intensity_mobile, Exec_time_scale_mobile, Exec_time_rot_mobile), axis=0)
        if mobile == "_mobile2":
            Exec_time_mobile2 = np.concatenate((Exec_time_intensity_mobile2, Exec_time_scale_mobile2, Exec_time_rot_mobile2), axis=0)
    elif data == "oxford":
        Exec_time = np.concatenate((Exec_time_graf, Exec_time_bikes, Exec_time_boat, Exec_time_leuven, Exec_time_wall, Exec_time_trees, Exec_time_bark, Exec_time_ubc), axis=0)
        if mobile:
            Exec_time_mobile = np.concatenate((Exec_time_graf_mobile, Exec_time_bikes_mobile, Exec_time_boat_mobile, Exec_time_leuven_mobile, Exec_time_wall_mobile, Exec_time_trees_mobile, Exec_time_bark_mobile, Exec_time_ubc_mobile), axis=0)
        if mobile == "_mobile2":
            Exec_time_mobile2 = np.concatenate((Exec_time_graf_mobile2, Exec_time_bikes_mobile2, Exec_time_boat_mobile2, Exec_time_leuven_mobile2, Exec_time_wall_mobile2, Exec_time_trees_mobile2, Exec_time_bark_mobile2, Exec_time_ubc_mobile2), axis=0)
    else:
        Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    fig = go.Figure()
    fig = make_subplots(rows=7 if mobile else 5, cols=1, subplot_titles=["<span style='font-size: 22px;'>Total time <b>BF</b> - Total time <b>Flann</b> (Detector level)</span>",
                                                        "<span style='font-size: 22px;'>Total time <b>BF</b> - Total time <b>Flann</b> (Descriptor level)</span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>BF</b> - Inlier time <b>Flann</b> (Detector level)</span>",
                                                        "<span style='font-size: 22px;'>Inlier time <b>BF</b> - Inlier time <b>Flann</b> (Descriptor level)</span>",
                                                        "<span style='font-size: 22px;'>All Timings</span>",
                                                        "<span style='font-size: 22px;'>Deltas Detector Level</span>",
                                                        "<span style='font-size: 22px;'>Deltas Descriptor Level</span>"], vertical_spacing=0.075)
    fig.update_layout(  template="ggplot2", font_size=16, margin=dict(l=20, r=20, t=75, b=20), hovermode="x unified", height=3700 if mobile else 2900,
                        title=dict( text=f"<span style='font-size: 26px;'><b>{data.capitalize()} Dataset Timings for Average 1k</b></span>",
                                    x=0.5, xanchor="center", yanchor="bottom", xref="paper", yref="paper"))
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(Exec_time[:, m, :, i, j, 6])
                result4 = np.nanmean(Exec_time[:, m, :, i, j, 7])
                if mobile:
                    result3m1= np.nanmean(Exec_time_mobile [:, m, :, i, j, 6])
                    result4m1= np.nanmean(Exec_time_mobile [:, m, :, i, j, 7])
                if mobile == "_mobile2":
                    result3m2= np.nanmean(Exec_time_mobile2[:, m, :, i, j, 6])
                    result4m2= np.nanmean(Exec_time_mobile2[:, m, :, i, j, 7])
                # * 1K Total Time
                if not np.isnan(result3):
                    fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]]], y=[result3],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-pc",
                                            text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=1, col=1)
                    fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]]], y=[result3],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-pc",
                                            text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=2, col=1)
                    fig.add_trace(go.Bar(   x=['.'+DetectorsLegend[i]+'-'+DescriptorsLegend[j] + '-' + Matcher[m] + '-tot.-p'], y=[result3],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-pc",
                                            text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=5, col=1)
                # * Inlier Time
                if not np.isnan(result4):
                    fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]]], y=[result4],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-pc",
                                            text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=3, col=1)
                    fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]]], y=[result4],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-pc",
                                            text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=4, col=1)
                    fig.add_trace(go.Bar(   x=['.'+DetectorsLegend[i]+'-'+DescriptorsLegend[j] + '-' + Matcher[m] + '-inl.-p'], y=[result4],
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-pc",
                                            text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                            showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=5, col=1)
                if mobile:
                    # * 1K Total Time
                    if not np.isnan(result3m1):
                        fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]+'-m1']], y=[result3m1],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m1",
                                                text=[f"{result3m1:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=1, col=1)
                        fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]+'-m1']], y=[result3m1],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m1",
                                                text=[f"{result3m1:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=2, col=1)
                        fig.add_trace(go.Bar(   x=['.'+DetectorsLegend[i]+'-'+DescriptorsLegend[j] + '-' + Matcher[m] + '-tot.-m1'], y=[result3m1],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m1",
                                                text=[f"{result3m1:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=5, col=1 )
                    # * Inlier Time
                    if not np.isnan(result4m1):
                        fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]+'-m1']], y=[result4m1],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m1",
                                                text=[f"{result4m1:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=3, col=1)
                        fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]+'-m1']], y=[result4m1],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m1",
                                                text=[f"{result4m1:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=4, col=1)
                        fig.add_trace(go.Bar(   x=['.'+DetectorsLegend[i]+'-'+DescriptorsLegend[j] + '-' + Matcher[m] + '-inl.-m1'], y=[result4m1],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m1",
                                                text=[f"{result4m1:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=5, col=1 )
                    result3m1diff = result3m1 - result3
                    result4m1diff = result4m1 - result4
                    if not np.isnan(result3m1diff):
                        fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]+'-total-m1']], y=[result3m1diff],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m1",
                                                text=[f"{result3m1diff:.3f}"], marker_color=colors[color_index % len(colors)],
                                                legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                showlegend=True, hovertemplate="<b>%{y:.3f}</b>"), row=6, col=1)
                        fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]+'-total-m1']], y=[result3m1diff],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m1",
                                                text=[f"{result3m1diff:.3f}"], marker_color=colors[color_index % len(colors)],
                                                legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                showlegend=True, hovertemplate="<b>%{y:.3f}</b>"), row=7, col=1)
                    if not np.isnan(result4m1diff):
                        fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]+'-inlier-m1']], y=[result4m1diff],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m1",
                                                text=[f"{result4m1diff:.3f}"], marker_color=colors[color_index % len(colors)],
                                                legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                showlegend=True,hovertemplate="<b>%{y:.3f}</b>"), row=6, col=1)
                        fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]+'-inlier-m1']], y=[result4m1diff],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m1",
                                                text=[f"{result4m1diff:.3f}"], marker_color=colors[color_index % len(colors)],
                                                legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                showlegend=True, hovertemplate="<b>%{y:.3f}</b>"), row=7, col=1)
                if mobile == "_mobile2":
                    # * 1K Total Time
                    if not np.isnan(result3m2):
                        fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]+'-m2']], y=[result3m2],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m2",
                                                text=[f"{result3m2:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=1, col=1)
                        fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]+'-m2']], y=[result3m2],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m2",
                                                text=[f"{result3m2:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=2, col=1)
                        fig.add_trace(go.Bar(   x=['.'+DetectorsLegend[i]+'-'+DescriptorsLegend[j] + '-' + Matcher[m] + '-tot.-m2'], y=[result3m2],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m2",
                                                text=[f"{result3m2:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=5, col=1 )
                    # * Inlier Time
                    if not np.isnan(result4m2):
                        fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]+'-m2']], y=[result4m2],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m2",
                                                text=[f"{result4m2:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=3, col=1)
                        fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]+'-m2']], y=[result4m2],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m2",
                                                text=[f"{result4m2:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=4, col=1)
                        fig.add_trace(go.Bar(   x=['.'+DetectorsLegend[i]+'-'+DescriptorsLegend[j] + '-' + Matcher[m] + '-inl.-m2'], y=[result4m2],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m2",
                                                text=[f"{result4m2:.3f}"], marker_color=colors[color_index],
                                                showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>"), row=5, col=1 )
                    # * Mobile Difference
                    result3m2diff = result3m2 - result3
                    result4m2diff = result4m2 - result4
                    if not np.isnan(result3m2diff):
                        fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]+'-total-m2']], y=[result3m2diff],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m2",
                                                text=[f"{result3m2diff:.3f}"], marker_color=colors[color_index % len(colors)],
                                                legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                showlegend=True, hovertemplate="<b>%{y:.3f}</b>"), row=6, col=1)
                        fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]+'-total-m2']], y=[result3m2diff],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m2",
                                                text=[f"{result3m2diff:.3f}"], marker_color=colors[color_index % len(colors)],
                                                legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                showlegend=True, hovertemplate="<b>%{y:.3f}</b>"), row=7, col=1)
                    if not np.isnan(result4m2diff):
                        fig.add_trace(go.Bar(   x=[['-'+DescriptorsLegend[j]], ['.'+DetectorsLegend[i]+'-'+Matcher[m]+'-inlier-m2']], y=[result4m2diff],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m2",
                                                text=[f"{result4m2diff:.3f}"], marker_color=colors[color_index % len(colors)],
                                                legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                showlegend=True, hovertemplate="<b>%{y:.3f}</b>"), row=6, col=1)
                        fig.add_trace(go.Bar(   x=[['.'+DetectorsLegend[i]], ['-'+DescriptorsLegend[j]+'-'+Matcher[m]+'-inlier-m2']], y=[result4m2diff],
                                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-m2",
                                                text=[f"{result4m2diff:.3f}"], marker_color=colors[color_index % len(colors)],
                                                legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                showlegend=True, hovertemplate="<b>%{y:.3f}</b>"), row=7, col=1)
            color_index = (color_index + 14) % num_combinations
    for i in range(1, 8):
        fig.update_xaxes(tickangle=90, row=i, col=1)
    args_linear = {"yaxis.type": "linear",  "yaxis2.type": "linear",    "yaxis3.type": "linear",    "yaxis4.type": "linear",    "yaxis5.type": "linear"}
    args_log    = {"yaxis.type": "log",     "yaxis2.type": "log",       "yaxis3.type": "log",       "yaxis4.type": "log",       "yaxis5.type": "log"}
    
    if mobile:
        args_linear.update( {"yaxis6.type": "linear",   "yaxis7.type": "linear"})
        args_log.update(    {"yaxis6.type": "log",      "yaxis7.type": "log"})
    
    fig.update_layout(updatemenus=[ dict(   type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                    dict(   type="dropdown", x=0, xanchor="left", y=1, yanchor="bottom",
                                            buttons=[   dict(label="Linear", method="relayout", args=[args_linear]),
                                                        dict(label="Log", method="relayout", args=[args_log])])])
    fig.write_html(f"./html/{data}/{data}Timing{mobile}.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}Timing{mobile}.html", "a") as f:
        f.write(custom_html)

def efficiencyAndHeatmap(data="drone"):
    if data == "synthetic":
        Exec_time = np.concatenate((Exec_time_intensity, Exec_time_scale, Exec_time_rot), axis=0)
        Rate = np.concatenate((Rate_intensity, Rate_scale, Rate_rot), axis=0)
    elif data == "oxford":
        Exec_time = np.concatenate((Exec_time_graf, Exec_time_wall, Exec_time_trees, Exec_time_bikes, Exec_time_bark, Exec_time_boat, Exec_time_leuven, Exec_time_ubc), axis=0)
        Rate = np.concatenate((Rate_graf, Rate_wall, Rate_trees, Rate_bikes, Rate_bark, Rate_boat, Rate_leuven, Rate_ubc), axis=0)
    else:
        Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
        Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig = go.Figure()
    fig_heatmap = make_subplots(rows=2, cols=2, horizontal_spacing=0.1, vertical_spacing=0.17,
                                subplot_titles=[f"<span style='font-size: 22px;'>L2-BruteForce</span>",
                                                "<span style='font-size: 22px;'>L2-Flann</span>",
                                                "<span style='font-size: 22px;'>Hamming-BruteForce</span>",
                                                "<span style='font-size: 22px;'>Hamming-Flann</span>"])
    fig.update_layout(  template="ggplot2", font_size=16, margin=dict(l=20, r=20, t=70, b=20),
                        title=dict(text=f"<span style='font-size: 26px;'><b>{data.capitalize()} Efficiency</b></span>", x=0.5, xanchor="center", yanchor="middle", xref="paper", yref="paper"), 
                        xaxis_tickangle=90, yaxis=dict(range=[-0.01, 1.01], autorange=False))
    
    def collect_metrics():
        metrics_data = []
        combinations = []
        for i in range(len(DetectorsLegend)):
            for j in range(len(DescriptorsLegend)):
                for c3 in range(2):  # Normalization
                    for m in range(2):  # Matcher
                        metrics_row = [
                            np.nanmean(Exec_time[:, m, c3, i, j, 6]),  # 1K Total Time
                            np.nanmean(Exec_time[:, m, c3, i, j, 7]),  # 1K Inlier Time
                            np.nanmean(Rate[:, m, c3, i, j, 9]),       # Inliers
                            np.nanmean(Rate[:, m, c3, i, j, 10]),      # Matches
                            np.nanmean(Rate[:, m, c3, i, j, 12]),      # Recall
                            np.nanmean(Rate[:, m, c3, i, j, 13]),      # Precision
                            np.nanmean(Rate[:, m, c3, i, j, 14]),      # Repeatability
                            np.nanmean(Rate[:, m, c3, i, j, 15])       # F1 Score
                        ]
                        if data == "drone":
                            metrics_row.extend([
                                np.nanmean(Rate[:, m, c3, i, j, 11]),      # Reprojection Error
                                np.nanmean(Rate[:, m, c3, i, j, 16]),      # 3D Points
                                np.nanmean(Exec_time[:, m, c3, i, j, 8])   # Reconstruction Time
                            ])
                        if not np.any(np.isnan(metrics_row)):
                            metrics_data.append(metrics_row)
                            combinations.append((i, j, c3, m))
        return np.array(metrics_data), combinations
    
    metrics_data, combinations = collect_metrics()
    
    def normalize_metrics(metrics_data):
        normalized = np.zeros_like(metrics_data)
        normalized[:, 0] = 1 -  nonlinear_normalize(metrics_data[:, 0], metrics_data[:, 0], alpha=0.2)  # 1K Total Time (inverse)
        normalized[:, 1] = 1 -  nonlinear_normalize(metrics_data[:, 1], metrics_data[:, 1], alpha=0.2)  # 1K Inlier Time (inverse)
        normalized[:, 2] =      nonlinear_normalize(metrics_data[:, 2], metrics_data[:, 2], alpha=0.3)  # Inliers
        normalized[:, 3] =      nonlinear_normalize(metrics_data[:, 3], metrics_data[:, 3], alpha=0.3)  # Matches
        normalized[:, 4] =      nonlinear_normalize(metrics_data[:, 4], metrics_data[:, 4], alpha=0.2)  # Recall
        normalized[:, 5] =      nonlinear_normalize(metrics_data[:, 5], metrics_data[:, 5], alpha=0.2)  # Precision
        normalized[:, 6] =      nonlinear_normalize(metrics_data[:, 6], metrics_data[:, 6], alpha=0.2)  # Repeatability
        normalized[:, 7] =      nonlinear_normalize(metrics_data[:, 7], metrics_data[:, 7], alpha=0.2)  # F1 Score
        if data == "drone":
            normalized[:, 8] = 1 - nonlinear_normalize(metrics_data[:, 8], metrics_data[:, 8], alpha=0.4)  # Reprojection Error (inverse)
            normalized[:, 9] =     nonlinear_normalize(metrics_data[:, 9], metrics_data[:, 9], alpha=0.2)  # 3D Points
            normalized[:,10] = 1 - nonlinear_normalize(metrics_data[:,10], metrics_data[:,10], alpha=0.2)  # Reconstruction Time (inverse)
        return normalized
    
    normalized_metrics = normalize_metrics(metrics_data)

    def calculate_composite_scores(data_norm):
        # Handle NaN values by masking them out
        mask = np.isfinite(data_norm).all(axis=1)
        data_norm = data_norm[mask]
        
        # 1. Entropy weights
        p = data_norm / (np.sum(data_norm, axis=0))
        p = np.where(p == 0, 1e-10, p)
        entropy = -np.sum(p * np.log(p), axis=0) / np.log(data_norm.shape[0])
        w_entropy = (1 - entropy) / np.sum(1 - entropy)
        
        # 2. PCA weights
        pca = PCA()
        pca.fit(data_norm)
        loadings = pca.components_
        explained_var = pca.explained_variance_ratio_
        weighted_loadings = np.zeros(data_norm.shape[1])
        for i in range(len(explained_var)):
            weighted_loadings += explained_var[i] * np.abs(loadings[i, :])
        w_pca = weighted_loadings / np.sum(weighted_loadings)
        
        # 3. CRITIC weights
        corr_matrix = np.corrcoef(data_norm.T)
        np.fill_diagonal(corr_matrix, 0)
        std_dev = np.std(data_norm, axis=0)
        conflict = np.sum(1 - np.abs(corr_matrix), axis=1)
        w_critic = std_dev * conflict
        w_critic = w_critic / np.sum(w_critic)
        
        # 4. Simple variance weighting
        w_variance = np.var(data_norm, axis=0)
        w_variance = w_variance / np.sum(w_variance)
        
        weight_matrix = np.array([w_entropy, w_critic, w_variance])
        weight_dispersion = np.std(weight_matrix, axis=0) / np.mean(weight_matrix, axis=0)
        
        # Combine weights and calculate scores
        weights = (w_entropy + w_pca + w_critic + w_variance) / 4
        
        # Print weights in table format
        metrics = ["1k Total", "1k Inlier", "Inliers", "Matches", "Recall", "Precision", "Repeatability", "F1 Score"]
        if data == "drone":
            metrics.extend(["Reproj Error", "3D Points", "Reconst Time"])
        print(f"\n{data.capitalize()} Dataset Weights")
        print("=" * 75)
        print(f"{'Metric':<15} {'Entropy':<8} {'PCA':<8} {'CRITIC':<8} {'Variance':<10} {'Dispersion':<10} {'Combined':<8}")
        print("-" * 75)
        for i, metric in enumerate(metrics):
            print(f"{metric:<15} {w_entropy[i]:<8.3f} {w_pca[i]:<8.3f} {w_critic[i]:<8.3f} {w_variance[i]:<10.3f} {weight_dispersion[i]:<10.3f} {weights[i]:<8.3f}")
        print("-" * 75)
        return np.sum(data_norm * weights, axis=1)

    composite_scores = calculate_composite_scores(normalized_metrics)
    scores = np.full((len(DetectorsLegend), len(DescriptorsLegend), 2, 2), np.nan)
    for idx, (i, j, c3, m) in enumerate(combinations):
        if idx < len(composite_scores):
            scores[i, j, c3, m] = composite_scores[idx]
        
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    if not np.isnan(scores[i, j, c3, m]):
                        fig.add_trace(go.Scatter(
                            x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], 
                            y=[scores[i, j, c3, m]], 
                            text=f"{DetectorsLegend[i]}-{DescriptorsLegend[j]}<br>{Norm[c3]}-{Matcher[m]}",
                            textposition='top center',
                            textfont=dict(size=11),
                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}", 
                            mode="markers+text",
                            marker=dict(color=colors[color_index], size=20, symbol=marker_symbols[symbol_index]), 
                            showlegend=True,
                            legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", 
                            hovertemplate="<b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    fig.update_layout(updatemenus=[
        dict(type="buttons",  buttons=[ dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
        dict(type="dropdown", buttons=[ dict(label="Linear",          method="relayout", args=[{"yaxis.type": "linear"}]),
                                        dict(label="Log",             method="relayout", args=[{"yaxis.type": "log"}])], x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html(f"./html/{data}/{data}_Efficiency.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}_Efficiency.html", "a") as f:
        f.write(custom_html)
    for c3 in range(2):
        for m in range(2):
            fig_heatmap.add_trace(go.Heatmap(z=scores[:, :, c3, m], x=DescriptorsLegend, y=DetectorsLegend, colorscale="matter", hovertemplate='Detector: %{y}<br>Descriptor: %{x}<br>Score: %{z:.3f}'), row=c3+1, col=m+1)    
    fig_heatmap.update_layout(template="ggplot2", font_size=20, margin=dict(l=20, r=20, t=70, b=20), title=dict(text=f"<span style='font-size: 26px;'><b>{data.capitalize()} Efficiency Heatmaps</b></span>", x=0.5, xanchor="center", yanchor="bottom"))
    fig_heatmap.write_html(f"./html/{data}/{data}_Heatmap.html", include_plotlyjs="cdn", full_html=True, config=config)    
    np.save(f"./arrays/Scores_{data}.npy", scores)

def correlationHeatmap(data="drone"):
    if data == "synthetic":
        Exec_time = np.concatenate((Exec_time_intensity, Exec_time_scale, Exec_time_rot), axis=0)
        Rate = np.concatenate((Rate_intensity, Rate_scale, Rate_rot), axis=0)
    elif data == "oxford":
        Exec_time = np.concatenate((Exec_time_graf, Exec_time_wall, Exec_time_trees, Exec_time_bikes, Exec_time_bark, Exec_time_boat, Exec_time_leuven, Exec_time_ubc), axis=0)
        Rate = np.concatenate((Rate_graf, Rate_wall, Rate_trees, Rate_bikes, Rate_bark, Rate_boat, Rate_leuven, Rate_ubc), axis=0)
    else:
        Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
        Rate = np.load(f"./arrays/Rate_{data}.npy")
    metrics = {
        "Precision":            Rate[:, :, :, :, :, 13].flatten(),
        "Recall":               Rate[:, :, :, :, :, 12].flatten(),
        "Repeatibility":        Rate[:, :, :, :, :, 14].flatten(),
        "F1 Score":             Rate[:, :, :, :, :, 15].flatten(),
        "Inliers":              Rate[:, :, :, :, :,  9].flatten(),
        "Matches":              Rate[:, :, :, :, :, 10].flatten(),
        "1K Total Time":        Exec_time[:, :, :, :, :,  6].flatten(),
        "1K Inlier Time":       Exec_time[:, :, :, :, :,  7].flatten()
    }
    if data == "drone":
        metrics.update({
            "Reprojection Error":   Rate[:, :, :, :, :, 11].flatten(),
            "3D Points Count":      Rate[:, :, :, :, :, 16].flatten(),
            "Reconstruction Time":  Exec_time[:, :, :, :, :,  8].flatten(),
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
    fig.add_trace(go.Heatmap(   z=corr_matrix, x=metric_names, y=metric_names, colorscale='RdBu', zmid=0, text=np.round(corr_matrix, 3),
                                texttemplate='%{text}', hoverongaps=False, hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>'))
    fig.update_layout(  template="ggplot2", font_size=20, margin=dict(l=20, r=20, t=50, b=20),
                        title=dict(text=f"<span style='font-size: 26px;'><b>{data.capitalize()} Metric Correlations</b></span>", x=0.5, xanchor="center", yanchor="middle"))
    fig.write_html(f"./html/{data}/{data}_Correlation.html", include_plotlyjs="cdn", full_html=True, config=config)

def violinPlot(data="drone"):
    if data == "synthetic":
        Rate = np.concatenate((Rate_intensity, Rate_scale, Rate_rot), axis=0)
        Exec_time = np.concatenate((Exec_time_intensity, Exec_time_scale, Exec_time_rot), axis=0)
    elif data == "oxford":
        Rate = np.concatenate((Rate_graf, Rate_wall, Rate_trees, Rate_bikes, Rate_bark, Rate_boat, Rate_leuven, Rate_ubc), axis=0)
        Exec_time = np.concatenate((Exec_time_graf, Exec_time_wall, Exec_time_trees, Exec_time_bikes, Exec_time_bark, Exec_time_boat, Exec_time_leuven, Exec_time_ubc), axis=0)
    else:
        Rate = np.load(f"./arrays/Rate_{data}.npy")
        Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    fig = go.Figure()
    traces = []
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):  # Normalization Type
                for m in range(2):  # Matcher Type
                    xydata = np.array([
                        Rate[:, m, c3, i, j, 13], # Precision
                        Rate[:, m, c3, i, j, 12], # Recall
                        Rate[:, m, c3, i, j, 14], # Repeatibility
                        Rate[:, m, c3, i, j, 15], # F1 Score
                        Rate[:, m, c3, i, j,  9], # Inliers
                        Rate[:, m, c3, i, j, 10], # Matches
                        Exec_time[:, m, c3, i, j, 6],  # 1K Total Time
                        Exec_time[:, m, c3, i, j, 7]   # 1K Inlier Time
                    ])
                    if not np.all(np.isnan(xydata)):
                        traces.append(go.Violin(
                                x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]]*len(xydata[0]), [Norm[c3]]*len(xydata[0])], y=xydata,
                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                marker=dict(color=colors[color_index]), box_visible=True, meanline_visible=True))
                        fig.add_trace(go.Violin(
                                x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]]*len(xydata[0]), [Norm[c3]]*len(xydata[0])], y=xydata[0],
                                name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                marker=dict(color=colors[color_index]), box_visible=True, meanline_visible=True))
            color_index = (color_index + 14) % num_combinations
    dropdown_axis = ["Precision", "Recall", "Repeatability", "F1-Score", "Inliers", "Matches", "1k Match Time", "1k Inlier Time"]
    button_list = []
    for idx, axis in enumerate(dropdown_axis):
        button_list.append(dict(label=f"y: {axis}", method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": f"<span style='font-size: 22px;'><b>{axis}</b></span>"}]))
    fig.update_layout(  template="ggplot2", font_size=16, margin=dict(l=20, r=20, t=50, b=20), hovermode="x unified",
                        title=dict(text=f"<span style='font-size: 26px;'><b>{data.capitalize()} Violin Plots</b></span>", x=0.5, xanchor="center", yanchor="middle"), 
                        updatemenus=[   dict(type="buttons", buttons=[dict(label="<b>≡ Legend</b>", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1, yanchor="bottom"),
                                        dict(type="dropdown", showactive=True, active=0, buttons=button_list, direction="down", x=0, xanchor="left", y=1, yanchor="bottom")])
    fig.write_html(f"./html/{data}/{data}_Violin.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}_Violin.html", "a") as f:
        f.write(custom_html)