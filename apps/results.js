/**
 * Created by dora on 1/06/15.
 */

function drawLegends(id_div, params, range_min, range_max) {
    var id = "#".concat(id_div).concat("-legend");
    var div = d3.select(id).html("");

    var colours_size = params["colours_size"];
    var colours = params["colours"];

    var width_max = parseFloat(d3.select(id).style('width'));
    var height_max = window.innerHeight;
    var width_stroke = 1;
    var height_svg = height_max * 0.05;
    var width_svg = width_max;
    var width_legend = width_svg / colours_size;
    var height_legend = height_max * 0.015;

    // var value_text_ending;
    // if (id_div.includes("load")) value_text_ending = " kw/h";
    // else if (id_div.includes("price")) value_text_ending = " cent";

    var svg = div.append("svg").attr("width", width_svg).attr("height", height_svg);
    var g = svg.append("g");

    var x = 0, rect, path, text, value_text;
    for (var i = 0; i < colours_size; i++) {
        rect = g.append("rect").attr("width", width_legend - 1 + "px").attr("height", height_legend + "px")
            .attr("x", x + "px").style("fill", colours[i]);
        path = g.append("path").attr("stroke", "white").attr("stroke-width", width_stroke + "px");
        if (i % 1 == 0) {
            if (i == 0) {
                value_text = Math.round(range_min);
                text = g.append("text").attr("x", x + "px").attr("y", height_max * 0.027 + "px")
                    .text(value_text);
            }
            else {
                value_text = Math.round(range_min + (range_max - range_min) / colours_size * i);
                // value_text = value_text.toString().concat(value_text_ending);
                text = g.append("text").attr("x", x - width_legend / 9 + "px").attr("y", height_max * 0.027 + "px")
                    .text(value_text);
            }
        }
        x += width_legend;
    }
    value_text = Math.round(range_max);
    text = g.append("text").attr("x", x - width_legend / 2.5 + "px").attr("y", height_max * 0.027 + "px")
        .text(value_text);
}

function showResults(csv_file_load, csv_file_price, csv_file_cost, csv_file_sum, params_load, params_price) {

    d3.queue()
        .defer(d3.csv, csv_file_load)
        .defer(d3.csv, csv_file_price)
        .defer(d3.csv, csv_file_cost)
        .defer(d3.csv, csv_file_sum)
        .await(function (error, data_load, data_price, data_cost, data_sum) {
                var id_sum = "#summary-div";
                var whitespace = "&nbsp;&nbsp;&nbsp;&nbsp;";
                var content = data_sum[0]["households"] + " households" + whitespace;
                content += data_sum[0]["minJobs"] + " ~ " + data_sum[0]["maxJobs"] + " jobs per household" + whitespace;
                content += data_sum[0]["batteries"] + " batteries" + whitespace;
                // if (data_sum[0]["batteries"] != 0) content += "no batteries" + whitespace;
                content += parseFloat(data_sum[0]["time"]).toFixed(2) + "s" + " run time" + whitespace;

                var no_iters = data_load[data_load.length - 1]["itr"];
                var keys = Object.keys(data_load[0]);
                var no_periods = keys.length - 2;
                var type_load = "f", type_price = "f";
                var loads_fw = [], prices = [], loads_o = [], prices_o = [];

                var graph_load_class_actual = "load-graph-actual",
                    graph_load_class_expected = "load-graph-expected",
                    graph_price_class_actual = "price-graph-actual",
                    graph_price_class_expected = "price-graph-expected";
                var point_cost_class = "point-cost", point_penalty_class = "point-penalty";
                var tooltip_cost_class = "tooltip-cost", tooltip_penalty_class = "tooltip-penalty";
                var popup_load_class ="popup-load", popup_price_class = "popup-price";

                var id_table, type;
                id_table = "t-load";
                type = "o";
                drawTable(id_table, type, data_load);

                id_table = "t-fwload";
                type = "f";
                drawTable(id_table, type, data_load);

                id_table = "t-price";
                type = "f";
                drawTable(id_table, type, data_price);

                id_table = "t-oprice";
                type = "o";
                drawTable(id_table, type, data_price);

                var id_heatmap, params, scale_heatmap_x, scale_heatmap_y, scale_heatmap_peak_x;
                id_heatmap = "v-load";

                params = params_load;
                scale_heatmap_x = d3.scale.linear().domain([0, no_periods]);
                scale_heatmap_y = d3.scale.linear();
                scale_heatmap_peak_x = d3.scale.linear();
                d3.select("#v-load-heading").html("<h3>FW Loads (kw)</h3>");
                drawHeatmap(id_heatmap, loads_fw, params);

                id_heatmap = "v-price";
                params = params_price;
                drawHeatmap(id_heatmap, prices, params);

                var id_graph, scale_graph_x, scale_graph_y, scale_graph_price_y, scale_graph_load_y;
                var first_row, last_row;
                scale_graph_x = d3.scale.linear().domain([0, no_periods]);
                scale_graph_y = d3.scale.linear();

                id_graph = "v-load";
                first_row = loads_fw[0];
                last_row = loads_fw[loads_fw.length - 2];
                drawGraph(id_graph, first_row, last_row);

                id_graph = "v-price";
                first_row = prices[0];
                last_row = prices[prices.length - 2];
                drawGraph(id_graph, first_row, last_row);

                var scale_graph_cost_x, scale_graph_cost_y, scale_graph_penalty_y;
                var bills = [], penalties = [];
                scale_graph_cost_x = d3.scale.linear().domain([0, no_iters]);

                id_graph = "v-cost";
                type = type_load;
                drawCostGraph(id_graph, type, data_cost);

                id_graph = "v-penalty";
                type = type_load;
                drawCostGraph(id_graph, type, data_cost);

                var rects = d3.selectAll("rect");
                rects.on("mouseover", drawCurrentData)
                    .on("mouseout", clearDraw);

                d3.select(id_sum).html(content);

                // show the screen
                $("body").css('opacity', 1);
                $("div#divLoading").removeClass('show');

                function drawTable(id_table, type, data) {
                    var no_rows = data.length;
                    var table = d3.select("#".concat(id_table)).html("");
                    var header = table.append("thead");
                    var body = table.append("tbody");

                    header.append("th").text('Itr');
                    for (var i = 0; i < no_periods; i++) {
                        header.append("th").text(i + 1);
                    }

                    var table_loads_row, value;
                    var arr, arrs = [];
                    for (var j = 0; j < no_rows; j++) {
                        if (data[j]["type"] == type) {
                            table_loads_row = body.append("tr");
                            table_loads_row.append("td").text(data[j]["itr"]);
                            arr = [];
                            for (var k = 0; k < no_periods; k++) {
                                value = +data[j][k + 1];
                                table_loads_row.append("td").text((Math.round(value * 100) / 100).toFixed(2));
                                arr.push(value);
                            }
                            arrs.push(arr);
                        }
                    }

                    if (id_table.includes("-load")) loads_o = arrs;
                    if (id_table.includes("-fwload")) loads_fw = arrs;
                    if (id_table.includes("-price")) prices = arrs;
                    if (id_table.includes("-oprice")) prices_o = arrs;
                } // end table

                function drawHeatmap(id_heatmap_div, data, params) {
                    var no_iters1 = data.length;

                    var id_heatmap = "#".concat(id_heatmap_div).concat("-div");
                    var heatmap_div = d3.select(id_heatmap).html("");

                    var height_max = window.innerHeight;
                    var width_max = parseFloat(d3.select(id_heatmap).style('width'));
                    var width_stroke = 0;
                    var width_svg = width_max - 20;
                    var width_rect_ = width_svg / no_periods;
                    // var height_rect = height_max * 0.018;
                    // var height_svg = height_rect * no_iters1;
                    var height_svg = height_max * 0.78;
                    var height_rect = height_svg / no_iters1;
                    var heatmap_svg = heatmap_div.append("svg").attr("width", width_svg)
                        .attr("height", height_svg).append("g").attr("class", "heatmap");

                    var first_row = data[0];

                    var range_min = Math.min.apply(undefined, first_row) * 0.8;
                    var range_min = 0;
                    var range_max = Math.max.apply(undefined, first_row) * params["max_scale"];

                    scale_heatmap_x.range([0, width_svg]);
                    scale_heatmap_y.domain([0, no_iters1]).range([0, height_svg]);

                    var x, y;
                    var value1, value2, value_rect, rect, path;
                    var row_array, row_max, rows_max = [];
                    var colours_size = params["colours_size"] - 1;
                    var colours = params["colours"];

                    // load or price heat map
                    for (var j2 = 0; j2 < no_iters1; j2++) {
                        y = scale_heatmap_y(j2);
                        var g = heatmap_svg.append("g");

                        // peak demand
                        row_array = data[j2];
                        row_max = Math.max.apply(undefined, row_array);
                        rows_max.push(row_max);

                        for (var k2 = 0; k2 < no_periods; k2++) {
                            x = scale_heatmap_x(k2);

                            value1 = +data[j2][k2];
                            if (value1 == 0) value_rect = colours[0];
                            else {
                                value2 = Math.round((value1 - range_min) / (range_max - range_min) * colours_size);
                                value_rect = colours[value2];
                            }

                            rect = g.append("rect").attr("width", width_rect_ + "px")
                                .attr("height", height_rect + "px")
                                .attr("x", x + "px").attr("y", y).style("fill", value_rect);
                            // path = g.append("path").attr("y", y).attr("stroke", "white")
                            // .attr("stroke-width", width_stroke + "px");
                        }
                    }

                    // legends
                    drawLegends(id_heatmap_div, params, range_min, range_max);

                    // peak demand heat map
                    if (id_heatmap_div.includes("load")) {
                        // tooltips / popups
                        heatmap_svg.append("g").attr("class", popup_load_class);

                        var peak_heatmap_div = d3.select("#v-peak-div").html("");
                        var width_peak_heatmap_svg = parseFloat(d3.select("#v-peak-div").style('width')) - 15;
                        var peak_heatmap_svg = peak_heatmap_div.append("svg").attr("width", width_peak_heatmap_svg)
                            .attr("height", height_svg);
                        var width_text = width_peak_heatmap_svg * 0.15;
                        var width_rect_max = width_peak_heatmap_svg * 0.60;
                        var width_rect;

                        scale_heatmap_peak_x.domain([range_min, range_max]).range([0, width_rect_max]);

                        var peak_max = rows_max[0];
                        var peak_min = rows_max[rows_max.length - 1];
                        var peak_reduction = ((peak_max - peak_min) / peak_max * 100).toFixed(2);
                        // d3.select("#v-peak-legend").html("Reduction (%): " + peak_reduction).style("margin-left", 0);
                        content += peak_reduction + "% peak reduction" + whitespace;

                        for (var i3 = 0; i3 < rows_max.length; i3++) {
                            value1 = rows_max[i3];
                            if (value1 == 0) value_rect = "white";
                            else {
                                value2 = Math.round((value1 - range_min) / (range_max - range_min) * colours_size);
                                value_rect = colours[value2];
                            }

                            y = scale_heatmap_y(i3);
                            width_rect = scale_heatmap_peak_x(value1);
                            g = peak_heatmap_svg.append("g").attr("transform", "translate(" + width_text + ", 0)");
                            g.append("text").text(i3).attr("y", y + height_rect / 1.2).attr("x", -width_text);
                            g.append("rect").attr("width", width_rect + "px")
                                .attr("height", height_rect + "px").style("fill", value_rect).attr("y", y);
                            // g.append("path").attr("stroke", "white").attr("stroke-width", width_stroke + "px");
                            g.append("text").attr("x", width_rect + 10).attr("y", y + height_rect / 1.2).text(value1.toFixed(2));
                        }
                    }
                    else // tooltips / popups
                      heatmap_svg.append("g").attr("class", popup_price_class);
                }

                function drawGraph(id_graph_div, first_row, last_row) {
                    var id_graph = "#".concat(id_graph_div).concat("-graph-div");
                    var graph_div = d3.select(id_graph).html("");

                    var height_max = window.innerHeight;
                    var width_max = parseFloat(d3.select(id_graph).style('width'));

                    var width_svg = width_max - 15;
                    var width_graph = width_svg * 0.9;
                    var width_axis = width_svg * 0.1;

                    var height_svg = height_max * 0.2;
                    var height_graph = height_svg * 0.8;
                    var height_axis = height_svg * 0.2;
                    var height_margin = 8;

                    // axis
                    var y_text = "Load (kwh)";
                    var class_name = [graph_load_class_expected, graph_load_class_actual];
                    if (id_graph_div.includes("price")) {
                        y_text = "Price (cent)";
                        class_name = [graph_price_class_expected, graph_price_class_actual]
                    }
                    var svg = graph_div.append("svg").attr("width", width_svg).attr("height", height_svg)
                        .append("g").attr("transform", "translate(0, " + height_margin + ")");

                    // y axis
                    svg.append("g").append("text").attr("transform", "rotate(-90)")
                        .attr("y", width_axis * 0.2).attr("x", -height_svg / 2)
                        .attr("dy", "1em").style("text-anchor", "middle").text(y_text);
                    // x axis
                    svg.append("g").append("text").attr("transform", "translate(0, " + height_graph + ")")
                        .attr("x", width_axis + width_graph / 2).attr("dy", height_axis * 0.6)
                        .style("text-anchor", "middle").text("Periods");



                    var x1, y1 = 0, x2 = 0, y2 = 0, y1_2, y2_2;

                    x1 = width_axis;
                    var value;
                    var line = svg.append("g").attr("transform", "translate(0, " + height_graph + ")");
                    var line2 = svg.append("g").attr("transform", "translate(0, " + height_graph + ")");
                    // line - current iteration
                    for (var c = 0; c < class_name.length; c ++){
                        svg.append("g").attr("transform", "translate(0, " + height_graph + ")")
                            .attr("class", class_name[c]);
                    }


                    var range_max = Math.round(Math.max.apply(undefined, first_row) / 10 + 1) * 10;

                    scale_graph_x.range([width_axis, width_graph + width_axis]);
                    var scale_graph_y = d3.scale.linear().domain([range_max, 0]).range([-height_graph, 0]);
                    if (id_graph_div.includes("load")) scale_graph_load_y = scale_graph_y;
                    if (id_graph_div.includes("price")) scale_graph_price_y = scale_graph_y;

                    var height_axis_line = height_axis * 0.1;
                    var x_axis_line = svg.append("g").attr("transform", "translate(0, " + height_graph + ")");
                    var x_axis_interval = 3;


                    for (var i = 0; i < no_periods - 1; i++) {
                        x1 = scale_graph_x(i);
                        x2 = scale_graph_x(i + 1);
                        y1 = scale_graph_y(first_row[i]);
                        y2 = scale_graph_y(first_row[i + 1]);
                        line.append("line").attr("x1", x1).attr("x2", x2).attr("y1", y1).attr("y2", y2)
                            .style("stroke", "grey");

                        // x axis line
                        x_axis_line.append("line").attr("x1", x1).attr("x2", x2).style("stroke", "grey");
                        x_axis_line.append("line").attr("x1", x2).attr("x2", x2).attr("y1", 0).attr("y2", height_axis_line).style("stroke", "grey");
                        if (i % x_axis_interval == 0)
                            x_axis_line.append("text").attr("x", x1 * 0.99).attr("y", height_axis_line * 3).text(i + 1);

                        if (last_row != []) {
                            y1_2 = scale_graph_y(last_row[i]);
                            y2_2 = scale_graph_y(last_row[i + 1]);
                            line2.append("line").attr("x1", x1).attr("x2", x2).attr("y1", y1_2).attr("y2", y2_2)
                                .style("stroke", "purple");
                        }
                    }
                    // x_axis_line.append("text").attr("x", x1 * 0.988).attr("y", height_axis_line * 3).text(no_periods);

                    // legend
                    if (last_row != []) {
                        var width_legend = width_graph / 48;
                        var legend1 = svg.append("g");
                        x = width_axis * 1.2;
                        legend1.append("rect").attr("x", x).attr("y", 0)
                            .attr("width", width_legend).attr("height", width_legend).style("fill", "grey");
                        legend1.append("text").attr("x", x + width_legend * 1.5).attr("y", width_legend * 0.8).text("Before Optimization");

                        var legend2 = svg.append("g");
                        legend2.append("rect").attr("x", x).attr("y", width_legend * 1.5)
                            .attr("width", width_legend).attr("height", width_legend).style("fill", "purple");
                        legend2.append("text").attr("x", x + width_legend * 1.5).attr("y", width_legend * 2.3).text("Aftter Optimization");

                        var legend3 = svg.append("g").attr("class", "current-legend-expected").attr("visibility", "hidden");
                        legend3.append("rect").attr("x", x + width_legend * 10).attr("y", 0)
                            .attr("width", width_legend).attr("height", width_legend).style("fill", "green");
                        legend3.append("text").attr("x", x + width_legend * 11.5).attr("y", width_legend * 0.8).text("Current Iteration - Expected");

                        var legend4 = svg.append("g").attr("class", "current-legend-expected").attr("visibility", "hidden");
                        legend4.append("rect").attr("x", x + width_legend * 10).attr("y", width_legend * 1.5)
                            .attr("width", width_legend).attr("height", width_legend).style("fill", "orange");
                        legend4.append("text").attr("x", x + width_legend * 11.5).attr("y", width_legend * 2.3).text("Current Iteration - Actual");
                    }

                    // y axis line
                    y1 = 0;
                    x2 = 0;
                    y2 = 0;
                    var y_axis_interval = 10;
                    var y_step = height_graph / y_axis_interval;
                    var x = width_axis;
                    var width_axis_line = width_axis * 0.08;
                    var y_axis_line = svg.append("g").attr("transform", "translate(" + x + ", 0)");
                    for (var j = 0; j < y_axis_interval; j++) {
                        y2 += y_step;
                        value = range_max / y_axis_interval * ( y_axis_interval - j);
                        y_axis_line.append("line").attr("x1", 0).attr("x2", 0).attr("y1", y1).attr("y2", y2).style("stroke", "grey");
                        y_axis_line.append("line").attr("x1", -width_axis_line).attr("x2", 0).attr("y1", y1).attr("y2", y1).style("stroke", "grey");
                        y_axis_line.append("text").attr("x", -width_axis_line * 4).attr("y", y1 + y_step * 0.08).text(value);
                        y1 += y_step;
                    }
                    y_axis_line.append("line").attr("x1", -width_axis_line).attr("x2", 0).attr("y1", y1).attr("y2", y1).style("stroke", "grey");
                    y_axis_line.append("text").attr("x", -width_axis_line * 4).attr("y", y1 + y_step * 0.08).text("0");

                }

                function drawCostGraph(id_graph_div, type, data) {
                    var no_rows = data.length;
                    var i, j;

                    var id_graph = "#".concat(id_graph_div).concat("-graph-div");
                    var graph_div = d3.select(id_graph).html("");

                    var height_max = window.innerHeight;
                    var width_max = parseFloat(d3.select(id_graph).style('width'));

                    var width_svg = width_max - 15;
                    var width_graph = width_svg * 0.9;
                    var width_axis = width_svg * 0.1;

                    var height_svg = height_max * 0.2;
                    var height_graph = height_svg * 0.8;
                    var height_axis = height_svg * 0.2;
                    var height_margin = 8;

                    var svg = graph_div.append("svg").attr("width", width_svg).attr("height", height_svg)
                        .append("g").attr("transform", "translate(0, " + height_margin + ")");

                    // axis text
                    var y_text, cost_type, point_class, tooltip_class;
                    if (id_graph_div.includes("cost")) {
                        y_text = "Total Cost (dollars)";
                        cost_type = "tbill";
                        point_class = point_cost_class;
                        tooltip_class = tooltip_cost_class;
                    }
                    if (id_graph_div.includes("penalty")) {
                        y_text = "Total Penalty";
                        cost_type = "tpenalty";
                        point_class = point_penalty_class;
                        tooltip_class = tooltip_penalty_class
                    }

                    // y axis
                    svg.append("g").append("text").attr("transform", "rotate(-90)")
                        .attr("y", width_axis * 0.2).attr("x", -height_svg / 2)
                        .attr("dy", "1em").style("text-anchor", "middle").text(y_text);
                    // x_axis =
                    svg.append("g").append("text").attr("transform", "translate(0, " + height_graph + ")")
                        .attr("x", width_axis + width_graph / 2).attr("dy", height_axis * 0.6)
                        .style("text-anchor", "middle").text("Iterations");

                    // read data
                    var costs = [];
                    for (i = 0; i < no_rows; i++) {
                        if (data[i]["type"] == type) costs.push(data[i][cost_type] / 100);
                    }

                    var range_max = Math.round(Math.max.apply(undefined, costs) / 10 + 1) * 10;
                    var range_min = Math.round(Math.min.apply(undefined, costs) / 10 - 1) * 10;
                    if (range_min < 0) range_min = Math.round(Math.min.apply(undefined, costs) / 10) * 10;

                    // y axis line
                    var x1, y1 = 0, x2 = 0, y2 = 0, value, value2, value3;
                    var y_axis_interval = 10;
                    var y_step = height_graph / y_axis_interval;
                    var width_axis_line = width_axis * 0.08;
                    var y_axis_line = svg.append("g").attr("transform", "translate(" + width_axis + ", 0)");
                    for (j = 0; j < y_axis_interval; j++) {
                        y2 += y_step;
                        value = (range_max - range_min) / y_axis_interval * ( y_axis_interval - j) + range_min;
                        y_axis_line.append("line").attr("x1", 0).attr("x2", 0).attr("y1", y1).attr("y2", y2).style("stroke", "grey");
                        y_axis_line.append("line").attr("x1", -width_axis_line).attr("x2", 0).attr("y1", y1).attr("y2", y1).style("stroke", "grey");
                        y_axis_line.append("text").attr("x", -width_axis_line * 4).attr("y", y1 + y_step * 0.08).text(value);
                        y1 += y_step;
                    }
                    y_axis_line.append("line").attr("x1", -width_axis_line).attr("x2", 0).attr("y1", y1).attr("y2", y1).style("stroke", "grey");
                    y_axis_line.append("text").attr("x", -width_axis_line * 4).attr("y", y1 + y_step * 0.08).text(range_min);

                    // the graph
                    var line = svg.append("g").attr("transform", "translate(" + width_axis + ", " + height_graph + ")")
                        .attr("class", "costgraph");

                    scale_graph_cost_x.range([0, width_graph]);
                    scale_graph_y.domain([range_max, range_min]).range([-height_graph, 0]);

                    var height_axis_line = height_axis * 0.1;
                    var x_axis_line = svg.append("g").attr("transform", "translate(" + width_axis + ", " + height_graph + ")");
                    var x_axis_interval = 2;
                    for (i = 0; i < costs.length - 1; i++) {
                        x1 = scale_graph_cost_x(i);
                        x2 = scale_graph_cost_x(i + 1);
                        y1 = scale_graph_y(costs[i]);
                        y2 = scale_graph_y(costs[i + 1]);
                        line.append("line").attr("x1", x1).attr("x2", x2).attr("y1", y1).attr("y2", y2).style("stroke", "grey");

                        x_axis_line.append("line").attr("x1", x1).attr("x2", x2).style("stroke", "grey");
                        x_axis_line.append("line").attr("x1", x2).attr("x2", x2).attr("y1", 0).attr("y2", height_axis_line).style("stroke", "grey");
                        if (i % x_axis_interval == 0)
                            x_axis_line.append("text").attr("x", x1).attr("y", height_axis_line * 3).text(i);
                    }

                    // dynamic point and tooltip
                    svg.append("g").attr("class", point_class).attr("transform", "translate(" + width_axis + ", " + height_graph + ")");
                    svg.append("g").attr("class", tooltip_class).attr("transform", "translate(" + width_axis + ", " + height_graph + ")");

                    // summary
                    var summary = svg.append("g");
                    var width_summary = width_svg * 0.3;
                    var cost_reduction = ((costs[0] - costs[costs.length - 1]) / costs[0] * 100).toFixed(2);

                    if (id_graph_div.includes("cost")) {
                        bills = costs;
                        scale_graph_cost_y = d3.scale.linear().domain([range_max, range_min]).range([-height_graph, 0]);

                        value = "Total Cost Before Optimization: ".concat(costs[0].toFixed(2));
                        value2 = "Total Cost After Optimization: ".concat(costs[costs.length - 1].toFixed(2));
                        content += cost_reduction + "% cost reduction" + whitespace;
                    }
                    if (id_graph_div.includes("penalty")) {
                        penalties = costs;
                        scale_graph_penalty_y = scale_graph_y;

                        value = "Total Penalty Before Optimization: ".concat(costs[0]);
                        value2 = "Total Penalty After Optimization: ".concat(costs[costs.length - 1]);
                    }
                    summary.append("text").attr("x", width_svg - width_summary).attr("y", height_margin * 2).text(value);
                    summary.append("text").attr("x", width_svg - width_summary).attr("y", height_margin * 2 + y_step).text(value2);
                    value3 = "Reduction (%): " + cost_reduction;
                    summary.append("text").attr("x", width_svg - width_summary).attr("y", height_margin * 2 + y_step * 2).text(value3);
                }

                function drawLine(graph_class, row, colour) {
                    var line = d3.select("." + graph_class).html("");
                    var scale_graph_y2;

                    if (graph_class.includes("load")) scale_graph_y2 = scale_graph_load_y;
                    if (graph_class.includes("price")) scale_graph_y2 = scale_graph_price_y;

                    var x1, x2, y1, y2;
                    for (var i = 0; i < no_periods - 1; i++) {
                        x1 = scale_graph_x(i);
                        x2 = scale_graph_x(i + 1);
                        y1 = scale_graph_y2(row[i]);
                        y2 = scale_graph_y2(row[i + 1]);

                        line.append("line").attr("x1", x1).attr("x2", x2).attr("y1", y1).attr("y2", y2)
                            .style("stroke", colour).style("stroke-width", "3");
                    }
                }

                function drawPoint(point_class, tooltip_class, x, x2, y, value) {
                    var point = d3.select("." + point_class).html("");
                    point.append("circle").attr("cx", x).attr("cy", y).attr("r", 3).attr("stroke", "green").attr("stroke-width", "2");

                    var tooltip = d3.select("." + tooltip_class).html("");
                    tooltip.append("text").attr("x", x2).attr("y", y - 12).text(value).style("font-weight", "bold");
                }

                function drawPopup(popup_class, value, x, y, width_popup, height_popup) {
                    var popup = d3.select("." + popup_class).html("");
                    popup.append("rect").attr("x", x + 10).attr("y", y - height_popup / 2).attr("width", width_popup).attr("height", height_popup).style("fill", "white").attr("stroke", "grey");
                    popup.append("text").attr("x", x + height_popup).attr("y", y + 5).text(value).style("font-weight", "bold");
                }

                function clearDraw() {
                    d3.select("." + graph_price_class_actual).html("");
                    d3.select("." + graph_price_class_expected).html("");
                    d3.select("." + graph_load_class_actual).html("");
                    d3.select("." + graph_load_class_expected).html("");
                    d3.select("." + point_cost_class).html("");
                    d3.select("." + point_penalty_class).html("");
                    d3.select("." + tooltip_cost_class).html("");
                    d3.select("." + tooltip_penalty_class).html("");
                    d3.select("." + popup_load_class).html("");
                    d3.select("." + popup_price_class).html("");
                    d3.selectAll(".current-legend-actual").attr("visibility", "hidden");
                    d3.selectAll(".current-legend-expected").attr("visibility", "hidden");

                    // d3.select("." + "current-legend").html("");
                }

                function drawCurrentData() {

                    var x = d3.mouse(this)[0], y = d3.mouse(this)[1],
                    // periods
                        x0 = Math.floor(scale_heatmap_x.invert(x)),
                    // iteration
                        y0 = Math.floor(scale_heatmap_y.invert(y));


                    // console.log(x0  + ", " + y0);

                    var second_row = loads_fw[y0];
                    var colour = "green";
                    drawLine(graph_load_class_expected, second_row, colour);
                    d3.selectAll(".current-legend-expected").attr("visibility", "visible");

                    second_row = prices[y0];
                    drawLine(graph_price_class_expected, second_row, colour);

                    second_row = loads_o[y0];
                    colour = "orange";
                    drawLine(graph_load_class_actual, second_row, colour);
                    d3.selectAll(".current-legend-actual").attr("visibility", "visible");

                    second_row = prices_o[y0];
                    drawLine(graph_price_class_actual, second_row, colour);

                    var bill_y, penalty_y, tooltip_x, cost_x = scale_graph_cost_x(y0);
                    bill_y = scale_graph_cost_y(bills[y0]);
                    penalty_y = scale_graph_penalty_y(penalties[y0]);

                    if (y0 < no_iters - 4) tooltip_x = cost_x;
                    else tooltip_x = scale_graph_cost_x(no_iters - 4);
                    drawPoint(point_cost_class, tooltip_cost_class, cost_x, tooltip_x, bill_y, bills[y0] + " @ i" + y0);
                    drawPoint(point_penalty_class, tooltip_penalty_class, cost_x, tooltip_x, penalty_y, penalties[y0] + " @ i" + y0);

                    var load = loads_fw[y0][x0], price = prices[y0][x0];
                    var width_popup = 110, height_popup = 20;
                    if (x0 > 38) x = scale_heatmap_x(38);
                    load = (Math.round(load * 100) / 100).toFixed(2);
                    drawPopup(popup_load_class, load + " kw @ p" + x0, x, y, width_popup, height_popup);
                    drawPopup(popup_price_class, price + " cent @ p" + x0, x, y, width_popup, height_popup);

                }
            }
        )
    ;
}

function showPriceTable(csv_file, id_table) {
    var id = "#".concat(id_table);
    var table = d3.select(id).html("");
    var header = table.append("thead");
    var body = table.append("tbody");


    d3.csv(csv_file, function (error, data) {
        var no_iters = data.length;
        var first_row = data[0];
        var keys = Object.keys(first_row);
        var no_periods = keys.length - 1;
        var prices = [], level = [], levels = [];

        header.append("th").text('Price');
        for (var i = 0; i < no_periods; i++) {
            header.append("th").text(i + 1);
        }

        // add rows
        body.selectAll("tr").data(data).enter().append("tr");
        for (var j = 0; j < no_iters; j++) {
            var table_loads_row = body.append("tr");
            table_loads_row.append("td").text(data[j]["prices"]);
            prices.push(data[j]["prices"]);
            level = [];
            for (var k = 0; k < no_periods; k++) {
                var value = parseFloat(Math.round(+data[j][k + 1] * 100) / 100).toFixed(2);
                table_loads_row.append("td").text(value);
                level.push(value);
            }
            levels.push(level);
        }

        var no_level = prices.length;
        var id_graph = "#t-lookup-graph";
        var graph_div = d3.select(id_graph).html("");
        var height_max = window.innerHeight;
        var width_max = parseFloat(d3.select(id_graph).style('width'));
        var width_svg = width_max - 15;
        var width_graph = width_svg * 0.98 - 10;
        var width_axis = width_svg * 0.02;

        debugger;

        var height_margin = 8;
        var height_svg = height_max * 0.95;
        var height_graph = height_svg * 0.8;
        var height_axis = height_svg * 0.05;

        var level_max = Math.max.apply(null, levels[no_level - 1]);
        var level_min = Math.min.apply(null, levels[0]);

        var scale_x = d3.scale.linear().domain([level_min, level_max]).range([width_axis, width_graph + width_axis]);
        var scale_y = d3.scale.linear().domain([0, prices[no_level - 1]]).range([height_graph, 0]);

        var svg = graph_div.append("svg").attr("width", width_svg).attr("height", height_svg).append("g").attr("transform", "translate(0, " + height_margin + ")");
        // y axis
        var y_axis = d3.svg.axis().scale(scale_y).orient("left").ticks(no_level).tickFormat(d3.format("d"));
        svg.append("g").attr("transform", "rotate(-90)")
            .append("text").attr("y", 0).attr("x", -height_svg / 2)
            .attr("dy", "1em").style("text-anchor", "middle").text("Prices (cent)");
        svg.append("g").attr("transform", "translate(" + width_axis + ", " + 0 + ")").attr("class", "y-axis").call(y_axis);
        // x axis
        var x_axis = d3.svg.axis().scale(scale_x).orient("bottom").ticks(50).tickFormat(d3.format("d"));
        svg.append("g").attr("transform", "translate(0" + ", " + height_graph + ")").call(x_axis).attr("class", "x-axis")
            .append("text").attr("x", width_axis + width_graph / 2).attr("y", height_axis)
            .style("text-anchor", "middle").text("Loads (kw)");

        var levels_trans = levels[0].map(function (col, i) {
            return levels.map(function (row) {
                return row[i];
            })
        });
        var line = d3.svg.line().x(function (d) {
            return scale_x(d);
        }).y(function (d, i) {
            return scale_y(prices[i]);
        });

        var level_period;
        var tooltip = svg.append("g").attr("class", "tooltip_class");
        var lines = svg.append("g");
        var x, y;
        for (i = 0; i < no_periods; i++) {
            level_period = levels_trans[i];
            lines.append("path").datum(level_period).attr('class', 'line').attr("d", line);
            lines.selectAll("dot").data(level_period).enter().append("circle").attr("r", 5).attr("fill", "green")
            .attr("cx", function (d) {return scale_x(d);}).attr("cy", function (d, i) {return scale_y(prices[i]);})
            .on("mouseover", function(d, i) {
                if (i < no_level - 1) {
                    x = scale_x(d);
                    y = scale_y(prices[i]) - 40;
                }
                else {
                    x = scale_x(d) - 45;
                    y = scale_y(prices[i]) + 40;
                }
                tooltip.html("");
                tooltip.append("text").attr("x",x).attr("y", y).style("font-weight", "bold")
                    .append("tspan").attr("x", x).attr("dy", 0).text(d + " kw")
                    .append("tspan").attr("x", x).attr("dy", 20).text(prices[i] + " cent");
            });
        }

        // show the screen
        $("body").css('opacity', 1);
        $("div#divLoading").removeClass('show');
    });

}

function showData(dir, tab) {

    // // show the screen
    //             $("body").css('opacity', 1);
    //             $("div#divLoading").removeClass('show');

    if (tab.includes("lookup")) {

        var fname_lookup = dir + "/lookup.csv";
        showPriceTable(fname_lookup, "t-lookup");
    }

    if (tab.includes("heatmap")) {
        var fname_loads = dir + "/loads.csv";
        var fname_prices = dir + "/prices.csv";
        var fname_costs = dir + "/costs.csv";
        var fname_sum = dir + "/overview.csv";

        var colours_size = 9;
        var params_loads = {max_scale: 1.05, colours_size: colours_size, colours: colorbrewer.Reds[colours_size]};
        var params_prices = {max_scale: 1.06, colours_size: colours_size, colours: colorbrewer.Greens[colours_size]};
        showResults(fname_loads, fname_prices, fname_costs, fname_sum, params_loads, params_prices);
    }


}


