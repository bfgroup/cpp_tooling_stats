
function render_execution_item(params, api) {
    var categoryIndex = api.value(0);
    var start = api.coord([api.value(1), categoryIndex]);
    var end = api.coord([api.value(2), categoryIndex]);
    var height = api.size([0, 1])[1] * 0.4;

    var rectShape = echarts.graphic.clipRectByRect({
        x: start[0],
        y: start[1] - height / 2,
        width: end[0] - start[0],
        height: height
    }, {
        x: params.coordSys.x,
        y: params.coordSys.y,
        width: params.coordSys.width,
        height: params.coordSys.height
    });

    return rectShape && {
        type: 'rect',
        shape: rectShape,
        style: api.style()
    };
}

function create_execution_chart(target, title, data) {
    var categories = [];
    echarts.util.each(data, function(item, index) {
        if (!categories.includes(item[0])) categories.push(item[0]);
    });
    categories.sort(function(a, b){return b-a});
    var chart = echarts.init(document.getElementById(target));
    chart.setOption({
        tooltip: {
            formatter: function (params) {
                return params.value[3] + ' s';
            }
        },
        title: title,
        dataZoom: [{
            type: 'slider',
            filterMode: 'weakFilter',
            showDataShadow: false,
            top: 800,
            height: 10,
            borderColor: 'transparent',
            backgroundColor: '#e2e2e2',
            handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7v-1.2h6.6z M13.3,22H6.7v-1.2h6.6z M13.3,19.6H6.7v-1.2h6.6z',
            handleSize: 20,
            handleStyle: {
                shadowBlur: 6,
                shadowOffsetX: 1,
                shadowOffsetY: 2,
                shadowColor: '#aaa'
            },
            labelFormatter: ''
        }, {
            type: 'inside',
            filterMode: 'weakFilter'
        }],
        grid: {
            height:700
        },
        xAxis: {
            min: 0,
            scale: true,
            axisLabel: {
                formatter: function (val) {
                    return val + ' s';
                }
            }
        },
        yAxis: {
            data: categories
        },
        series: [{
            type: 'custom',
            renderItem: render_execution_item,
            itemStyle: {
                normal: {
                    opacity: 1,
                    color: '#ccd',
                    borderWidth: 1.0,
                    borderColor: '#000'
                }
            },
            encode: {
                x: [1, 2],
                y: 0
            },
            data: data
        }]
    });
}