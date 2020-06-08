---
layout: page
title: Calculators
permalink: /calcs/
---


<html>
<head>
<script type = "text/javascript">

function s_min(){
    var tsys = parseFloat(document.getElementById("tsys").value)
    var gain = parseFloat(document.getElementById("gain").value)
    var bw = parseFloat(document.getElementById("bw").value)
    var snr = parseFloat(document.getElementById("snr").value)
    var w = parseFloat(document.getElementById("width").value)

    var fluence = (tsys*snr)/(gain*(Math.pow(2*w*bw*Math.pow(10,3), 1/2)));
    document.getElementById('minimum_fluence').value = fluence;
    }
    

function calc_delay(){
    var dm = parseFloat(document.getElementById("dm").value)
    var freq = parseFloat(document.getElementById("freq").value)
    var bandwidth = parseFloat(document.getElementById("bandwidth").value)
    
    if (bandwidth == 0) {
      var delay = 4148.808*dm*(1/Math.pow(freq,2));
	} else {  
      var min_freq = freq - bandwidth/2;
      var max_freq = freq + bandwidth/2;
      var delay = 4148.808*dm*(1/Math.pow(min_freq,2) - 1/Math.pow(max_freq,2));
	}
    document.getElementById('dm_delay').value = delay;
    }


</script>

</head>
<body>
<h2>
Search Sensitivity Calculator</h2>
Tsys (K): &emsp;&emsp;&emsp;&emsp;<input type = "text" id = "tsys" maxlength = "7" value = "10">
<br>
Gain (K/Jy): &emsp;&emsp;&ensp;&nbsp;<input type = "text" id = "gain" maxlength = "7" value = "2">
<br>
Bandwidth (MHz): &nbsp;<input type = "text" id = "bw" maxlength = "7" value = "200">
<br>
SNR: &emsp;&emsp;&emsp;&emsp;&emsp;&ensp;<input type = "text" id = "snr" maxlength = "7" value = "10">
<br>
Width (ms): &emsp;&emsp;&emsp;<input type = "text" id = "width" maxlength = "7" value = "10">
<br><br>

<input type = "Button" value = "Calculate Minimum Fluence" onclick="s_min();" style="font-size : 15px;">
<br>
<br>
Minimum Detectable Fluence (Jy ms): <input type = "text" id = "minimum_fluence"><br><br>

<hr>
<h2>
Dispersion Delay Calculator</h2>
DM (pc/cc): &emsp;&emsp;&emsp;<input type = "text" id = "dm" maxlength = "7" value = "1000">
<br>
Center Freq (MHz): &emsp;<input type = "text" id = "freq" maxlength = "7" value = "1400">
<br>
Bandwidth (MHz): &emsp;<input type = "text" id = "bandwidth" maxlength = "7" value = "0">
<br>
<br>
<input type = "Button" value = "Calculate Dispersion Delay" onclick="calc_delay();" style="font-size : 15px;">
<br>
<br>
Dispersion Delay (s): <input type = "text" id = "dm_delay"><br><br>



</body>
</html>
