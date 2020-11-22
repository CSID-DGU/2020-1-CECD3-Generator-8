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

$.getScript("/static/js/dateformat.js");
var tempChart, humidChart, illumChart, radorChart, co2Chart, tvocChart;
const PERIOD_MINUTE = 10;

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
  this.datasets.push(new ChartDataSets(label, backgroundColor, '#adadad'));
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
        // type: 'time',
        // time: {
        //   displayFormats: {
        //     second: "yyyy-mm-dd'T'HH:MM:ss"
        //   }
        // },
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
  var i, j, k;
  var date = "";
  for (i = 0; i < json_arr.length; i++) {
    var data_arr = [
      json_arr[i].temp,
      json_arr[i].humid,
      json_arr[i].illum,
      json_arr[i].radar,
      json_arr[i].co2,
      json_arr[i].tvoc,
    ];
    var today = new Date();
    var today_minus_3 = today;
    today_minus_3.setDate(today_minus_3.getDate() - 3);
    var updated_time = new Date(json_arr[i].updated_time);
    var updated_time2 = new Date(json_arr[i].updated_time);
    var formated_updated_time = dateFormat(updated_time, "yyyy-mm-dd'T'HH:MM:ss");
    var updated_date = formated_updated_time.substring(0, 10);

    if (date != updated_date) {
      date = updated_date;
    } else {
      formated_updated_time = formated_updated_time.substr(11);
    }

    if (updated_time2 < today_minus_3) {//처음 들어온 데이터가 3일전이면 고장

      for (j = 0; j < CHART_NUM; j++) {
        charts[j].data.labels.push(formated_updated_time);
        charts[j].data.datasets[0].data.push(data_arr[j]);
        charts[j].data.datasets[1].data.push(data_arr[j]);
      }
      for (j = 0; j < CHART_NUM; j++) {
        charts[j].data.labels.push(dateFormat(new Date(), "yyyy-mm-dd'T'HH:MM:ss"));
        //charts[j].data.datasets[0].data.push(data_arr[j]);
        charts[j].data.datasets[1].data.push(data_arr[j]);
      }
      return charts;
    }
    else {//아니라면 정상적으로 값 넣기
      for (j = 0; j < CHART_NUM; j++) {
        charts[j].data.labels.push(formated_updated_time);
        charts[j].data.datasets[0].data.push(data_arr[j]);
        charts[j].data.datasets[1].data.push(null);
      }


      if (i = json_arr.length - 1) {
        for (j = 0; j < CHART_NUM; j++) {
          charts[j].data.labels.push(dateFormat(new Date(), "yyyy-mm-dd'T'HH:MM:ss"));
          charts[j].data.datasets[0].data.push(data_arr[j]);
          // charts[j].data.datasets[1].data.push(null);
        }
      }

      // check gap between next log
      var next_log_updated_time;
      // get next log's updated time
      if (i == json_arr.length - 1) {
        next_log_updated_time = new Date(); // for the last log, next updated time is current time
      }
      else {
        next_log_updated_time = new Date(json_arr[i + 1].updated_time);
      }
      console.log("cur: " + updated_time + "\nnext: " + next_log_updated_time);

      // calculate difference in minute
      var diff_minutes_between_logs = Math.floor(((next_log_updated_time - updated_time) / 1000) / 60);
      console.log(diff_minutes_between_logs);
      // calculate numbers of missed logs
      var num_missed_logs = diff_minutes_between_logs / PERIOD_MINUTE - 1;
      console.log(num_missed_logs);
      for (j = 1; j < num_missed_logs; j++) {
        var missed_updated_time = new Date(updated_time.getTime() + j * 1000 * 60 * PERIOD_MINUTE);
        var formated_missed_updated_time = dateFormat(missed_updated_time, "yyyy-mm-dd'T'HH:MM:ss");
        var missed_updated_date = formated_missed_updated_time.substring(0, 10);
        if (date != missed_updated_date) {
          date = missed_updated_date;
        } else {
          formated_missed_updated_time = formated_missed_updated_time.substr(11);
        }
        console.log('Pushing ' + formated_missed_updated_time);
        for (k = 0; k < CHART_NUM; k++) {
          charts[k].data.labels.push(formated_missed_updated_time);
          charts[k].data.datasets[1].data.push(data_arr[k]);
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