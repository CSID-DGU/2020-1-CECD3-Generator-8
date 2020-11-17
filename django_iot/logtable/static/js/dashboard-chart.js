/*
 * File: dashboard-chart.js
 * Project: js
 * File Created: Monday, 16th November 2020 11:57:57 pm
 * Author: Jongyeon Yoon (0417yjy@naver.com)
 * -----
 * Last Modified: Tuesday, 17th November 2020 12:02:20 am
 * Modified By: Jongyeon Yoon (0417yjy@naver.com>)
 * -----
 * Copyright 2020 Jongyeon Yoon
 */
$.getScript("https://unpkg.com/dateformat@3.0.3/lib/dateformat.js");
var tempChart, humidChart, illumChart, radorChart, co2Chart, tvocChart;

function ChartDataSets(label, backgroundColor, borderColor) {
    this.label = label;
    // this.backgroundColor = backgroundColor; // use default value
    this.borderColor = borderColor;
    this.pointRadius = 2;
    this.data = [];
  }

  function ChartData(label, backgroundColor, borderColor) {
    this.labels = []; // x-axis (date)
    this.datasets = [];
    this.datasets.push(new ChartDataSets(label, backgroundColor, borderColor));
    this.datasets.push(new ChartDataSets('broken', backgroundColor, borderColor));
  }

  function ChartConfig(label, sign, backgroundColor, borderColor, minValue, maxValue, step) {
    this.type = 'line';
    this.data = new ChartData(label, backgroundColor, borderColor);
    this.options = {
      responsive: true,
      title: {
        text: label,
        position: 'top',
        display: true,
        fontSize: 25
      },
      legend: {
        display: false,
      },
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      hover: {
        mode: 'nearest',
        intersect: true,
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              suggestedMin: minValue,
              suggestedMax: maxValue,
              callback: function (value, index, values) {
                return value + sign;
              }
            }
          }
        ],
        xAxes: [{
          ticks: {
            fontSize: 10
          }
        }]
      }
    };
  }

  function getDataArray(json_arr) {
    const CHART_NUM = 6;
    const borderColor = '#FF0000';
    const backgroundColor = "#e0e0e0";
    var charts = [
      new ChartConfig('Temperature', '°C', backgroundColor, borderColor, -10, 85, 5),
      new ChartConfig('Humidity', '%', backgroundColor, borderColor, 0, 100, 5),
      new ChartConfig('Illumination', '%', backgroundColor, borderColor, 0, 100, 5),
      new ChartConfig('Rador', '', backgroundColor, borderColor, 0, 100, 50),
      new ChartConfig('CO2', 'ppm', backgroundColor, borderColor, 0, 8192, 400),
      new ChartConfig('tVOC', 'ppb', backgroundColor, borderColor, 0, 1187, 50),
    ];
    var i, j;
    var date = "";
    var today = new Date();
    for (i = 0; i < json_arr.length; i++) {
      var data_arr = [
        json_arr[i].temp,
        json_arr[i].humid,
        json_arr[i].illum,
        json_arr[i].radar,
        json_arr[i].co2,
        json_arr[i].tvoc,
      ];
      var updated_time = new Date(json_arr[i].updated_time);
      updated_time = dateFormat(updated_time, "yyyy-mm-dd'T'HH:MM:ss");
      var updated_date = updated_time.substring(0, 10);
      if (date != updated_date) {
        date = updated_date;
      } else {
        updated_time = updated_time.substr(11);
      }

      for (j = 0; j < CHART_NUM; j++) {
        charts[j].data.labels.push(updated_time);
        charts[j].data.datasets[0].data.push(data_arr[j]);

        if (i === json_arr.length - 1) {
          charts[j].data.datasets[1].data.push(data_arr[j]);
        } else {
          charts[j].data.datasets[1].data.push(null);
        }
      }
    }

    data_arr = [
      json_arr[json_arr.length - 1].temp,
      json_arr[json_arr.length - 1].humid,
      json_arr[json_arr.length - 1].illum,
      json_arr[json_arr.length - 1].radar,
      json_arr[json_arr.length - 1].co2,
      json_arr[json_arr.length - 1].tvoc,
    ];

    var y = updated_time.substr(0, 4);
    var m = updated_time.substr(5, 2);
    var d = updated_time.substr(8, 2);
    var hh = updated_time.substr(11, 2);
    var mm = updated_time.substr(14, 2);
    var ss = updated_time.substr(17, 2);

    var last_updated_time = new Date(y, m - 1, d, hh, mm, ss); //updated_time을 date형식으로 변환
    last_updated_time.setMinutes(last_updated_time.getMinutes() + 13) //12분더하기

    var i = last_updated_time;
    var today_minus_3 = today;
    today_minus_3.setDate(today_minus_3.getDate() - 3);
    date2 = updated_date;
    today = new Date();

    if (last_updated_time < today) {//업뎃시간이 현재시간보다 12분이상 차이나면 10분 간격으로 그리기
      if (last_updated_time < today_minus_3) { //마지막 업데이트가 3일이상 차이나면
        var j = today_minus_3;

        for (j; j < today; j.setMinutes(j.getMinutes() + 10)) {
          var input_date = String(j.getFullYear()) + '-' + ("00" + String(j.getMonth() + 1)).slice(-2) + '-' + ("00" + String(j.getDate())).slice(-2) + 'T' + ("00" + String(j.getHours())).slice(-2) + ':' + ("00" + String(j.getMinutes())).slice(-2) + ':' + ("00" + String(j.getSeconds())).slice(-2);
          var input_time2 = input_date;
          var updated_date2 = input_date.substr(0, 10);

          if (date2 != updated_date2) {
            date2 = updated_date2;
          } else {
            input_time2 = input_date.substr(11);
          }

          for (var k = 0; k < CHART_NUM; k++) {
            charts[k].data.labels.push(input_time2);
            charts[k].data.datasets[1].data.push(data_arr[k]);
            charts[k].data.datasets[1].borderColor = '#adadad';
          }
        }
      }
      else {
        for (i; i < today; i.setMinutes(i.getMinutes() + 10)) {
          var input_date = String(i.getFullYear()) + '-' + ("00" + String(i.getMonth() + 1)).slice(-2) + '-' + ("00" + String(i.getDate())).slice(-2) + 'T' + ("00" + String(i.getHours())).slice(-2) + ':' + ("00" + String(i.getMinutes())).slice(-2) + ':' + ("00" + String(i.getSeconds())).slice(-2);
          var input_time2 = input_date;
          var updated_date2 = input_date.substr(0, 10);

          if (date2 != updated_date2) {
            date2 = updated_date2;
          } else {
            input_time2 = input_date.substr(11);
          }

          for (var k = 0; k < CHART_NUM; k++) {
            charts[k].data.labels.push(input_time2);
            charts[k].data.datasets[1].data.push(data_arr[k]);
            charts[k].data.datasets[1].borderColor = '#adadad';

          }
        }
      }
    }

    return charts;
  }

  function chartButtonHandler(item) {
    var pid = item.parentNode.id;
    var sensor_code = pid.substring(5);
    document.getElementById("chartModalLabel").innerHTML = sensor_code;

    var xmlhttp = new XMLHttpRequest();
    const SEARCH_DAYS = 3;
    var url = "sme20u/" + sensor_code + "/json/days/" + SEARCH_DAYS;

    xmlhttp.onreadystatechange = function () { // http response 받고 수행할 동작
      if (this.readyState == 4 && this.status == 200) {
        const sensor_values_arr = JSON.parse(this.responseText); // json파일을 object로 파싱
        var chart_data = getDataArray(sensor_values_arr); // chart.js에 적용할 수 있도록 변환

        // 각 값의 차트를 하나씩 생성
        var ctx = document.getElementById("temp_chart").getContext('2d');
        if (tempChart) tempChart.destroy();
        tempChart = new Chart(ctx, chart_data[0]);

        ctx = document.getElementById("humid_chart").getContext('2d');
        if (humidChart) humidChart.destroy();
        humidChart = new Chart(ctx, chart_data[1]);

        ctx = document.getElementById("illum_chart").getContext('2d');
        if (illumChart) illumChart.destroy();
        illumChart = new Chart(ctx, chart_data[2]);

        ctx = document.getElementById("rador_chart").getContext('2d');
        if (radorChart) radorChart.destroy();
        radorChart = new Chart(ctx, chart_data[3]);

        ctx = document.getElementById("co2_chart").getContext('2d');
        if (co2Chart) co2Chart.destroy();
        co2Chart = new Chart(ctx, chart_data[4]);

        ctx = document.getElementById("tvoc_chart").getContext('2d');
        if (tvocChart) tvocChart.destroy();
        tvocChart = new Chart(ctx, chart_data[5]);
      }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
  }