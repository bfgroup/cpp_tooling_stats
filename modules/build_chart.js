// Copyright (C) 2018-2019 Rene Rivera.
// Use, modification and distribution are subject to the
// Boost Software License, Version 1.0. (See accompanying file
// LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
function parallel_build_value_fmt(v) {
    return Number.parseFloat(v).toFixed(1).toString();
}
function create_parallel_build_chart(target, title, data) {
    var chart = echarts.init(document.getElementById(target));
    chart.setOption({
        title: title,
        legend: { data: ['Non-Modular', 'Modular'] },
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' }
        },
        xAxis: [{ name: 'DAG Depth', type: 'category', nameLocation: 'center', nameGap: 30 }],
        yAxis: [{ name: 'Wall Clock Seconds', type: 'value', nameLocation: 'center', nameGap: 45 }],
        series: [
            {
                name: 'Non-Modular',
                type: 'bar',
                // type: 'pictorialBar', symbol: 'rect',
                label: {
                    normal: {
                        show: true, position: 'top', rotate: 90,
                        align: 'left', verticalAlign: 'middle',
                        formatter: function (params) { return parallel_build_value_fmt(params.value[1]); }
                    }
                },
                encode: { x: 'dag_depth', y: 'headers' },
            },
            {
                name: 'Modular',
                type: 'bar',
                // type: 'pictorialBar', symbol: 'roundRect', symbolRepeat: true, symbolSize: ['100%', 5], barGap: '0%',
                label: {
                    normal: {
                        show: true, position: 'top', rotate: 90,
                        align: 'left', verticalAlign: 'middle',
                        formatter: function (params) { return parallel_build_value_fmt(params.value[2]); }
                    }
                },
                encode: { x: 'dag_depth', y: 'modules' },
                formatter: parallel_build_value_fmt,
            },
        ],
        dataset: { source: data }
    });
}

function create_parallel_build_chart_multi(target, title, compiler_and_data) {
    var compilers = [];
    var dataset = [];
    var series = [];
    var legend = [];
    var line_styles = [
        { normal: { type: 'solid' } },
        { normal: { type: 'dashed' } },
        { normal: { type: 'dotted' } },
    ];
    while (compiler_and_data.length > 0) {
        var compiler = compiler_and_data.shift();
        var table = compiler_and_data.shift();
        compilers.push(compiler);
        dataset.push({ source: table });
        legend.push('Non-Modular, ' + compiler);
        series.push({
            name: 'Non-Modular, ' + compiler,
            type: 'line',
            smooth: true,
            symbol: 'triangle', symbolSize: 10,
            lineStyle: line_styles[(dataset.length - 1) % line_styles.length],
            encode: { x: 'dag_depth', y: 'headers' },
            datasetIndex: dataset.length - 1
        });
        legend.push('Modular, ' + compiler);
        series.push({
            name: 'Modular, ' + compiler,
            type: 'line',
            smooth: true,
            symbol: 'circle', symbolSize: 10,
            lineStyle: line_styles[(dataset.length - 1) % line_styles.length],
            encode: { x: 'dag_depth', y: 'modules' },
            datasetIndex: dataset.length - 1
        });
    }
    var chart = echarts.init(document.getElementById(target));
    chart.setOption({
        title: title,
        legend: { data: legend },
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' }
        },
        xAxis: [
            { name: 'DAG Depth', type: 'category', nameLocation: 'center', nameGap: 30 }
        ],
        yAxis: [
            { name: 'Wall Clock Seconds', type: 'value', nameLocation: 'center', nameGap: 45 }
        ],
        series: series,
        dataset: dataset
    });
}
