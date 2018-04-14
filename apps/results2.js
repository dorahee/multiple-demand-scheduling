/**
 * Created by dora on 1/06/15.
 */

function loadsPriceData(file) {

    //******************** Start: codes for preparing data overview ********************

    // container for data
    d3.select('#data').html('');
    var containerData = d3.select('#data').append('div').attr('class', 'container-fluid');
    var containerRow1Data = containerData.append('div').attr('class', 'row');
    containerRow1Data.append('div').attr('class', 'col-xs-12').html('<h1>Data Overview</h1>');
    var dataDiv = containerRow1Data.append('div').attr('class', 'col-xs-12').attr('id', 'data-div');
    var dataParametersDiv = containerRow1Data.append('div').attr('class', 'col-xs-12').attr('id', 'para-div');

     //******************** Start: codes for preparing pricing table view ********************

    // container for table
    d3.select('#lookup').html('');
    var containerPTB = d3.select('#lookup').append('div').attr('class', 'container-fluid');
    var containerRow1PTB = containerPTB.append('div').attr('class', 'row');
    containerRow1PTB.append('div').attr('class', 'col-xs-12').html('<h1>Pricing Table</h1>');
    var PTDivTB = containerRow1PTB.append('div').attr('class', 'col-xs-12').attr('id', 'lookup-div-table');

    var pricingTable = PTDivTB.append("table").attr('id', 'pricingTable').attr('class', 'table table-striped table-hover table-condensed');
    var pricingTableHeader = pricingTable.append("thead");
    var pricingTableBody = pricingTable.append("tbody");

    //******************** Start: codes for preparing table view ********************

    // container for table
    d3.select('#table').html('');
    var containerTB = d3.select('#table').append('div').attr('class', 'container-fluid');
    var containerRow1TB = containerTB.append('div').attr('class', 'row');
    var containerRow2TB = containerTB.append('div').attr('class', 'row');
    var containerRow3TB = containerTB.append('div').attr('class', 'row');

    // div for loads and prices table
    containerRow1TB.append('div').attr('class', 'col-xs-12').html('<h1>Load Data (kw/h)</h1>');
    var loadDivTB = containerRow1TB.append('div').attr('class', 'col-xs-12').attr('id', 'load-div-table');
    containerRow2TB.append('div').attr('class', 'col-xs-12').html('<h1>Price Data (cent)</h1>');
    var priceDivTB = containerRow2TB.append('div').attr('class', 'col-xs-12').attr('id', 'price-div-table');
    containerRow3TB.append('div').attr('class', 'col-xs-12').html('<h1>FW Load Data (cent)</h1>');
    var fwloadDivTB = containerRow3TB.append('div').attr('class', 'col-xs-12').attr('id', 'fwload-div-table');

    // table for loads and prices
    var loadTable = loadDivTB.append("table").attr('id', 'loadTable').attr('class', 'table table-striped table-hover table-condensed');
    var loadTableHeader = loadTable.append("thead");
    var loadTableBody = loadTable.append("tbody");
    var priceTable = priceDivTB.append("table").attr('id', 'myTable').attr('class', 'table table-striped table-hover table-condensed');
    var priceTableHeader = priceTable.append("thead");
    var priceTableBody = priceTable.append("tbody");
    var fwloadTable = fwloadDivTB.append("table").attr('id', 'fwloadTable').attr('class', 'table table-striped table-hover table-condensed');
    var fwloadTableHeader = fwloadTable.append("thead");
    var fwloadTableBody = fwloadTable.append("tbody");

    //console.log('test: ' + file.substr(0, file.length - 5) + "-P.py");
    var fileParameters = file.substr(0, file.indexOf(".") + 3) + "-P.py";
    d3.text(fileParameters, function (error, data) {
        data2 = data.replace(/\n/g, "<br>");
        dataParametersDiv.html("<hr>" + data2);
    });
    //dataParametersDiv.html("<iframe src="+ fileParameters +"><//iframe> ");

    d3.json(file, function (error, data) {

        //******************** Start: loading data for data overview ********************

        var notes = "";
        // console.log(data[0].notes);
        if(data[0].notes != 'null') notes += "<br/><br/>" + data[0].notes;

        dataDiv.html("Number of households: " + data[0].households
            + "<br/>" + "Number of jobs per household: " + data[0].minJobs + " ~ " + data[0].maxJobs
            + "<br/>" + "Total run time: " + Math.ceil(data[data.length - 1].time * 1000) / 1000 + "s" + notes);

        //******************** Start: loading data for pricing table ********************

        dataPTHeader = data[0].pricingTable[0];

        pricingTableHeader.selectAll("thead")
            .data(dataPTHeader).enter().append("th").text(function (d, i) {
            if (i == 0) return "Price";
            else return "p=" + (i);
        });
        var rowPTBody = pricingTableBody.selectAll("tbody")
            .data(data[0].pricingTable)
            .enter().append("tr");
        rowPTBody.selectAll("tr")
            .data(function (d) {
                newdata = d;
                // console.log(newdata);
                return newdata;
            })
            .enter().append("td").text(function (d) {
            return Math.round(d * 100) / 100;
        })
        ;

        //******************** Start: loading data for table view ********************

        dataHeader = [0].concat(data[0].loads);

        loadTableHeader.selectAll("thead")
            .data(dataHeader).enter().append("th").text(function (d, i) {
            if (i == 0) return "Iter";
            else return "p=" + (i);
        });
        var rowLoadBody = loadTableBody.selectAll("tbody")
            .data(data)
            .enter().append("tr");
        rowLoadBody.selectAll("tr")
            .data(function (d) {
                newdata = [d.key].concat(d.loads);
                return newdata;
            })
            .enter().append("td").text(function (d) {
            return Math.round(d * 100) / 100;
        })
        ;

        fwloadTableHeader.selectAll("thead")
            .data(dataHeader).enter().append("th").text(function (d, i) {
            if (i == 0) return "Iter";
            else return "p=" + (i);
        });
        var rowfwLoadBody = fwloadTableBody.selectAll("tbody")
            .data(data)
            .enter().append("tr");
        rowfwLoadBody.selectAll("tr")
            .data(function (d) {
                newdata = [d.key].concat(d.loads_fw);
                return newdata;
            })
            .enter().append("td").text(function (d) {
            return Math.round(d * 100) / 100;
        })
        ;

        priceTableHeader.selectAll("thead")
            .data(dataHeader).enter().append("th").text(function (d, i) {
            if (i == 0) return "Iter";
            else return "p = " + (i);
        });
        var rowPriceBody = priceTableBody.selectAll("tbody")
            .data(data)
            .enter().append("tr");
        rowPriceBody.selectAll("tr")
            .data(function (d) {
                newdata = [d.key].concat(d.prices);
                return newdata;
            })
            .enter().append("td").text(function (d) {
            return Math.round(d * 100) / 100;
        });
    });
}

function loadsPriceAnalysis(file) {
    d3.select('#anaylsis').html('');
    var containerAnalysis = d3.select('#anaylsis').append('div').attr('class', 'container-fluid');

    var containerRow1Analysis = containerAnalysis.append('div').attr('class', 'row');
    containerRow1Analysis.append('div').attr('class', 'col-xs-12').html('<h1>Data Analysis</h1>');

    var containerRow2Analysis = containerAnalysis.append('div').attr('class', 'row');
    var tbillDiv = containerRow2Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'tbill-div');
    var parDiv = containerRow2Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'par-div');
    var tBALoadDiv = containerRow2Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'baload-div');

    var containerRow3Analysis = containerAnalysis.append('div').attr('class', 'row');
    var tTobjDiv = containerRow3Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'tobj-div');
    var tAlphaDiv = containerRow3Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'talpha-div');
    var tBALoadFWDiv = containerRow3Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'baloadfw-div');

    var containerRow4Analysis = containerAnalysis.append('div').attr('class', 'row');
    var tTpenDiv = containerRow4Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'tpen-div');
    var tFWitrDiv = containerRow4Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'tfwitr-div');
    var tBAPriceDiv = containerRow4Analysis.append('div').attr('class', 'col-xs-4').attr('id', 'baprice-div');

    var margin = {top: 20, right: 20, bottom: 30, left: 70},
        maxWidth = parseInt(d3.select('.col-xs-4').style('width'), 10),
        width = maxWidth - margin.left * 1.5 - margin.right * 1.5,
        height = (window.innerHeight - parseInt(d3.select('#selectionDropdown').style('height'), 10) - parseInt(d3.select('.site-footer').style('height'), 10)) / 3 - (margin.top + margin.bottom) * 2,
        svgWidth = width + margin.left + margin.right,
        svgHeight = height + (margin.top + margin.bottom),
    // 100 means Dollars, and 1 means cent
        centOrDollars = 100;

    var formatTime = d3.time.format("%H"),
        formatHour = function (d) {
            //if (d == 24) return "noon";
            if (d == 48 || d == 0) return " ";
            return formatTime(new Date(2013, 2, 9, d / 2, 00));
        };
    var formatYaixs = function (d) {
        var prefix = d3.formatPrefix(d);
        return prefix.scale(d) + prefix.symbol;
    };

    var x = d3.scale.linear().rangeRound([0, width - margin.right * 2]);
    var x2 = d3.scale.linear().rangeRound([0, width - margin.right * 2]);

    var yTbill = d3.scale.linear().rangeRound([height, 0]);
    var yPar = d3.scale.linear().rangeRound([height, 0]);
    var yTobj = d3.scale.linear().rangeRound([height, 0]);
    var yTpen = d3.scale.linear().rangeRound([height, 0]);
    var yBAload = d3.scale.linear().rangeRound([height, 0]);
    var yBAloadfw = d3.scale.linear().rangeRound([height, 0]);
    var yBAprice = d3.scale.linear().rangeRound([height, 0]);
    var yAlpha = d3.scale.linear().rangeRound([height, 0]);
    var yFWitr = d3.scale.linear().rangeRound([height, 0]);

    var xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(20).tickFormat(d3.format("d")).ticks(Math.floor(width / 50));
    var xAxis2 = d3.svg.axis().scale(x2).orient("bottom").ticks(20).tickFormat(formatHour).ticks(Math.floor(width / 50));

    //var yTbillAxis = d3.svg.axis().scale(yTbill).orient("left").tickFormat(d3.format("d"));
    var yTbillAxis = d3.svg.axis().scale(yTbill).orient("left").tickFormat(formatYaixs).ticks(Math.floor(height / 30));
    var yParAxis = d3.svg.axis().scale(yPar).orient("left").tickFormat(d3.format("d"));
    var yTobjAxis = d3.svg.axis().scale(yTobj).orient("left").tickFormat(formatYaixs).ticks(Math.floor(height / 30));
    var yTpenAxis = d3.svg.axis().scale(yTpen).orient("left").tickFormat(formatYaixs).ticks(Math.floor(height / 30));
    var yBAloadAxis = d3.svg.axis().scale(yBAload).orient("left").tickFormat(d3.format("d")).ticks(Math.floor(height / 30));
    var yBAloadfwAxis = d3.svg.axis().scale(yBAloadfw).orient("left").tickFormat(d3.format("d")).ticks(Math.floor(height / 30));
    var yBApriceAxis = d3.svg.axis().scale(yBAprice).orient("left").tickFormat(d3.format("d")).ticks(Math.floor(height / 30));
    var yAlphaAxis = d3.svg.axis().scale(yAlpha).orient("left").tickFormat(d3.format("d"));
    var yFWitrAxis = d3.svg.axis().scale(yFWitr).orient("left").tickFormat(d3.format("d"));

    var svgTbill = tbillDiv.append('svg')
        .attr('id', 'svgTbill').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    var svgPar = parDiv.append('svg')
        .attr('id', 'svgPar').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    var svgObj = tTobjDiv.append('svg')
        .attr('id', 'svgObj').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    var svgPen = tTpenDiv.append('svg')
        .attr('id', 'svgPen').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    var svgBAload = tBALoadDiv.append('svg')
        .attr('id', 'svgBAload').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    var svgBAloadfw = tBALoadFWDiv.append('svg')
        .attr('id', 'svgBAloadfw').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    var svgBAprice = tBAPriceDiv.append('svg')
        .attr('id', 'svgBAprice').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    var svgAlpha = tAlphaDiv.append('svg')
        .attr('id', 'svgAlpha').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
    var svgFWitr = tFWitrDiv.append('svg')
        .attr('id', 'svgFWitr').attr('width', svgWidth).attr('height', svgHeight)
        .append('g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    svgTbill.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('Total cost (Dollars)')
        .attr('class', 'mono');
    svgPar.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('Peak-to-average Rate')
        .attr('class', 'mono');
    svgObj.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('Total objective')
        .attr('class', 'mono');
    svgPen.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('Total penalty')
        .attr('class', 'mono');
    svgBAload.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('Load (KW)')
        .attr('class', 'mono');
    svgBAloadfw.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('Load FW (KW)')
        .attr('class', 'mono');
    svgBAprice.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('Price (cent)')
        .attr('class', 'mono');
    svgAlpha.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('Alpha per iteration')
        .attr('class', 'mono');
    svgFWitr.append('text').attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left).attr('x', 0 - (height / 2)).attr('dy', '1em')
        .style('text-anchor', 'middle').text('FW itrs per iteration')
        .attr('class', 'mono');

    var tooltipTbill = tbillDiv.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipTbill.append('div').attr('class', 'iter');
    tooltipTbill.append('div').attr('class', 'iniTbill');
    tooltipTbill.append('div').attr('class', 'curTbill');
    var tooltipTbillfixed = tbillDiv.append('div').attr('class', 'tooltips');
    tooltipTbillfixed.append('div').attr('class', 'reduced');

    var tooltipPar = parDiv.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipPar.append('div').attr('class', 'iter');
    tooltipPar.append('div').attr('class', 'iniPar');
    tooltipPar.append('div').attr('class', 'curPar');
    var tooltipParfixed = parDiv.append('div').attr('class', 'tooltips');
    tooltipParfixed.append('div').attr('class', 'reduced');

    var tooltipObj = tTobjDiv.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipObj.append('div').attr('class', 'iter');
    tooltipObj.append('div').attr('class', 'iniObj');
    tooltipObj.append('div').attr('class', 'curObj');
    var tooltipObjfixed = tTobjDiv.append('div').attr('class', 'tooltips');
    tooltipObjfixed.append('div').attr('class', 'reduced');

    var tooltipPen = tTpenDiv.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipPen.append('div').attr('class', 'iter');
    tooltipPen.append('div').attr('class', 'iniPen');
    tooltipPen.append('div').attr('class', 'curPen');
    var tooltipPenfixed = tTpenDiv.append('div').attr('class', 'tooltips');
    tooltipPenfixed.append('div').attr('class', 'reduced');

    var tooltipAlpha = tAlphaDiv.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipAlpha.append('div').attr('class', 'iter');
    tooltipAlpha.append('div').attr('class', 'iniAlpha');
    tooltipAlpha.append('div').attr('class', 'curAlpha');

    var tooltipFWitr = tFWitrDiv.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipFWitr.append('div').attr('class', 'iter');
    tooltipFWitr.append('div').attr('class', 'iniFWitr');
    tooltipFWitr.append('div').attr('class', 'curFWitr');

    d3.json(file, function (error, data) {
        var iterMax = 1 + d3.max(data, function (d) {
                    return d.key;
                }),
            tbillMax = 1 + d3.max(data, function (d) {
                    return d.tbill;
                }),
            tbillMin = 1 + d3.min(data, function (d) {
                    if (d.tbill == 0) return 0.986 * data[1].tbill;
                    else return d.tbill;
                }),
            parMax = 1 + d3.max(data, function (d) {
                    par = d3.max(d.loads) / d3.mean(d.loads);
                    return par;
                }),
            parMin = 1 + d3.min(data, function (d) {
                    par = d3.max(d.loads) / d3.mean(d.loads);
                    return par;
                }),
        //tobjMax = 1 + d3.max(data, function (d) {
        //        return d.tobj;
        //    }),
            tobjMax = 1 + d3.max(data, function (d) {
                    return d.tbill + d.tpenalty;
                }),
            tobjMin = 1 + d3.min(data, function (d) {
                    if (d.tbill + d.tpenalty == 0) return 0.986 * (data[1].tbill + data[1].tpenalty);
                    return d.tbill + d.tpenalty;
                }),
            tpenMax = 1 + d3.max(data, function (d) {
                    return d.tpenalty;
                }),
            tpenMin = 1 + d3.min(data, function (d) {
                    return d.tpenalty;
                }),
            periodMax = d3.max(data[0].loads, function (d, i) {
                return i;
            }),
            loadMax = d3.max(data, function (d) {
                return d3.max(d.loads);
            }),
            loadfwMax = d3.max(data, function (d, i) {
                if (i == 0) return d3.max(data[1].loads_fw);
                else return d3.max(d.loads_fw);
            }),
            priceMax = d3.max(data, function (d) {
                return d3.max(d.prices);
            }),
            fwitrMax = d3.max(data, function (d) {
                if (d.fw_itrs == null) return 0;
                else return d.fw_itrs;
            }),
            alphaMax = d3.max(data, function (d) {
                if (d.alpha == null) return 0;
                else return d.alpha;
            }),
            oTbill = data[1].tbill,
            fTbill = data[iterMax - 1].tbill,
            oPar = d3.max(data[0].loads) / d3.mean(data[0].loads),
            fPar = d3.max(data[iterMax - 1].loads) / d3.mean(data[iterMax - 1].loads),
        //oTobj = data[1].tobj,
            oTobj = data[1].tbill + data[1].tpenalty,
        //fTobj = data[iterMax - 1].tobj,
            fTobj = data[iterMax - 1].tbill + data[iterMax - 1].tpenalty,
            oTpen = data[1].tpenalty,
            fTpen = data[iterMax - 1].tpenalty,
            oloads = data[0].loads,
            oloadsfw = data[1].loads_fw,
            floads = data[iterMax - 1].loads,
            floadsfw = data[iterMax - 1].loads_fw,
            oprices = data[1].prices,
            fprices = data[iterMax - 1].prices;

        // console.log(fwitrMax);
        x.domain([0, iterMax]);
        x2.domain([0, periodMax + 1]);
        yTbill.domain([tbillMin / centOrDollars, tbillMax / centOrDollars]);
        yPar.domain([0, parMax]);
        yTobj.domain([tobjMin, tobjMax]);
        yTpen.domain([tpenMin, tpenMax]);
        yBAload.domain([0, d3.max(oloads)]);
        yBAloadfw.domain([0, d3.max(oloadsfw)]);
        yBAprice.domain([0, d3.max(oprices)]);
        yAlpha.domain([0, alphaMax]);
        yFWitr.domain([0, fwitrMax]);

        svgTbill.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Iterations').attr('class', 'mono');
        svgTbill.append('g').attr('class', 'y-axis').call(yTbillAxis);

        svgPar.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Iterations').attr('class', 'mono');
        svgPar.append('g').attr('class', 'y-axis').call(yParAxis);

        svgObj.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Iterations').attr('class', 'mono');
        svgObj.append('g').attr('class', 'y-axis').call(yTobjAxis);

        svgPen.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Iterations').attr('class', 'mono');
        svgPen.append('g').attr('class', 'y-axis').call(yTpenAxis);

        svgBAload.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis2)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Time step').attr('class', 'mono');
        svgBAload.append('g').attr('class', 'y-axis').call(yBAloadAxis);

        svgBAloadfw.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis2)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Time step').attr('class', 'mono');
        svgBAloadfw.append('g').attr('class', 'y-axis').call(yBAloadfwAxis);

        svgBAprice.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis2)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Time step').attr('class', 'mono');
        svgBAprice.append('g').attr('class', 'y-axis').call(yBApriceAxis);

        svgAlpha.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Iterations').attr('class', 'mono');
        svgAlpha.append('g').attr('class', 'y-axis').call(yAlphaAxis);

        svgFWitr.append('g').attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')').call(xAxis)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Iterations').attr('class', 'mono');
        svgFWitr.append('g').attr('class', 'y-axis').call(yFWitrAxis);

        var drawLineTbill = d3.svg.line()
            .x(function (d, i) {
                return x(i);
            })
            .y(function (d) {
                bill = d.tbill / centOrDollars;
                if (bill == 0) return yTbill(oTbill);
                else return yTbill(d.tbill / centOrDollars);
            });
        var drawLinePar = d3.svg.line()
            .x(function (d, i) {
                return x(i);
            })
            .y(function (d) {
                par = d3.max(d.loads) / d3.mean(d.loads);
                if (par == 0) return yPar(oPar);
                else return yPar(par);
            });
        var drawLineObj = d3.svg.line()
            .x(function (d, i) {
                return x(i);
            })
            .y(function (d) {
                obj = d.tbill + d.tpenalty;
                if (obj == 0) return yTobj(oTobj);
                else return yTobj(obj);
            });
        var drawLinePen = d3.svg.line()
            .x(function (d, i) {
                return x(i);
            })
            .y(function (d) {
                return yTpen(d.tpenalty);
            });
        var drawLineLoad = d3.svg.line()
            .x(function (d, i) {
                return x2(i);
            })
            .y(function (d) {
                return yBAload(d);
            });
        var drawLineLoadfw = d3.svg.line()
            .x(function (d, i) {
                return x2(i);
            })
            .y(function (d) {
                return yBAloadfw(d);
            });
        var drawLinePrice = d3.svg.line()
            .x(function (d, i) {
                return x2(i);
            })
            .y(function (d) {
                return yBAprice(d);
            });
        var drawLineAlpha = d3.svg.line()
            .x(function (d, i) {
                return x(i);
            })
            .y(function (d) {
                if (d.alpha != null) return yAlpha(d.alpha);
                else return 0;
            });
        var drawLineFWitr = d3.svg.line()
            .x(function (d, i) {
                return x(i);
            })
            .y(function (d) {
                if (d.fw_itrs != null) return yFWitr(d.fw_itrs);
                else return 0;
            });

        //var lineTbill = svgTbill.append('g');
        //var linePar = svgPar.append('g');

        svgTbill.append('path').datum(data).attr('class', 'line').attr('id', 'lineTbill').attr('d', drawLineTbill);
        svgPar.append('path').datum(data).attr('class', 'line').attr('id', 'linePar').attr('d', drawLinePar);
        svgObj.append('path').datum(data).attr('class', 'line').attr('id', 'lineTobj').attr('d', drawLineObj);
        svgPen.append('path').datum(data).attr('class', 'line').attr('id', 'lineTpen').attr('d', drawLinePen);
        svgBAload.append('path').datum(oloads).attr('class', 'line').attr('id', 'lineBload').attr('d', drawLineLoad);
        svgBAload.append('path').datum(floads).attr('class', 'line').attr('id', 'lineAload').attr('d', drawLineLoad);
        svgBAloadfw.append('path').datum(oloadsfw).attr('class', 'line').attr('id', 'lineBloadfw').attr('d', drawLineLoadfw);
        svgBAloadfw.append('path').datum(floadsfw).attr('class', 'line').attr('id', 'lineAloadfw').attr('d', drawLineLoadfw);
        svgBAprice.append('path').datum(oprices).attr('class', 'line').attr('id', 'lineBprices').attr('d', drawLinePrice);
        svgBAprice.append('path').datum(fprices).attr('class', 'line').attr('id', 'lineAprices').attr('d', drawLinePrice);
        svgAlpha.append('path').datum(data).attr('class', 'line').attr('id', 'lineAlpha').attr('d', drawLineAlpha);
        svgFWitr.append('path').datum(data).attr('class', 'line').attr('id', 'lineFWitr').attr('d', drawLineFWitr);

        var focusTbill = svgTbill.append('g').style('display', 'none');
        var focusPar = svgPar.append('g').style('display', 'none');
        var focusObj = svgObj.append('g').style('display', 'none');
        var focusPen = svgPen.append('g').style('display', 'none');
        var focusAlpha = svgAlpha.append('g').style('display', 'none');
        var focusFWitr = svgFWitr.append('g').style('display', 'none');

        focusTbill.append('circle').attr('r', 5);
        focusPar.append('circle').attr('r', 5);
        focusObj.append('circle').attr('r', 5);
        focusPen.append('circle').attr('r', 5);
        focusAlpha.append('circle').attr('r', 5);
        focusFWitr.append('circle').attr('r', 5);

        tooltipTbillfixed.select(".reduced").html('Reduced by ' + Math.floor((oTbill - fTbill) / oTbill * 10000) / 100 + '%');
        tooltipTbillfixed.style('left', svgWidth - 30 + 'px').style('top', 0 + 'px');
        tooltipParfixed.select(".reduced").html('Reduced by ' + Math.floor((oPar - fPar) / oPar * 10000) / 100 + '%');
        tooltipParfixed.style('left', svgWidth - 30 + 'px').style('top', 0 + 'px');
        tooltipObjfixed.select(".reduced").html('Reduced by ' + Math.floor((oTobj - fTobj) / oTobj * 10000) / 100 + '%');
        tooltipObjfixed.style('left', svgWidth - 30 + 'px').style('top', 0 + 'px');
        tooltipPenfixed.select(".reduced").html('Reduced by ' + Math.floor((oTpen - fTpen) / oTpen * 10000) / 100 + '%');
        tooltipPenfixed.style('left', svgWidth - 30 + 'px').style('top', 0 + 'px');

        //focusTbill.append("text").attr("x", 9).attr("dy", ".25em");
        //focusPar.append("text").attr("x", 9).attr("dy", ".25em");

        svgTbill.append("rect")
            .attr("class", "overlay")
            .attr("width", width)
            .attr("height", height)
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .on("mousemove", mousemove);

        svgPar.append("rect")
            .attr("class", "overlay")
            .attr("width", width)
            .attr("height", height)
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .on("mousemove", mousemove);

        svgObj.append("rect")
            .attr("class", "overlay")
            .attr("width", width)
            .attr("height", height)
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .on("mousemove", mousemove);

        svgPen.append("rect")
            .attr("class", "overlay")
            .attr("width", width)
            .attr("height", height)
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .on("mousemove", mousemove);

        svgAlpha.append("rect")
            .attr("class", "overlay")
            .attr("width", width)
            .attr("height", height)
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .on("mousemove", mousemove);

        svgFWitr.append("rect")
            .attr("class", "overlay")
            .attr("width", width)
            .attr("height", height)
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .on("mousemove", mousemove);

        function mousemove() {
            var x0 = x.invert(d3.mouse(this)[0]),
                i0 = Math.floor(x0),
                i1 = Math.ceil(x0),
                d = x0 - i0 > i1 - x0 ? i1 : i0,
                par = d3.max(data[d].loads) / d3.mean(data[d].loads),
                obj = data[d].tbill + data[d].tpenalty,
                alpha = 0,
                fwitr = 0;
            if (data[d].alpha != null) alpha = data[d].alpha;
            if (data[d].fw_itrs != null) fwitr = data[d].fw_itrs;

            focusTbill.attr("transform", "translate(" + x(d) + "," + yTbill(data[d].tbill / centOrDollars) + ")");
            // tooltipTbill.select(".iter").html('Iteration ' + d + ': reduced by ' + Math.floor((oTbill - data[d].tbill) / oTbill * 10000) / 100 + '%');
            tooltipTbill.select(".iniTbill").html('$' + Math.floor(oTbill) / 100 + '- 1st iteration');
            tooltipTbill.select(".curTbill").html('$' + Math.floor(data[d].tbill) / 100 + ' - ' + d + 'th iteration' + '<br>' + Math.floor((oTbill - data[d].tbill) / oTbill * 10000) / 100 + '%, $' + Math.floor((oTbill - data[d].tbill) * 100 / centOrDollars) / 100 + ' reduced');
            tooltipTbill.style('left', x(d) + 'px').style('top', yTbill(data[d].tbill / centOrDollars) + 35 + 'px');
            if (oTbill >= data[d].tbill) tooltipTbill.select(".curTbill").style('color', 'green');
            else tooltipTbill.select(".curTbill").style('color', 'red');

            focusPar.attr("transform", "translate(" + x(d) + "," + yPar(par) + ")");
            // tooltipPar.select(".iter").html('Iteration: ' + d + ': reduced by ' + Math.floor((oPar - par) / oPar * 10000) / 100 + '%');
            tooltipPar.select(".iniPar").html(Math.floor(oPar * 100) / 100 + ' - before optimization');
            tooltipPar.select(".curPar").html(Math.floor(par * 100) / 100 + ' - ' + d + 'th iteration' + '<br>' + Math.floor((oPar - par) / oPar * 10000) / 100 + '%, ' + Math.floor((oPar - par) * 100) / 100 + ' reduced');
            tooltipPar.style('left', x(d) + 'px').style('top', yPar(par) + 35 + 'px');
            if (oPar >= par) tooltipPar.select(".curPar").style('color', 'green');
            else tooltipPar.select(".curPar").style('color', 'red');

            //focusObj.attr("transform", "translate(" + x(d) + "," + yTobj(data[d].tobj) + ")");
            //tooltipObj.select(".iter").html('Iteration: ' + d + ': reduced ' + Math.floor((oTobj - data[d].tobj) / oTobj * 10000) / 100 + '%');
            //tooltipObj.select(".iniObj").html('Initial total objective: ' + Math.floor(oTobj * 100) / 100);
            //tooltipObj.select(".curObj").html('Current total objective:  ' + Math.floor(data[d].tobj * 100) / 100);
            //tooltipObj.style('left', x(d) + 'px').style('top', yTobj(data[d].tobj) + 35 + 'px');
            //if (oTobj >= data[d].tobj) tooltipObj.select(".curObj").style('color', 'green');
            //else tooltipObj.select(".curObj").style('color', 'red');

            focusObj.attr("transform", "translate(" + x(d) + "," + yTobj(obj) + ")");
            // tooltipObj.select(".iter").html('Iteration: ' + d + ': reduced by ' + Math.floor((oTobj - obj) / oTobj * 10000) / 100 + '%');
            tooltipObj.select(".iniObj").html(Math.floor(oTobj * 100 / centOrDollars) / 100 + '- 1st iteration');
            tooltipObj.select(".curObj").html(Math.floor(obj * 100 / centOrDollars) / 100 + ' - ' + d + 'th iteration' + '<br>' + Math.floor((oTobj - obj) / oTobj * 10000) / 100 + '%, ' + Math.floor((oTobj - obj) * 100 / centOrDollars) / 100 + ' reduced');
            tooltipObj.style('left', x(d) + 'px').style('top', yTobj(obj) + 35 + 'px');
            if (oTobj >= obj) tooltipObj.select(".curObj").style('color', 'green');
            else tooltipObj.select(".curObj").style('color', 'red');

            focusPen.attr("transform", "translate(" + x(d) + "," + yTpen(data[d].tpenalty) + ")");
            // tooltipPen.select(".iter").html('Iteration: ' + d + ': reduced by ' + Math.floor((oTpen - data[d].tpenalty) / oTpen * 10000) / 100 + '%');
            tooltipPen.select(".iniPen").html(Math.floor(oTpen * 100 / centOrDollars) / 100 + '- 1st iteration');
            tooltipPen.select(".curPen").html(Math.floor(data[d].tpenalty * 100 / centOrDollars) / 100 + ' - ' + d + 'th iteration' + '<br>' + Math.floor((oTpen - data[d].tpenalty) / oTpen * 10000) / 100 + '%, ' + Math.floor((oTpen - data[d].tpenalty) * 100 / centOrDollars) / 100 + ' reduced');
            tooltipPen.style('left', x(d) + 'px').style('top', yTpen(data[d].tpenalty) + 35 + 'px');
            if (oTpen >= data[d].tpenalty) tooltipPen.select(".curPen").style('color', 'green');
            else tooltipPen.select(".curPen").style('color', 'red');

            focusAlpha.attr("transform", "translate(" + x(d) + "," + yAlpha(alpha) + ")");
            tooltipAlpha.select(".curAlpha").html(alpha + ' - ' + d + 'th iteration');
            tooltipAlpha.style('left', x(d) + 'px').style('top', yAlpha(alpha) + 35 + 'px');

            focusFWitr.attr("transform", "translate(" + x(d) + "," + yFWitr(fwitr) + ")");
            tooltipFWitr.select(".curFWitr").html(fwitr + ' - ' + d + 'th iteration');
            tooltipFWitr.style('left', x(d) + 'px').style('top', yFWitr(fwitr) + 35 + 'px');
        }

        function mouseover() {
            focusTbill.style("display", null);
            focusPar.style("display", null);
            focusObj.style("display", null);
            focusPen.style("display", null);
            focusAlpha.style("display", null);
            focusFWitr.style("display", null);
            tooltipTbill.classed('hidden', false);
            tooltipPar.classed('hidden', false);
            tooltipObj.classed('hidden', false);
            tooltipPen.classed('hidden', false);
            tooltipAlpha.classed('hidden', false);
            tooltipFWitr.classed('hidden', false);
        }

        function mouseout() {
            focusPar.style("display", "none");
            focusTbill.style("display", "none");
            focusObj.style("display", "none");
            focusPen.style("display", "none");
            tooltipTbill.classed('hidden', true);
            tooltipPar.classed('hidden', true);
            tooltipObj.classed('hidden', true);
            tooltipPen.classed('hidden', true);
            tooltipAlpha.classed('hidden', true);
            tooltipFWitr.classed('hidden', true);
        }

    });
}

function about() {
    d3.select('#about').html('');
    var container = d3.select('#about').append('div').attr('class', 'container-fluid');
    var containerRow1 = container.append('div').attr('class', 'row');
    containerRow1.append('div').attr('class', 'col-xs-12').html('<h1>About This Research</h1>');
    var containerRow2 = container.append('div').attr('class', 'row');
    var aboutCell = containerRow2.append('div').attr('class', 'col-xs-12').attr('id', 'about-div');
    aboutCell.html('<h3>Simulation of dynamic pricing based energy resource schedule in a suburban smart grid</h3>' +
        '<p>This Demo shows how 1000 houses can collectively reduce their electricity costs in response to ' +
        'a dynamic price negotiated between a house’s home energy management system and the utility. ' +
        'The visualisation shows how the negotiations eventually flatten the price shape and the aggregate ' +
        'electricity load profile for all the houses in the suburb. </p><br/>' +
        'Student: Shan (Dora) He, shan.he@monash.edu<br/>' +
        'Supervisors: Ariel Liebman (ariel.liebman@monash.edu), Mark Wallace (mark.wallace@monash.edu), Campbell Wilson (campbell.wilson@monash.edu)<br/>'
    );


}

function loadsPriceComparison(file) {

}

function visualiseLoadsPrices(file) {

    //******************** Start: codes for preparing heat map view ********************

    // container for heat map
    d3.select('#heatmap').html('');
    var container = d3.select('#heatmap').append('div').attr('class', 'container-fluid');
    var containerRow1 = container.append('div').attr('class', 'row');
    var containerRow2 = container.append('div').attr('class', 'row');
    var containerRow3 = container.append('div').attr('class', 'row');

    // div for title
    //containerRow1.append('div').attr('class', 'col-xs-12').html('<h1>Load and Price Visualisation</h1>');

    // div for loads and prices heat maps
    var priceDivHM = containerRow2.append('div').attr('class', 'col-xs-4').attr('id', 'price-div');
    var loadfwDivHM = containerRow2.append('div').attr('class', 'col-xs-4').attr('id', 'loadfw-div');
    var loadDivHM = containerRow2.append('div').attr('class', 'col-xs-4').attr('id', 'load-div');

    var maxWidth = parseInt(d3.select('.col-xs-4').style('width'), 10),
    //maxHeight = window.innerHeight;
        maxHeight = window.innerHeight;

    // legend settings
    var legendRectSize = 25,
        legendSpacing = 4;

    var margin = {top: 20, right: 20, bottom: 30, left: 70},
        width = maxWidth - margin.left - margin.right - (legendRectSize + legendSpacing) * 6,
    //height = width * aspect - margin.top - margin.bottom,
        height = maxHeight - (margin.top + margin.bottom) * 2 - parseInt(d3.select('#selectionDropdown').style('height'), 10) - parseInt(d3.select('.site-footer').style('height'), 10),
    //colorsLoad = ['rgb(255,247,243)', 'rgb(73,0,106)', 'rgb(0, 0, 0)'],
    //    colorsLoad = ['#fff7ec', '#fee8c8', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#b30000', '#7f0000'],
        colorsLoad = ['#fff7f3', '#fde0dd', '#fcc5c0', '#fa9fb5', '#f768a1', '#dd3497', '#ae017e', '#7a0177', '#49006a'],
    //colorsPrice = ['rgb(239, 236, 224)', 'rgb(rgb(0, 69, 41)'];
    //    colorsPrice = ['#f7fcfd','#e5f5f9','#ccece6', '#99d8c9', '#66c2a4', '#41ae76', '#238b45', '#006d2c', '#00441b'],
    //    colorsPrice = ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603', '#7f2704'],
        colorsPrice = ['#fff7fb', '#ece2f0', '#d0d1e6', '#a6bddb', '#67a9cf', '#3690c0', '#02818a', '#016c59', '#014636'],
    //colorsPrice = ['#a50026','#d73027','#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695'],
        hooverGraphHeight = 150;

    var formatTime = d3.time.format("%H"),
        formatHour = function (d) {
            //if (d == 24) return "noon";
            if (d == 48 || d == 0) return " ";
            return formatTime(new Date(2013, 2, 9, d / 2, 00));
        };

    var x = d3.scale.linear().rangeRound([0, width]);
    var xAxis = d3.svg.axis().scale(x).orient("bottom").tickFormat(formatHour);
    xAxis.ticks(Math.floor(width / 30));

    var y = d3.scale.linear().rangeRound([0, height]);
    var yAxis = d3.svg.axis().scale(y).orient("left").tickFormat(d3.format("d"));
    yAxis.ticks(Math.floor(height / 50));

    // color scale for loads and prices
    //var colorLoad = d3.scale.category20b(),
    //    colorPrice = d3.scale.category20c();
    //var colorLoad = d3.scale.linear().range(colorsLoad),
    //    colorPrice = d3.scale.linear().range(colorsPrice);

    // svg for loads and prices
    var svgWidth = width + margin.left + margin.right + (legendRectSize + legendSpacing) * 6;
    var svgHeight = height + (margin.top + margin.bottom) * 2;
    var svgLoad = loadDivHM.append('svg')
        .attr('id', 'svgLoad')
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var svgLoadfw = loadfwDivHM.append('svg')
        .attr('id', 'svgLoad')
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var svgPrice = priceDivHM.append('svg')
        .attr('id', 'svgPrice')
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // tooltips for loads and prices
    var tooltipLoad = loadDivHM.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipLoad.append('div').attr('class', 'iter');
    tooltipLoad.append('div').attr('class', 'load');
    tooltipLoad.append('div').attr('class', 'time');

    var tooltipLoadfw = loadfwDivHM.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipLoadfw.append('div').attr('class', 'iter');
    tooltipLoadfw.append('div').attr('class', 'load');
    tooltipLoadfw.append('div').attr('class', 'time');

    var tooltipPrice = priceDivHM.append('div').attr('class', 'tooltips').classed('hidden', true);
    tooltipPrice.append('div').attr('class', 'iter');
    tooltipPrice.append('div').attr('class', 'price');
    tooltipPrice.append('div').attr('class', 'time');

    // labels for loads and prices
    svgLoad.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("No. of iterations")
        .attr("class", "mono");

    svgLoadfw.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("No. of iterations")
        .attr("class", "mono");

    svgPrice.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("No. of iterations")
        .attr("class", "mono");

    // legend for loads and prices

    // legend scale for loads and prices
    //var legendScaleLoad = d3.scale.linear().domain([0, legendData.length]);
    //var legendScalePrice = d3.scale.linear().domain([0, legendData.length]);
    var numColorsInLegends = Math.floor(height / legendRectSize),
        colorLoad = d3.scale.quantize().range(colorsLoad),
        colorLoadfw = d3.scale.quantize().range(colorsLoad),
        colorPrice = d3.scale.quantize().range(colorsPrice);
    //colorLoad = d3.scale.linear().range(colorsLoad),
    //colorPrice = d3.scale.linear().range(colorsPrice);


    //var legendLoad = svgLoad.selectAll(".legend").data(legendData).enter().append("g").attr("class", "legend");
    //var legendPrice = svgPrice.selectAll(".legend").data(legendData).enter().append("g").attr("class", "legend");
    //var legendLoad = svgLoad.selectAll(".legend").data(d3.range(numColorsInLegends)).enter().append("g").attr("class", "legend");
    //var legendPrice = svgPrice.selectAll(".legend").data(d3.range(numColorsInLegends)).enter().append("g").attr("class", "legend");
    //console.log(colorLoad.range());

    // legend arrow for loads and prices
    var arrowLoad = loadDivHM.append('div').attr('class', 'arrow').classed('hidden', true);
    var arrowLoadfw = loadfwDivHM.append('div').attr('class', 'arrow').classed('hidden', true);
    var arrowPrice = priceDivHM.append('div').attr('class', 'arrow').classed('hidden', true);

    //******************** Start: codes for preparing hoover line graph ********************

    svgHooverHeight = hooverGraphHeight + (margin.top + margin.bottom);
    var yLineLoad = d3.scale.linear().rangeRound([hooverGraphHeight, 0]);
    var yLineLoadAxis = d3.svg.axis().scale(yLineLoad).orient("left");
    yLineLoadAxis.ticks(hooverGraphHeight / 20);

    var yLineLoadfw = d3.scale.linear().rangeRound([hooverGraphHeight, 0]);
    var yLineLoadfwAxis = d3.svg.axis().scale(yLineLoadfw).orient("left");
    yLineLoadfwAxis.ticks(hooverGraphHeight / 20);

    var yLinePrice = d3.scale.linear().rangeRound([hooverGraphHeight, 0]);
    var yLinePriceAxis = d3.svg.axis().scale(yLinePrice).orient("left");
    yLinePriceAxis.ticks(hooverGraphHeight / 20);

    // line graphs for loads and prices
    var lineGraphLoad = loadDivHM.append('div').attr('class', 'linegraphs').classed('hidden', true);

    var svgLineLoad = lineGraphLoad.append('svg').attr('id', 'svgLineLoad')
        .attr('width', svgWidth - (legendRectSize + legendSpacing * 3) * 5)
        .attr('height', svgHooverHeight)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    svgLineLoad.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (svgHooverHeight / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Load (kw)")
        .attr("class", "mono");

    //var legendLineLoad = svg.selectAll('.legend')
    //    .data(['#aaa', '#49006a']).append('g')
    //    .attr('class', 'legend').append('text')
    //    .attr('x', svgWidth - (legendRectSize + legendSpacing) * 5)
    //    .attr('y', )
    //    .text(function(d){ return 'test'; });

    var lineGraphLoadfw = loadfwDivHM.append('div').attr('class', 'linegraphs').classed('hidden', true);

    var svgLineLoadfw = lineGraphLoadfw.append('svg').attr('id', 'svgLineLoadfw')
        .attr('width', svgWidth - (legendRectSize + legendSpacing * 3) * 5)
        .attr('height', svgHooverHeight)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    svgLineLoadfw.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (svgHooverHeight / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Load FW (kw)")
        .attr("class", "mono");

    var lineGraphPrice = priceDivHM.append('div').attr('class', 'linegraphs').classed('hidden', true);

    var svgLinePrice = lineGraphPrice.append('svg').attr('id', 'svgLinePrice')
        .attr('width', svgWidth - (legendRectSize + legendSpacing * 3) * 5)
        .attr('height', svgHooverHeight)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    svgLinePrice.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (svgHooverHeight / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Price (cent)")
        .attr("class", "mono");


    //******************** Start: codes for preparing analysis view ********************

    //// container for analysis graphs
    //d3.select('#anaylsis').html('');
    //var containerAnalysis = d3.select('#anaylsis').append('div').attr('class', 'container-fluid');
    //var containerRow1Analysis = containerAnalysis.append('div').attr('class', 'row');
    ////containerRow1Analysis.innerHTML('<h3>Coming up soon...</h3>');


    // load data
    d3.json(file, function (error, data) {

        //******************** Start: loading data for heat map view ********************

        // maximum values of time step, load, and price
        var iterMax = 1 + d3.max(data, function (d) {
                return d.key;
            });
        var loadMax = d3.max(data, function (d) {
            return d3.max(d.loads);
            //return d3.mean(d.loads);
        });
        var loadfwMax = d3.max(data, function (d, i) {
            if (i == 0) return d3.max(data[1].loads_fw);
            else return d3.max(d.loads_fw);
            //return d3.mean(d.loads);
        });
        var priceMax = d3.max(data, function (d) {
            return d3.max(d.prices);
            //return d3.mean(d.prices);
        });
        var periodMax = d3.max(data[0].loads, function (d, i) {
            return i;
        });
        //var loadMax_round = Math.ceil(Math.ceil(loadMax / numColorsInLegends) * numColorsInLegends / 5) * 5;
        var loadMax_round = Math.ceil(loadMax / numColorsInLegends / 5) * numColorsInLegends * 5;
        var loadfwMax_round = Math.ceil(loadfwMax / numColorsInLegends / 5) * numColorsInLegends * 5;
        var priceMax_round = Math.ceil(priceMax / numColorsInLegends / 5) * numColorsInLegends * 5;


        //console.log('number of colors = ' + numColorsInLegends);
        //console.log(loadMax);
        //console.log(loadMax_round);

        var initialLoad = data[0].loads;
        var initialLoadfw = data[1].loads_fw;
        var initialPrice = data[1].prices;

        x.domain([0, periodMax + 1]);
        y.domain([0, iterMax]);
        //yAxis.ticks(Math.floor(iterMax / 10));
        yLineLoad.domain([0, loadMax]);
        yLineLoadfw.domain([0, loadfwMax]);
        yLinePrice.domain([0, priceMax]);
        colorLoad.domain([0, loadMax_round]);
        colorLoadfw.domain([0, loadfwMax_round]);
        colorPrice.domain([0, priceMax_round]);
        //legendLoadText.domain([0, loadMax_round]);
        //legendPriceText.domain([0, priceMax_round]);

        // glucose for loads and prices
        var glucoseLoad = svgLoad.selectAll('.glucose')
            .data(data)
            .enter().append('g')
            .attr('class', 'glucose');
        var glucoseLoadfw = svgLoadfw.selectAll('.glucose')
            .data(data)
            .enter().append('g')
            .attr('class', 'glucose');
        var glucosePrice = svgPrice.selectAll('.glucose')
            .data(data)
            .enter().append('g')
            .attr('class', 'glucose');

        // glucose bins for loads and prices
        var binLoad = glucoseLoad.selectAll('.bin')
            .data(function (d) {
                return d.loads;
            })
            .enter().append('rect')
            .attr('class', 'bin')
            .attr('x', function (d, i) {
                return x(i);
            })
            .attr('width', function (d, i) {
                return x(i + 1) - x(i);
            })
            .style('fill', function (d) {
                return colorLoad(d);
            });
        var binLoadfw = glucoseLoadfw.selectAll('.bin')
            .data(function (d, i) {
                if (i == 0) return data[1].loads_fw;
                else return d.loads_fw;
            })
            .enter().append('rect')
            .attr('class', 'bin')
            .attr('x', function (d, i) {
                return x(i);
            })
            .attr('width', function (d, i) {
                return x(i + 1) - x(i);
            })
            .style('fill', function (d) {
                return colorLoadfw(d);
            });
        var binPrice = glucosePrice.selectAll('.bin')
            .data(function (d) {
                return d.prices;
            })
            .enter().append('rect')
            .attr('class', 'bin')
            .attr('x', function (d, i) {
                return x(i);
            })
            .attr('width', function (d, i) {
                return x(i + 1) - x(i);
            })
            .style('fill', function (d) {
                return colorPrice(d);
            });

        // show glucose bins for loads and prices
        glucoseLoad.each(function (d) {
            d3.select(this).selectAll('.bin')
                .attr('y', y(d.key))
                .attr('height', height / iterMax + 1);
        });
        glucoseLoadfw.each(function (d) {
            d3.select(this).selectAll('.bin')
                .attr('y', y(d.key))
                .attr('height', height / iterMax + 1);
        });
        glucosePrice.each(function (d) {
            d3.select(this).selectAll('.bin')
                .attr('y', y(d.key))
                .attr('height', height / iterMax + 1);
        });

        // x axis for loads and prices
        svgLoad.append('g')
            .attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(xAxis)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Time of day').attr('class', 'mono');
        svgLoadfw.append('g')
            .attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(xAxis)
            .append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Time of day').attr('class', 'mono');
        svgPrice.append('g')
            .attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(xAxis).append('text').attr('y', margin.bottom).attr('x', width / 2).attr('dy', '1em')
            .style('text-anchor', 'middle').text('Time of day').attr('class', 'mono');

        // y axis for loads and prices
        svgLoad.append('g')
            .attr('class', 'y-axis')
            .call(yAxis);
        svgLoadfw.append('g')
            .attr('class', 'y-axis')
            .call(yAxis);
        svgPrice.append('g')
            .attr('class', 'y-axis')
            .call(yAxis);

        svgLineLoad.append('g')
            .attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + hooverGraphHeight + ')')
            .call(xAxis);
        svgLineLoad.append('g')
            .attr('id', 'yaxisLineLoad')
            .attr('class', 'y-axis')
            .call(yLineLoadAxis);

        svgLineLoadfw.append('g')
            .attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + hooverGraphHeight + ')')
            .call(xAxis);
        svgLineLoadfw.append('g')
            .attr('id', 'yaxisLineLoadfw')
            .attr('class', 'y-axis')
            .call(yLineLoadfwAxis);

        svgLinePrice.append('g')
            .attr('class', 'x-axis')
            .attr('transform', 'translate(0, ' + hooverGraphHeight + ')')
            .call(xAxis);
        svgLinePrice.append('g')
            .attr('id', 'yaxisLinePrice')
            .attr('class', 'y-axis')
            .call(yLinePriceAxis);

        // hover line graph initialisation
        var lineLoad = d3.svg.line()
            .x(function (d, i) {
                return x(i);
                //return 50;
            })
            .y(function (d) {
                return yLineLoad(d);
                //return 50;
            });
        var lineLoadfw = d3.svg.line()
            .x(function (d, i) {
                return x(i);
                //return 50;
            })
            .y(function (d) {
                return yLineLoadfw(d);
                //return 50;
            });
        var linePrice = d3.svg.line()
            .x(function (d, i) {
                return x(i);
                //return 50;
            })
            .y(function (d) {
                return yLinePrice(d);
                //return 50;
            });

        // legend for loads and prices
        var legendLoad = svgLoad.selectAll(".legend")
            .data(d3.range(numColorsInLegends + (loadMax - loadMax_round) / (loadMax_round / numColorsInLegends)))
            .enter()
            .append("g").attr("class", "legend");
        var legendLoadfw = svgLoadfw.selectAll(".legend")
            .data(d3.range(numColorsInLegends + (loadfwMax - loadfwMax_round) / (loadfwMax_round / numColorsInLegends)))
            .enter()
            .append("g").attr("class", "legend");
        var legendPrice = svgPrice.selectAll(".legend")
            .data(d3.range(numColorsInLegends)).enter()
            .append("g").attr("class", "legend");
        //console.log((priceMax - priceMax_round) / (priceMax_round / numColorsInLegends));

        legendLoad.append('rect')
            .attr('x', width + (legendRectSize + legendSpacing) * 1.5)
            .attr('y', function (d, i) {
                return legendRectSize * i
            })
            .attr('width', legendRectSize)
            .attr('height', legendRectSize * 1.5)
            .style('fill', function (d, i) {
                //console.log(loadMax / (numColorsInLegends - d + 1));
                return colorLoad(loadMax_round / numColorsInLegends * d);
            });
        legendLoadfw.append('rect')
            .attr('x', width + (legendRectSize + legendSpacing) * 1.5)
            .attr('y', function (d, i) {
                return legendRectSize * i
            })
            .attr('width', legendRectSize)
            .attr('height', legendRectSize * 1.5)
            .style('fill', function (d, i) {
                //console.log(loadMax / (numColorsInLegends - d + 1));
                return colorLoad(loadfwMax_round / numColorsInLegends * d);
            });
        legendPrice.append('rect')
            .attr('x', width + (legendRectSize + legendSpacing) * 1.5)
            .attr('y', function (d, i) {
                return legendRectSize * i
            })
            .attr('width', legendRectSize)
            .attr('height', legendRectSize * 1.5)
            .style('fill', function (d, i) {
                return colorPrice(priceMax_round / numColorsInLegends * d);
            });

        legendLoad.append('text').attr('class', 'mono')
            .attr('x', width + (legendRectSize + legendSpacing) * 1.5)
            .attr('y', legendRectSize * (numColorsInLegends + 2))
            .text('Unit: kw');
        legendLoadfw.append('text').attr('class', 'mono')
            .attr('x', width + (legendRectSize + legendSpacing) * 1.5)
            .attr('y', legendRectSize * (numColorsInLegends + 2))
            .text('Unit: kw');
        legendPrice.append('text').attr('class', 'mono')
            .attr('x', width + (legendRectSize + legendSpacing) * 1.5)
            .attr('y', legendRectSize * (numColorsInLegends + 2))
            .text('Unit: cent');
        // console.log(numColorsInLegends);

        // legend text for loads and prices
        legendLoad.append('text')
            .attr('class', 'mono')
            .attr('x', margin.left + width + legendRectSize * 0.5)
            .attr('y', function (d, i) {
                return margin.top + legendRectSize * i
            })
            .text(function (d) {
                //console.log(legendScaleLoad(Math.floor(d/10)*10));
                //console.log(d);
                return loadMax_round / numColorsInLegends * d;
            });
        legendLoadfw.append('text')
            .attr('class', 'mono')
            .attr('x', margin.left + width + legendRectSize * 0.5)
            .attr('y', function (d, i) {
                return margin.top + legendRectSize * i
            })
            .text(function (d) {
                //console.log(legendScaleLoad(Math.floor(d/10)*10));
                //console.log(d);
                return loadfwMax_round / numColorsInLegends * d;
            });
        legendPrice.append('text')
            .attr('class', 'mono')
            .attr('x', margin.left + width + legendRectSize * 0.5)
            .attr('y', function (d, i) {
                return margin.top + legendRectSize * i
            })
            .text(function (d) {
                return priceMax_round / numColorsInLegends * d;
            });
        //console.log(legendData.length);
        //legend_text_loadMax = legendLoadText(legendData.length);
        //legend_text_PriceMax = legendPriceText(legendData.length);

        binLoad
            .on('mouseover', mouseover);
        binLoad
            .on('mouseout', mouseout);
        binLoadfw
            .on('mouseover', mouseover);
        binLoadfw
            .on('mouseout', mouseout);
        binPrice
            .on('mouseover', mouseover);
        binPrice
            .on('mouseout', mouseout);

        function mouseover() {
            var x0 = Math.floor(x.invert(d3.mouse(this)[0])),
                y0 = Math.floor(y.invert(d3.mouse(this)[1]));

            var price_itr = data[y0].prices,
                price_time = data[y0].prices[x0],
                load_itr = data[y0].loads,
                load_time = data[y0].loads[x0],
                loadfw_itr = data[y0].loads_fw,
                loadfw_time = data[y0].loads_fw[x0];

            binLoad.classed('bin-hover', function (d, x, y) {
                return (x == x0 && y == y0);
            });
            binLoadfw.classed('bin-hover', function (d, x, y) {
                return (x == x0 && y == y0);
            });
            binPrice.classed('bin-hover', function (d, x, y) {
                return (x == x0 && y == y0);
            });
            d3.selectAll(".x-axis text").classed("text-highlight", function (x) {
                return x == x0;
            });
            d3.selectAll(".y-axis text").classed("text-highlight", function (x) {
                return x == y0;
            });

            // update the tooltip position and value
            tooltipLoad.select('.iter').html('Iteration: ' + y0);
            tooltipLoad.select('.load').html('Load: ' + Math.round(load_time * 100) / 100 + ' kw');
            tooltipLoad.select('.time').html('Time step: ' + x0 + '');

            tooltipLoadfw.select('.iter').html('Iteration: ' + y0);
            tooltipLoadfw.select('.load').html('Load: ' + Math.round(loadfw_time * 100) / 100 + ' kw');
            tooltipLoadfw.select('.time').html('Time step: ' + x0 + '');

            tooltipPrice.select('.iter').html('Iteration: ' + y0);
            tooltipPrice.select('.price').html('Price: ' + Math.round(price_time * 100) / 100 + ' c');
            tooltipPrice.select('.time').html('Time step: ' + x0 + '');

            tooltipLoad.style('left', '10px').style('top', (d3.event.pageY) - 10 * 10 + 'px');
            tooltipLoad.classed('hidden', false);

            tooltipLoadfw.style('left', '10px').style('top', (d3.event.pageY) - 10 * 10 + 'px');
            tooltipLoadfw.classed('hidden', false);

            tooltipPrice.style('left', '10px').style('top', (d3.event.pageY) - 10 * 10 + 'px');
            tooltipPrice.classed('hidden', false);

            //update the line graphs position and value
            var yLineLoadDomain = d3.max([d3.max(load_itr), d3.max(initialLoad)]);
            yLineLoad.domain([0, yLineLoadDomain]);
            d3.selectAll('#yaxisLineLoad')
                .call(yLineLoadAxis);

            var yLineLoadfwDomain = d3.max([d3.max(loadfw_itr), d3.max(initialLoadfw)]);
            yLineLoadfw.domain([0, yLineLoadfwDomain]);
            d3.selectAll('#yaxisLineLoadfw')
                .call(yLineLoadfwAxis);

            var yLinePriceDomain = d3.max([d3.max(price_itr), d3.max(initialPrice)]);
            yLinePrice.domain([0, yLinePriceDomain]);
            d3.selectAll('#yaxisLinePrice')
                .call(yLinePriceAxis);

            if (d3.select("#currentLineLoad")[0][0] == null) {
                svgLineLoad.append('path').datum(data[0].loads).attr('class', 'line').attr('id', 'initialLineLoad').attr('d', lineLoad);
                svgLineLoad.append('path').datum(load_itr).attr('class', 'line').attr('id', 'currentLineLoad').attr('d', lineLoad);
            }
            else {
                d3.selectAll('#initialLineLoad').datum(data[0].loads).attr('class', 'line').attr('id', 'initialLineLoad').attr('d', lineLoad);
                d3.selectAll('#currentLineLoad').datum(load_itr).attr('class', 'line').attr('id', 'currentLineLoad')
                    .attr('d', lineLoad);
            }
            lineGraphLoad.style('left', (5) + 'px').style('top', function () {
                if ((d3.event.pageY + svgHooverHeight) < svgHeight) {
                    return (d3.event.pageY) - 15 + 'px';
                }
                else {
                    return (d3.event.pageY) - 33 * 11 + 'px';
                }
            });
            lineGraphLoad.classed('hidden', false);

            if (d3.select("#currentLineLoadfw")[0][0] == null) {
                svgLineLoadfw.append('path').datum(data[1].loads_fw).attr('class', 'line').attr('id', 'initialLineLoadfw').attr('d', lineLoadfw);
                svgLineLoadfw.append('path').datum(loadfw_itr).attr('class', 'line').attr('id', 'currentLineLoadfw').attr('d', lineLoadfw);
            }
            else {
                d3.selectAll('#initialLineLoadfw').datum(data[1].loads_fw).attr('class', 'line').attr('id', 'initialLineLoadfw').attr('d', lineLoadfw);
                d3.selectAll('#currentLineLoadfw').datum(loadfw_itr).attr('class', 'line').attr('id', 'currentLineLoadfw').attr('d', lineLoadfw);
            }
            lineGraphLoadfw.style('left', (5) + 'px').style('top', function () {
                if ((d3.event.pageY + svgHooverHeight) < svgHeight) {
                    return (d3.event.pageY) - 15 + 'px';
                }
                else {
                    return (d3.event.pageY) - 33 * 11 + 'px';
                }
            });
            lineGraphLoadfw.classed('hidden', false);

            if (d3.select("#currentLinePrice")[0][0] == null) {
                svgLinePrice.append('path').datum(data[0].prices).attr('class', 'line').attr('id', 'initialLinePrice').attr('d', linePrice);
                svgLinePrice.append('path').datum(price_itr).attr('class', 'line').attr('id', 'currentLinePrice').attr('d', linePrice);
            }
            else {
                d3.selectAll('#initialLinePrice').datum(data[1].prices).attr('class', 'line').attr('id', 'initialLinePrice').attr('d', linePrice);

                d3.selectAll('#currentLinePrice').datum(price_itr).attr('class', 'line').attr('id', 'currentLinePrice').attr('d', linePrice);
            }
            lineGraphPrice.style('left', (5) + 'px').style('top', function () {
                if ((d3.event.pageY + svgHooverHeight) < svgHeight) {
                    return (d3.event.pageY) - 15 + 'px';
                }
                else {
                    return (d3.event.pageY) - 33 * 11 + 'px';
                }
            });
            lineGraphPrice.classed('hidden', false);

            // update the arrow position
            arrowLoad.transition()
                .style("top", legendRectSize * (1 + load_time / loadMax_round * numColorsInLegends) + "px")
                .style("left", (width + margin.left + margin.right + (legendRectSize + legendSpacing)) + "px");
            arrowLoad.classed("hidden", false);
            arrowLoadfw.transition()
                .style("top", legendRectSize * (1 + loadfw_time / loadfwMax_round * numColorsInLegends) + "px")
                .style("left", (width + margin.left + margin.right + (legendRectSize + legendSpacing)) + "px");
            arrowLoadfw.classed("hidden", false);
            arrowPrice.transition()
                .style("top", legendRectSize * (1 + price_time / priceMax_round * numColorsInLegends) + "px")
                .style("left", (width + margin.left + margin.right + (legendRectSize + legendSpacing)) + "px");
            arrowPrice.classed("hidden", false);
        }

        function mouseout() {
            binLoad.classed('bin-hover', false);
            binLoadfw.classed('bin-hover', false);
            binPrice.classed('bin-hover', false);
            d3.selectAll(".x-axis text").classed("text-highlight", false);
            d3.selectAll(".y-axis text").classed("text-highlight", false);
            tooltipLoad.classed('hidden', true);
            tooltipLoadfw.classed('hidden', true);
            tooltipPrice.classed('hidden', true);
            lineGraphLoad.classed('hidden', true);
            lineGraphLoadfw.classed('hidden', true);
            lineGraphPrice.classed('hidden', true);
            arrowLoad.classed('hidden', true);
            arrowLoadfw.classed('hidden', true);
            arrowPrice.classed('hidden', true);
        }
    });
}

function resize() {
    var file = d3.select("#selectionDropdown").property("value");
    visualiseLoadsPrices(file);
    loadsPriceAnalysis(file);
    //maxWidth = parseInt(d3.select('.container-fluid').style('width'), 10);
}

var TO = false;
d3.select(window)
    .on('resize', function () {
        if (TO !== false)
            clearTimeout(TO);
        TO = setTimeout(resize, 400);
    });

