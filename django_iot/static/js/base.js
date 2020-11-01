/* globals Chart:false, feather:false */

function updateClock() {
  var now = new Date(), // current date
    time = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds(), // again, you get the idea

    // a cleaner way than string concatenation
    date = [now.getFullYear(),
    now.getMonth() + 1,
    now.getDate()].join('-');

  // set the content of the element with the ID time to the formatted string
  document.getElementById('currenttime').innerHTML = [date, time].join(' / ');

  // call this function again in 1000ms
  setTimeout(updateClock, 1000);
}
updateClock(); // initial call