import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from define import *

custom_html = '''
    <div style="position: absolute; top: 20px; left: 20px; z-index: 1000;">
        <span style="margin: 20px;">
            <input type="text" id="filterInput" oninput="applyFilters()" placeholder="Method">
        </span>
        <span style="left: 20px;">
            <label for="minValueInput">Min:</label>
            <input type="number" id="minValueInput" class="min-range" step="0.1" oninput="applyFilters()">
            <label for="maxValueInput">Max:</label>
            <input type="number" id="maxValueInput" class="max-range" step="0.1" oninput="applyFilters()">
        </span>
    </div>
    <script>
    function applyFilters() {
        var input, filter, minInput, maxInput, minThreshold, maxThreshold;
        var i, j;
        input = document.getElementById('filterInput');
        filter = input.value.toUpperCase();
        minInput = document.getElementById('minValueInput');
        maxInput = document.getElementById('maxValueInput');
        minThreshold = parseFloat(minInput.value);
        maxThreshold = parseFloat(maxInput.value);
        if (isNaN(minThreshold)) minThreshold = -Infinity;
        if (isNaN(maxThreshold)) maxThreshold = Infinity;
        var plot = document.querySelectorAll('.js-plotly-plot')[0];
        var data = plot.data;
        // Apply both filters
        for (i = 0; i < data.length; i++) {
            var traceName = data[i].name || "";
            var yValues = data[i].y;
            var showTrace = false;
            // Check name filter
            if (traceName.toUpperCase().indexOf(filter) > -1) {
                // If there's a name filter, check the value filter
                if (yValues) {
                    for (j = 0; j < yValues.length; j++) {
                        if (yValues[j] >= minThreshold && yValues[j] <= maxThreshold) {
                            showTrace = true;
                            break;
                        }
                    }
                } else {
                    showTrace = true; // No y-values, just based on name filter
                }
            }
            // Set visibility based on combined filters
            data[i].visible = showTrace ? true : false;
        }
        // Redraw the plot with updated visibility
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
                            horizontal_spacing=0.05, vertical_spacing=0.07, y_title=f"{name}")
    fig1.update_layout(title_text=f"Synthetic Dataset - {name}", title_x=0.45, hovermode='x', margin=dict(l=60, r=0, t=60, b=25))
    fig1.update_layout(xaxis = dict(tickvals = val_b), xaxis2 = dict(tickvals = val_c), xaxis3 = dict(tickvals = scale), xaxis4 = dict(tickvals = rot))
    fig1.update_yaxes(range=[0, 1])
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1 = Rate_intensity[:len(val_b), m, c3, i, j, rate]
                    Rate2_I2 = Rate_intensity[len(val_c):, m, c3, i, j, rate]
                    Rate2_S  = Rate_scale    [          :, m, c3, i, j, rate]
                    Rate2_R  = Rate_rot      [          :, m, c3, i, j, rate]
                    color = colors[color_index]
                    style = line_styles[j % len(line_styles)]
                    legend_groupfig1 = f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}'
                    if not (np.isnan(Rate2_I1).any()):
                        fig1trace_I1    = go.Scatter(x=val_b, y=Rate2_I1, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=True,  legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_I1, row=1, col=1)
                    if not (np.isnan(Rate2_I2).any()):   
                        fig1trace_I2    = go.Scatter(x=val_c, y=Rate2_I2, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_I2, row=1, col=2)
                    if not (np.isnan(Rate2_S).any()):              
                        fig1trace_Scale = go.Scatter(x=scale, y=Rate2_S,  mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_Scale,  row=2, col=1)
                    if not (np.isnan(Rate2_R).any()):
                        fig1trace_Rot   = go.Scatter(x=rot,   y=Rate2_R,  mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_Rot,  row=2, col=2)
                    color_index += 1
    # Dropdown for Detector
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [detector == trace.legendgroup.split('-')[0] for trace in fig1.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    # Dropdown for Descriptor
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [descriptor == trace.legendgroup.split('-')[1] for trace in fig1.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig1.data)},{"title": "Synthetic Dataset - {name}"}])
    fig1.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.04),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.04)
        ]
    )
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
    fig1 = make_subplots(   rows=2, cols=2, subplot_titles=['Intensity changing I+b', 'Intensity changing Ixc', 'Scale changing', 'Rotation changing'],
                            horizontal_spacing=0.05, vertical_spacing=0.07, x_title='Recall', y_title='Precision')
    fig1.update_layout(title_text=f"Synthetic Dataset - {name}", title_x=0.45, hovermode='x', margin=dict(l=60, r=0, t=60, b=60))
    fig1.update_xaxes(range=[0, 1])
    fig1.update_yaxes(range=[0, 1])
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate2_I1_x = Rate_intensity[:len(val_b), m, c3, i, j, x]
                    Rate2_I1_y = Rate_intensity[:len(val_b), m, c3, i, j, y]
                    Rate2_I2_x = Rate_intensity[len(val_c):, m, c3, i, j, x]
                    Rate2_I2_y = Rate_intensity[len(val_c):, m, c3, i, j, y]
                    Rate2_S_x  = Rate_scale    [          :, m, c3, i, j, x]
                    Rate2_S_y  = Rate_scale    [          :, m, c3, i, j, y]
                    Rate2_R_x  = Rate_rot      [          :, m, c3, i, j, x]
                    Rate2_R_y  = Rate_rot      [          :, m, c3, i, j, y]
                    color = colors[color_index]
                    style = line_styles[j % len(line_styles)]
                    legend_groupfig1 = f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}'
                    if not (np.isnan(Rate2_I1_x).any()) and not (np.isnan(Rate2_I1_y).any()):
                        fig1trace_I1    = go.Scatter(x=Rate2_I1_x, y=Rate2_I1_y, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig1, showlegend=True,  legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_I1, row=1, col=1)
                    if not (np.isnan(Rate2_I2_x).any()) and not (np.isnan(Rate2_I2_y).any()):
                        fig1trace_I2    = go.Scatter(x=Rate2_I2_x, y=Rate2_I2_y, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name='',               showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_I2, row=1, col=2)
                    if not (np.isnan(Rate2_S_x).any()) and not (np.isnan(Rate2_S_y).any()):
                        fig1trace_Scale = go.Scatter(x=Rate2_S_x, y=Rate2_S_y, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name='',               showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_Scale, row=2, col=1)
                    if not (np.isnan(Rate2_R_x).any()) and not (np.isnan(Rate2_R_y).any()):
                        fig1trace_Rot   = go.Scatter(x=Rate2_R_x, y=Rate2_R_y, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name='',               showlegend=False, legendgroup=legend_groupfig1)
                        fig1.add_trace(fig1trace_Rot, row=2, col=2)
                    color_index += 1
    # Dropdown for Detector
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [detector == trace.legendgroup.split('-')[0] for trace in fig1.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    # Dropdown for Descriptor
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [descriptor == trace.legendgroup.split('-')[1] for trace in fig1.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig1.data)},{"title": "Synthetic Dataset - {name}"}])
    fig1.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.03),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.03)
        ]
    )
    fig1.write_html(f"./html/synthetic_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/synthetic_{name}.html', 'a') as f:
        f.write(custom_html)

###########################
# MARK: - Synthetic Timing
###########################
def synthetic_timing():
    Exec_time_intensity = np.load('./arrays/Exec_time_intensity.npy')
    Exec_time_scale     = np.load('./arrays/Exec_time_scale.npy')
    Exec_time_rot       = np.load('./arrays/Exec_time_rot.npy')
    fig25 = make_subplots(  rows=5, cols=2, subplot_titles=['Average 1k Detect time',
                                                            'Average 1k Describe time',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)',
                                                            'Average 1k Total time (Detect + Descript + Match(BF+FL))',
                                                            'Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)',],
                            specs=[[{}, {}], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.07)
    fig25.update_layout(title_text=f"Synthetic Data Timings", title_x=0.5, margin=dict(l=20, r=0, t=60, b=25), barmode='stack', height=2600)
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                color_index += 28
                result3 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 6], Exec_time_scale[:, m, :, i, j, 6], Exec_time_rot[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_intensity[:, m, :, i, j, 7], Exec_time_scale[:, m, :, i, j, 7], Exec_time_rot[:, m, :, i, j, 7]), axis=0))
                if (np.isnan(result3) or np.isnan(result4)):
                    continue
                trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result3],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total',
                                                    text=[f'{result3:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig25.add_trace(trace_match_synt_result3, row=2, col=1) if m == 0 else fig25.add_trace(trace_match_synt_result3, row=3, col=1)
                trace_match_synt_result3.showlegend = False
                fig25.add_trace(trace_match_synt_result3, row=4, col=1)
                trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result4], #base=-result4,
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier',
                                                    text=[f'{result4:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig25.add_trace(trace_match_synt_result4, row=2, col=1) if m == 0 else fig25.add_trace(trace_match_synt_result4, row=3, col=1)
                trace_match_synt_result4.showlegend = False
                fig25.add_trace(trace_match_synt_result4, row=5, col=1)
    # Detector Time
    color_index = 0
    for i in range(len(DetectorsLegend)):
        result = np.nanmean(np.concatenate((Exec_time_intensity[:, :, :, i, :, 4], Exec_time_scale[:, :, :, i, :, 4], Exec_time_rot[:, :, :, i, :, 4]), axis=0))
        trace_detect_synt = go.Bar(x=[DetectorsLegend[i]], y=[result], name=DetectorsLegend[i], showlegend=True, text=[f'{result:.3f}'], textposition='auto', marker=dict(color = colors[color_index%num_combinations]))
        fig25.add_trace(trace_detect_synt, row=1, col=1)
        color_index += 56
    # Descriptor Time
    color_index = 0
    for j in range(len(DescriptorsLegend)):
        result2 = np.nanmean(np.concatenate((Exec_time_intensity[:, :, :, :, j, 5], Exec_time_scale[:, :, :, :, j, 5], Exec_time_rot[:, :, :, :, j, 5]), axis=0))
        trace_descr_synt = go.Bar(x=[DescriptorsLegend[j]], y=[result2], name=DescriptorsLegend[j], showlegend=True, text=[f'{result2:.3f}'], textposition='auto', marker=dict(color = colors[color_index%num_combinations]))
        fig25.add_trace(trace_descr_synt, row=1, col=2)
        color_index += 56
    ## Filters (Dropdowns) Reset Button
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [trace.legendgroup is not None and detector == trace.legendgroup.split('-')[0] for trace in fig25.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [trace.legendgroup is not None and descriptor == trace.legendgroup.split('-')[1] for trace in fig25.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig25.data)},{"title": "Synthetic Dataset Timings"}])
    fig25.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=0.98, y=1.015),
            dict(buttons=dropdown_detectors,   x=1.07, y=1.015),
            dict(buttons=dropdown_descriptors, x=1.14, y=1.015)
        ]
    )
    fig25.write_html("./html/synthetic_timing.html", include_plotlyjs='cdn', full_html=True)
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
    fig2 = make_subplots(   rows=3, cols=3, subplot_titles=['Graf(Viewpoint)', 'Bikes(Blur)', 'Boat(Zoom + Rotation)', 'Leuven(Light)', 'Wall(Viewpoint)', 'Trees(Blur)', 'Bark(Zoom + Rotation)', 'UBC(JPEG)', 'Overall'],
                            horizontal_spacing=0.04, vertical_spacing=0.06, y_title=f"{name}")
    fig2.update_layout(title_text=f"Oxford Affine Dataset - {name}", title_x=0.45, hovermode='x', margin=dict(l=60, r=0, t=60, b=25))
    xvals = ["Img2", "Img3", "Img4", "Img5", "Img6"]
    fig2.update_layout( xaxis  = dict(tickmode = 'array', tickvals = xvals),xaxis2 = dict(tickmode = 'array', tickvals = xvals),xaxis3 = dict(tickmode = 'array', tickvals = xvals),
                        xaxis4 = dict(tickmode = 'array', tickvals = xvals),xaxis5 = dict(tickmode = 'array', tickvals = xvals),xaxis6 = dict(tickmode = 'array', tickvals = xvals),
                        xaxis7 = dict(tickmode = 'array', tickvals = xvals),xaxis8 = dict(tickmode = 'array', tickvals = xvals),xaxis9 = dict(tickmode = 'array', tickvals = xvals))
    fig2.update_yaxes(range=[0, 1])
    color_index = 0
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
                    color = colors[color_index]
                    style = line_styles[j % len(line_styles)]
                    legend_groupfig2 = f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}'
                    if not (np.isnan(Rate_Graf).any()):
                        fig2trace_Graf   = go.Scatter(x = xvals, y=Rate_Graf,   mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=True)
                        fig2.add_trace(fig2trace_Graf, row=1, col=1)
                    if not (np.isnan(Rate_Bikes).any()):
                        fig2trace_Bikes  = go.Scatter(x = xvals, y=Rate_Bikes,  mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Bikes, row=1, col=2)
                    if not (np.isnan(Rate_Boat).any()):
                        fig2trace_Boat   = go.Scatter(x = xvals, y=Rate_Boat,   mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Boat, row=1, col=3)
                    if not (np.isnan(Rate_Leuven).any()):
                        fig2trace_Leuven = go.Scatter(x = xvals, y=Rate_Leuven, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Leuven, row=2, col=1)
                    if not (np.isnan(Rate_Wall).any()):
                        fig2trace_Wall   = go.Scatter(x = xvals, y=Rate_Wall,   mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Wall, row=2, col=2)
                    if not (np.isnan(Rate_Trees).any()):
                        fig2trace_Trees  = go.Scatter(x = xvals, y=Rate_Trees,  mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Trees, row=2, col=3)
                    if not (np.isnan(Rate_Bark).any()):
                        fig2trace_Bark   = go.Scatter(x = xvals, y=Rate_Bark,   mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Bark, row=3, col=1)
                    if not (np.isnan(Rate_Ubc).any()):
                        fig2trace_Ubc    = go.Scatter(x = xvals, y=Rate_Ubc,    mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Ubc, row=3, col=2)
                    fig2trace_overall = go.Scatter(x = xvals, y=np.nanmean([Rate_Graf, Rate_Bikes, Rate_Boat, Rate_Leuven, Rate_Wall, Rate_Trees, Rate_Bark, Rate_Ubc], axis=0), mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                    fig2.add_trace(fig2trace_overall, row=3, col=3)
                    color_index += 1
    # Dropdown for Detector
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [detector == trace.legendgroup.split('-')[0] for trace in fig2.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    # Dropdown for Descriptor
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [descriptor == trace.legendgroup.split('-')[1] for trace in fig2.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig2.data)},{"title": "Oxford Dataset - {name}"}])
    fig2.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.03),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.03)
        ]
    )
    fig2.write_html(f"./html/oxford_{name}.html", include_plotlyjs='cdn', full_html=True)
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
    fig2 = make_subplots(   rows=3, cols=3, subplot_titles=['Graf(Viewpoint)', 'Bikes(Blur)', 'Boat(Zoom + Rotation)', 'Leuven(Light)', 'Wall(Viewpoint)', 'Trees(Blur)', 'Bark(Zoom + Rotation)', 'UBC(JPEG)', 'Overall'],
                            horizontal_spacing=0.06, vertical_spacing=0.06, x_title='Recall', y_title='Precision')
    fig2.update_layout(title_text=f"Oxford Affine Dataset - {name}", title_x=0.45, hovermode='x')
    fig2.update_layout(margin=dict(l=60, r=0, t=60, b=60))
    fig2.update_xaxes(range=[0, 1])
    fig2.update_yaxes(range=[0, 1])
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_Graf_x  = Rate_graf  [:, m, c3, i, j, x]
                    Rate_Graf_y  = Rate_graf  [:, m, c3, i, j, y]
                    Rate_Bikes_x = Rate_bikes [:, m, c3, i, j, x]
                    Rate_Bikes_y = Rate_bikes [:, m, c3, i, j, y]
                    Rate_Boat_x  = Rate_boat  [:, m, c3, i, j, x]
                    Rate_Boat_y  = Rate_boat  [:, m, c3, i, j, y]
                    Rate_Leuven_x= Rate_leuven[:, m, c3, i, j, x]
                    Rate_Leuven_y= Rate_leuven[:, m, c3, i, j, y]
                    Rate_Wall_x  = Rate_wall  [:, m, c3, i, j, x]
                    Rate_Wall_y  = Rate_wall  [:, m, c3, i, j, y]
                    Rate_Trees_x = Rate_trees [:, m, c3, i, j, x]
                    Rate_Trees_y = Rate_trees [:, m, c3, i, j, y]
                    Rate_Bark_x  = Rate_bark  [:, m, c3, i, j, x]
                    Rate_Bark_y  = Rate_bark  [:, m, c3, i, j, y]
                    Rate_Ubc_x   = Rate_ubc   [:, m, c3, i, j, x]
                    Rate_Ubc_y   = Rate_ubc   [:, m, c3, i, j, y]
                    color = colors[color_index]
                    style = line_styles[j % len(line_styles)]
                    legend_groupfig2 = f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}'
                    if not (np.isnan(Rate_Graf_x).any()) and not (np.isnan(Rate_Graf_y).any()):
                        fig2trace_Graf   = go.Scatter(x=Rate_Graf_x,   y=Rate_Graf_y,   mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=True)
                        fig2.add_trace(fig2trace_Graf, row=1, col=1)
                    if not (np.isnan(Rate_Bikes_x).any()) and not (np.isnan(Rate_Bikes_y).any()):
                        fig2trace_Bikes  = go.Scatter(x=Rate_Bikes_x,  y=Rate_Bikes_y,  mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Bikes, row=1, col=2)
                    if not (np.isnan(Rate_Boat_x).any()) and not (np.isnan(Rate_Boat_y).any()):
                        fig2trace_Boat   = go.Scatter(x=Rate_Boat_x,   y=Rate_Boat_y,   mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Boat, row=1, col=3)
                    if not (np.isnan(Rate_Leuven_x).any()) and not (np.isnan(Rate_Leuven_y).any()):
                        fig2trace_Leuven = go.Scatter(x=Rate_Leuven_x, y=Rate_Leuven_y, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Leuven, row=2, col=1)
                    if not (np.isnan(Rate_Wall_x).any()) and not (np.isnan(Rate_Wall_y).any()):
                        fig2trace_Wall   = go.Scatter(x=Rate_Wall_x,   y=Rate_Wall_y,   mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Wall, row=2, col=2)
                    if not (np.isnan(Rate_Trees_x).any()) and not (np.isnan(Rate_Trees_y).any()):
                        fig2trace_Trees  = go.Scatter(x=Rate_Trees_x,  y=Rate_Trees_y,  mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Trees, row=2, col=3)
                    if not (np.isnan(Rate_Bark_x).any()) and not (np.isnan(Rate_Bark_y).any()):
                        fig2trace_Bark   = go.Scatter(x=Rate_Bark_x,   y=Rate_Bark_y,   mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Bark, row=3, col=1)
                    if not (np.isnan(Rate_Ubc_x).any()) and not (np.isnan(Rate_Ubc_y).any()):
                        fig2trace_Ubc    = go.Scatter(x=Rate_Ubc_x,    y=Rate_Ubc_y,    mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                        fig2.add_trace(fig2trace_Ubc, row=3, col=2)
                    fig2trace_overall = go.Scatter( x=np.nanmean([Rate_Graf_x, Rate_Bikes_x, Rate_Boat_x, Rate_Leuven_x, Rate_Wall_x, Rate_Trees_x, Rate_Bark_x, Rate_Ubc_x], axis=0),
                                                    y=np.nanmean([Rate_Graf_y, Rate_Bikes_y, Rate_Boat_y, Rate_Leuven_y, Rate_Wall_y, Rate_Trees_y, Rate_Bark_y, Rate_Ubc_y], axis=0),
                                                    mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=legend_groupfig2, legendgroup=legend_groupfig2, showlegend=False)
                    fig2.add_trace(fig2trace_overall, row=3, col=3)
                    color_index += 1
    # Dropdown for Detector
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [detector == trace.legendgroup.split('-')[0] for trace in fig2.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    # Dropdown for Descriptor
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [descriptor == trace.legendgroup.split('-')[1] for trace in fig2.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig2.data)},{"title": "Oxford Dataset - {name}"}])
    fig2.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.03),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.03)
        ]
    )
    fig2.write_html(f"./html/oxford_{name}.html", include_plotlyjs='cdn', full_html=True)
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
    fig55 = make_subplots(  rows=5, cols=2, subplot_titles=['Average 1k Detect time',
                                                            'Average 1k Describe time',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)',
                                                            'Average 1k Total time (Detect + Descript + Match(BF+FL))',
                                                            'Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)',],
                            specs=[[{}, {}], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.07)
    fig55.update_layout(title_text="Oxford Affine Dataset - Timing", title_x=0.5, margin=dict(l=20, r=0, t=60, b=25), barmode='stack', height=2600)
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                color_index += 28        
                result3 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 6], Exec_time_wall[:, m, :, i, j, 6], Exec_time_trees[:, m, :, i, j, 6], Exec_time_bikes[:, m, :, i, j, 6], Exec_time_bark[:, m, :, i, j, 6], Exec_time_boat[:, m, :, i, j, 6], Exec_time_leuven[:, m, :, i, j, 6], Exec_time_ubc[:, m, :, i, j, 6]), axis=0))
                result4 = np.nanmean(np.concatenate((Exec_time_graf[:, m, :, i, j, 7], Exec_time_wall[:, m, :, i, j, 7], Exec_time_trees[:, m, :, i, j, 7], Exec_time_bikes[:, m, :, i, j, 7], Exec_time_bark[:, m, :, i, j, 7], Exec_time_boat[:, m, :, i, j, 7], Exec_time_leuven[:, m, :, i, j, 7], Exec_time_ubc[:, m, :, i, j, 7]), axis=0))
                if (np.isnan(result3) or np.isnan(result4)):
                    continue
                trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result3],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total',
                                                    text=[f'{result3:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig55.add_trace(trace_match_synt_result3, row=2, col=1) if m == 0 else fig55.add_trace(trace_match_synt_result3, row=3, col=1)
                trace_match_synt_result3.showlegend = False
                fig55.add_trace(trace_match_synt_result3, row=4, col=1)
                trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result4], #base=-result4,
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier',
                                                    text=[f'{result4:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig55.add_trace(trace_match_synt_result4, row=2, col=1) if m == 0 else fig55.add_trace(trace_match_synt_result4, row=3, col=1)
                trace_match_synt_result4.showlegend = False
                fig55.add_trace(trace_match_synt_result4, row=5, col=1)
    # Detector time
    color_index = 0
    for i in range(len(DetectorsLegend)):
        result = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, i, :, 4], Exec_time_wall[:, :, :, i, :, 4], Exec_time_trees[:, :, :, i, :, 4], Exec_time_bikes[:, :, :, i, :, 4], Exec_time_bark[:, :, :, i, :, 4], Exec_time_boat[:, :, :, i, :, 4], Exec_time_leuven[:, :, :, i, :, 4], Exec_time_ubc[:, :, :, i, :, 4]), axis=0))
        trace_detect_oxford = go.Bar(x=[DetectorsLegend[i]], y=[result], name=DetectorsLegend[i], showlegend=True, text=[f'{result:.3f}'], textposition='auto')
        fig55.add_trace(trace_detect_oxford, row=1, col=1)
        color_index += 56
    # Descriptor time
    color_index = 0
    for j in range(len(DescriptorsLegend)):
        result2 = np.nanmean(np.concatenate((Exec_time_graf[:, :, :, :, j, 5], Exec_time_wall[:, :, :, :, j, 5], Exec_time_trees[:, :, :, :, j, 5], Exec_time_bikes[:, :, :, :, j, 5], Exec_time_bark[:, :, :, :, j, 5], Exec_time_boat[:, :, :, :, j, 5], Exec_time_leuven[:, :, :, :, j, 5], Exec_time_ubc[:, :, :, :, j, 5]), axis=0))
        trace_descr_oxford = go.Bar(x=[DescriptorsLegend[j]], y=[result2], name=DescriptorsLegend[j], showlegend=True, text=[f'{result2:.3f}'], textposition='auto')
        fig55.add_trace(trace_descr_oxford, row=1, col=2)
        color_index += 56
    ## Filters (Dropdowns) Reset Button
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [trace.legendgroup is not None and detector == trace.legendgroup.split('-')[0] for trace in fig55.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [trace.legendgroup is not None and descriptor == trace.legendgroup.split('-')[1] for trace in fig55.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig55.data)},{"title": "Oxford Dataset Timings"}])
    fig55.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.01),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.01)
        ]
    )
    fig55.write_html("./html/oxford_timing.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/oxford_timing.html', 'a') as f:
        f.write(custom_html)

####################
# MARK: - Drone Data
####################
def drone(name='Precision', rate=13):
    Rate_drone = np.load('./arrays/Rate_drone.npy')
    fig551 = go.Figure()
    xvals = [f'Img{i}' for i in range(153, 188)]
    fig551.update_layout(title_text=f"Drone Data - {name}", title_x=0.5, hovermode='x', margin=dict(l=60, r=0, t=60, b=25), xaxis = dict(tickmode = 'array', tickvals = xvals))
    fig551.update_yaxes(range=[0, 1], title_text=f"{name}")
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_dr  = Rate_drone [:, m, c3, i, j, rate]
                    color = colors[color_index%num_combinations]
                    style = line_styles[j % len(line_styles)]
                    if not (np.isnan(Rate_dr).any()):
                        fig551trace_Drone  = go.Scatter(x=xvals, y=Rate_dr, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}', showlegend=True)
                        fig551.add_trace(fig551trace_Drone)
                    color_index += 14
    # Dropdown for Detector
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [detector == trace.name.split('-')[0] for trace in fig551.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    # Dropdown for Descriptor
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [descriptor == trace.name.split('-')[1] for trace in fig551.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig551.data)},{"title": "Drone Dataset - {name}"}])
    fig551.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.03),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.03)
        ]
    )
    fig551.write_html(f"./html/drone_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/drone_{name}.html', 'a') as f:
        f.write(custom_html)

#####################################
# MARK: - Drone Data Precision-Recall
#####################################
def dronePR(name='Precision-Recall', x=13, y=12):
    Rate_drone = np.load('./arrays/Rate_drone.npy')
    fig551 = go.Figure()
    xvals = [f'Img{i}' for i in range(153, 188)]
    fig551.update_layout(title_text=f"Drone Data - {name}", title_x=0.5, hovermode='x', margin=dict(l=60, r=0, t=60, b=60), xaxis = dict(tickmode = 'array', tickvals = xvals))
    fig551.update_yaxes(range=[0, 1], title_text="Precision")
    fig551.update_xaxes(range=[0, 1], title_text="Recall") 
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_dr_x = Rate_drone [:, m, c3, i, j, x]
                    Rate_dr_y = Rate_drone [:, m, c3, i, j, y]
                    color = colors[color_index%num_combinations]
                    style = line_styles[j % len(line_styles)]
                    if not (np.isnan(Rate_dr_x).any()) and not (np.isnan(Rate_dr_y).any()):
                        fig551trace_Drone  = go.Scatter(x=Rate_dr_x, y=Rate_dr_y, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}', showlegend=True)
                        fig551.add_trace(fig551trace_Drone)
                    color_index += 14
    # Dropdown for Detector
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [detector == trace.name.split('-')[0] for trace in fig551.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    # Dropdown for Descriptor
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [descriptor == trace.name.split('-')[1] for trace in fig551.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig551.data)},{"title": "Drone Dataset - {name}"}])
    fig551.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.03),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.03)
        ]
    )
    fig551.write_html(f"./html/drone_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/drone_{name}.html', 'a') as f:
        f.write(custom_html)

######################
# MARK: - Drone Timing
######################
def drone_timing():
    Exec_time_drone = np.load('./arrays/Exec_time_drone.npy')  
    fig56 = make_subplots(  rows=5, cols=2, subplot_titles=['Average 1k Detect time',
                                                            'Average 1k Describe time',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)',
                                                            'Average 1k Total time (Detect + Descript + Match(BF+FL))',
                                                            'Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)',],
                            specs=[[{}, {}], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.07)
    fig56.update_layout(title_text="Drone Data Timing", title_x=0.5, margin=dict(l=20, r=20, t=60, b=25), barmode='stack', height=2600)
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                color_index += 28
                result3 = np.nanmean(Exec_time_drone[:, m, :, i, j, 6])
                result4 = np.nanmean(Exec_time_drone[:, m, :, i, j, 7])
                if (np.isnan(result3) or np.isnan(result4)):
                    continue
                trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result3],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total',
                                                    text=[f'{result3:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig56.add_trace(trace_match_synt_result3, row=2, col=1) if m == 0 else fig56.add_trace(trace_match_synt_result3, row=3, col=1)
                trace_match_synt_result3.showlegend = False
                fig56.add_trace(trace_match_synt_result3, row=4, col=1)
                trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result4], #base=-result4,
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier',
                                                    text=[f'{result4:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig56.add_trace(trace_match_synt_result4, row=2, col=1) if m == 0 else fig56.add_trace(trace_match_synt_result4, row=3, col=1)
                trace_match_synt_result4.showlegend = False
                fig56.add_trace(trace_match_synt_result4, row=5, col=1)
    # Detector time
    color_index = 0
    for i in range(len(DetectorsLegend)):
        result = np.nanmean(Exec_time_drone[:, :, :, i, :, 4])
        trace_detect_drone = go.Bar(x=[DetectorsLegend[i]], y=[result], name=DetectorsLegend[i], showlegend=True, text=[f'{result:.3f}'], textposition='auto')
        fig56.add_trace(trace_detect_drone, row=1, col=1)
        color_index += 56
    # Descriptor time
    color_index = 0
    for j in range(len(DescriptorsLegend)):
        result2 = np.nanmean(Exec_time_drone[:, :, :, :, j, 5])
        trace_descr_drone = go.Bar(x=[DescriptorsLegend[j]], y=[result2], name=DescriptorsLegend[j], showlegend=True, text=[f'{result2:.3f}'], textposition='auto')
        fig56.add_trace(trace_descr_drone, row=1, col=2)
        color_index += 56
    ## Filters (Dropdowns) Reset Button
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [trace.legendgroup is not None and detector == trace.legendgroup.split('-')[0] for trace in fig56.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [trace.legendgroup is not None and descriptor == trace.legendgroup.split('-')[1] for trace in fig56.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig56.data)},{"title": "Drone Dataset Timings"}])
    fig56.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.01),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.01)
        ]
    )
    fig56.write_html("./html/drone_timing.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/drone_timing.html', 'a') as f:
        f.write(custom_html)

##################
# MARK: - UAV Data
##################
def uav(name='Precision', rate=13):
    Rate_uav = np.load('./arrays/Rate_uav.npy')
    fig552 = go.Figure()
    xvals = ['Bahamas', 'Office', 'Suburban', 'Building', 'Construction', 'Dominica', 'Cadastre', 'Rivaz', 'Urban', 'Belleview']
    fig552.update_layout(title_text=f"UAV Data - {name}", title_x=0.5, hovermode='x', margin=dict(l=60, r=0, t=60, b=25), xaxis = dict(tickmode = 'array', tickvals = xvals))
    fig552.update_yaxes(range=[0, 1], title_text=f"{name}") 
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_u  = Rate_uav [:, m, c3, i, j, rate]
                    color = colors[color_index%num_combinations]
                    style = line_styles[j % len(line_styles)]
                    if not (np.isnan(Rate_u).any()):
                        fig552trace_UAV  = go.Scatter(x=xvals, y=Rate_u, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}', showlegend=True)
                        fig552.add_trace(fig552trace_UAV)
                    color_index += 14
    # Dropdown for Detector
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [detector == trace.name.split('-')[0] for trace in fig552.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    # Dropdown for Descriptor
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [descriptor == trace.name.split('-')[1] for trace in fig552.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig552.data)},{"title": "UAV Dataset - {name}"}])
    fig552.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.03),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.03)
        ]
    )
    fig552.write_html(f"./html/uav_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/uav_{name}.html', 'a') as f:
        f.write(custom_html)
    
###################################
# MARK: - UAV Data Precision-Recall
###################################
def uavPR(name='Precision-Recall', x=13, y=12):
    Rate_uav = np.load('./arrays/Rate_uav.npy')
    fig552 = go.Figure()
    xvals = ['Bahamas', 'Office', 'Suburban', 'Building', 'Construction', 'Dominica', 'Cadastre', 'Rivaz', 'Urban', 'Belleview']
    fig552.update_layout(title_text=f"UAV Data - {name}", title_x=0.5, hovermode='x', margin=dict(l=60, r=20, t=60, b=25), xaxis = dict(tickmode = 'array', tickvals = xvals))
    fig552.update_yaxes(range=[0, 1], title_text="Precision")
    fig552.update_xaxes(range=[0, 1], title_text="Recall") 
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for c3 in range(2): # Normalization Type 0: L2 1: Hamming
                for m in range(2): # Matcher 0: BruteForce 1: FlannBased
                    Rate_u_x = Rate_uav [:, m, c3, i, j, x]
                    Rate_u_y = Rate_uav [:, m, c3, i, j, y]
                    color = colors[color_index%num_combinations]
                    style = line_styles[j % len(line_styles)]
                    if not (np.isnan(Rate_u_x).any()) and not (np.isnan(Rate_u_y).any()):
                        fig552trace_UAV  = go.Scatter(x=Rate_u_x, y=Rate_u_y, mode='lines+markers', marker_symbol=raw_symbols[color_index%56], marker_size=7, line=dict(color=color, dash=style), name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Norm[c3]}-{Matcher[m]}', showlegend=True)
                        fig552.add_trace(fig552trace_UAV)
                    color_index += 14
    # Dropdown for Detector
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [detector == trace.name.split('-')[0] for trace in fig552.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    # Dropdown for Descriptor
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [descriptor == trace.name.split('-')[1] for trace in fig552.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig552.data)},{"title": "UAV Dataset - {name}"}])
    fig552.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.03),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.03)
        ]
    )
    fig552.write_html(f"./html/uav_{name}.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/uav_{name}.html', 'a') as f:
        f.write(custom_html)

####################
# MARK: - UAV Timing
####################
def uav_timing():
    Exec_time_uav = np.load('./arrays/Exec_time_uav.npy')  
    fig57 = make_subplots(  rows=5, cols=2, subplot_titles=['Average 1k Detect time',
                                                            'Average 1k Describe time',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(Brute Force) | RANSAC)',
                                                            'Average 1k Total & Inlier time (Detect + Descript + Match(FLANN) | RANSAC)',
                                                            'Average 1k Total time (Detect + Descript + Match(BF+FL))',
                                                            'Average 1k Inlier time (Detect + Descript + Match(BF+FL) + RANSAC)',],
                            specs=[[{}, {}], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None], [{"colspan": 2}, None]], horizontal_spacing=0.05, vertical_spacing=0.07)
    fig57.update_layout(title_text="UAV Data - Timing", title_x=0.5, margin=dict(l=20, r=20, t=60, b=25), barmode='stack', height=2600)
    color_index = 0
    for i in range(len(DetectorsLegend)):
        for j in range(len(DescriptorsLegend)):
            for m in range(2):
                color_index += 28
                result3 = np.nanmean(Exec_time_uav[:, m, :, i, j, 6])
                result4 = np.nanmean(Exec_time_uav[:, m, :, i, j, 7])
                if (np.isnan(result3) or np.isnan(result4)):
                    continue
                trace_match_synt_result3 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result3],
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-total',
                                                    text=[f'{result3:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig57.add_trace(trace_match_synt_result3, row=2, col=1) if m == 0 else fig57.add_trace(trace_match_synt_result3, row=3, col=1)
                trace_match_synt_result3.showlegend = False
                fig57.add_trace(trace_match_synt_result3, row=4, col=1)
                trace_match_synt_result4 = go.Bar(  x=[[DetectorsLegend[i]], [DescriptorsLegend[j]], [Matcher[m]]], y=[result4], #base=-result4,
                                                    name=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}-{Matcher[m]}-inlier',
                                                    text=[f'{result4:.3f}'], marker=dict(color = colors[color_index%num_combinations]),
                                                    showlegend=True, legendgroup=f'{DetectorsLegend[i]}-{DescriptorsLegend[j]}')
                fig57.add_trace(trace_match_synt_result4, row=2, col=1) if m == 0 else fig57.add_trace(trace_match_synt_result4, row=3, col=1)
                trace_match_synt_result4.showlegend = False
                fig57.add_trace(trace_match_synt_result4, row=5, col=1)
                
    # Detector time
    color_index = 0
    for i in range(len(DetectorsLegend)):
        result = np.nanmean(Exec_time_uav[:, :, :, i, :, 4])
        trace_detect_uav = go.Bar(x=[DetectorsLegend[i]], y=[result], name=DetectorsLegend[i], showlegend=True, text=[f'{result:.3f}'], textposition='auto')
        fig57.add_trace(trace_detect_uav, row=1, col=1)
        color_index += 56
    # Descriptor time
    color_index = 0
    for j in range(len(DescriptorsLegend)):
        result2 = np.nanmean(Exec_time_uav[:, :, :, :, j, 5])
        trace_descr_uav = go.Bar(x=[DescriptorsLegend[j]], y=[result2], name=DescriptorsLegend[j], showlegend=True, text=[f'{result2:.3f}'], textposition='auto')
        fig57.add_trace(trace_descr_uav, row=1, col=2)
        color_index += 56
    ## Filters (Dropdowns) Reset Button
    dropdown_detectors = []
    for detector in DetectorsLegend:
        visible = [trace.legendgroup is not None and detector == trace.legendgroup.split('-')[0] for trace in fig57.data]
        dropdown_detectors.append(dict(label=detector, method="update", args=[{"visible": visible}, {"title": f"Filtered by Detector: {detector}"}]))
    dropdown_descriptors = []
    for descriptor in DescriptorsLegend:
        visible = [trace.legendgroup is not None and descriptor == trace.legendgroup.split('-')[1] for trace in fig57.data]
        dropdown_descriptors.append(dict(label=descriptor, method="update", args=[{"visible": visible}, {"title": f"Filtered by Descriptor: {descriptor}"}]))
    reset_button = dict(label="Reset", method="update", args=[{"visible": [True] * len(fig57.data)},{"title": "UAV Dataset Timings"}])
    fig57.update_layout(
        updatemenus=[
            dict(type="buttons", buttons=[reset_button], x=1.10, y=0),
            dict(buttons=dropdown_detectors,   x=1.05, y=1.01),
            dict(buttons=dropdown_descriptors, x=1.15, y=1.01)
        ]
    )
    fig57.write_html("./html/uav_timing.html", include_plotlyjs='cdn', full_html=True)
    with open(f'./html/uav_timing.html', 'a') as f:
        f.write(custom_html)
    