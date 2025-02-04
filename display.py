import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from define import *

custom_html = """
<div style="position: fixed; top: 45px; right: 115px;">
    <span id="trace-count">Total Traces: 0</span>
</div>
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
</div>
<script>
function applyFilters() {
    var i, j;
    var filter = document.getElementById("filterInput").value.toUpperCase();
    var minYThreshold = parseFloat(document.getElementById("minYValueInput").value) || -Infinity;
    var maxYThreshold = parseFloat(document.getElementById("maxYValueInput").value) ||  Infinity;
    var minXThreshold = parseFloat(document.getElementById("minXValueInput").value) || -Infinity;
    var maxXThreshold = parseFloat(document.getElementById("maxXValueInput").value) ||  Infinity;
    var plot = document.querySelectorAll(".js-plotly-plot")[0];
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
    for (i = 0; i < data.length; i++) {
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
                visibleTraceCount++;
            }
        }
        data[i].visible = showTrace;
    }
    document.getElementById('trace-count').innerText = "Total Traces: " + visibleTraceCount;
    Plotly.redraw(plot);
}
window.onload = function() {
    applyFilters();
};
</script>
"""

config = {
        "toImageButtonOptions":     {"format": "svg"},
        "modeBarButtonsToRemove":   ["zoom", "pan", "select", "lasso2d", "zoomIn2d", "zoomOut2d"],
        "modeBarButtonsToAdd":      ["v1hovermode", "toggleSpikeLines", "hoverClosestCartesian", "hoverCompareCartesian"],
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
def synthetic():
    fig1 = go.Figure()
    fig1 = make_subplots(   rows=2, cols=2, subplot_titles=["Intensity changing I+b", "Intensity changing Ixc", "Scale changing", "Rotation changing"],
                            horizontal_spacing=0.04, vertical_spacing=0.045)
    fig1.update_layout(title_text="<b>Synthetic Dataset</b>", title_x=0.45, title_y=0.97, title_xanchor="center", hovermode="x", margin=dict(l=20, r=20, t=60, b=20))
    sett_axis = dict(autorange=False, range=[0, 1])
    fig1.update_layout(xaxis = dict(tickvals = val_b), xaxis2 = dict(tickvals = val_c), xaxis3 = dict(tickvals = scale), xaxis4 = dict(tickvals = rot), uirevision="73", yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1 = [Rate_intensity[:len(val_b), m, c3, i, j, 13], Rate_intensity[:len(val_b), m, c3, i, j, 12], Rate_intensity[:len(val_b), m, c3, i, j, 14], Rate_intensity[:len(val_b), m, c3, i, j, 15], Rate_intensity[:len(val_b), m, c3, i, j, 9], Rate_intensity[:len(val_b), m, c3, i, j, 10]]
                    Rate2_I2 = [Rate_intensity[len(val_c):, m, c3, i, j, 13], Rate_intensity[len(val_c):, m, c3, i, j, 12], Rate_intensity[len(val_c):, m, c3, i, j, 14], Rate_intensity[len(val_c):, m, c3, i, j, 15], Rate_intensity[len(val_c):, m, c3, i, j, 9], Rate_intensity[len(val_c):, m, c3, i, j, 10]]
                    Rate2_S  = [Rate_scale    [          :, m, c3, i, j, 13], Rate_scale    [          :, m, c3, i, j, 12], Rate_scale    [          :, m, c3, i, j, 14], Rate_scale    [          :, m, c3, i, j, 15], Rate_scale    [          :, m, c3, i, j, 9], Rate_scale    [          :, m, c3, i, j, 10]]
                    Rate2_R  = [Rate_rot      [          :, m, c3, i, j, 13], Rate_rot      [          :, m, c3, i, j, 12], Rate_rot      [          :, m, c3, i, j, 14], Rate_rot      [          :, m, c3, i, j, 15], Rate_rot      [          :, m, c3, i, j, 9], Rate_rot      [          :, m, c3, i, j, 10]]
                    legend_groupfig1 = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker=dict(symbol=marker_symbols[symbol_index], size=9, color=colors[color_index]),
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig1, legendgroup=legend_groupfig1, showlegend=False, hovertemplate="<b>%{y:.3f}</b>")
                    if not (np.isnan(Rate2_I1).any()):
                        traces.append (go.Scatter(x=val_b, y=Rate2_I1,    arg=sett))
                        fig1.add_trace(go.Scatter(x=val_b, y=Rate2_I1[0], arg=sett),  row=1, col=1)
                    if not (np.isnan(Rate2_I2).any()):   
                        traces.append (go.Scatter(x=val_c, y=Rate2_I2,    arg=sett))
                        fig1.add_trace(go.Scatter(x=val_c, y=Rate2_I2[0], arg=sett), row=1, col=2)
                    if not (np.isnan(Rate2_S).any()):              
                        traces.append (go.Scatter(x=scale, y=Rate2_S,     arg=sett))
                        fig1.add_trace(go.Scatter(x=scale, y=Rate2_S[0],  arg=sett), row=2, col=1)
                    if not (np.isnan(Rate2_R).any()):
                        traces.append (go.Scatter(x=rot,   y=Rate2_R,     arg=sett))
                        fig1.add_trace(go.Scatter(x=rot,   y=Rate2_R[0],  arg=sett, showlegend=True), row=2, col=2)
                    symbol_index = (symbol_index + 25) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeatibility", "F1 Score", "Inliers", "Matches"]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=y, method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": y, "yaxis2.title": y, "yaxis3.title": y, "yaxis4.title": y}]))
    
    fig1.update_layout(updatemenus=[    dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06),
                                        dict(type="dropdown", buttons=button_list, x=0.5, xanchor="center", y=-0.04, direction="up")]) 
    fig1.write_html(f"./html/synthetic/synthetic.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic.html", "a") as f:
        f.write(custom_html)

#########################################
# MARK: - Synthetic Data Precision-Recall
#########################################
def syntheticMulti(name="Precision-Recall", x=13, y=12):
    fig2 = go.Figure()
    fig2 = make_subplots(   rows=2, cols=2, subplot_titles=["Intensity changing I+b", "Intensity changing Ixc", "Scale changing", "Rotation changing"],
                            horizontal_spacing=0.05, vertical_spacing=0.06, x_title=f"<span style='font-size: 12px;'>{name.split('-')[0]}</span>", y_title=f"<span style='font-size: 12px;'>{name.split('-')[1]}</span>")
    fig2.update_layout(title_text=f"<b>Synthetic Dataset - {name}</b>", title_x=0.45, hovermode="x", uirevision="73", margin=dict(l=60, r=20, t=60, b=60))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1_x = np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, x])
                    Rate2_I1_y = np.nanmean(Rate_intensity[:len(val_b), m, c3, i, j, y])
                    Rate2_I2_x = np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, x])
                    Rate2_I2_y = np.nanmean(Rate_intensity[len(val_c):, m, c3, i, j, y])
                    Rate2_S_x  = np.nanmean(Rate_scale    [          :, m, c3, i, j, x])
                    Rate2_S_y  = np.nanmean(Rate_scale    [          :, m, c3, i, j, y])
                    Rate2_R_x  = np.nanmean(Rate_rot      [          :, m, c3, i, j, x])
                    Rate2_R_y  = np.nanmean(Rate_rot      [          :, m, c3, i, j, y])
                    legend_groupfig2 = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers", marker=dict(symbol=marker_symbols[symbol_index], size=9, color=colors[color_index]), name=legend_groupfig2,
                                showlegend=False, hovertemplate=f"{name.split('-')[0]}:" + "%{x:.3f} | " + f"{name.split('-')[1]}:" + "%{y:.3f}")
                    if not (np.isnan(Rate2_I1_x).any() or (np.isnan(Rate2_I1_y).any())):
                        fig2.add_trace(go.Scatter(  x=[Rate2_I1_x], y=[Rate2_I1_y], arg=sett), row=1, col=1)
                    if not (np.isnan(Rate2_I2_x).any() or (np.isnan(Rate2_I2_y).any())):
                        fig2.add_trace(go.Scatter(  x=[Rate2_I2_x], y=[Rate2_I2_y], arg=sett), row=1, col=2)
                    if not (np.isnan(Rate2_S_x).any() or (np.isnan(Rate2_S_y).any())):
                        fig2.add_trace(go.Scatter(  x=[Rate2_S_x],  y=[Rate2_S_y],  arg=sett), row=2, col=1)
                    if not (np.isnan(Rate2_R_x).any() or (np.isnan(Rate2_R_y).any())):
                        fig2.add_trace(go.Scatter(  x=[Rate2_R_x],  y=[Rate2_R_y],  arg=sett, showlegend=True),   row=2, col=2)
                    symbol_index = (symbol_index + 25) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    fig2.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig2.write_html(f"./html/synthetic/synthetic_{name}.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic_{name}.html", "a") as f:
        f.write(custom_html)

###########################
# MARK: - Synthetic Timing
###########################
def synthetic_timing():
    fig3 = go.Figure()
    fig3 = make_subplots(  rows=5, cols=2, subplot_titles=[ f"<span style='font-size: 12px;'>Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)</span>",
                                                            f"<span style='font-size: 12px;'>Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)</span>",
                                                            f"<span style='font-size: 12px;'>Average 1k Total time (Detect + Descript + Match(BF+FL))</span>",
                                                            f"<span style='font-size: 12px;'>Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)</span>",
                                                            f"<span style='font-size: 12px;'>Average 1k Detect time</span>",
                                                            f"<span style='font-size: 12px;'>Average 1k Describe time</span>"],
                            specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}]], horizontal_spacing=0.05, vertical_spacing=0.06)
    fig3.update_layout(title_text=f"<b>Synthetic Data Timings</b>", title_x=0.5, barmode="stack", height=2000, margin=dict(l=20, r=20, t=60, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 6], Exec_time_scale[:, m, :, i, j, 6], Exec_time_rot[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 7], Exec_time_scale[:, m, :, i, j, 7], Exec_time_rot[:, m, :, i, j, 7]), axis=0))
                if not (result3 == 0 or np.isnan(result3)):
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig3.add_trace(trace_match_synt_result3, row=1, col=1) if m == 0 else fig3.add_trace(trace_match_synt_result3, row=2, col=1)
                    trace_match_synt_result3.showlegend = False
                    fig3.add_trace(trace_match_synt_result3, row=3, col=1)
                if not (result4 == 0 or np.isnan(result4)):
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig3.add_trace(trace_match_synt_result4, row=1, col=1) if m == 0 else fig3.add_trace(trace_match_synt_result4, row=2, col=1)
                    trace_match_synt_result4.showlegend = False
                    fig3.add_trace(trace_match_synt_result4, row=4, col=1)
            color_index = (color_index + 14) % num_combinations
        result = np.nanmean(np.concatenate((Exec_time_intensity[:, :, :, i, :, 4], Exec_time_scale[:, :, :, i, :, 4], Exec_time_rot[:, :, :, i, :, 4]), axis=0))
        if not (result == 0 or np.isnan(result)):
            trace_detect_synt = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=f".{DetectorsLegend[i]}",  showlegend=True,  text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            fig3.add_trace(trace_detect_synt, row=5, col=1)
        result2 = np.nanmean(np.concatenate((Exec_time_intensity[:, :, :, :, i, 5], Exec_time_scale[:, :, :, :, i, 5], Exec_time_rot[:, :, :, :, i, 5]), axis=0))
        if not (result2 == 0 or np.isnan(result2)):
            trace_descr_synt = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=f"-{DescriptorsLegend[i]}", showlegend=True, text=[f"{result2:.3f}"], marker=dict(color = colors[14*i]))
            fig3.add_trace(trace_descr_synt, row=5, col=2)
    
    fig3.update_layout(updatemenus=[dict(type="buttons",  buttons=[ dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.02),
                                    dict(type="dropdown", buttons=[ dict(label="Linear",   method="relayout", args=[{"yaxis.type": "linear","yaxis2.type": "linear","yaxis3.type": "linear","yaxis4.type": "linear","yaxis5.type": "linear","yaxis6.type": "linear"}]),
                                                                    dict(label="Log",      method="relayout", args=[{"yaxis.type": "log","yaxis2.type": "log","yaxis3.type": "log","yaxis4.type": "log","yaxis5.type": "log","yaxis6.type": "log"}])], x=0, xanchor="left", y=1.02)])
    fig3.write_html("./html/synthetic/synthetic_timing.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open("./html/synthetic/synthetic_timing.html", "a") as f:
        f.write(custom_html)

def synthetic_timing2():
    fig15 = go.Figure()
    fig15.update_layout(title_text="<b>Synthetic Data - Overall Timings</b>", title_x=0.45, yaxis_title="1/Inlier Time", hovermode="x", margin=dict(l=20, r=20, t=60, b=20))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    x_data = [
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 13], Rate_scale[:, m, c3, i, j, 13], Rate_rot[:, m, c3, i, j, 13]), axis=0)), # Precision
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 12], Rate_scale[:, m, c3, i, j, 12], Rate_rot[:, m, c3, i, j, 12]), axis=0)), # Recall
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 14], Rate_scale[:, m, c3, i, j, 14], Rate_rot[:, m, c3, i, j, 14]), axis=0)), # Repeatibility
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 15], Rate_scale[:, m, c3, i, j, 15], Rate_rot[:, m, c3, i, j, 15]), axis=0)), # F1 Score
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j,  9], Rate_scale[:, m, c3, i, j,  9], Rate_rot[:, m, c3, i, j,  9]), axis=0)), # Inliers
                        np.nanmean(np.concatenate((Rate_intensity[:, m, c3, i, j, 10], Rate_scale[:, m, c3, i, j, 10], Rate_rot[:, m, c3, i, j, 10]), axis=0))  # Matches
                    ]
                    inlierTime = np.nanmean(np.concatenate((Exec_time_intensity[:, m, c3, i, j, 7], Exec_time_scale[:, m, c3, i, j, 7], Exec_time_rot[:, m, c3, i, j, 7]), axis=0))
                    if not (inlierTime == 0 or np.isnan(inlierTime) or np.isnan(x_data).any()):
                        trace = go.Scatter( x=x_data, y=[1/inlierTime], mode="markers", 
                                            marker=dict(color=colors[color_index], size=10, symbol=marker_symbols[symbol_index]),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>")
                        traces.append(trace)
                        fig15.add_trace(trace)
                    symbol_index = (symbol_index + 25) % len(marker_symbols)
            color_index = (color_index + 14) % num_combinations
    dropdown_xaxis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches"]
    button_list = []
    for idx, axis in enumerate(dropdown_xaxis):
        button_list.append(dict( label=axis, method="update", args=[{"x": [[trace.x[idx]] for trace in traces]},
                                                                    {"xaxis.title": axis}]))    
    fig15.update_layout(updatemenus=[   dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06),
                                        dict(type="dropdown", buttons=button_list, direction="up", x=0.55, y=-0.04)])
    fig15.write_html(f"./html/synthetic/synthetic_timing2.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/synthetic/synthetic_timing2.html", "a") as f:
        f.write(custom_html)

##################################
# MARK: - Oxford all 8 and Overall
##################################
def oxford():
    fig4 = go.Figure()
    fig4 = make_subplots(   rows=3, cols=3, subplot_titles=["Graf(Viewpoint)", "Bikes(Blur)", "Boat(Zoom + Rotation)", "Leuven(Light)", "Wall(Viewpoint)", "Trees(Blur)", "Bark(Zoom + Rotation)", "UBC(JPEG)", "Overall"],
                            horizontal_spacing=0.04, vertical_spacing=0.05)
    xvals = ["Img2", "Img3", "Img4", "Img5", "Img6"]
    sett_axis = dict(autorange=False, range=[0, 1])
    fig4.update_layout( title_text="<b>Oxford Affine Dataset</b>", title_x=0.45, title_xanchor="right", hovermode="x", margin=dict(l=20, r=20, t=60, b=20), uirevision="73", yaxis=sett_axis, yaxis2=sett_axis, yaxis3=sett_axis, yaxis4=sett_axis, yaxis5=sett_axis, yaxis6=sett_axis, yaxis7=sett_axis, yaxis8=sett_axis, yaxis9=sett_axis)
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_Graf  = [Rate_graf  [:, m, c3, i, j, 13], Rate_graf  [:, m, c3, i, j, 12], Rate_graf  [:, m, c3, i, j, 14], Rate_graf  [:, m, c3, i, j, 15], Rate_graf  [:, m, c3, i, j, 9], Rate_graf  [:, m, c3, i, j, 10]]
                    Rate_Bikes = [Rate_bikes [:, m, c3, i, j, 13], Rate_bikes [:, m, c3, i, j, 12], Rate_bikes [:, m, c3, i, j, 14], Rate_bikes [:, m, c3, i, j, 15], Rate_bikes [:, m, c3, i, j, 9], Rate_bikes [:, m, c3, i, j, 10]]
                    Rate_Boat  = [Rate_boat  [:, m, c3, i, j, 13], Rate_boat  [:, m, c3, i, j, 12], Rate_boat  [:, m, c3, i, j, 14], Rate_boat  [:, m, c3, i, j, 15], Rate_boat  [:, m, c3, i, j, 9], Rate_boat  [:, m, c3, i, j, 10]]
                    Rate_Leuven= [Rate_leuven[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 9], Rate_leuven[:, m, c3, i, j, 10]]
                    Rate_Wall  = [Rate_wall  [:, m, c3, i, j, 13], Rate_wall  [:, m, c3, i, j, 12], Rate_wall  [:, m, c3, i, j, 14], Rate_wall  [:, m, c3, i, j, 15], Rate_wall  [:, m, c3, i, j, 9], Rate_wall  [:, m, c3, i, j, 10]]
                    Rate_Trees = [Rate_trees [:, m, c3, i, j, 13], Rate_trees [:, m, c3, i, j, 12], Rate_trees [:, m, c3, i, j, 14], Rate_trees [:, m, c3, i, j, 15], Rate_trees [:, m, c3, i, j, 9], Rate_trees [:, m, c3, i, j, 10]]
                    Rate_Bark  = [Rate_bark  [:, m, c3, i, j, 13], Rate_bark  [:, m, c3, i, j, 12], Rate_bark  [:, m, c3, i, j, 14], Rate_bark  [:, m, c3, i, j, 15], Rate_bark  [:, m, c3, i, j, 9], Rate_bark  [:, m, c3, i, j, 10]]
                    Rate_Ubc   = [Rate_ubc   [:, m, c3, i, j, 13], Rate_ubc   [:, m, c3, i, j, 12], Rate_ubc   [:, m, c3, i, j, 14], Rate_ubc   [:, m, c3, i, j, 15], Rate_ubc   [:, m, c3, i, j, 9], Rate_ubc   [:, m, c3, i, j, 10]]
                    legend_groupfig4 = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker_symbol=symbol_index, marker_size=9,
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False, hovertemplate="<b>%{y:.3f}</b>")
                    if not (np.isnan(Rate_Graf).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Graf,       arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Graf[0],    arg=sett), row=1, col=1)
                    if not (np.isnan(Rate_Bikes).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Bikes,      arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Bikes[0],   arg=sett), row=1, col=2)
                    if not (np.isnan(Rate_Boat).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Boat,       arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Boat[0],    arg=sett), row=1, col=3)
                    if not (np.isnan(Rate_Leuven).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Leuven,     arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Leuven[0],  arg=sett), row=2, col=1)
                    if not (np.isnan(Rate_Wall).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Wall,       arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Wall[0],    arg=sett), row=2, col=2)
                    if not (np.isnan(Rate_Trees).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Trees,      arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Trees[0],   arg=sett), row=2, col=3)
                    if not (np.isnan(Rate_Bark).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Bark,       arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Bark[0],    arg=sett), row=3, col=1)
                    if not (np.isnan(Rate_Ubc).any()):
                        traces.append (go.Scatter(x = xvals, y=Rate_Ubc,        arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=Rate_Ubc[0],     arg=sett), row=3, col=2)
                    yval = np.nanmean([Rate_Graf, Rate_Bikes, Rate_Boat, Rate_Leuven, Rate_Wall, Rate_Trees, Rate_Bark, Rate_Ubc], axis=0)
                    if not (np.isnan(yval).any()):
                        traces.append (go.Scatter(x = xvals, y=yval, arg=sett))
                        fig4.add_trace(go.Scatter(x = xvals, y=np.nanmean([Rate_Graf[0], Rate_Bikes[0], Rate_Boat[0], Rate_Leuven[0], Rate_Wall[0], Rate_Trees[0], Rate_Bark[0], Rate_Ubc[0]], axis=0), arg=sett, showlegend=True), row=3, col=3)
                    symbol_index = (symbol_index + 1) % 27
            color_index = (color_index + 14) % num_combinations
    
    dropdown_yaxis = ["Precision", "Recall", "Repeatibility", "F1 Score", "Inliers", "Matches"]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=y, method="update", 
                                args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": y, "yaxis2.title": y, "yaxis3.title": y, "yaxis4.title": y, "yaxis5.title": y, "yaxis6.title": y, "yaxis7.title": y, "yaxis8.title": y, "yaxis9.title": y}]))
    fig4.update_layout(updatemenus=[    dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06),
                                        dict(type="dropdown", buttons=button_list, x=0.55, xanchor="left", y=1.06)])          
    fig4.write_html(f"./html/oxford/oxford.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford.html", "a") as f:
        f.write(custom_html)

######################
# MARK: - Oxford Multi
######################
def oxfordMulti(name="Precision-Recall", x=13, y=12):
    fig5 = go.Figure()
    fig5 = make_subplots(   rows=3, cols=3,subplot_titles=["Graf(Viewpoint)", "Bikes(Blur)", "Boat(Zoom + Rotation)", "Leuven(Light)", "Wall(Viewpoint)", "Trees(Blur)", "Bark(Zoom + Rotation)", "UBC(JPEG)", "Overall"],
                            horizontal_spacing=0.05, vertical_spacing=0.06, x_title=name.split('-')[0], y_title=name.split('-')[1])
    fig5.update_layout(title_text=f"<b>Oxford Affine Dataset - {name}</b>", title_x=0.45, hovermode="x", uirevision="73")
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_Graf_x  = np.nanmean(Rate_graf  [:, m, c3, i, j, x])
                    Rate_Graf_y  = np.nanmean(Rate_graf  [:, m, c3, i, j, y])
                    Rate_Bikes_x = np.nanmean(Rate_bikes [:, m, c3, i, j, x])
                    Rate_Bikes_y = np.nanmean(Rate_bikes [:, m, c3, i, j, y])
                    Rate_Boat_x  = np.nanmean(Rate_boat  [:, m, c3, i, j, x])
                    Rate_Boat_y  = np.nanmean(Rate_boat  [:, m, c3, i, j, y])
                    Rate_Leuven_x= np.nanmean(Rate_leuven[:, m, c3, i, j, x])
                    Rate_Leuven_y= np.nanmean(Rate_leuven[:, m, c3, i, j, y])
                    Rate_Wall_x  = np.nanmean(Rate_wall  [:, m, c3, i, j, x])
                    Rate_Wall_y  = np.nanmean(Rate_wall  [:, m, c3, i, j, y])
                    Rate_Trees_x = np.nanmean(Rate_trees [:, m, c3, i, j, x])
                    Rate_Trees_y = np.nanmean(Rate_trees [:, m, c3, i, j, y])
                    Rate_Bark_x  = np.nanmean(Rate_bark  [:, m, c3, i, j, x])
                    Rate_Bark_y  = np.nanmean(Rate_bark  [:, m, c3, i, j, y])
                    Rate_Ubc_x   = np.nanmean(Rate_ubc   [:, m, c3, i, j, x])
                    Rate_Ubc_y   = np.nanmean(Rate_ubc   [:, m, c3, i, j, y])
                    legend_groupfig5 = f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}"
                    sett = dict(mode="markers+lines", marker_symbol=symbol_index, marker_size=9,
                                line=dict(color=colors[color_index], dash=line_styles[(i+j) % len(line_styles)], width=3),
                                name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False, hovertemplate=f"{name.split('-')[0]}:" + "<b>%{x:.3f}</b> | " + f"{name.split('-')[1]}:"+ "<b>%{y:.3f}</b>")
                    if not (np.isnan(Rate_Graf_x).any()     or (np.isnan(Rate_Graf_y).any())):
                        fig5.add_trace(go.Scatter(x=[Rate_Graf_x],   y=[Rate_Graf_y],   arg=sett),  row=1, col=1)
                    if not (np.isnan(Rate_Bikes_x).any()    or (np.isnan(Rate_Bikes_y).any())):
                        fig5.add_trace(go.Scatter(x=[Rate_Bikes_x],  y=[Rate_Bikes_y],  arg=sett), row=1, col=2)
                    if not (np.isnan(Rate_Boat_x).any()     or (np.isnan(Rate_Boat_y).any())):
                        fig5.add_trace(go.Scatter(x=[Rate_Boat_x],   y=[Rate_Boat_y],   arg=sett), row=1, col=3)
                    if not (np.isnan(Rate_Leuven_x).any()   or (np.isnan(Rate_Leuven_y).any())):
                        fig5.add_trace(go.Scatter(x=[Rate_Leuven_x], y=[Rate_Leuven_y], arg=sett), row=2, col=1)
                    if not (np.isnan(Rate_Wall_x).any()     or (np.isnan(Rate_Wall_y).any())):
                        fig5.add_trace(go.Scatter(x=[Rate_Wall_x],   y=[Rate_Wall_y],   arg=sett), row=2, col=2)
                    if not (np.isnan(Rate_Trees_x).any()    or (np.isnan(Rate_Trees_y).any())):
                        fig5.add_trace(go.Scatter(x=[Rate_Trees_x],  y=[Rate_Trees_y],  arg=sett), row=2, col=3)
                    if not (np.isnan(Rate_Bark_x).any()     or (np.isnan(Rate_Bark_y).any())):
                        fig5.add_trace(go.Scatter(x=[Rate_Bark_x],   y=[Rate_Bark_y],   arg=sett), row=3, col=1)
                    if not (np.isnan(Rate_Ubc_x).any()      or (np.isnan(Rate_Ubc_y).any())):
                        fig5.add_trace(go.Scatter(x=[Rate_Ubc_x],    y=[Rate_Ubc_y],    arg=sett), row=3, col=2)
                    xval = np.nanmean([Rate_Graf_x, Rate_Bikes_x, Rate_Boat_x, Rate_Leuven_x, Rate_Wall_x, Rate_Trees_x, Rate_Bark_x, Rate_Ubc_x], axis=0)
                    yval = np.nanmean([Rate_Graf_y, Rate_Bikes_y, Rate_Boat_y, Rate_Leuven_y, Rate_Wall_y, Rate_Trees_y, Rate_Bark_y, Rate_Ubc_y], axis=0)
                    if not (np.isnan(xval).any() or np.isnan(yval).any()):
                        fig5.add_trace(go.Scatter(  x=[xval], y=[yval], arg=sett, showlegend=True), row=3, col=3)
                    symbol_index = (symbol_index + 1) % 27
            color_index = (color_index + 14) % num_combinations
    fig5.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig5.write_html(f"./html/oxford/oxford_{name}.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford_{name}.html", "a") as f:
        f.write(custom_html)

###########################
# MARK: - Oxford Timing
###########################
def oxford_timing():
    fig6 = go.Figure()
    fig6 = make_subplots(  rows=5, cols=2, subplot_titles=[ "Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)",
                                                            "Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)",
                                                            "Average 1k Total time (Detect + Descript + Match(BF+FL))",
                                                            "Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)",
                                                            "Average 1k Detect time",
                                                            "Average 1k Describe time"],
                            specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}]], horizontal_spacing=0.05, vertical_spacing=0.06)
    fig6.update_layout(title_text="<b>Oxford Affine Dataset - Timing</b>", title_x=0.5, barmode="stack", height=2000, margin=dict(l=20, r=20, t=60, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 6], Exec_time_wall[:, m, :, i, j, 6], Exec_time_trees[:, m, :, i, j, 6], Exec_time_bikes[:, m, :, i, j, 6], Exec_time_bark[:, m, :, i, j, 6], Exec_time_boat[:, m, :, i, j, 6], Exec_time_leuven[:, m, :, i, j, 6], Exec_time_ubc[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 7], Exec_time_wall[:, m, :, i, j, 7], Exec_time_trees[:, m, :, i, j, 7], Exec_time_bikes[:, m, :, i, j, 7], Exec_time_bark[:, m, :, i, j, 7], Exec_time_boat[:, m, :, i, j, 7], Exec_time_leuven[:, m, :, i, j, 7], Exec_time_ubc[:, m, :, i, j, 7]), axis=0))
                if not (result3 == 0 or np.isnan(result3)):
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig6.add_trace(trace_match_synt_result3, row=1, col=1) if m == 0 else fig6.add_trace(trace_match_synt_result3, row=2, col=1)
                    trace_match_synt_result3.showlegend = False
                    fig6.add_trace(trace_match_synt_result3, row=3, col=1)
                if not (result4 == 0 or np.isnan(result4)):
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig6.add_trace(trace_match_synt_result4, row=1, col=1) if m == 0 else fig6.add_trace(trace_match_synt_result4, row=2, col=1)
                    trace_match_synt_result4.showlegend = False
                    fig6.add_trace(trace_match_synt_result4, row=4, col=1)
            color_index = (color_index + 14) % num_combinations            
        result = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, i, :, 4], Exec_time_wall[:, :, :, i, :, 4], Exec_time_trees[:, :, :, i, :, 4], Exec_time_bikes[:, :, :, i, :, 4], Exec_time_bark[:, :, :, i, :, 4], Exec_time_boat[:, :, :, i, :, 4], Exec_time_leuven[:, :, :, i, :, 4], Exec_time_ubc[:, :, :, i, :, 4]), axis=0))
        if not (result == 0 or np.isnan(result)):
            trace_detect_oxford = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=f".{DetectorsLegend[i]}",  showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            fig6.add_trace(trace_detect_oxford, row=5, col=1)
        result2 = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, :, i, 5], Exec_time_wall[:, :, :, :, i, 5], Exec_time_trees[:, :, :, :, i, 5], Exec_time_bikes[:, :, :, :, i, 5], Exec_time_bark[:, :, :, :, i, 5], Exec_time_boat[:, :, :, :, i, 5], Exec_time_leuven[:, :, :, :, i, 5], Exec_time_ubc[:, :, :, :, i, 5]), axis=0))
        if not (result2 == 0 or np.isnan(result2)):
            trace_descr_oxford = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=f"-{DescriptorsLegend[i]}",showlegend=True, text=[f"{result2:.3f}"], marker=dict(color = colors[14*i]))
            fig6.add_trace(trace_descr_oxford, row=5, col=2)
        
    fig6.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.015),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis.type" : "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis.type" : "log"}])], x=0, xanchor="left", y=1.015),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis2.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis2.type": "log"}])], x=0, xanchor="left", y=0.80),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis3.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis3.type": "log"}])], x=0, xanchor="left", y=0.59),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis4.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis4.type": "log"}])], x=0, xanchor="left", y=0.38),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis5.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis5.type": "log"}])], x=0, xanchor="left", y=0.17),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis6.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis6.type": "log"}])], x=0.5, xanchor="left", y=0.175)])
    fig6.write_html("./html/oxford/oxford_timing.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford_timing.html", "a") as f:
        f.write(custom_html)

def oxford_timing2():
    fig14 = go.Figure()
    fig14.update_layout(title_text=f"<b>Oxford Data - Timings</b>", title_x=0.5, yaxis_title="1/Inlier Time", hovermode="x", margin=dict(l=20, r=20, t=60, b=20))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    x_data = [
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 13], Rate_bikes[:, m, c3, i, j, 13], Rate_boat[:, m, c3, i, j, 13], Rate_leuven[:, m, c3, i, j, 13], Rate_wall[:, m, c3, i, j, 13], Rate_trees[:, m, c3, i, j, 13], Rate_bark[:, m, c3, i, j, 13], Rate_ubc[:, m, c3, i, j, 13]), axis=0)),  # Precision
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 12], Rate_bikes[:, m, c3, i, j, 12], Rate_boat[:, m, c3, i, j, 12], Rate_leuven[:, m, c3, i, j, 12], Rate_wall[:, m, c3, i, j, 12], Rate_trees[:, m, c3, i, j, 12], Rate_bark[:, m, c3, i, j, 12], Rate_ubc[:, m, c3, i, j, 12]), axis=0)),  # Recall
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 14], Rate_bikes[:, m, c3, i, j, 14], Rate_boat[:, m, c3, i, j, 14], Rate_leuven[:, m, c3, i, j, 14], Rate_wall[:, m, c3, i, j, 14], Rate_trees[:, m, c3, i, j, 14], Rate_bark[:, m, c3, i, j, 14], Rate_ubc[:, m, c3, i, j, 14]), axis=0)),  # Repeatibility
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 15], Rate_bikes[:, m, c3, i, j, 15], Rate_boat[:, m, c3, i, j, 15], Rate_leuven[:, m, c3, i, j, 15], Rate_wall[:, m, c3, i, j, 15], Rate_trees[:, m, c3, i, j, 15], Rate_bark[:, m, c3, i, j, 15], Rate_ubc[:, m, c3, i, j, 15]), axis=0)),  # F1 Score
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 9],  Rate_bikes[:, m, c3, i, j, 9],  Rate_boat[:, m, c3, i, j, 9],  Rate_leuven[:, m, c3, i, j, 9],  Rate_wall[:, m, c3, i, j, 9],  Rate_trees[:, m, c3, i, j, 9],  Rate_bark[:, m, c3, i, j, 9],  Rate_ubc[:, m, c3, i, j, 9]), axis=0)),   # Inliers
                        np.nanmean(np.concatenate((Rate_graf[:, m, c3, i, j, 10], Rate_bikes[:, m, c3, i, j, 10], Rate_boat[:, m, c3, i, j, 10], Rate_leuven[:, m, c3, i, j, 10], Rate_wall[:, m, c3, i, j, 10], Rate_trees[:, m, c3, i, j, 10], Rate_bark[:, m, c3, i, j, 10], Rate_ubc[:, m, c3, i, j, 10]), axis=0))   # Matches
                    ]
                    inlierTime = np.nanmean(np.concatenate((Exec_time_graf[:, m, c3, i, j, 7], Exec_time_wall[:, m, c3, i, j, 7], Exec_time_trees[:, m, c3, i, j, 7], Exec_time_bikes[:, m, c3, i, j, 7], Exec_time_bark[:, m, c3, i, j, 7], Exec_time_boat[:, m, c3, i, j, 7], Exec_time_leuven[:, m, c3, i, j, 7], Exec_time_ubc[:, m, c3, i, j, 7]), axis=0))
                    if not (inlierTime == 0 or np.isnan(inlierTime) or np.isnan(x_data).any()):
                        trace = go.Scatter( x=x_data, y=[1/inlierTime], mode="markers", 
                                            marker=dict(color=colors[color_index], size=10, symbol=symbol_index),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>")
                        traces.append(trace)
                        fig14.add_trace(trace)
                    symbol_index = (symbol_index + 1) % 27
            color_index = (color_index + 14) % num_combinations
    dropdown_xaxis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches"]
    button_list = []
    for idx, axis in enumerate(dropdown_xaxis):
        button_list.append(dict( label=axis, method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}]))    
    
    fig14.update_layout(updatemenus=[   dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06),
                                        dict(type="dropdown", buttons=button_list, direction="up", x=0.55, y=-0.04)])
    fig14.write_html(f"./html/oxford/oxford_timing2.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford_timing2.html", "a") as f:
        f.write(custom_html)

#################################
# MARK: - Single Data (Drone-UAV)
#################################
def single(data="drone"):
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig7 = go.Figure()
    xvals = [f"Img{i}" for i in range(153, 188)] if data == "drone" else (
        ["Bahamas", "Office", "Suburban", "Building", "Construction", "Dominica", "Cadastre", "Rivaz", "Urban", "Belleview"] if data == "uav" else 
        [f"Img{i}" for i in range(653, 774, 5)])
    fig7.update_layout(title_text=f"<b>{data.upper()} Data</b>", title_x=0.45, title_xanchor="right", yaxis_title="Precision", hovermode="x", margin=dict(l=20, r=20, t=60, b=20), uirevision="73", yaxis=dict(range=[0, 1]))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    y_data = [
                        Rate[:, m, c3, i, j, 13],  # Precision
                        Rate[:, m, c3, i, j, 12],  # Recall
                        Rate[:, m, c3, i, j, 14],  # Repeatibility
                        Rate[:, m, c3, i, j, 15],  # F1 Score
                        Rate[:, m, c3, i, j,  9],  # Inliers
                        Rate[:, m, c3, i, j, 10]   # Matches
                    ]
                    if not (np.isnan(y_data).any()):
                        traces.append (go.Scatter(  x=xvals, y=y_data, mode="markers+lines",
                                                    marker=dict(symbol=symbol_index, color=colors[color_index], size=9),
                                                    line=dict(color=color, dash=style, width=3),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="<b>%{y:.3f}</b>"))
                    if not (np.isnan(y_data[0]).any()):
                        fig7.add_trace(go.Scatter(  x=xvals, y=y_data[0], mode="markers+lines",
                                                    marker=dict(symbol=symbol_index, color=colors[color_index], size=9),
                                                    line=dict(color=color, dash=style, width=3),
                                                    name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                                    showlegend=True, hovertemplate="<b>%{y:.3f}</b>"))
                    symbol_index = (symbol_index + 1) % 27
            color_index = (color_index + 14) % num_combinations
    dropdown_yaxis = ["Precision", "Recall", "Repeatibility", "F1 Score", "Inliers", "Matches"]
    button_list = []
    for idx, y in enumerate(dropdown_yaxis):
        button_list.append(dict(label=y, method="update", args=[{"y": [trace.y[idx] for trace in traces]}, {"yaxis.title": y}]))
    
    fig7.update_layout(updatemenus=[   dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06),
                                        dict(type="dropdown", buttons=button_list, active=0, x=0.55, xanchor="left", y=1.06)])
    fig7.write_html(f"./html/{data}/{data}.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}.html", "a") as f:
        f.write(custom_html)

##################################
# MARK: - Single Multi (UAV-Drone)
##################################
def singleMulti(data="drone",name="Precision-Recall", x=13, y=12):
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig11 = go.Figure()
    xvals = [f"Img{i}" for i in range(153, 188)] if data == "drone" else (
        ["Bahamas", "Office", "Suburban", "Building", "Construction", "Dominica", "Cadastre", "Rivaz", "Urban", "Belleview"] if data == "uav" else 
        [f"Img{i}" for i in range(653, 774, 5)])
    fig11.update_layout(title_text=f"<b>{data.upper()} Data - {name}</b>", title_x=0.5, title_xanchor="right", margin=dict(l=20, r=20, t=20, b=20),
                        xaxis_title=name.split('-')[0], yaxis_title=name.split('-')[1], hovermode="x", uirevision="73")
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_x = np.nanmean(Rate[:, m, c3, i, j, x])
                    Rate_y = np.nanmean(Rate[:, m, c3, i, j, y])
                    if not (np.isnan(Rate_x).any()) and not (np.isnan(Rate_y).any()):
                        fig11trace_UAV  = go.Scatter(   x=[Rate_x], y=[Rate_y], mode="markers+lines", marker=dict(symbol=symbol_index, size=9, color=colors[color_index]),
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}", showlegend=True,
                                                        customdata=xvals, hovertemplate="%{customdata} | " + f"{name.split('-')[0]}:" + "%{x:.3f} | " + f"{name.split('-')[1]}:"+ "%{y:.3f}")
                        fig11.add_trace(fig11trace_UAV)
                    symbol_index = (symbol_index + 1) % 27
            color_index = (color_index + 26) % num_combinations
    fig11.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig11.write_html(f"./html/{data}/{data}_{name}.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}_{name}.html", "a") as f:
        f.write(custom_html)
        
###################################
# MARK: - Single Timing (UAV-Drone)
###################################
def single_timing(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    fig12 = go.Figure()
    fig12 = make_subplots(  rows=5, cols=2, subplot_titles=["Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)",
                                                            "Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)",
                                                            "Average 1k Total time (Detect + Descript + Match(BF+FL))",
                                                            "Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)",
                                                            "Average 1k Detect time",
                                                            "Average 1k Describe time"],
                            specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}]],
                            horizontal_spacing=0.05, vertical_spacing=0.06)
    fig12.update_layout(title_text=f"<b>{data.upper()} Data - Timing</b>", title_x=0.5, title_xanchor="right", barmode="stack", height=2000, margin=dict(l=20, r=20, t=60, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(Exec_time[:, m, :, i, j, 6])
                result4 = np.nanmean(Exec_time[:, m, :, i, j, 7])
                if not (result3 == 0 or np.isnan(result3)):
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total",
                                                        text=[f"{result3:.3f}"], marker=dict(color = colors[color_index]),
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig12.add_trace(trace_match_synt_result3, row=1, col=1) if m == 0 else fig12.add_trace(trace_match_synt_result3, row=2, col=1)
                    trace_match_synt_result3.showlegend = False
                    fig12.add_trace(trace_match_synt_result3, row=3, col=1)
                if not (result4 == 0 or np.isnan(result4)):
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier",
                                                        text=[f"{result4:.3f}"], marker=dict(color = colors[color_index]),
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig12.add_trace(trace_match_synt_result4, row=1, col=1) if m == 0 else fig12.add_trace(trace_match_synt_result4, row=2, col=1)
                    trace_match_synt_result4.showlegend = False
                    fig12.add_trace(trace_match_synt_result4, row=4, col=1)
            color_index = (color_index + 14) % num_combinations
        result = np.nanmean(Exec_time[:, :, :, i, :, 4])
        if not (result == 0 or np.isnan(result)):
            trace_detect = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=f".{DetectorsLegend[i]}",  showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            fig12.add_trace(trace_detect, row=5, col=1)
        result2 = np.nanmean(Exec_time[:, :, :, :, i, 5])
        if not (result2 == 0 or np.isnan(result2)):
            trace_descr = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=f"-{DescriptorsLegend[i]}",showlegend=True, text=[f"{result2:.3f}"], marker=dict(color = colors[14*i]))
            fig12.add_trace(trace_descr, row=5, col=2)
        
    fig12.update_layout(updatemenus=[   dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.015),
                                        dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis.type" : "linear"}]),
                                                        dict(label="Log",   method="relayout", args=[{"yaxis.type" : "log"}])], x=0, xanchor="left", y=1.015),
                                        dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis2.type": "linear"}]),
                                                        dict(label="Log",   method="relayout", args=[{"yaxis2.type": "log"}])], x=0, xanchor="left", y=0.80),
                                        dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis3.type": "linear"}]),
                                                        dict(label="Log",   method="relayout", args=[{"yaxis3.type": "log"}])], x=0, xanchor="left", y=0.59),
                                        dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis4.type": "linear"}]),
                                                        dict(label="Log",   method="relayout", args=[{"yaxis4.type": "log"}])], x=0, xanchor="left", y=0.38),
                                        dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis5.type": "linear"}]),
                                                        dict(label="Log",   method="relayout", args=[{"yaxis5.type": "log"}])], x=0, xanchor="left", y=0.17),
                                        dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis6.type": "linear"}]),
                                                        dict(label="Log",   method="relayout", args=[{"yaxis6.type": "log"}])], x=0.5, xanchor="left", y=0.175)])
    fig12.write_html(f"./html/{data}/{data}_timing.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}_timing.html", "a") as f:
        f.write(custom_html)

def single_timing2(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig13 = go.Figure()
    fig13.update_layout(title_text=f"<b>{data.upper()} Data - Timings</b>", title_x=0.5, title_xanchor="right", yaxis_title="1/Inlier Time", hovermode="x", margin=dict(l=20, r=20, t=60, b=20))
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    x_data = [
                        np.nanmean(Rate[:, m, c3, i, j, 13]),  # Precision
                        np.nanmean(Rate[:, m, c3, i, j, 12]),  # Recall
                        np.nanmean(Rate[:, m, c3, i, j, 14]),  # Repeatibility
                        np.nanmean(Rate[:, m, c3, i, j, 15]),  # F1 Score
                        np.nanmean(Rate[:, m, c3, i, j,  9]),  # Inliers
                        np.nanmean(Rate[:, m, c3, i, j, 10])   # Matches
                    ]
                    inlierTime = np.nanmean(Exec_time[:, m, c3, i, j, 7]) # 1K feature Inlier Time
                    if not (inlierTime == 0 or np.isnan(inlierTime) or np.isnan(x_data).any()):
                        trace = go.Scatter( x=x_data, y=[1/inlierTime], mode="markers", 
                                            marker=dict(color=colors[color_index], size=10, symbol=symbol_index),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>")
                        traces.append(trace)
                        fig13.add_trace(trace)
                    symbol_index = (symbol_index + 1) % 27
            color_index = (color_index + 14) % num_combinations
    dropdown_xaxis = ["Precision", "Recall", "Repeatibility", "F1Score", "Inliers", "Matches"]
    button_list = []
    for idx, xaxis in enumerate(dropdown_xaxis):
        button_list.append(dict( label=xaxis, method="update", args=[{"x": [[trace.x[idx]] for trace in traces]}]))
    
    fig13.update_layout(updatemenus=[   dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.045),
                                        dict(type="dropdown", buttons=button_list, direction="up", x=0.55, y=-0.03)])
    fig13.write_html(f"./html/{data}/{data}_timing2.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/{data}/{data}_timing2.html", "a") as f:
        f.write(custom_html)
        
###############################
# MARK: Synthetic Timing Mobile
###############################
def synthetic_timing_mobile():
    fig15 = go.Figure()
    fig15 = make_subplots(  rows=5, cols=2, subplot_titles=[   "Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)",
                                                                "Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)",
                                                                "Average 1k Total time (Detect + Descript + Match(BF+FL))",
                                                                "Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)",
                                                                "Average 1k Detect time",
                                                                "Average 1k Describe time"],
                            specs=[[{"colspan": 2}, None], [{"colspan": 2}, None],[{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}]], horizontal_spacing=0.05, vertical_spacing=0.06)
    fig15.update_layout(title_text=f"<b>Synthetic Data Timings</b>", title_x=0.5, barmode="stack", height=2000, margin=dict(l=20, r=20, t=60, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 6], Exec_time_scale[:, m, :, i, j, 6], Exec_time_rot[:, m, :, i, j, 6]), axis=0))
                result3m= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, m, :, i, j, 6], Exec_time_scale_mobile[:, m, :, i, j, 6], Exec_time_rot_mobile[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 7], Exec_time_scale[:, m, :, i, j, 7], Exec_time_rot[:, m, :, i, j, 7]), axis=0))
                result4m= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, m, :, i, j, 7], Exec_time_scale_mobile[:, m, :, i, j, 7], Exec_time_rot_mobile[:, m, :, i, j, 7]), axis=0))
                if not (result3 == 0 or np.isnan(result3) or result3m == 0 or np.isnan(result3m)):
                    trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["pc"]], y=[result3],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-p",
                                                        text=[f"{result3:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig15.add_trace(trace_match_synt_result3,  row=1, col=1) if m == 0 else fig15.add_trace(trace_match_synt_result3,  row=2, col=1)
                    trace_match_synt_result3m= go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["mobile"]], y=[result3m],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total-m",
                                                        text=[f"{result3m:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig15.add_trace(trace_match_synt_result3m, row=1, col=1) if m == 0 else fig15.add_trace(trace_match_synt_result3m, row=2, col=1)
                    
                    trace_match_synt_result3.showlegend = False
                    fig15.add_trace(trace_match_synt_result3,  row=3, col=1)
                    trace_match_synt_result3m.showlegend = False
                    fig15.add_trace(trace_match_synt_result3m, row=3, col=1)
                if not (result4 == 0 or np.isnan(result4) or result4m == 0 or np.isnan(result4m)):
                    trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]+'-'+DescriptorsLegend[j]], ["pc"]], y=[result4],
                                                        name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier-p",
                                                        text=[f"{result4:.3f}"], marker_color=colors[color_index],
                                                        showlegend=True, legendgroup=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}", hovertemplate="<b>%{y:.3f}</b>")
                    fig15.add_trace(trace_match_synt_result4,  row=1, col=1) if m == 0 else fig15.add_trace(trace_match_synt_result4,  row=2, col=1)
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
        result = np.nanmean(np.concatenate((Exec_time_intensity[:, :, :, i, :, 4], Exec_time_scale[:, :, :, i, :, 4], Exec_time_rot[:, :, :, i, :, 4]), axis=0))
        resultm= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, :, :, i, :, 4], Exec_time_scale_mobile[:, :, :, i, :, 4], Exec_time_rot_mobile[:, :, :, i, :, 4]), axis=0))
        if not (result == 0 or np.isnan(result) or resultm == 0 or np.isnan(resultm)):
            trace_detect_synt  = go.Bar(x=[[DetectorsLegend[i]],["pc"]],     y=[result],  name=f".{DetectorsLegend[i]}-p",    showlegend=True,  text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            trace_detect_syntm = go.Bar(x=[[DetectorsLegend[i]],["mobile"]], y=[resultm], name=f".{DetectorsLegend[i]}-m",  showlegend=True,  text=[f"{resultm:.3f}"], marker=dict(color = colors[14*i]))
            fig15.add_trace(trace_detect_synt,  row=5, col=1)
            fig15.add_trace(trace_detect_syntm, row=5, col=1)
        
        result2 = np.nanmean(np.concatenate((Exec_time_intensity[:, :, :, :, i, 5], Exec_time_scale[:, :, :, :, i, 5], Exec_time_rot[:, :, :, :, i, 5]), axis=0))
        result2m= np.nanmean(np.concatenate((Exec_time_intensity_mobile[:, :, :, :, i, 5], Exec_time_scale_mobile[:, :, :, :, i, 5], Exec_time_rot_mobile[:, :, :, :, i, 5]), axis=0))
        if not (result2 == 0 or np.isnan(result2) or result2m == 0 or np.isnan(result2m)):
            trace_descr_synt  = go.Bar(x=[[DescriptorsLegend[i]],["pc"]],     y=[result2],  name=f"-{DescriptorsLegend[i]}-p",   showlegend=True, text=[f"{result2:.3f}"],  marker=dict(color = colors[14*i]))
            trace_descr_syntm = go.Bar(x=[[DescriptorsLegend[i]],["mobile"]], y=[result2m], name=f"-{DescriptorsLegend[i]}-m", showlegend=True, text=[f"{result2m:.3f}"], marker=dict(color = colors[14*i]))
            fig15.add_trace(trace_descr_synt,  row=5, col=2)
            fig15.add_trace(trace_descr_syntm, row=5, col=2)
        
    fig15.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.015),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis.type" : "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis.type" : "log"}])], x=0, xanchor="left", y=1.015),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis2.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis2.type": "log"}])], x=0, xanchor="left", y=0.80),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis3.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis3.type": "log"}])], x=0, xanchor="left", y=0.59),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis4.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis4.type": "log"}])], x=0, xanchor="left", y=0.38),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis5.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis5.type": "log"}])], x=0, xanchor="left", y=0.17),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis6.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis6.type": "log"}])], x=0.5, xanchor="left", y=0.175)])
    fig15.write_html("./html/synthetic/synthetic_timing_mobile.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open("./html/synthetic/synthetic_timing_mobile.html", "a") as f:
        f.write(custom_html)
        
############################
# MARK: Oxford Timing Mobile
############################
def oxford_timing_mobile():
    fig6 = go.Figure()
    fig6 = make_subplots(  rows=5, cols=2, subplot_titles=[ "Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)",
                                                            "Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)",
                                                            "Average 1k Total time (Detect + Descript + Match(BF+FL))",
                                                            "Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)",
                                                            "Average 1k Detect time",
                                                            "Average 1k Describe time"],
                            specs=[[{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{}, {}]], horizontal_spacing=0.05, vertical_spacing=0.06)
    fig6.update_layout(title_text="<b>Oxford Affine Dataset Timings</b>", title_x=0.5, barmode="stack", height=2000, margin=dict(l=20, r=20, t=60, b=20), hovermode="x unified")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 6], Exec_time_wall[:, m, :, i, j, 6], Exec_time_trees[:, m, :, i, j, 6], Exec_time_bikes[:, m, :, i, j, 6], Exec_time_bark[:, m, :, i, j, 6], Exec_time_boat[:, m, :, i, j, 6], Exec_time_leuven[:, m, :, i, j, 6], Exec_time_ubc[:, m, :, i, j, 6]), axis=0))
                result3m= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, m, :, i, j, 6], Exec_time_wall_mobile[:, m, :, i, j, 6], Exec_time_trees_mobile[:, m, :, i, j, 6], Exec_time_bikes_mobile[:, m, :, i, j, 6], Exec_time_bark_mobile[:, m, :, i, j, 6], Exec_time_boat_mobile[:, m, :, i, j, 6], Exec_time_leuven_mobile[:, m, :, i, j, 6], Exec_time_ubc_mobile[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 7], Exec_time_wall[:, m, :, i, j, 7], Exec_time_trees[:, m, :, i, j, 7], Exec_time_bikes[:, m, :, i, j, 7], Exec_time_bark[:, m, :, i, j, 7], Exec_time_boat[:, m, :, i, j, 7], Exec_time_leuven[:, m, :, i, j, 7], Exec_time_ubc[:, m, :, i, j, 7]), axis=0))
                result4m= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, m, :, i, j, 7], Exec_time_wall_mobile[:, m, :, i, j, 7], Exec_time_trees_mobile[:, m, :, i, j, 7], Exec_time_bikes_mobile[:, m, :, i, j, 7], Exec_time_bark_mobile[:, m, :, i, j, 7], Exec_time_boat_mobile[:, m, :, i, j, 7], Exec_time_leuven_mobile[:, m, :, i, j, 7], Exec_time_ubc_mobile[:, m, :, i, j, 7]), axis=0))
                if not (result3 == 0 or np.isnan(result3) or result3m == 0 or np.isnan(result3m)):
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
                if not (result4 == 0 or np.isnan(result4) or result4m == 0 or np.isnan(result4m)):
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
        if not (result == 0 or np.isnan(result) or resultm == 0 or np.isnan(resultm)):
            trace_detect_oxford = go.Bar(x=[[DetectorsLegend[i]],["pc"]],     y=[result],  name=f".{DetectorsLegend[i]}-p",   showlegend=True, text=[f"{result:.3f}"],  marker=dict(color = colors[14*i]))
            trace_detect_oxfordm= go.Bar(x=[[DetectorsLegend[i]],["mobile"]], y=[resultm], name=f".{DetectorsLegend[i]}-m", showlegend=True, text=[f"{resultm:.3f}"], marker=dict(color = colors[14*i]))
            fig6.add_trace(trace_detect_oxford,  row=5, col=1)
            fig6.add_trace(trace_detect_oxfordm, row=5, col=1)
        
        result2 = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, :, i, 5], Exec_time_wall[:, :, :, :, i, 5], Exec_time_trees[:, :, :, :, i, 5], Exec_time_bikes[:, :, :, :, i, 5], Exec_time_bark[:, :, :, :, i, 5], Exec_time_boat[:, :, :, :, i, 5], Exec_time_leuven[:, :, :, :, i, 5], Exec_time_ubc[:, :, :, :, i, 5]), axis=0))
        result2m= np.nanmean(np.concatenate((Exec_time_graf_mobile[:, :, :, :, i, 5], Exec_time_wall_mobile[:, :, :, :, i, 5], Exec_time_trees_mobile[:, :, :, :, i, 5], Exec_time_bikes_mobile[:, :, :, :, i, 5], Exec_time_bark_mobile[:, :, :, :, i, 5], Exec_time_boat_mobile[:, :, :, :, i, 5], Exec_time_leuven_mobile[:, :, :, :, i, 5], Exec_time_ubc_mobile[:, :, :, :, i, 5]), axis=0))
        if not (result2 == 0 or np.isnan(result2) or result2m == 0 or np.isnan(result2m)):
            trace_descr_oxford = go.Bar(x=[[DescriptorsLegend[i]],["pc"]],     y=[result2],  name=f"-{DescriptorsLegend[i]}-p",   showlegend=True, text=[f"{result2:.3f}"],  marker=dict(color = colors[14*i]))
            trace_descr_oxfordm= go.Bar(x=[[DescriptorsLegend[i]],["mobile"]], y=[result2m], name=f"-{DescriptorsLegend[i]}-m", showlegend=True, text=[f"{result2m:.3f}"], marker=dict(color = colors[14*i]))
            fig6.add_trace(trace_descr_oxford,  row=5, col=2)
            fig6.add_trace(trace_descr_oxfordm, row=5, col=2)
        
    fig6.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.015),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis.type" : "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis.type" : "log"}])], x=0, xanchor="left", y=1.015),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis2.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis2.type": "log"}])], x=0, xanchor="left", y=0.80),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis3.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis3.type": "log"}])], x=0, xanchor="left", y=0.59),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis4.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis4.type": "log"}])], x=0, xanchor="left", y=0.38),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis5.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis5.type": "log"}])], x=0, xanchor="left", y=0.175),
                                    dict(buttons=[  dict(label="Linear",method="relayout", args=[{"yaxis6.type": "linear"}]),
                                                    dict(label="Log",   method="relayout", args=[{"yaxis6.type": "log"}])], x=0.5, xanchor="left", y=0.175)])
    fig6.write_html("./html/oxford/oxford_timing_mobile.html", include_plotlyjs="cdn", full_html=True, config=config)
    with open(f"./html/oxford/oxford_timing_mobile.html", "a") as f:
        f.write(custom_html)

################################
# MARK: Reprojection Error from Rate 11
################################        
def rep_err(data="drone"):
    Exec_time = np.load(f"./arrays/Exec_time_{data}.npy")
    Rate = np.load(f"./arrays/Rate_{data}.npy")
    fig14 = go.Figure()
    fig14.update_layout(title_text=f"<b>{data} Reprojection Error</b>", title_x=0.5, title_xanchor="right", xaxis_title="pixel", yaxis_title="1/Inlier Time", hovermode="x", margin=dict(l=20, r=20, t=60, b=20), uirevision="73")
    color_index = 0
    symbol_index = 0
    traces = []
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2):
                for m in range(2):
                    x_data = [np.nanmean(Rate[:, m, c3, i, j, 11])]
                    inlierTime = np.nanmean(Exec_time[:, m, c3, i, j, 7]) # 1K feature Inlier Time
                    if not (inlierTime == 0 or np.isnan(inlierTime) or np.isnan(x_data).any()):
                        trace = go.Scatter( x=x_data, y=[1/inlierTime], mode="markers", 
                                            marker=dict(color=colors[color_index], size=10, symbol=symbol_index),
                                            name=f".{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}",
                                            showlegend=True, hovertemplate="x: <b>%{x:.3f}</b> | y: <b>%{y:.3f}</b>")
                        traces.append(trace)
                        fig14.add_trace(trace)
                    symbol_index = (symbol_index + 1) % 27
            color_index = (color_index + 14) % num_combinations
    
    fig14.update_layout(updatemenus=[   dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.045)])
    file = f"./html/{data}/{data}_reprojection_error.html"
    fig14.write_html(file, include_plotlyjs="cdn", full_html=True, config=config)
    with open(file, "a") as f:
        f.write(custom_html)