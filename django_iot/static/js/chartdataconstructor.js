/*
 * File: chartdataconstructor.js
 * Project: js
 * File Created: Wednesday, 28th October 2020 4:25:19 pm
 * Author: Jongyeon Yoon (0417yjy@naver.com)
 * -----
 * Last Modified: Wednesday, 28th October 2020 4:25:35 pm
 * Modified By: Jongyeon Yoon (0417yjy@naver.com>)
 * -----
 * Copyright 2020 Jongyeon Yoon
 */

function ChartDataSets(label) {
    this.label = label;
    this.data = [];
}

function ChartData(label) {
    this.labels = []; // x-axis (date)
    this.datasets = [];
    this.datasets.push(new ChartDataSets(label));
}

function ChartConfig(label, backgroundColor, borderColor) {
    this.type = 'line';
    this.data = new ChartData(label);
    this.backgroundColor = backgroundColor;
    this.borderColor = borderColor;
}

function getDataArray(json_arr) {
    const CHART_NUM = 6;
    var charts = [
        new ChartConfig('Temperature', '#FF0000', '#FF0000'), 
        new ChartConfig('Humidity', '#FF0000', '#FF0000'), 
        new ChartConfig('Illumination', '#FF0000', '#FF0000'), 
        new ChartConfig('Rador', '#FF0000', '#FF0000'), 
        new ChartConfig('CO2', '#FF0000', '#FF0000'), 
        new ChartConfig('tVOC', '#FF0000', '#FF0000'),
    ];
    var i, j;
    for (i = 0; i < json_arr.length; i++) {
        var data_arr = [
            json_arr[i].fields.temp,
            json_arr[i].fields.humid,
            json_arr[i].fields.illum,
            json_arr[i].fields.radar,
            json_arr[i].fields.co2,
            json_arr[i].fields.tvoc,
        ];

        for(j=0;j<CHART_NUM;j++) {
            var updated_time = json_arr[i].fields.updated_time;
            charts[j].data.labels.push(updated_time);
            charts[j].data.datasets[0].data.push(data_arr[j]);
        }
    }
    return charts;
}