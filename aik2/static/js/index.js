var tmdata = null;
var tmstat = [];
var achart = null;
var astat = null;

var limstop = 0.95;
function getdata(url, root, token) {
   astat =  $.ajax(
        {
            url: url,
            data: {
                id: 0, 'csrfmiddlewaretoken': token
            },
            timeout: 100000,
            type: 'POST',
            beforeSend: function () {
            },
            success: function (data) {
                drawinfo(data, root);
                tmdata = window.setTimeout(function () {
                   getdata(url, root, token);
                }, 10000);
            },
            error: function() {
                tmdata = window.setTimeout(function () {
                    getdata(url, root, token);
                }, 10000);
            }
        });
}

function getstat(url, token) {
    $.ajax(
        {
            url: url,
            data: {
                id: 0, 'csrfmiddlewaretoken': token
            },
            timeout: 300000,
            type: 'POST',
            beforeSend: function () {
            },
            success: function (data) {
                drawstat(data);
                tmstat = window.setTimeout(function () {
                   getstat(url, token);
                }, 108000);
            },
            error: function() {
                tmstat = window.setTimeout(function () {
                    getstat(url, token);
                }, 108000);
            }
        });
}

function drawstat(data)
{
  var sm = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
  for(var i=0; i < 3; i++) {
      var ind = 0;
      for(var y=-1; y < 5; y++)
      {
          var v = data[i][y.toString()];
          if( v != null) {
              $("#s" + (i + 1) + "_" + y).text((v/60).toFixed(2) + "ч.");
              sm[ind] += v;
          }
          else
          {
              $("#s" + (i + 1) + "_" + y).text("-");
          }
          ind +=1;
      }
  }
  var ind = -1;
  for (var i=0; i < sm.length; i++)
  {
      if(sm[i] !== 0.0) {
          $("#s4" + "_" + ind).text((sm[i]/60).toFixed(2) + "ч.");
      }
      else
      {
          $("#s4" + "_" + ind).text("-");
      }
      ind +=1;
  }

}


function drawdata(data, root)
{
    if(data == null)
         return;
    $("[id^='line']", root).each(
        function(){
            $(this).css('stroke', '#595b5d');
        });

    $("[id^='circle-']", root).each(
        function(){
            $(this).css('stroke', '#595b5d');
            $(this).css('fill-opacity', 0.0);
        });

    $("[id^='br']", root).each(
        function(){
            $(this).css('display', 'none');
        });
    $("[id^='bcircle-']", root).each(
        function(){
            $(this).css('display', 'none');
        });

    $("[id^='cce']", root).each(
        function(){
            $(this).css('fill', '#747474');
        });

    if (data['snnclass'] !== 1) {
        $("#line-0", root).css('stroke', '#eaeaea');
        $("#line-1", root).css('stroke', '#eaeaea');
        $("#circle-0", root).css('stroke', '#eaeaea');
        $("#bcircle-0", root).css('display', 'inline');
        if (data['stop'] <= limstop) {
            $("[id^='cce']", root).each(
                function () {
                    $(this).css('fill', '#32f90a');
                });
        }
        else
        {
            return;
        }
    }
    const br = $("[id^='br']", root);
    if (data['full'] > data['empty'] && data['snnclass'] !== 1) {
        br.each(
        function(){
            $(this).css('display', 'inline');
        });
    }
    else
    {
        br.each(
        function(){
            $(this).css('display', 'none');
        });
    }
    switch (data['snnclass']) {
        case 0:
            br.each(
                function () {
                    $(this).css('display', 'none');
                });
            break;
        case 1:
            $("#line-6", root).css('stroke', '#f20855');
            $("#circle-4", root).css('stroke', '#f20855');
            $("#bcircle-4", root).css('display', 'inline');
            break;
        case 2:
            $("#line-3", root).css('stroke', '#ff0f3c');
            $("#circle-1", root).css('stroke', '#ff0f3c');
            $("#bcircle-1", root).css('display', 'inline');
            break;
        case 3:
            $("#line-4", root).css('stroke', '#ef7419');
            $("#circle-2", root).css('stroke', '#ef7419');
            $("#bcircle-2", root).css('display', 'inline');
            break;
        case 4:
            $("#line-5", root).css('stroke', '#32ff15');
            $("#circle-3", root).css('stroke', '#32ff15');
            $("#bcircle-3", root).css('display', 'inline');
            break;
        default:
            break;
    }
}

function strokew(min, max, coeff) {
    return (max-min)*coeff+min;

}

function getdatachart(id, url, chart, options, subscribe, token)
{
     achart = $.ajax(
        {
            url: url,
            data: {
                id: id, 'csrfmiddlewaretoken': token
            },
            timeout: 300000,
            type: 'POST',
            beforeSend: function () {
            },
            success: function (data) {
                if (id < 3)
                {
                    $("#c_" + id).text("Смена " + data[1]);
                    $("#s_" + id).text("Смена " + data[1]);
                    data = data[0];
                }
                drawchart(id, chart, options, data);
                drawstattable(id, chart, data);
                if(subscribe) {
                    tmstat[id] = window.setTimeout(function () {
                        getdatachart(id, url, chart, options, subscribe, token);
                    }, 120000);
                }
            },
            error: function() {
                tmstat[id] = window.setTimeout(function () {
                    getdatachart(id, url, chart, options, subscribe, token);
                }, 120000);
            }
        });
}

function drawchart(id, chart, options, data) {
    options['yaxes'][0]['min'] = 0.0;
    options['yaxes'][0]['max'] = 105.0;
    if(id < 3)
    {
        options['yaxes'][0]['min'] = 0.0;
        options['yaxes'][0]['max'] = 105.0;
    }
    $.plot("#" + chart, [ data[0], data[1], data[2],
        data[3], data[4], data[5]], options);
}

function drawinfo(data, root)
{
    $("#cam").css('background-image', 'url(data:image/jpeg;base64,' + data['img'] + ')');
    $("#cam-label").text("Дата " + data['tstamp']);
    if (data['stop'] > limstop && data['snnclass'] !== 1) {
        $("#img").css('box-shadow', '0 0 40px #759ebf');
    }
    else
    {
        if (data['full'] < data['empty'] && data['snnclass'] !== 1)
        {
            $("#img").css('box-shadow', '0 0 25px 2px #666d6e');
        }
        else {
            //    if (data['idnext'] != null) {
            switch (data['snnclass']) {
                case 0:
                    $("#img").css('box-shadow', '0 0 25px 2px #666d6e');
                    break;
                case 1:
                    $("#img").css('box-shadow', '0 0 25px 2px #f20855');
                    break;
                case 2:
                    $("#img").css('box-shadow', '0 0 25px 2px #ff0f3c');
                    break;
                case 3:
                    $("#img").css('box-shadow', '0 0 25px 2px #ef7419');
                    break;
                case 4:
                    $("#img").css('box-shadow', '0 0 25px 2px #32ff15');
                    break;
            }
        }
    }
    drawdata(data, root)
}

function drawstattable(id, chart, data) {
    var ch = chart.split('_');
    for (var i = 0; i < data.length; i++) {
        var a = data[i][0];
        if(a[1] !== null && a[1] !== 0.0)
          $("#" + ch[0] + "_" + id + "_" + i).text((a[1]).toFixed(2));
        else
          $("#" + ch[0] + "_" + id + "_" + i).text("-");
    }
}

function getDays() {
    var today = new Date();
    var result = new Date(today);
    result.setDate(result.getDate() - 1);
    var days = result.getDate();
    var month = result.getMonth() + 1;
    month = (month<10?'0':'') + month;
    var years = result.getFullYear();
  return days + '.' + month + '.' + years;
}

function getDaysCurrent() {
    var today = new Date();
    var result = new Date(today);
    result.setDate(result.getDate());
    var days = result.getDate();
    var month = result.getMonth() + 1;
    month = (month<10?'0':'') + month;
    var years = result.getFullYear();
  return days + '.' + month + '.' + years;
}

function getDaysStart() {
    var today = new Date();
    var result = new Date(today);
    result.setDate(result.getDate());
    var days = 1;
    var month = result.getMonth() + 1;
    month = (month<10?'0':'') + month;
    var years = result.getFullYear();
  return days + '.' + month + '.' + years;
}

function gestatdata(url, st, en, token, options) {
    $.ajax(
        {
            url: url,
            data: {
                st: st, en: en, 'csrfmiddlewaretoken': token
            },
            timeout: 100000,
            type: 'POST',
            beforeSend: function () {
                $("#wait").show();
            },
            success: function (data) {
                $("#wait").hide();
               setstat(data, options);
            },
            error: function() {
                 $("#wait").hide();
            }
        });
}

function getstatsesgrdata(url, ds, de, type, token, options) {
    $.ajax(
        {
            url: url,
            data: {
                ds: ds, de: de, type: type, 'csrfmiddlewaretoken': token
            },
            timeout: 600000,
            type: 'POST',
            beforeSend: function () {
                $("#wait").show();
            },
            success: function (data) {
                $("#wait").hide();
                grses(data, options);
            },
            error: function () {
                $("#wait").hide();
            }
        });
}


function setstat(data, options)
{
  for (var i = 0; i < data.length && i < 4; i++) {
      var chart = 'ch_';
      if (i < 3) {
          chart += i;
      }
      else {
          chart += 'all';
      }
      var tdata = data[i];
      drawstattable(i, chart, tdata);
      options['yaxes'][0]['min'] = 0.0;
      options['yaxes'][0]['max'] = 105.0;
      //if (i < 3) {
      //    options['yaxes'][0]['min'] = 0.0;
      //    options['yaxes'][0]['max'] = data[4][0][0];
      //}
      $.plot("#" + chart, [tdata[0], tdata[1], tdata[2],
          tdata[3], tdata[4], tdata[5]], options);
  }
}

function grses(data, options)
{
  for (var i = 0; i < data.length && i < 5; i++) {
      var chart = 'ch_' + i;
      var tdata = data[i];
      drawstattable(i, chart, tdata);
      options['yaxes'][0]['min'] = 0.0;
      options['yaxes'][0]['max'] = 105.0;
      $.plot("#" + chart, [tdata[0], tdata[1], tdata[2],
          tdata[3], tdata[4], tdata[5]], options);
  }
}


function getprotocol(url, token, dt , direct) {
   astat =  $.ajax(
        {
            url: url,
            data: {
                dt: dt, dr: direct, 'csrfmiddlewaretoken': token
            },
            timeout: 100000,
            type: 'POST',
            beforeSend: function () {
                 $("#wait").show();
            },
            success: function (data) {
               $("#wait").hide();
               protocolview(data);
            },
            error: function() {
                $("#wait").hide();
            }
        });
}

function gettrends(url, token, id) {
   astat =  $.ajax(
        {
            url: url,
            data: {
                id: id, 'csrfmiddlewaretoken': token
            },
            timeout: 100000,
            type: 'POST',
            beforeSend: function () {
                 $("#wait_" +  (id === 0? 'month' : 'year')).show();
            },
            success: function (data) {
               $("#wait_" +  (id === 0? 'month' : 'year')).hide();
               drawtrend(id, data);
            },
            error: function() {
                $("#wait_" +  (id === 0? 'month' : 'year')).hide();
            }
        });
}

function protocolview(data) {
    $('div[id^="rw"]').remove();
    for (var i = 0; i < data.length; i++) {
        var r = "<div id='rw" + i + "' class='prot-row-form'>" +
            "<div id='t" + i + "' class='float-left prot-row-font-form'>" + data[i]['tstamp'] + "</div>" +
            "<div class='float-left prot-row-font-form'>" + data[i]['tfile'] + "</div>" +
            "<div class='float-left prot-row-font-form'><a href='data:image/jpeg;base64," + data[i]['img'] + "'" +
            "class='preview' title='Класс: " + snnclass(data[i]['snnclass']) + "'><img class='prot-row-img-form' " +
            "src='data:image/jpeg;base64," + data[i]['img'] + "'></a></div>" +
            "<div class='float-left prot-row-font-form'>" + data[i]['stop'].toFixed(2) + "</div>" +
            "<div class='float-left prot-row-font-form'>" + data[i]['empty'].toFixed(2) + "</div>" +
            "<div class='float-left prot-row-font-form'>" + data[i]['full'].toFixed(2) + "</div>" +
            "<div class='float-left prot-row-font-form'>" + data[i]['imerror'].toFixed(2) + "</div>" +
            "<div class='float-left prot-row-font-form'>" + snnclass(data[i]['snnclass']) + "</div>" +
            "<div class='float-left prot-row-font-form'>" + data[i]['snn1'] + "</div>" +
            "<div class='float-left prot-row-font-form'>" + data[i]['snn2'] + "</div>" +
            "<div class='float-left prot-row-font-form'>" + data[i]['snn3'] + "</div></div>";
        //$("#nstat").append(r);
        $(r).insertAfter("#hd");
    }
    $('.preview').anarchytip();
}

function snnclass(id) {
    var t_class = {'-1': 'простой', '0': 'без материала', '2': 'пыль', '1': 'не распознано',
        '3': 'брикеты, мелочь', '4': 'брикеты'};
    return t_class[id.toString()];
}


function drawtrend(id, data) {
     var options = {
            colors: ["#759ebf", "#666d6e", "#f20855", "#ff0f3c", "#ef7419", "#32ff15"]
            ,
            xaxis:
            {
                mode: "time",
                timezone: "browser",
                useLocalTime: true,
                timeformat: "%d.%m.%y",
                font: {
                    color: "#efeeef"
                }

            },
            yaxes: [
                {
                    position: "left",
                    min: 0,
                    max: 105.0,
                    color: "#759ebf",
                    font: {
                        color: "#efeeef"
                    }
                },
                {
                    position: "left",
                    min: 0,
                    max: 105.0,
                    color: "#666d6e"
                },
                {
                    position: "left",
                    min: 0,
                    max: 105.0,
                    color: "#f20855"
                },
                {
                    position: "left",
                    min: 0,
                    max: 105.0,
                    color: "#ff0f3c"
                },
                {
                    position: "left",
                    min: 0,
                    max: 105.0,
                    color: "#ef7419"
                },
                {
                    position: "left",
                    min: 0,
                    max: 105.0,
                    color: "#32ff15"
                }
                ],
            legend: {
                position: "ne",
                backgroundOpacity: 0.0,
                labelBoxBorderColor: null,
                margin: 0,
                noColumns: 0,
                show: true,
                sorted: null},
            grid: {
                color: "#eaeaea",
                hoverable: true
            }
        };
        var ncart = id === 0? 'month' : 'year';
        $.plot("#ch_" + ncart, data, options);
        //$(".legend>table").css({ top: 0 });
}