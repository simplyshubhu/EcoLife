window.onload = function () {
  startCount()
  getData()
}

var hour = 0
var mins = 0
var secs = 0
var status = 0

function getData () {
  var req = new XMLHttpRequest()
  console.log('inside getData')
  req.open('GET', '/timer', true)
  req.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      console.log(this.responseText)
      var time = JSON.parse(this.responseText)
      console.log(time)
      let startTime = time['time'].split(':')
      status = Number(time['status'])
      hour = Number(startTime[0])
      mins = Number(startTime[1])
      secs = Number(startTime[2])
    }
  }
  req.onerror = function () {
    // There was a connection error of some sort
    console.log('error occurred')
  }
  req.send()
}

function sendData () {
   let time = hour + ':' + mins + ':' + secs
   let timer = {'time': time, 'status': status}
   console.log(timer)
   var data = JSON.stringify(timer)

  var httpRequest = new XMLHttpRequest()
  console.log('inside sendData')
  httpRequest.open('POST', '/gettimer', true)
  console.log('connection opened')
  httpRequest.setRequestHeader('Content-Type', 'application/json')
  console.log('header set')

  httpRequest.onreadystatechange = function () {
    console.log('inside onreadystatechange')
    if (this.readyState === 4 && this.status === 200) {
      console.log('connection done')
    }
  }
  console.log(data)
  httpRequest.send(data)

  httpRequest.onerror = function (err) {
    // There was a connection error of some sort
    console.log('error occurred in connection:' + err)
  }
}

console.log('timer loaded and initializes successfully')
var timer = null

function startCount () {
  timer = setInterval(count, 1000)
  console.log('inside startcounter')
}

function stopCounter () {
  clearInterval(timer)
  console.log('counter stopped')
}

function count () {
  console.log('in count')
  secs = secs + 1
  if (secs === 60) {
    secs = 0
    mins = mins + 1
  }
  if (mins === 60) {
    mins = 0
    hour = hour + 1
  }
  let str = plz(hour) + ': ' + plz(mins) + ': ' + plz(secs)
  console.log(str)
  document.getElementById('counter').innerHTML = str
}

function plz (digit) {
  var zpad = digit + ''
  if (digit < 10) {
    zpad = '0' + zpad
  }
  return zpad
}
