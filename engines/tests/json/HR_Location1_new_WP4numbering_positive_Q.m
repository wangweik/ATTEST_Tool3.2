function mpc = Location1
%LOCATION1
%   PSS(R)E-33.9    WED, MAR 03 2021  10:07
%   CREATED BY NETVISION RAW CONVERTER FROM FILES: NDC_2020-07-0
%   , BEGIN BUS DATA
%
%   Converted by MATPOWER 7.1 using PSSE2MPC on 04-May-2022
%   from 'Loaction1.raw' using PSS/E rev 33 format.
%
%   WARNINGS:
%       Conversion explicitly using PSS/E revision 33
%       Skipped 1 line of zone data.
%
%   See CASEFORMAT for details on the MATPOWER case file format.

%% MATPOWER Case Format : Version 2
mpc.version = '2';

%%-----  Power Flow Data  -----%%
%% system MVA base
mpc.baseMVA = 100;

%% bus data
%	bus_i	type	Pd	Qd	Gs	Bs	area	Vm	Va	baseKV	zone	Vmax	Vmin
mpc.bus = [
1	1	3.69900000000000	3.15300000000000	0	0	8	1.03921000000000	-0.662800000000000	110	1	1.10000000000000	0.900000000000000;
2	1	25.3970000000000	0.00000000000000	0	0	8	1.00452000000000	-4.91390000000000	35	1	1.10000000000000	0.900000000000000;
3	1	38.6220000000000	2.37900000000000	0	0	8	1.04178000000000	1.14050000000000	110	1	1.10000000000000	0.900000000000000;
4	1	46.6240000000000	7.77500000000000	0	0	8	1.05521000000000	-1.55370000000000	110	1	1.10000000000000	0.900000000000000;
5	1	9.81600000000000	1.85300000000000	0	0	8	1.03849000000000	-1.69700000000000	110	1	1.10000000000000	0.900000000000000;
6	2	0	0	0	0	8	1.05134000000000	2.49250000000000	110	1	1.10000000000000	0.900000000000000;
7	2	0	103	0	0	8	1.05400000000000	0.729700000000000	220	1	1.10000000000000	0.900000000000000;
8	1	-18.8960000000000	28.7540000000000	0	0	8	1.04698000000000	1.94050000000000	110	1	1.10000000000000	0.900000000000000;
9	2	32.6950000000000	4.31900000000000	0	0	8	1.05259000000000	-0.853400000000000	110	1	1.10000000000000	0.900000000000000;
10	2	0	0	0	0	8	1.03500000000000	-0.143900000000000	400	1	1.10000000000000	0.900000000000000;
11	1	188.523000000000	0.00000000000000	0	0	8	1.07296000000000	-1.90370000000000	110	1	1.10000000000000	0.900000000000000;
12	3	0	0	0	0	8	1.03700000000000	0	400	1	1.10000000000000	0.900000000000000;
13	2	0	0	0	0	8	1.07400000000000	0.882400000000000	220	1	1.10000000000000	0.900000000000000;
14	1	4.31800000000000	0.00000000000000	0	0	8	1.05695000000000	-1.19040000000000	110	1	1.10000000000000	0.900000000000000;
15	1	33.2310000000000	3.90700000000000	0	0	8	1.04287000000000	1.25950000000000	110	1	1.10000000000000	0.900000000000000;
16	1	8.22500000000000	0.00000000000000	0	0	8	1.04313000000000	1.20780000000000	110	1	1.10000000000000	0.900000000000000;
17	1	-0.0160000000000000	0.00000000000000	0	0	8	1.05609000000000	-1.40340000000000	110	1	1.10000000000000	0.900000000000000;
18	1	0	0	0	0	8	1.03595000000000	-1.22610000000000	110	1	1.10000000000000	0.900000000000000;
19	1	4.32500000000000	0.00000000000000	0	0	8	1.00666000000000	-2.73250000000000	35	1	1.10000000000000	0.900000000000000;
20	1	9.66000000000000	0.00000000000000	0	0	8	1.00043000000000	-4.68110000000000	35	1	1.10000000000000	0.900000000000000;
21	1	30.0480000000000	3.83100000000000	0	0	8	1.05184000000000	-1.69480000000000	110	1	1.10000000000000	0.900000000000000;
22	1	0	0	0	0	8	1.04120000000000	0.331400000000000	110	1	1.10000000000000	0.900000000000000;
23	1	14.7750000000000	0.00000000000000	0	0	8	1.00482000000000	-4.56260000000000	35	1	1.10000000000000	0.900000000000000;
24	2	0	0	0	0	8	1.04461000000000	1.28680000000000	110	1	1.10000000000000	0.900000000000000;
25	1	15.9050000000000	1.77300000000000	0	0	8	1.04342000000000	0.854600000000000	110	1	1.10000000000000	0.900000000000000;
26	2	-0.806000000000000	2.10300000000000	0	0	8	1.04442000000000	0.741300000000000	110	1	1.10000000000000	0.900000000000000;
27	1	21.2790000000000	1.85200000000000	0	0	8	1.04681000000000	-1.99200000000000	110	1	1.10000000000000	0.900000000000000;
28	1	7.10600000000000	1.05800000000000	0	0	8	1.04411000000000	-1.37080000000000	110	1	1.10000000000000	0.900000000000000;
29	1	5.70700000000000	2.48600000000000	0	0	8	1.03785000000000	-1.74030000000000	110	1	1.10000000000000	0.900000000000000;
30	1	11.6490000000000	8.01700000000000	0	0	8	1.06362000000000	-1.12530000000000	110	1	1.10000000000000	0.900000000000000;
31	1	62.9090000000000	12.6730000000000	0	0	8	1.05488000000000	-1.61110000000000	110	1	1.10000000000000	0.900000000000000;
];

%% generator data
%	bus	Pg	Qg	Qmax	Qmin	Vg	mBase	status	Pmax	Pmin	Pc1	Pc2	Qc1min	Qc1max	Qc2min	Qc2max	ramp_agc	ramp_10	ramp_30	ramp_q	apf
mpc.gen = [
6	44.1580000000000	5.80200000000000	25	-4	1.05134000000000	55	1	47.5000000000000	18	0	0	0	0	0	0	0	0	0	0	0;
6	45.3400000000000	5.95700000000000	25	-4	1.05134000000000	55	1	47.5000000000000	18	0	0	0	0	0	0	0	0	0	0	0;
7	65	9.23600000000000	9999	-9999	1.05400000000000	100	1	9999	-9999	0	0	0	0	0	0	0	0	0	0	0;
9	0	0	8	-2.80000000000000	1.05368000000000	35.9500000000000	0	30.5500000000000	5	0	0	0	0	0	0	0	0	0	0	0;
9	0	0	8	-2.80000000000000	1.05368000000000	35.9500000000000	0	30.5500000000000	5	0	0	0	0	0	0	0	0	0	0	0;
9	0	0	13	-12	1.05368000000000	16	0	12.8000000000000	3	0	0	0	0	0	0	0	0	0	0	0;
9	0	13	13	-12	1.05368000000000	16	1	12.8000000000000	3	0	0	0	0	0	0	0	0	0	0	0;
10	132	9.39700000000000	9999	-9999	1.03500000000000	100	1	9999	-9999	0	0	0	0	0	0	0	0	0	0	0;
12	51.1000000000000	75.4390000000000	9999	-9999	1.03700000000000	100	1	9999	-9999	0	0	0	0	0	0	0	0	0	0	0;
13	109	25.6310000000000	9999	-9999	1.07400000000000	100	1	9999	-9999	0	0	0	0	0	0	0	0	0	0	0;
24	37.0440000000000	0.0490000000000000	21	-12.6000000000000	1.04461000000000	42	1	40	15	0	0	0	0	0	0	0	0	0	0	0;
24	37.2020000000000	0.0490000000000000	21	-12.6000000000000	1.04461000000000	42	1	40	15	0	0	0	0	0	0	0	0	0	0	0;
26	0	0	20	-8.40000000000000	1.04442000000000	42	0	40	0.0100000000000000	0	0	0	0	0	0	0	0	0	0	0;
26	38.2870000000000	3.14200000000000	20	-8.40000000000000	1.04442000000000	42	1	40	0.0100000000000000	0	0	0	0	0	0	0	0	0	0	0;
];

%% branch data
%	fbus	tbus	r	x	b	rateA	rateB	rateC	ratio	angle	status	angmin	angmax
mpc.branch = [
1	5	0.0318347000000000	0.108769000000000	0.0105300000000000	123	0	0	0	0	1	-360	360;
1	18	0.0221157000000000	0.0755620000000000	0.00731000000000000	123	0	0	0	0	1	-360	360;
1	22	0.0193388000000000	0.0676859000000000	0.00649000000000000	123	0	0	0	0	1	-360	360;
1	26	0.0169587000000000	0.0593554000000000	0.00563000000000000	123	0	0	0	0	1	-360	360;
1	28	0.0318645000000000	0.109785000000000	0.0106200000000000	123	0	0	0	0	1	-360	360;
3	8	0.0215124000000000	0.0475537000000000	0.00449000000000000	90	0	0	0	0	1	-360	360;
3	24	0.0121984000000000	0.0426942000000000	0.00405000000000000	123	0	0	0	0	1	-360	360;
4	14	0.00300826000000000	0.0218099000000000	0.00396000000000000	300	0	0	0	0	1	-360	360;
4	14	0.00300826000000000	0.0218099000000000	0.00396000000000000	300	0	0	0	0	1	-360	360;
4	31	0.00338843000000000	0.0114876000000000	0.00111000000000000	123	0	0	0	0	1	-360	360;
4	31	0.00338843000000000	0.0118182000000000	0.00112000000000000	123	0	0	0	0	1	-360	360;
5	27	0.0573140000000000	0.126694000000000	0.0120100000000000	90	0	0	0	0	1	-360	360;
5	29	0.00476033000000000	0.0162645000000000	0.00157000000000000	123	0	0	0	0	1	-360	360;
6	8	0.00704132000000000	0.0246446000000000	0.00234000000000000	123	0	0	0	0	1	-360	360;
6	8	0.00704132000000000	0.0246446000000000	0.00234000000000000	123	0	0	0	0	1	-360	360;
7	13	0.00436364000000000	0.0223636000000000	0.0355200000000000	311	0	0	0	0	1	-360	360;
8	9	0.0360000000000000	0.121800000000000	0.0119000000000000	123	0	0	0	0	1	-360	360;
8	15	0.0103140000000000	0.0348959000000000	0.00341000000000000	123	0	0	0	0	1	-360	360;
9	14	0.0221157000000000	0.0774050000000000	0.00731000000000000	123	0	0	0	0	1	-360	360;
10	12	0.00114375000000000	0.0118950000000000	0.337700000000000	1330	0	0	0	0	1	-360	360;
11	30	0.0206281000000000	0.0704793000000000	0.00682000000000000	123	0	0	0	0	1	-360	360;
11	30	0.0206281000000000	0.0704793000000000	0.00682000000000000	123	0	0	0	0	1	-360	360;
14	17	0.00644628000000000	0.0220248000000000	0.00216000000000000	123	0	0	0	0	1	-360	360;
14	21	0.0138843000000000	0.0474380000000000	0.00461000000000000	123	0	0	0	0	1	-360	360;
15	16	0.00560331000000000	0.0196116000000000	0.00186000000000000	123	0	0	0	0	1	-360	360;
16	24	0.0129422000000000	0.0452975000000000	0.00430000000000000	123	0	0	0	0	1	-360	360;
17	31	0.00644628000000000	0.0220248000000000	0.00216000000000000	123	0	0	0	0	1	-360	360;
21	28	0.0360000000000000	0.121800000000000	0.0119000000000000	123	0	0	0	0	1	-360	360;
21	31	0.0137124000000000	0.0459702000000000	0.00446000000000000	123	0	0	0	0	1	-360	360;
22	24	0.0121984000000000	0.0426942000000000	0.00403000000000000	123	0	0	0	0	1	-360	360;
24	25	0.0112066000000000	0.0379157000000000	0.00371000000000000	123	0	0	0	0	1	-360	360;
25	26	0.0100165000000000	0.0350579000000000	0.00332000000000000	123	0	0	0	0	1	-360	360;
27	30	0.0460083000000000	0.101702000000000	0.00961000000000000	90	0	0	0	0	1	-360	360;
30	31	0.0211240000000000	0.0739339000000000	0.00701000000000000	123	0	0	0	0	1	-360	360;
30	31	0.0211240000000000	0.0739339000000000	0.00701000000000000	123	0	0	0	0	1	-360	360;
1	2	0.00903800000000000	0.268098000000000	0	40	0	0	1.03030303000000	0	1	-360	360;
1	2	0.00903800000000000	0.268098000000000	0	40	48	48	1.03030303000000	0	0	-360	360;
7	30	0.00164444000000000	0.0699807000000000	0	150	0	0	0.991913043000000	0	1	-360	360;
7	30	0.00164889000000000	0.0699806000000000	0	150	0	0	0.991913043000000	0	1	-360	360;
10	11	0.000709110000000000	0.0415606000000000	0	300	0	0	0.956521739000000	0	1	-360	360;
10	11	0.000697560000000000	0.0425609000000000	0	300	0	0	0.956521739000000	0	1	-360	360;
12	13	0.000364560000000000	0.0317479000000000	0	400	0	0	0.947619048000000	0.460000000000000	1	-360	360;
12	14	0.000526330000000000	0.0407299000000000	0	300	0	0	0.978521739000000	0	1	-360	360;
12	14	0.000542330000000000	0.0407964000000000	0	300	0	0	0.978521739000000	0	1	-360	360;
18	19	0.0339725000000000	0.553959000000000	0	20	24	24	1.03030303000000	0	1	-360	360;
18	20	0.0339725000000000	0.568987000000000	0	20	24	24	1.03030303000000	0	1	-360	360;
22	23	0.0419100000000000	0.524328000000000	0	20	24	24	1.03030303000000	0	0	-360	360;
22	23	0.0256818000000000	0.531198000000000	0	22	26.4000000000000	26.4000000000000	1.03030303000000	0	1	-360	360;
];

%% bus names
mpc.bus_name = {
	'SUBST01     ';
	'SUBST02     ';
	'SUBST3      ';
	'SUBST4      ';
	'SUBST5      ';
	'SUBST7      ';
	'SUBST8      ';
	'SUBST9      ';
	'SUBST10     ';
	'SUBST11     ';
	'SUBST12     ';
	'SUBST13     ';
	'SUBST14     ';
	'SUBST15     ';
	'SUBST16     ';
	'SUBST17     ';
	'SUBST18     ';
	'SUBST19     ';
	'SUBST20     ';
	'SUBST21     ';
	'SUBST26     ';
	'SUBST29     ';
	'SUBST30     ';
	'SUBST34     ';
	'SUBST35     ';
	'SUBST36     ';
	'SUBST42     ';
	'SUBST55     ';
	'SUBST68     ';
	'SUBST72     ';
	'SUBST103    ';
};
%% generator cost data
%	1	startup	shutdown	n	x1	y1	...	xn	yn
%	2	startup	shutdown	n	c(n-1)	...	c0
mpc.gencost = [
	2	0	0	2	31	0;
	2	0	0	2	52	0;
	2	0	0	2	23		0;
	2	0	0	2	44		0;
    2	0	0	2	7	0;
    2	0	0	2	11	0;
    2	0	0	2	21	0;
    2	0	0	2	15	0;
    2	0	0	2	17	0;
    2	0	0	2	11	0;
    2	0	0	2	12	0;
    2	0	0	2	31	0;
	2	0	0	2	5	0;
	2	0	0	2	23		0;
];


results = runpf(mpc)