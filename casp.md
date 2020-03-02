---
layout: page
title: FRB Association Probability Calculator
permalink: /casp/
---

<html>
<head>
<script type = "text/javascript">
var R_0 = 0.2
var R_h = 0.25
var num_dens_gal_eb17 = [0.00000000e+00, 3.47341375e-09, 8.37867722e-09, 1.53325193e-08,
       2.52268089e-08, 3.93548623e-08, 5.95971043e-08, 8.86944980e-08,
       1.30651979e-07, 1.91334722e-07, 2.79350820e-07, 4.07359904e-07,
       5.94015870e-07, 8.66854596e-07, 1.26659115e-06, 1.85352082e-06,
       2.71706245e-06, 3.98999727e-06, 5.86972686e-06, 8.65002631e-06,
       1.27684917e-05, 1.88774558e-05, 2.79499920e-05, 4.14383625e-05,
       6.15108217e-05, 9.14054163e-05, 1.35958361e-04, 2.02392682e-04,
       3.01494495e-04, 4.49365966e-04, 6.70035090e-04, 9.99336664e-04,
       1.49067629e-03, 2.22357881e-03, 3.31634629e-03, 4.94476893e-03,
       7.36973135e-03, 1.09778607e-02, 1.63412473e-02, 2.43049806e-02,
       3.61151361e-02, 5.36054075e-02, 7.94684847e-02, 1.17649482e-01,
       1.73914504e-01, 2.56669563e-01, 3.78135970e-01, 5.56031117e-01,
       8.15962675e-01, 1.19482519e+00, 1.74559829e+00, 2.54409468e+00,
       3.69840636e+00, 5.36206357e+00, 7.75227298e+00, 1.11750621e+01,
       1.60597537e+01, 2.30059606e+01, 3.28472630e+01, 4.67369501e+01,
       6.62627185e+01, 9.35990556e+01, 1.31708251e+02, 1.84603571e+02,
       2.57691136e+02, 3.58210389e+02, 4.95796718e+02, 6.83193595e+02,
       9.37145342e+02, 1.27950502e+03, 1.73859449e+03, 2.35085482e+03,
       3.16282442e+03, 4.23347813e+03, 5.63695309e+03, 7.46567415e+03,
       9.83387320e+03, 1.28814710e+04, 1.67782572e+04, 2.17282639e+04,
       2.79741785e+04, 3.58015896e+04, 4.55427987e+04, 5.75798749e+04,
       7.23465717e+04, 9.03286841e+04, 1.12062393e+05, 1.38130146e+05,
       1.69153642e+05, 2.05783569e+05, 2.48685850e+05, 2.98524299e+05,
       3.55939814e+05, 4.21526460e+05, 4.95805081e+05, 5.79195331e+05,
       6.71987342e+05, 7.74314421e+05, 8.86128393e+05, 1.00717926e+06]

var ms_eb17 = [ 0.        ,  0.3030303 ,  0.60606061,  0.90909091,  1.21212121,
        1.51515152,  1.81818182,  2.12121212,  2.42424242,  2.72727273,
        3.03030303,  3.33333333,  3.63636364,  3.93939394,  4.24242424,
        4.54545455,  4.84848485,  5.15151515,  5.45454545,  5.75757576,
        6.06060606,  6.36363636,  6.66666667,  6.96969697,  7.27272727,
        7.57575758,  7.87878788,  8.18181818,  8.48484848,  8.78787879,
        9.09090909,  9.39393939,  9.6969697 , 10.        , 10.3030303 ,
       10.60606061, 10.90909091, 11.21212121, 11.51515152, 11.81818182,
       12.12121212, 12.42424242, 12.72727273, 13.03030303, 13.33333333,
       13.63636364, 13.93939394, 14.24242424, 14.54545455, 14.84848485,
       15.15151515, 15.45454545, 15.75757576, 16.06060606, 16.36363636,
       16.66666667, 16.96969697, 17.27272727, 17.57575758, 17.87878788,
       18.18181818, 18.48484848, 18.78787879, 19.09090909, 19.39393939,
       19.6969697 , 20.        , 20.3030303 , 20.60606061, 20.90909091,
       21.21212121, 21.51515152, 21.81818182, 22.12121212, 22.42424242,
       22.72727273, 23.03030303, 23.33333333, 23.63636364, 23.93939394,
       24.24242424, 24.54545455, 24.84848485, 25.15151515, 25.45454545,
       25.75757576, 26.06060606, 26.36363636, 26.66666667, 26.96969697,
       27.27272727, 27.57575758, 27.87878788, 28.18181818, 28.48484848,
       28.78787879, 29.09090909, 29.39393939, 29.6969697 , 30.        ]

z_mins = [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
z_maxs = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
ix = [0, 1, 2, 3, 4, 5, 6]
num_gal_z = [7391864.650475038, 55891941.91887342, 442633949.7433847, 895232758.005576, 1503624391.9486768, 2175720871.4302573, 1729558966.4161413]

function get_R(R_frb){
    return Math.max(2*R_frb, Math.sqrt(Math.pow(R_0, 2) + 4*Math.pow(R_h,2)));
}


function p_bloom(){
    var m_i = parseFloat(document.getElementById("m_i").value)
    var R_frb = parseFloat(document.getElementById("R_frb").value)
    var r_i = get_R(R_frb);
    var factor  = Math.pow(3600,2)*0.334*Math.LN10;
    // galaxy per arcsecond square
    var mean_surfden_gal = (1/factor)*Math.pow(10,(0.334*(m_i - 22.963) + 4.320));
    var num_gal = Math.PI*(Math.pow(r_i, 2))*mean_surfden_gal;
    document.getElementById('bloom_prob_result').value = 1 - Math.exp(-1*num_gal);
}


function p_eb17(){
    var m_i = parseFloat(document.getElementById("m_i").value)
    var R_frb = parseFloat(document.getElementById("R_frb").value)
    var r_i = get_R(R_frb);

    // value in ms_eb17 closest to m_i
    var closest = ms_eb17.reduce(function(prev, curr) {
    return (Math.abs(curr - m_i) < Math.abs(prev - m_i) ? curr : prev);
    });

    // find the index of closest value and pick that from num_dens_gal_eb17
    var mask = ms_eb17.map(item => item == closest);
    var num_density_gal = num_dens_gal_eb17.filter((item, i) => mask[i])[0];

    deg2arcsec = 60*60
    num_gals = Math.PI*Math.pow(r_i/deg2arcsec,2)*num_density_gal

    document.getElementById('eb17_prob_result').value = 1 - Math.exp(-1*num_gals);
}

function p_eb17_z(){
    var R_frb = parseFloat(document.getElementById("R_frb_z").value)
    var z = parseFloat(document.getElementById("redshift").value)

    var r_i = get_R(R_frb);
    
    if ((z > 0) && (z < 1.2 || z == 1.2)){

        var z_min = z_mins.reduce(function(prev, curr) {
            return (curr > z ? prev : curr);
            });        
        
        var mask = z_mins.map(item => (item == z_min));
        var idx = ix.filter((item, i) => mask[i]);
        var z_max = z_maxs.filter((item, i) => mask[i]);  

        var n = 0;
        var i;
        for (i = 0; i <= idx; i++){
            n += num_gal_z[i];
        }
    
        var f_a = Math.PI*Math.pow(r_i,2)/(5.346*Math.pow(10,11));
        var num_gals = f_a*n;
        document.getElementById('eb17_prob_z_result').value = 1 - Math.exp(-1*num_gals);
        
    } else {
        document.getElementById('eb17_prob_z_result').value = -1;
    }
}
</script>
</head>
<body>
<h1>
Chance Coincidence Probability
</h1>
Localisation Radius (arcsec): &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type = "text" id = "R_frb" maxlength = "7" value = "0.0">
<br>
r band magnitude:&nbsp; <input type = "text" id = "m_i" maxlength = "7" value = "0.0"><br><br>
<input type = "Button" value = "Calculate Association Prob." onclick="p_bloom();p_eb17();" style="font-size : 20px;">
<br>
<br>
Chance Coincidence Probability (<a href="https://ui.adsabs.harvard.edu/abs/2002AJ....123.1111B/abstract">Bloom 2003</a>): <input type = "text" id = "bloom_prob_result"><br>
Chance Coincidence Probability (<a href="https://ui.adsabs.harvard.edu/abs/2017ApJ...849..162E/abstract">EB17</a>): <input type = "text" id = "eb17_prob_result"><br><br>

<hr>

<h1>
Chance Coincidence Probability <br>
(with redshift)
</h1>
Localisation Radius (arcsec): &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type = "text" id = "R_frb_z" maxlength = "7" value = "0.0">
<br>
<!-- r band magnitude:&nbsp; <input type = "text" id = "m_i" maxlength = "7" value = "0.0"><br><br> -->
Max Redshift:&nbsp; <input type = "text" id = "redshift" maxlength = "7" value = "0.0"><br><br>
<input type = "Button" value = "Calculate Association Prob." onclick="p_eb17_z();" style="font-size : 20px;">
<br>
<br>
Chance Coincidence Probability (<a href="https://ui.adsabs.harvard.edu/abs/2017ApJ...849..162E/abstract">EB17</a>): <input type = "text" id = "eb17_prob_z_result"><br>
(using galaxies with &ge;0.01L* <br>
out to the max redshift)<br><br>

<hr>

If you want to dig deeper, the python code for the above is available <a href="https://github.com/KshitijAggarwal/casp">here</a>.

<p><font size="4">Please cite the following papers if you make use of the above tool:
<ul>
<li>Agarwal et al 2020</li>
<li><a href="https://ui.adsabs.harvard.edu/abs/2017ApJ...849..162E/abstract">EB17</a></li>
<li><a href="https://ui.adsabs.harvard.edu/abs/2002AJ....123.1111B/abstract">Bloom 2003</a></li>
</ul>
</font>
</p>

</body>
</html>
