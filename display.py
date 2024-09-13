import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from define import *

custom_html = '''
    <div style="position: fixed; top: 12px; left: 10px;">
        <span style="margin: 20px;">
            <input type="text" id="filterInput" size="15" onchange="applyFilters()" placeholder="and|or method">
            <input type="number" id="minYValueInput" min="0" max="99" step="0.05" onchange="applyFilters()" placeholder="min y">
            <input type="number" id="maxYValueInput" min="0" max="99" step="0.05" onchange="applyFilters()" placeholder="max y">
            <input type="number" id="minXValueInput" min="0" max="99" step="0.05" onchange="applyFilters()" placeholder="min x">
            <input type="number" id="maxXValueInput" min="0" max="99" step="0.05" onchange="applyFilters()" placeholder="max x">
        </span>
    </div>
    <script>
    function applyFilters() {
        var i, j;
        var filter = document.getElementById('filterInput').value.toUpperCase();
        var minYThreshold = parseFloat(document.getElementById('minYValueInput').value) || -Infinity;
        var maxYThreshold = parseFloat(document.getElementById('maxYValueInput').value) || Infinity;
        var minXThreshold = parseFloat(document.getElementById('minXValueInput').value) || -Infinity;
        var maxXThreshold = parseFloat(document.getElementById('maxXValueInput').value) || Infinity;
        var plot = document.querySelectorAll('.js-plotly-plot')[0];
        var data = plot.data;
        
        var filterParts = filter.split(" ");
        var logicKeyword = filterParts.shift() || "";
        var filterWords = filterParts;
        var filterFunction = word => {
            if (logicKeyword === "AND") {
                return filterWords.every(filterWord => word.includes(filterWord));
            } else if (logicKeyword === "OR") {
                return filterWords.some(filterWord => word.includes(filterWord));
            }
            return true; // Default case when no filter input is provided
        };
        for (i = 0; i < data.length; i++) {
            var traceName = data[i].name || "";
            var yValues = data[i].y;
            var xValues = data[i].x;
            var showTrace = false;
            if (filterFunction(traceName.toUpperCase())) {
                for (j = 0; j < yValues.length; j++) {
                    if (yValues[j] >= minYThreshold && yValues[j] <= maxYThreshold) {
                        if (xValues[j] >= minXThreshold && xValues[j] <= maxXThreshold) {
                            showTrace = true;
                            break;
                        }
                        if (isNaN(xValues[j])) {
                            showTrace = true;
                            break;
                        }
                    }
                }
            }
            data[i].visible = showTrace;
        }
        Plotly.redraw(plot);
    }
    </script>
'''

########################
# MARK: - Synthetic Data
########################
def synthetic(name='Precision', rate=13):
    Rate_intensity = np.load('./arrays/Rate_intensity.npy')
    Rate_scale     = np.load('./arrays/Rate_scale.npy')
    Rate_rot       = np.load('./arrays/Rate_rot.npy')
    fig1 = make_subplots(   rows=2, cols=2, subplot_titles=['Intensity changing I+b', 'Intensity changing Ixc', 'Scale changing', 'Rotation changing'],
                            horizontal_spacing=0.05, vertical_spacing=0.07, y_title=name)
    fig1.update_layout(title_text=f"Synthetic Dataset - {name}", title_x=0.45, hovermode='closest', margin=dict(l=60, r=60, t=60, b=60))
    fig1.update_layout(xaxis = dict(tickvals = val_b), xaxis2 = dict(tickvals = val_c), xaxis3 = dict(tickvals = scale), xaxis4 = dict(tickvals = rot))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1 = Rate_intensity[:len(val_b), m, c3, i, j, rate]
                    Rate2_I2 = Rate_intensity[len(val_c):, m, c3, i, j, rate]
                    Rate2_S  = Rate_scale    [          :, m, c3, i, j, rate]
                    Rate2_R  = Rate_rot      [          :, m, c3, i, j, rate]
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    legend_groupfig1 = f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}'
                    if not (np.isnan(Rate2_I1).any()):
                        fig1trace_I1    = go.Scatter(x=val_b, y=Rate2_I1, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=True,  legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_I1,   row=1, col=1)
                    if not (np.isnan(Rate2_I2).any()):   
                        fig1trace_I2    = go.Scatter(x=val_c, y=Rate2_I2, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_I2,   row=1, col=2)
                    if not (np.isnan(Rate2_S).any()):              
                        fig1trace_Scale = go.Scatter(x=scale, y=Rate2_S,  mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_Scale, row=2, col=1)
                    if not (np.isnan(Rate2_R).any()):
                        fig1trace_Rot   = go.Scatter(x=rot,   y=Rate2_R,  mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_Rot,   row=2, col=2)
                    symbol_index = (symbol_index + 1) % 27
            color_index += 26
    fig1.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig1.write_html(f"./html/synthetic_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/synthetic_{name}.html', 'a') as f:
        f.write(custom_html)

#########################################
# MARK: - Synthetic Data Precision-Recall
#########################################
def syntheticPR(name='Precision-Recall', x=13, y=12):
    Rate_intensity = np.load('./arrays/Rate_intensity.npy')
    Rate_scale     = np.load('./arrays/Rate_scale.npy')
    Rate_rot       = np.load('./arrays/Rate_rot.npy')
    fig2 = make_subplots(   rows=2, cols=2, subplot_titles=['Intensity changing I+b', 'Intensity changing Ixc', 'Scale changing', 'Rotation changing'],
                            horizontal_spacing=0.05, vertical_spacing=0.07, x_title=name.split('-')[0], y_title=name.split('-')[1])
    fig2.update_layout(title_text=f"Synthetic Dataset - {name}", title_x=0.45, hovermode='closest', margin=dict(l=60, r=60, t=60, b=60))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1_x = np.sort(Rate_intensity[:len(val_b), m, c3, i, j, x])
                    Rate2_I1_y = np.sort(Rate_intensity[:len(val_b), m, c3, i, j, y])
                    Rate2_I2_x = np.sort(Rate_intensity[len(val_c):, m, c3, i, j, x])
                    Rate2_I2_y = np.sort(Rate_intensity[len(val_c):, m, c3, i, j, y])
                    Rate2_S_x  = np.sort(Rate_scale    [          :, m, c3, i, j, x])
                    Rate2_S_y  = np.sort(Rate_scale    [          :, m, c3, i, j, y])
                    Rate2_R_x  = np.sort(Rate_rot      [          :, m, c3, i, j, x])
                    Rate2_R_y  = np.sort(Rate_rot      [          :, m, c3, i, j, y])
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    legend_groupfig2 = f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}'
                    if not (np.isnan(Rate2_I1_x).any()) and not (np.isnan(Rate2_I1_y).any()):
                        fig2trace_I1    = go.Scatter(x=Rate2_I1_x, y=Rate2_I1_y, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, showlegend=True,  legendgroup=legend_groupfig2)
                        fig2.add_trace(fig2trace_I1, row=1, col=1)
                    if not (np.isnan(Rate2_I2_x).any()) and not (np.isnan(Rate2_I2_y).any()):
                        fig2trace_I2    = go.Scatter(x=Rate2_I2_x, y=Rate2_I2_y, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, showlegend=False, legendgroup=legend_groupfig2)
                        fig2.add_trace(fig2trace_I2, row=1, col=2)
                    if not (np.isnan(Rate2_S_x).any()) and not (np.isnan(Rate2_S_y).any()):
                        fig2trace_Scale = go.Scatter(x=Rate2_S_x, y=Rate2_S_y,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, showlegend=False, legendgroup=legend_groupfig2)
                        fig2.add_trace(fig2trace_Scale, row=2, col=1)
                    if not (np.isnan(Rate2_R_x).any()) and not (np.isnan(Rate2_R_y).any()):
                        fig2trace_Rot   = go.Scatter(x=Rate2_R_x, y=Rate2_R_y,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, showlegend=False, legendgroup=legend_groupfig2)
                        fig2.add_trace(fig2trace_Rot, row=2, col=2)
                    symbol_index = (symbol_index + 1) % 27
            color_index += 26
    fig2.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig2.write_html(f"./html/synthetic_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/synthetic_{name}.html', 'a') as f:
        f.write(custom_html)

###########################
# MARK: - Synthetic Timing
###########################
def synthetic_timing():
    Exec_time_intensity = np.load('./arrays/Exec_time_intensity.npy')
    Exec_time_scale     = np.load('./arrays/Exec_time_scale.npy')
    Exec_time_rot       = np.load('./arrays/Exec_time_rot.npy')
    fig3 = make_subplots(  rows=5, cols=2, subplot_titles=['Average 1k Detect time',
                                                            'Average 1k Describe time',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)',
                                                            'Average 1k Total time (Detect + Descript + Match(BF+FL))',
                                                            'Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)',],
                            specs=[[{}, {}], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.07)
    fig3.update_layout(title_text=f"Synthetic Data Timings", title_x=0.5, margin=dict(l=60, r=60, t=60, b=60), barmode='stack', height=2600)
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 6], Exec_time_scale[:, m, :, i, j, 6], Exec_time_rot[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 7], Exec_time_scale[:, m, :, i, j, 7], Exec_time_rot[:, m, :, i, j, 7]), axis=0))
                if (np.isnan(result3) or np.isnan(result4)):
                    continue
                trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result3],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total',
                                                    text=[f'{result3:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig3.add_trace(trace_match_synt_result3, row=2, col=1) if m == 0 else fig3.add_trace(trace_match_synt_result3, row=3, col=1)
                trace_match_synt_result3.showlegend = False
                fig3.add_trace(trace_match_synt_result3, row=4, col=1)
                trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result4], #base=-result4,
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier',
                                                    text=[f'{result4:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig3.add_trace(trace_match_synt_result4, row=2, col=1) if m == 0 else fig3.add_trace(trace_match_synt_result4, row=3, col=1)
                trace_match_synt_result4.showlegend = False
                fig3.add_trace(trace_match_synt_result4, row=5, col=1)
            color_index = (color_index + 28) % num_combinations
        result = np.nanmean(np.concatenate((Exec_time_intensity[:, :, :, i, :, 4], Exec_time_scale[:, :, :, i, :, 4], Exec_time_rot[:, :, :, i, :, 4]), axis=0))
        trace_detect_synt = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=DetectorsLegend[i],  showlegend=True,  text=[f'{result:.3f}'],  marker=dict(color = colors[14*i]))
        fig3.add_trace(trace_detect_synt, row=1, col=1)
        result2 = np.nanmean(np.concatenate((Exec_time_intensity[:, :, :, :, i, 5], Exec_time_scale[:, :, :, :, i, 5], Exec_time_rot[:, :, :, :, i, 5]), axis=0))
        trace_descr_synt = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=DescriptorsLegend[i], showlegend=True, text=[f'{result2:.3f}'], marker=dict(color = colors[14*i]))
        fig3.add_trace(trace_descr_synt, row=1, col=2)

    fig3.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.015)])
    fig3.write_html("./html/synthetic_timing.html", include_plotlyjs='cdn', full_html=True)
    with open('./html/synthetic_timing.html', 'a') as f:
        f.write(custom_html)

##################################
# MARK: - Oxford all 8 and Overall
##################################
def oxford(name='Precision', rate=13):
    Rate_graf   = np.load('./arrays/Rate_graf.npy')
    Rate_bikes  = np.load('./arrays/Rate_bikes.npy')
    Rate_boat   = np.load('./arrays/Rate_boat.npy')
    Rate_leuven = np.load('./arrays/Rate_leuven.npy')
    Rate_wall   = np.load('./arrays/Rate_wall.npy')
    Rate_trees  = np.load('./arrays/Rate_trees.npy')
    Rate_bark   = np.load('./arrays/Rate_bark.npy')
    Rate_ubc    = np.load('./arrays/Rate_ubc.npy')
    fig4 = make_subplots(   rows=3, cols=3, subplot_titles=['Graf(Viewpoint)', 'Bikes(Blur)', 'Boat(Zoom + Rotation)', 'Leuven(Light)', 'Wall(Viewpoint)', 'Trees(Blur)', 'Bark(Zoom + Rotation)', 'UBC(JPEG)', 'Overall'],
                            horizontal_spacing=0.05, vertical_spacing=0.07, y_title=name)
    xvals = ["Img2", "Img3", "Img4", "Img5", "Img6"]
    fig4.update_layout( title_text=f"Oxford Affine Dataset - {name}", title_x=0.45, hovermode='closest', margin=dict(l=60, r=60, t=60, b=60),
                        xaxis  = dict(tickmode = 'array', tickvals = xvals),xaxis2 = dict(tickmode = 'array', tickvals = xvals),xaxis3 = dict(tickmode = 'array', tickvals = xvals),
                        xaxis4 = dict(tickmode = 'array', tickvals = xvals),xaxis5 = dict(tickmode = 'array', tickvals = xvals),xaxis6 = dict(tickmode = 'array', tickvals = xvals),
                        xaxis7 = dict(tickmode = 'array', tickvals = xvals),xaxis8 = dict(tickmode = 'array', tickvals = xvals),xaxis9 = dict(tickmode = 'array', tickvals = xvals))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_Graf  = Rate_graf  [:, m, c3, i, j, rate]
                    Rate_Bikes = Rate_bikes [:, m, c3, i, j, rate]
                    Rate_Boat  = Rate_boat  [:, m, c3, i, j, rate]
                    Rate_Leuven= Rate_leuven[:, m, c3, i, j, rate]
                    Rate_Wall  = Rate_wall  [:, m, c3, i, j, rate]
                    Rate_Trees = Rate_trees [:, m, c3, i, j, rate]
                    Rate_Bark  = Rate_bark  [:, m, c3, i, j, rate]
                    Rate_Ubc   = Rate_ubc   [:, m, c3, i, j, rate]
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    legend_groupfig4 = f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}'
                    if not (np.isnan(Rate_Graf).any()):
                        fig4trace_Graf   = go.Scatter(x = xvals, y=Rate_Graf,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=True)
                        fig4.add_trace(fig4trace_Graf, row=1, col=1)
                    if not (np.isnan(Rate_Bikes).any()):
                        fig4trace_Bikes  = go.Scatter(x = xvals, y=Rate_Bikes,  mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False)
                        fig4.add_trace(fig4trace_Bikes, row=1, col=2)
                    if not (np.isnan(Rate_Boat).any()):
                        fig4trace_Boat   = go.Scatter(x = xvals, y=Rate_Boat,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False)
                        fig4.add_trace(fig4trace_Boat, row=1, col=3)
                    if not (np.isnan(Rate_Leuven).any()):
                        fig4trace_Leuven = go.Scatter(x = xvals, y=Rate_Leuven, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False)
                        fig4.add_trace(fig4trace_Leuven, row=2, col=1)
                    if not (np.isnan(Rate_Wall).any()):
                        fig4trace_Wall   = go.Scatter(x = xvals, y=Rate_Wall,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False)
                        fig4.add_trace(fig4trace_Wall, row=2, col=2)
                    if not (np.isnan(Rate_Trees).any()):
                        fig4trace_Trees  = go.Scatter(x = xvals, y=Rate_Trees,  mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False)
                        fig4.add_trace(fig4trace_Trees, row=2, col=3)
                    if not (np.isnan(Rate_Bark).any()):
                        fig4trace_Bark   = go.Scatter(x = xvals, y=Rate_Bark,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False)
                        fig4.add_trace(fig4trace_Bark, row=3, col=1)
                    if not (np.isnan(Rate_Ubc).any()):
                        fig4trace_Ubc    = go.Scatter(x = xvals, y=Rate_Ubc,    mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False)
                        fig4.add_trace(fig4trace_Ubc, row=3, col=2)
                    fig4trace_overall = go.Scatter(x = xvals, y=np.nanmean([Rate_Graf, Rate_Bikes, Rate_Boat, Rate_Leuven, Rate_Wall, Rate_Trees, Rate_Bark, Rate_Ubc], axis=0), mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig4, legendgroup=legend_groupfig4, showlegend=False)
                    fig4.add_trace(fig4trace_overall, row=3, col=3)
                    symbol_index = (symbol_index + 1) % 27
            color_index += 26
    fig4.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig4.write_html(f"./html/oxford_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/oxford_{name}.html', 'a') as f:
        f.write(custom_html)
                    
#####################################
# MARK: - Oxford all 8 and Overall PR
#####################################
def oxfordPR(name='Precision-Recall', x=13, y=12):
    Rate_graf   = np.load('./arrays/Rate_graf.npy')
    Rate_bikes  = np.load('./arrays/Rate_bikes.npy')
    Rate_boat   = np.load('./arrays/Rate_boat.npy')
    Rate_leuven = np.load('./arrays/Rate_leuven.npy')
    Rate_wall   = np.load('./arrays/Rate_wall.npy')
    Rate_trees  = np.load('./arrays/Rate_trees.npy')
    Rate_bark   = np.load('./arrays/Rate_bark.npy')
    Rate_ubc    = np.load('./arrays/Rate_ubc.npy')
    fig5 = make_subplots(   rows=3, cols=3, subplot_titles=['Graf(Viewpoint)', 'Bikes(Blur)', 'Boat(Zoom + Rotation)', 'Leuven(Light)', 'Wall(Viewpoint)', 'Trees(Blur)', 'Bark(Zoom + Rotation)', 'UBC(JPEG)', 'Overall'],
                            horizontal_spacing=0.05, vertical_spacing=0.07, x_title=name.split('-')[0], y_title=name.split('-')[1])
    fig5.update_layout(title_text=f"Oxford Affine Dataset - {name}", title_x=0.45, hovermode='closest', margin=dict(l=60, r=60, t=60, b=60))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_Graf_x  =np.sort(Rate_graf  [:, m, c3, i, j, x])
                    Rate_Graf_y  =np.sort(Rate_graf  [:, m, c3, i, j, y])
                    Rate_Bikes_x =np.sort(Rate_bikes [:, m, c3, i, j, x])
                    Rate_Bikes_y =np.sort(Rate_bikes [:, m, c3, i, j, y])
                    Rate_Boat_x  =np.sort(Rate_boat  [:, m, c3, i, j, x])
                    Rate_Boat_y  =np.sort(Rate_boat  [:, m, c3, i, j, y])
                    Rate_Leuven_x=np.sort(Rate_leuven[:, m, c3, i, j, x])
                    Rate_Leuven_y=np.sort(Rate_leuven[:, m, c3, i, j, y])
                    Rate_Wall_x  =np.sort(Rate_wall  [:, m, c3, i, j, x])
                    Rate_Wall_y  =np.sort(Rate_wall  [:, m, c3, i, j, y])
                    Rate_Trees_x =np.sort(Rate_trees [:, m, c3, i, j, x])
                    Rate_Trees_y =np.sort(Rate_trees [:, m, c3, i, j, y])
                    Rate_Bark_x  =np.sort(Rate_bark  [:, m, c3, i, j, x])
                    Rate_Bark_y  =np.sort(Rate_bark  [:, m, c3, i, j, y])
                    Rate_Ubc_x   =np.sort(Rate_ubc   [:, m, c3, i, j, x])
                    Rate_Ubc_y   =np.sort(Rate_ubc   [:, m, c3, i, j, y])
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    legend_groupfig5 = f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}'
                    if not (np.isnan(Rate_Graf_x).any()) and not (np.isnan(Rate_Graf_y).any()):
                        fig5trace_Graf   = go.Scatter(x=Rate_Graf_x,   y=Rate_Graf_y,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=True)
                        fig5.add_trace(fig5trace_Graf, row=1, col=1)
                    if not (np.isnan(Rate_Bikes_x).any()) and not (np.isnan(Rate_Bikes_y).any()):
                        fig5trace_Bikes  = go.Scatter(x=Rate_Bikes_x,  y=Rate_Bikes_y,  mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False)
                        fig5.add_trace(fig5trace_Bikes, row=1, col=2)
                    if not (np.isnan(Rate_Boat_x).any()) and not (np.isnan(Rate_Boat_y).any()):
                        fig5trace_Boat   = go.Scatter(x=Rate_Boat_x,   y=Rate_Boat_y,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False)
                        fig5.add_trace(fig5trace_Boat, row=1, col=3)
                    if not (np.isnan(Rate_Leuven_x).any()) and not (np.isnan(Rate_Leuven_y).any()):
                        fig5trace_Leuven = go.Scatter(x=Rate_Leuven_x, y=Rate_Leuven_y, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False)
                        fig5.add_trace(fig5trace_Leuven, row=2, col=1)
                    if not (np.isnan(Rate_Wall_x).any()) and not (np.isnan(Rate_Wall_y).any()):
                        fig5trace_Wall   = go.Scatter(x=Rate_Wall_x,   y=Rate_Wall_y,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False)
                        fig5.add_trace(fig5trace_Wall, row=2, col=2)
                    if not (np.isnan(Rate_Trees_x).any()) and not (np.isnan(Rate_Trees_y).any()):
                        fig5trace_Trees  = go.Scatter(x=Rate_Trees_x,  y=Rate_Trees_y,  mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False)
                        fig5.add_trace(fig5trace_Trees, row=2, col=3)
                    if not (np.isnan(Rate_Bark_x).any()) and not (np.isnan(Rate_Bark_y).any()):
                        fig5trace_Bark   = go.Scatter(x=Rate_Bark_x,   y=Rate_Bark_y,   mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False)
                        fig5.add_trace(fig5trace_Bark, row=3, col=1)
                    if not (np.isnan(Rate_Ubc_x).any()) and not (np.isnan(Rate_Ubc_y).any()):
                        fig5trace_Ubc    = go.Scatter(x=Rate_Ubc_x,    y=Rate_Ubc_y,    mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False)
                        fig5.add_trace(fig5trace_Ubc, row=3, col=2)
                    fig5trace_overall = go.Scatter( x=np.nanmean([Rate_Graf_x, Rate_Bikes_x, Rate_Boat_x, Rate_Leuven_x, Rate_Wall_x, Rate_Trees_x, Rate_Bark_x, Rate_Ubc_x], axis=0),
                                                    y=np.nanmean([Rate_Graf_y, Rate_Bikes_y, Rate_Boat_y, Rate_Leuven_y, Rate_Wall_y, Rate_Trees_y, Rate_Bark_y, Rate_Ubc_y], axis=0),
                                                    mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig5, legendgroup=legend_groupfig5, showlegend=False)
                    fig5.add_trace(fig5trace_overall, row=3, col=3)
                    symbol_index = (symbol_index + 1) % 27
            color_index += 26
    fig5.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig5.write_html(f"./html/oxford_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/oxford_{name}.html', 'a') as f:
        f.write(custom_html)

###########################
# MARK: - Oxford Timing
###########################
def oxford_timing():
    Exec_time_graf      = np.load('./arrays/Exec_time_graf.npy')
    Exec_time_bikes     = np.load('./arrays/Exec_time_bikes.npy')
    Exec_time_boat      = np.load('./arrays/Exec_time_boat.npy')
    Exec_time_leuven    = np.load('./arrays/Exec_time_leuven.npy')
    Exec_time_wall      = np.load('./arrays/Exec_time_wall.npy')
    Exec_time_trees     = np.load('./arrays/Exec_time_trees.npy')
    Exec_time_bark      = np.load('./arrays/Exec_time_bark.npy')
    Exec_time_ubc       = np.load('./arrays/Exec_time_ubc.npy')
    fig6 = make_subplots(  rows=5, cols=2, subplot_titles=['Average 1k Detect time',
                                                            'Average 1k Describe time',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)',
                                                            'Average 1k Total time (Detect + Descript + Match(BF+FL))',
                                                            'Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)',],
                            specs=[[{}, {}], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.07)
    fig6.update_layout(title_text="Oxford Affine Dataset - Timing", title_x=0.5, margin=dict(l=60, r=60, t=60, b=60), barmode='stack', height=2600)
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 6], Exec_time_wall[:, m, :, i, j, 6], Exec_time_trees[:, m, :, i, j, 6], Exec_time_bikes[:, m, :, i, j, 6], Exec_time_bark[:, m, :, i, j, 6], Exec_time_boat[:, m, :, i, j, 6], Exec_time_leuven[:, m, :, i, j, 6], Exec_time_ubc[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 7], Exec_time_wall[:, m, :, i, j, 7], Exec_time_trees[:, m, :, i, j, 7], Exec_time_bikes[:, m, :, i, j, 7], Exec_time_bark[:, m, :, i, j, 7], Exec_time_boat[:, m, :, i, j, 7], Exec_time_leuven[:, m, :, i, j, 7], Exec_time_ubc[:, m, :, i, j, 7]), axis=0))
                if (np.isnan(result3) or np.isnan(result4)):
                    continue
                trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result3],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total',
                                                    text=[f'{result3:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig6.add_trace(trace_match_synt_result3, row=2, col=1) if m == 0 else fig6.add_trace(trace_match_synt_result3, row=3, col=1)
                trace_match_synt_result3.showlegend = False
                fig6.add_trace(trace_match_synt_result3, row=4, col=1)
                trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result4],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier',
                                                    text=[f'{result4:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig6.add_trace(trace_match_synt_result4, row=2, col=1) if m == 0 else fig6.add_trace(trace_match_synt_result4, row=3, col=1)
                trace_match_synt_result4.showlegend = False
                fig6.add_trace(trace_match_synt_result4, row=5, col=1)
            color_index = (color_index + 28) % num_combinations            
        result = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, i, :, 4], Exec_time_wall[:, :, :, i, :, 4], Exec_time_trees[:, :, :, i, :, 4], Exec_time_bikes[:, :, :, i, :, 4], Exec_time_bark[:, :, :, i, :, 4], Exec_time_boat[:, :, :, i, :, 4], Exec_time_leuven[:, :, :, i, :, 4], Exec_time_ubc[:, :, :, i, :, 4]), axis=0))
        trace_detect_oxford = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=DetectorsLegend[i],  showlegend=True, text=[f'{result:.3f}'],  marker=dict(color = colors[14*i]))
        fig6.add_trace(trace_detect_oxford, row=1, col=1)
        result2 = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, :, i, 5], Exec_time_wall[:, :, :, :, i, 5], Exec_time_trees[:, :, :, :, i, 5], Exec_time_bikes[:, :, :, :, i, 5], Exec_time_bark[:, :, :, :, i, 5], Exec_time_boat[:, :, :, :, i, 5], Exec_time_leuven[:, :, :, :, i, 5], Exec_time_ubc[:, :, :, :, i, 5]), axis=0))
        trace_descr_oxford = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=DescriptorsLegend[i],showlegend=True, text=[f'{result2:.3f}'], marker=dict(color = colors[14*i]))
        fig6.add_trace(trace_descr_oxford, row=1, col=2)

    fig6.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.015)])
    fig6.write_html("./html/oxford_timing.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/oxford_timing.html', 'a') as f:
        f.write(custom_html)

####################
# MARK: - Drone Data
####################
def drone(name='Precision', rate=13):
    Rate_drone = np.load('./arrays/Rate_drone.npy')
    fig7 = go.Figure()
    xvals = [f'Img{i}' for i in range(153, 188)]
    fig7.update_layout(title_text=f"Drone Data - {name}", yaxis_title=name, title_x=0.5, hovermode='closest', margin=dict(l=60, r=60, t=60, b=60), xaxis = dict(tickmode = 'array', tickvals = xvals))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_dr  = Rate_drone [:, m, c3, i, j, rate]
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    if not (np.isnan(Rate_dr).any()):
                        fig7trace_Drone  = go.Scatter(x=xvals, y=Rate_dr, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}', showlegend=True)
                        fig7.add_trace(fig7trace_Drone)
                    symbol_index = (symbol_index + 1) % 27
            color_index += 26
    fig7.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig7.write_html(f"./html/drone_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/drone_{name}.html', 'a') as f:
        f.write(custom_html)

#####################################
# MARK: - Drone Data Precision-Recall
#####################################
def dronePR(name='Precision-Recall', x=13, y=12):
    Rate_drone = np.load('./arrays/Rate_drone.npy')
    fig8 = go.Figure()
    fig8.update_layout(title_text=f"Drone Data - {name}", xaxis_title=name.split('-')[0], yaxis_title=name.split('-')[1], title_x=0.5, hovermode='closest', margin=dict(l=60, r=60, t=60, b=60))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_dr_x = np.sort(Rate_drone [:, m, c3, i, j, x])
                    Rate_dr_y = np.sort(Rate_drone [:, m, c3, i, j, y])
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    if not (np.isnan(Rate_dr_x).any()) and not (np.isnan(Rate_dr_y).any()):
                        fig8trace_Drone  = go.Scatter(x=Rate_dr_x, y=Rate_dr_y, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}', showlegend=True)
                        fig8.add_trace(fig8trace_Drone)
                    symbol_index = (symbol_index + 1) % 27
            color_index += 26
    fig8.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig8.write_html(f"./html/drone_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/drone_{name}.html', 'a') as f:
        f.write(custom_html)

######################
# MARK: - Drone Timing
######################
def drone_timing():
    Exec_time_drone = np.load('./arrays/Exec_time_drone.npy')  
    fig9 = make_subplots(  rows=5, cols=2, subplot_titles=['Average 1k Detect time',
                                                            'Average 1k Describe time',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)',
                                                            'Average 1k Total time (Detect + Descript + Match(BF+FL))',
                                                            'Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)',],
                            specs=[[{}, {}], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.07)
    fig9.update_layout(title_text="Drone Data Timing", title_x=0.5, margin=dict(l=60, r=60, t=60, b=60), barmode='stack', height=2600)
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(Exec_time_drone[:, m, :, i, j, 6])
                result4 = np.nanmean(Exec_time_drone[:, m, :, i, j, 7])
                if (np.isnan(result3) or np.isnan(result4)):
                    continue
                trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result3],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total',
                                                    text=[f'{result3:.3f}'], marker=dict(color = colors[color_index]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig9.add_trace(trace_match_synt_result3, row=2, col=1) if m == 0 else fig9.add_trace(trace_match_synt_result3, row=3, col=1)
                trace_match_synt_result3.showlegend = False
                fig9.add_trace(trace_match_synt_result3, row=4, col=1)
                trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result4],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier',
                                                    text=[f'{result4:.3f}'], marker=dict(color = colors[color_index]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig9.add_trace(trace_match_synt_result4, row=2, col=1) if m == 0 else fig9.add_trace(trace_match_synt_result4, row=3, col=1)
                trace_match_synt_result4.showlegend = False
                fig9.add_trace(trace_match_synt_result4, row=5, col=1)
            color_index = (color_index + 28) % num_combinations
        result = np.nanmean(Exec_time_drone[:, :, :, i, :, 4])
        trace_detect_drone = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=DetectorsLegend[i],  showlegend=True, text=[f'{result:.3f}'],  marker=dict(color = colors[14*i]))
        fig9.add_trace(trace_detect_drone, row=1, col=1)
        result2 = np.nanmean(Exec_time_drone[:, :, :, :, i, 5])
        trace_descr_drone = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=DescriptorsLegend[i],showlegend=True, text=[f'{result2:.3f}'], marker=dict(color = colors[14*i]))
        fig9.add_trace(trace_descr_drone, row=1, col=2)

    fig9.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.015)])
    fig9.write_html("./html/drone_timing.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/drone_timing.html', 'a') as f:
        f.write(custom_html)

##################
# MARK: - UAV Data
##################
def uav(name='Precision', rate=13):
    Rate_uav = np.load('./arrays/Rate_uav.npy')
    fig10 = go.Figure()
    xvals = ['Bahamas', 'Office', 'Suburban', 'Building', 'Construction', 'Dominica', 'Cadastre', 'Rivaz', 'Urban', 'Belleview']
    fig10.update_layout(title_text=f"UAV Data - {name}", yaxis_title=name, title_x=0.5, hovermode='closest', margin=dict(l=60, r=60, t=60, b=60), xaxis = dict(tickmode = 'array', tickvals = xvals))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_u  = Rate_uav [:, m, c3, i, j, rate]
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    if not (np.isnan(Rate_u).any()):
                        fig10trace_UAV  = go.Scatter(x=xvals, y=Rate_u, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}', showlegend=True)
                        fig10.add_trace(fig10trace_UAV)
                    symbol_index = (symbol_index + 1) % 27
            color_index += 26
    fig10.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig10.write_html(f"./html/uav_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/uav_{name}.html', 'a') as f:
        f.write(custom_html)
    
###################################
# MARK: - UAV Data Precision-Recall
###################################
def uavPR(name='Precision-Recall', x=13, y=12):
    Rate_uav = np.load('./arrays/Rate_uav.npy')
    fig11 = go.Figure()
    fig11.update_layout(title_text=f"UAV Data - {name}", xaxis_title=name.split('-')[0], yaxis_title=name.split('-')[1], title_x=0.5, hovermode='closest', margin=dict(l=60, r=60, t=60, b=60))
    color_index = 0
    symbol_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_u_x = np.sort(Rate_uav [:, m, c3, i, j, x])
                    Rate_u_y = np.sort(Rate_uav [:, m, c3, i, j, y])
                    color = colors[color_index%num_combinations]
                    style = line_styles[(i+j) % len(line_styles)]
                    if not (np.isnan(Rate_u_x).any()) and not (np.isnan(Rate_u_y).any()):
                        fig11trace_UAV  = go.Scatter(x=Rate_u_x, y=Rate_u_y, mode='lines+markers', marker_symbol=symbol_index, marker_size=7, line=dict(color=color, dash=style), name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}', showlegend=True)
                        fig11.add_trace(fig11trace_UAV)
                    symbol_index = (symbol_index + 1) % 27
            color_index += 26
    fig11.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.06)])
    fig11.write_html(f"./html/uav_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/uav_{name}.html', 'a') as f:
        f.write(custom_html)

####################
# MARK: - UAV Timing
####################
def uav_timing():
    Exec_time_uav = np.load('./arrays/Exec_time_uav.npy')  
    fig12 = make_subplots(  rows=5, cols=2, subplot_titles=['Average 1k Detect time',
                                                            'Average 1k Describe time',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)',
                                                            'Average 1k Total time (Detect + Descript + Match(BF+FL))',
                                                            'Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)',],
                            specs=[[{}, {}], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.07)
    fig12.update_layout(title_text="UAV Data - Timing", title_x=0.5, margin=dict(l=60, r=60, t=60, b=60), barmode='stack', height=2600)
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                result3 = np.nanmean(Exec_time_uav[:, m, :, i, j, 6])
                result4 = np.nanmean(Exec_time_uav[:, m, :, i, j, 7])
                if (np.isnan(result3) or np.isnan(result4)):
                    continue
                trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result3],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total',
                                                    text=[f'{result3:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig12.add_trace(trace_match_synt_result3, row=2, col=1) if m == 0 else fig12.add_trace(trace_match_synt_result3, row=3, col=1)
                trace_match_synt_result3.showlegend = False
                fig12.add_trace(trace_match_synt_result3, row=4, col=1)
                trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result4],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier',
                                                    text=[f'{result4:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig12.add_trace(trace_match_synt_result4, row=2, col=1) if m == 0 else fig12.add_trace(trace_match_synt_result4, row=3, col=1)
                trace_match_synt_result4.showlegend = False
                fig12.add_trace(trace_match_synt_result4, row=5, col=1)
            color_index = (color_index + 28) % num_combinations
        result = np.nanmean(Exec_time_uav[:, :, :, i, :, 4])
        trace_detect_uav = go.Bar(x=[DetectorsLegend[i]],  y=[result],  name=DetectorsLegend[i],  showlegend=True, text=[f'{result:.3f}'],  marker=dict(color = colors[14*i]))
        fig12.add_trace(trace_detect_uav, row=1, col=1)
        result2 = np.nanmean(Exec_time_uav[:, :, :, :, i, 5])
        trace_descr_uav = go.Bar(x=[DescriptorsLegend[i]], y=[result2], name=DescriptorsLegend[i],showlegend=True, text=[f'{result2:.3f}'], marker=dict(color = colors[14*i]))
        fig12.add_trace(trace_descr_uav, row=1, col=2)
        
    fig12.update_layout(updatemenus=[dict(type="buttons", buttons=[dict(label="≡ Legend", method="relayout", args=["showlegend", True], args2=["showlegend", False])], x=1, y=1.015)])
    fig12.write_html("./html/uav_timing.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/uav_timing.html', 'a') as f:
        f.write(custom_html)
    