#!/usr/bin/env python3
"""
Clear Prospects Keyword Audit - December 17, 2025
Process keyword and search term data for three-tier classification
"""

import json
import csv
import datetime
from pathlib import Path

# Keyword data (14-day period: Dec 3-16)
keywords_data = [
    {"keyword": "wheatybags", "match_type": "BROAD", "campaign": "CPL | WBS | Search | Brand Inclusion 18/6", "impressions": 1022, "clicks": 239, "cost_micros": 219616599, "conversions": 37.341367, "conversions_value": 560.093656171, "ctr": 0.23385518590998042},
    {"keyword": "face masks with photos on them", "match_type": "EXACT", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 986, "clicks": 150, "cost_micros": 155077766, "conversions": 27, "conversions_value": 255.024997793, "ctr": 0.15212981744421908},
    {"keyword": "wheat bag", "match_type": "EXACT", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 2689, "clicks": 201, "cost_micros": 125814965, "conversions": 14.896993, "conversions_value": 203.961192677, "ctr": 0.07474897731498699},
    {"keyword": "branded cushions", "match_type": "BROAD", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 404, "clicks": 36, "cost_micros": 98356228, "conversions": 0, "conversions_value": 0, "ctr": 0.0891089108910891},
    {"keyword": "photo face masks", "match_type": "BROAD", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 704, "clicks": 81, "cost_micros": 77121438, "conversions": 9, "conversions_value": 79.74, "ctr": 0.11505681818181818},
    {"keyword": "happy snap gifts", "match_type": "BROAD", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 220, "clicks": 61, "cost_micros": 75995638, "conversions": 12.825723, "conversions_value": 131.914238943, "ctr": 0.2772727272727273},
    {"keyword": "face pillow", "match_type": "BROAD", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 1006, "clicks": 85, "cost_micros": 64335598, "conversions": 9, "conversions_value": 73.45, "ctr": 0.08449304174950298},
    {"keyword": "personalised hot water bottles", "match_type": "EXACT", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 1086, "clicks": 64, "cost_micros": 63040212, "conversions": 3, "conversions_value": 25.259999723, "ctr": 0.058931860036832415},
    {"keyword": "happy snaps gifts", "match_type": "BROAD", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 57, "clicks": 15, "cost_micros": 51312354, "conversions": 4, "conversions_value": 36.02, "ctr": 0.2631578947368421},
    {"keyword": "happysnapgifts", "match_type": "BROAD", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 125, "clicks": 63, "cost_micros": 46910598, "conversions": 8.825723, "conversions_value": 128.024237914, "ctr": 0.504},
    {"keyword": "microwavable bean bag", "match_type": "BROAD", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 811, "clicks": 68, "cost_micros": 44721366, "conversions": 2, "conversions_value": 31.36, "ctr": 0.08384710234278668},
    {"keyword": "microwavable bean bags", "match_type": "PHRASE", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 609, "clicks": 66, "cost_micros": 41828627, "conversions": 7.192644, "conversions_value": 106.14209856, "ctr": 0.10837438423645321},
    {"keyword": "microwavable heating pad", "match_type": "EXACT", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 919, "clicks": 66, "cost_micros": 33456056, "conversions": 2, "conversions_value": 20.45, "ctr": 0.07181719260065289},
    {"keyword": "happy snap gifts discount code", "match_type": "BROAD", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 64, "clicks": 7, "cost_micros": 33279552, "conversions": 3, "conversions_value": 105.5, "ctr": 0.109375},
    {"keyword": "custom hot water bottle", "match_type": "EXACT", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 387, "clicks": 40, "cost_micros": 32748151, "conversions": 2, "conversions_value": 21.539999787, "ctr": 0.10335917312661498},
    {"keyword": "face pillows", "match_type": "EXACT", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 209, "clicks": 30, "cost_micros": 31976937, "conversions": 1, "conversions_value": 16.73, "ctr": 0.14354066985645933},
    {"keyword": "face pillows", "match_type": "BROAD", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 346, "clicks": 39, "cost_micros": 30782779, "conversions": 1, "conversions_value": 6.83, "ctr": 0.11271676300578035},
    {"keyword": "photo face masks next day delivery", "match_type": "EXACT", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 69, "clicks": 28, "cost_micros": 30683682, "conversions": 0, "conversions_value": 0, "ctr": 0.4057971014492754},
    {"keyword": "happysnapgifts", "match_type": "BROAD", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 38, "clicks": 6, "cost_micros": 26870000, "conversions": 1, "conversions_value": 8.39, "ctr": 0.15789473684210525},
    {"keyword": "wheat bags microwave", "match_type": "EXACT", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 333, "clicks": 42, "cost_micros": 26189612, "conversions": 3.085342, "conversions_value": 52.555870727, "ctr": 0.12612612612612611},
    {"keyword": "custom face pillow", "match_type": "EXACT", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 255, "clicks": 35, "cost_micros": 25440711, "conversions": 4, "conversions_value": 34.559999877, "ctr": 0.13725490196078433},
    {"keyword": "wheat heat pack", "match_type": "EXACT", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 288, "clicks": 33, "cost_micros": 24632556, "conversions": 0.085342, "conversions_value": 0.86451446, "ctr": 0.11458333333333333},
    {"keyword": "personalised face cushion", "match_type": "EXACT", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 131, "clicks": 24, "cost_micros": 24282650, "conversions": 2, "conversions_value": 20.7, "ctr": 0.183206106870229},
    {"keyword": "wheat heat bag", "match_type": "EXACT", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 349, "clicks": 41, "cost_micros": 24005790, "conversions": 5.08349, "conversions_value": 62.189096249, "ctr": 0.1174785100286533},
    {"keyword": "pillow of my face", "match_type": "EXACT", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 196, "clicks": 21, "cost_micros": 22728040, "conversions": 2, "conversions_value": 17.62, "ctr": 0.10714285714285714},
    {"keyword": "personalised hot water bottles", "match_type": "BROAD", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 306, "clicks": 14, "cost_micros": 21340662, "conversions": 1, "conversions_value": 10.15, "ctr": 0.0457516339869281},
    {"keyword": "microwave bean bag", "match_type": "EXACT", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 319, "clicks": 24, "cost_micros": 20843718, "conversions": 0.78937, "conversions_value": 8.97444146, "ctr": 0.07523510971786834},
    {"keyword": "bean bag warmers", "match_type": "EXACT", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 306, "clicks": 28, "cost_micros": 20564532, "conversions": 1, "conversions_value": 20.91, "ctr": 0.0915032679738562},
    {"keyword": "heat bags", "match_type": "PHRASE", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 633, "clicks": 38, "cost_micros": 20206360, "conversions": 2.543964, "conversions_value": 38.48223284, "ctr": 0.06003159557661927},
    {"keyword": "wheatbags uk", "match_type": "EXACT", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 106, "clicks": 25, "cost_micros": 20016057, "conversions": 3, "conversions_value": 39.67, "ctr": 0.2358490566037736},
]

# Search term data (60-day period: Oct 18 - Dec 16)
search_terms_data = [
    {"search_term": "wheatybags", "campaign": "CPL | WBS | Search | Brand Inclusion 18/6", "impressions": 2067, "clicks": 509, "cost_micros": 359344185, "conversions": 67.085366, "conversions_value": 882.269653103},
    {"search_term": "wheat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 7581, "clicks": 572, "cost_micros": 332253807, "conversions": 33.064527, "conversions_value": 401.302711127},
    {"search_term": "personalised face masks", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 1887, "clicks": 233, "cost_micros": 226939198, "conversions": 40.677923, "conversions_value": 396.224538321},
    {"search_term": "wheatybags uk", "campaign": "CPL | WBS | Search | Brand Inclusion 18/6", "impressions": 934, "clicks": 294, "cost_micros": 208106740, "conversions": 45.840591, "conversions_value": 669.445949207},
    {"search_term": "personalised hot water bottles", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 2601, "clicks": 175, "cost_micros": 162431279, "conversions": 13.50436, "conversions_value": 175.37896348},
    {"search_term": "personalised face masks", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 1450, "clicks": 150, "cost_micros": 135004019, "conversions": 21.018619, "conversions_value": 166.707687844},
    {"search_term": "happy snap gifts", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 447, "clicks": 176, "cost_micros": 106918325, "conversions": 34.013024, "conversions_value": 323.888498064},
    {"search_term": "branded cushions", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 81, "clicks": 12, "cost_micros": 72354379, "conversions": 1, "conversions_value": 630.29},
    {"search_term": "wheat bags uk", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 443, "clicks": 97, "cost_micros": 71086008, "conversions": 9.465188, "conversions_value": 157.399944752},
    {"search_term": "microwavable heating pad", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 1802, "clicks": 129, "cost_micros": 68358317, "conversions": 9.670364, "conversions_value": 108.89490856},
    {"search_term": "happysnapgifts", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 244, "clicks": 136, "cost_micros": 68298982, "conversions": 19.33478, "conversions_value": 241.173500452},
    {"search_term": "wheatbags uk", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 363, "clicks": 86, "cost_micros": 65104649, "conversions": 5, "conversions_value": 69.38},
    {"search_term": "happy snap gifts discount code", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 76, "clicks": 15, "cost_micros": 64516219, "conversions": 4.166667, "conversions_value": 132.246670942},
    {"search_term": "wheat bags for pain relief", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 1039, "clicks": 119, "cost_micros": 62169944, "conversions": 7.61036, "conversions_value": 84.483576178},
    {"search_term": "wheat bag microwave", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 1170, "clicks": 104, "cost_micros": 61871471, "conversions": 10.183197, "conversions_value": 99.712773109},
    {"search_term": "happy snap gifts reviews", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 76, "clicks": 4, "cost_micros": 61770973, "conversions": 1, "conversions_value": 8.81},
    {"search_term": "face pillow", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 704, "clicks": 71, "cost_micros": 56621550, "conversions": 8, "conversions_value": 57.81},
    {"search_term": "custom hot water bottle", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 630, "clicks": 70, "cost_micros": 55377028, "conversions": 7.821673, "conversions_value": 92.789486437},
    {"search_term": "wheat heat pack", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 827, "clicks": 85, "cost_micros": 49908838, "conversions": 1.760301, "conversions_value": 12.11714167},
    {"search_term": "happy snap gifts reviews", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 89, "clicks": 7, "cost_micros": 43971273, "conversions": 0, "conversions_value": 0},
    {"search_term": "personalised hot water bottle cover", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 683, "clicks": 51, "cost_micros": 42371696, "conversions": 2.450687, "conversions_value": 28.37330047},
    {"search_term": "wheatybags amazon", "campaign": "CPL | WBS | Search | Brand Inclusion 18/6", "impressions": 103, "clicks": 21, "cost_micros": 39246363, "conversions": 3.091599, "conversions_value": 26.97331792},
    {"search_term": "happysnapgifts reviews", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 44, "clicks": 4, "cost_micros": 38340000, "conversions": 0, "conversions_value": 0},
    {"search_term": "wheat bags microwave", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 430, "clicks": 53, "cost_micros": 35016145, "conversions": 3.585342, "conversions_value": 59.685870727},
    {"search_term": "printed cushions", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 44, "clicks": 7, "cost_micros": 34894553, "conversions": 0, "conversions_value": 0},
    {"search_term": "photo face masks next day delivery", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 141, "clicks": 32, "cost_micros": 33832372, "conversions": 1, "conversions_value": 9.12},
    {"search_term": "amazon wheatybags", "campaign": "CPL | WBS | Search | Brand Inclusion 18/6", "impressions": 24, "clicks": 4, "cost_micros": 31917728, "conversions": 0.722009, "conversions_value": 0.722009},
    {"search_term": "microwaveable wheat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 597, "clicks": 54, "cost_micros": 30781948, "conversions": 2, "conversions_value": 12.99},
    {"search_term": "wheatybags co uk", "campaign": "CPL | WBS | Search | Brand Inclusion 18/6", "impressions": 132, "clicks": 40, "cost_micros": 30539394, "conversions": 4, "conversions_value": 185.15},
    {"search_term": "lavender wheat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 646, "clicks": 53, "cost_micros": 29306266, "conversions": 3.5, "conversions_value": 31.2},
    {"search_term": "wheatybags discount code", "campaign": "CPL | WBS | Search | Brand Inclusion 18/6", "impressions": 9, "clicks": 2, "cost_micros": 28820000, "conversions": 0, "conversions_value": 0},
    {"search_term": "printed face masks", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 177, "clicks": 20, "cost_micros": 28105974, "conversions": 3, "conversions_value": 28.399999503},
    {"search_term": "personalised face pillow", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 278, "clicks": 31, "cost_micros": 27692164, "conversions": 2, "conversions_value": 9.81},
    {"search_term": "face cushion", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 392, "clicks": 33, "cost_micros": 27565028, "conversions": 8, "conversions_value": 91.839998844},
    {"search_term": "wheat heat bags", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 449, "clicks": 44, "cost_micros": 27454943, "conversions": 2, "conversions_value": 24.969999615},
    {"search_term": "microwave bean bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 577, "clicks": 40, "cost_micros": 27293809, "conversions": 0.456036, "conversions_value": 5.15776716},
    {"search_term": "wheat bag for neck", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 558, "clicks": 52, "cost_micros": 27268872, "conversions": 2.666666, "conversions_value": 39.08332658},
    {"search_term": "personalised masks with your face", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 163, "clicks": 29, "cost_micros": 26719334, "conversions": 6, "conversions_value": 112.65},
    {"search_term": "wheat bag company", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 316, "clicks": 47, "cost_micros": 25960295, "conversions": 0, "conversions_value": 0.0230243},
    {"search_term": "personalised photo face masks", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 84, "clicks": 22, "cost_micros": 25380267, "conversions": 5, "conversions_value": 45.099999393},
    {"search_term": "personalised face cushion", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 172, "clicks": 25, "cost_micros": 24537459, "conversions": 2, "conversions_value": 20.699999547},
    {"search_term": "microwave heat pack", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 941, "clicks": 51, "cost_micros": 24366939, "conversions": 0, "conversions_value": 0},
    {"search_term": "microwave heat pad", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 1323, "clicks": 54, "cost_micros": 24152556, "conversions": 2, "conversions_value": 19.16},
    {"search_term": "custom face pillow", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 268, "clicks": 35, "cost_micros": 24016782, "conversions": 1, "conversions_value": 8.81},
    {"search_term": "microwave hot water bottle", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 921, "clicks": 49, "cost_micros": 23396778, "conversions": 4, "conversions_value": 65.35},
    {"search_term": "cushions", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 179, "clicks": 10, "cost_micros": 23280000, "conversions": 0, "conversions_value": 0},
    {"search_term": "wheat bags for microwave", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 387, "clicks": 37, "cost_micros": 23192097, "conversions": 4, "conversions_value": 27.049999378},
    {"search_term": "custom hot water bottle cover", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 221, "clicks": 22, "cost_micros": 22368319, "conversions": 1, "conversions_value": 13.18},
    {"search_term": "personalised mask", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 174, "clicks": 25, "cost_micros": 22281342, "conversions": 3, "conversions_value": 11.63},
    {"search_term": "warmies", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 1357, "clicks": 48, "cost_micros": 22180164, "conversions": 2, "conversions_value": 32.679999399},
    {"search_term": "heated wheat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 408, "clicks": 43, "cost_micros": 21977187, "conversions": 1, "conversions_value": 12.19},
    {"search_term": "custom face masks", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 203, "clicks": 22, "cost_micros": 21343206, "conversions": 1, "conversions_value": 8.81},
    {"search_term": "face pillow custom", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 110, "clicks": 23, "cost_micros": 20265935, "conversions": 5, "conversions_value": 39.145794106},
    {"search_term": "bench cushions", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 96, "clicks": 5, "cost_micros": 20070000, "conversions": 0, "conversions_value": 0},
    {"search_term": "the wheat bag company", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 226, "clicks": 36, "cost_micros": 19998076, "conversions": 0, "conversions_value": 0},
    {"search_term": "pillow with face on it", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 172, "clicks": 18, "cost_micros": 19148791, "conversions": 3, "conversions_value": 28.07},
    {"search_term": "cherry stone pillow", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 198, "clicks": 32, "cost_micros": 18498643, "conversions": 3, "conversions_value": 32.749999412},
    {"search_term": "photo hot water bottle", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 210, "clicks": 23, "cost_micros": 18197078, "conversions": 2.972754, "conversions_value": 32.5621202},
    {"search_term": "heated neck wrap", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 930, "clicks": 35, "cost_micros": 18045741, "conversions": 1, "conversions_value": 8.41},
    {"search_term": "microwave heat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 480, "clicks": 30, "cost_micros": 18016587, "conversions": 1.00185, "conversions_value": 18.1285355},
    {"search_term": "happysnapgifts co uk", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 15, "clicks": 4, "cost_micros": 17990000, "conversions": 1, "conversions_value": 8.39},
    {"search_term": "cushion with face on", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 123, "clicks": 20, "cost_micros": 17972326, "conversions": 3, "conversions_value": 31.64},
    {"search_term": "heat bags for pain relief", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 293, "clicks": 25, "cost_micros": 17883102, "conversions": 1, "conversions_value": 20.34},
    {"search_term": "microwave neck warmer", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 374, "clicks": 35, "cost_micros": 17817770, "conversions": 0, "conversions_value": 0},
    {"search_term": "hot wheat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 207, "clicks": 22, "cost_micros": 17355298, "conversions": 2, "conversions_value": 20.65},
    {"search_term": "wheatybag", "campaign": "CPL | WBS | Search | Brand Inclusion 18/6", "impressions": 52, "clicks": 14, "cost_micros": 17322781, "conversions": 4, "conversions_value": 52.03758402},
    {"search_term": "bench seat cushions", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 44, "clicks": 4, "cost_micros": 17270000, "conversions": 1, "conversions_value": 10.97},
    {"search_term": "wheat hot water bottle", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 312, "clicks": 39, "cost_micros": 16955250, "conversions": 3, "conversions_value": 48.09},
    {"search_term": "heated bean bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 205, "clicks": 20, "cost_micros": 16089927, "conversions": 1, "conversions_value": 5.25},
    {"search_term": "microwave heating pad", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 535, "clicks": 33, "cost_micros": 15933641, "conversions": 4, "conversions_value": 40.70999935},
    {"search_term": "microwave wheat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 419, "clicks": 26, "cost_micros": 15615063, "conversions": 3, "conversions_value": 36},
    {"search_term": "printed face masks", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 171, "clicks": 18, "cost_micros": 15236289, "conversions": 1.5, "conversions_value": 14.915},
    {"search_term": "happy snaps gifts", "campaign": "CPL | HSG |  Search | Brand 120 28/5 140 8/9", "impressions": 29, "clicks": 19, "cost_micros": 15109109, "conversions": 3, "conversions_value": 27.66},
    {"search_term": "wheat neck warmer", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 202, "clicks": 24, "cost_micros": 15101020, "conversions": 3, "conversions_value": 52.9},
    {"search_term": "logo cushions", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 33, "clicks": 5, "cost_micros": 15000000, "conversions": 0, "conversions_value": 0},
    {"search_term": "wheat bag heat pack", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 403, "clicks": 25, "cost_micros": 14980756, "conversions": 2, "conversions_value": 18.95},
    {"search_term": "wheat bag hot water bottle", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 180, "clicks": 26, "cost_micros": 14857178, "conversions": 2, "conversions_value": 27.92},
    {"search_term": "printed 4 you", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 2, "clicks": 1, "cost_micros": 14800000, "conversions": 0, "conversions_value": 0},
    {"search_term": "personalised cushions", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 32, "clicks": 5, "cost_micros": 14690000, "conversions": 0, "conversions_value": 0},
    {"search_term": "heat pads", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 967, "clicks": 31, "cost_micros": 14628612, "conversions": 1, "conversions_value": 9.71},
    {"search_term": "face pillows", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 142, "clicks": 16, "cost_micros": 14078627, "conversions": 0, "conversions_value": 0},
    {"search_term": "wheat pack", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 443, "clicks": 26, "cost_micros": 13974421, "conversions": 0.222957, "conversions_value": 2.37895119},
    {"search_term": "wheat bag for neck and shoulders", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 179, "clicks": 24, "cost_micros": 13612918, "conversions": 0, "conversions_value": 0},
    {"search_term": "heat bags", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 272, "clicks": 22, "cost_micros": 13522241, "conversions": 2, "conversions_value": 29.8},
    {"search_term": "microwavable wheat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 325, "clicks": 23, "cost_micros": 13239779, "conversions": 2, "conversions_value": 31.72},
    {"search_term": "personalised masks with your face", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 86, "clicks": 9, "cost_micros": 12920000, "conversions": 2, "conversions_value": 27.93},
    {"search_term": "the wheatbag company", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 269, "clicks": 23, "cost_micros": 12642115, "conversions": 0, "conversions_value": 0},
    {"search_term": "heatable wheat bags", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 109, "clicks": 18, "cost_micros": 12479511, "conversions": 0, "conversions_value": 0},
    {"search_term": "microwavable heat pack", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 347, "clicks": 24, "cost_micros": 12095397, "conversions": 1, "conversions_value": 17.23},
    {"search_term": "wheat heat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 259, "clicks": 20, "cost_micros": 12077357, "conversions": 0, "conversions_value": 0},
    {"search_term": "custom made cushions", "campaign": "CPL | BMPM | Search | Promotional Merchandise", "impressions": 54, "clicks": 7, "cost_micros": 11979340, "conversions": 0, "conversions_value": 0},
    {"search_term": "photo hot water bottle cover", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 82, "clicks": 13, "cost_micros": 11494316, "conversions": 1, "conversions_value": 12.83},
    {"search_term": "face pillow", "campaign": "CPL | HSG | Search | Photo Face Cushion 130 18/6 120 24/6 Ai Max 14/10", "impressions": 140, "clicks": 16, "cost_micros": 11468658, "conversions": 2, "conversions_value": 17.09},
    {"search_term": "hot water bottle", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 44, "clicks": 3, "cost_micros": 11455852, "conversions": 0, "conversions_value": 0},
    {"search_term": "print masks of someone's face", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 21, "clicks": 7, "cost_micros": 11378518, "conversions": 2.5, "conversions_value": 22.47},
    {"search_term": "large wheat bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 223, "clicks": 27, "cost_micros": 11206281, "conversions": 0, "conversions_value": 0},
    {"search_term": "photo face masks uk", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 61, "clicks": 10, "cost_micros": 11070000, "conversions": 2, "conversions_value": 51.62},
    {"search_term": "face mask printing", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 47, "clicks": 9, "cost_micros": 10938465, "conversions": 0, "conversions_value": 0},
    {"search_term": "face on a pillow", "campaign": "CPL | HSG | Search | Products120 16/9", "impressions": 141, "clicks": 9, "cost_micros": 10783143, "conversions": 2, "conversions_value": 17.62},
    {"search_term": "face mask photo", "campaign": "CPL | HSG | Search | Photo Face Mask 130 20/6 AI 4/8 120 4/9 130 15/9", "impressions": 51, "clicks": 9, "cost_micros": 10715493, "conversions": 1, "conversions_value": 3.69},
    {"search_term": "microwavable bean bag", "campaign": "CPL | WBS | Search | Wheat Bags 120 28/5 Ai 7/8 110 10/11 120 9/12", "impressions": 98, "clicks": 15, "cost_micros": 10470370, "conversions": 0, "conversions_value": 0},
]

def classify_search_term(clicks, conversions, spend_gbp, conversions_value, period_days=60):
    """Classify search term into three-tier system"""
    daily_click_rate = clicks / period_days

    # Tier 1: High Confidence Negative Keywords
    if clicks >= 30 and conversions == 0 and spend_gbp >= 20:
        return {
            'tier': 1,
            'confidence': 'very_high',
            'daily_click_rate': daily_click_rate,
            'false_positive_risk': '<5%',
            'recommendation': 'Add as exact match negative keyword immediately',
            'action': 'immediate'
        }

    # Tier 2: Medium Confidence Negative Keywords
    elif 10 <= clicks < 30 and conversions == 0:
        next_review = datetime.date.today() + datetime.timedelta(days=7)
        return {
            'tier': 2,
            'confidence': 'moderate',
            'daily_click_rate': daily_click_rate,
            'false_positive_risk': '10-20%',
            'recommendation': f'Monitor closely - review on {next_review.strftime("%Y-%m-%d")}',
            'action': 'monitor',
            'next_review_date': next_review.strftime('%Y-%m-%d')
        }

    # Tier 3: Insufficient Data
    elif clicks < 10 and conversions == 0:
        return {
            'tier': 3,
            'confidence': 'low',
            'daily_click_rate': daily_click_rate,
            'false_positive_risk': 'N/A',
            'recommendation': 'No action - insufficient data',
            'action': 'none'
        }

    # Converting term
    elif conversions > 0:
        roas = (conversions_value / spend_gbp * 100) if spend_gbp > 0 else 0
        return {
            'tier': 'converting',
            'confidence': 'N/A',
            'daily_click_rate': daily_click_rate,
            'recommendation': 'Performing well - no action needed',
            'action': 'none',
            'roas': f'{roas:.0f}%'
        }

    return None

# Process search terms
tier1_terms = []
tier2_terms = []
tier3_terms = []
converting_terms = []

for term in search_terms_data:
    spend_gbp = term['cost_micros'] / 1000000
    classification = classify_search_term(
        clicks=term['clicks'],
        conversions=term['conversions'],
        spend_gbp=spend_gbp,
        conversions_value=term['conversions_value']
    )

    if classification:
        term_with_class = {
            'search_term': term['search_term'],
            'campaign': term['campaign'],
            'clicks': term['clicks'],
            'spend_gbp': f"£{spend_gbp:.2f}",
            'conversions': term['conversions'],
            'conversions_value': term['conversions_value'],
            **classification
        }

        if classification['tier'] == 1:
            tier1_terms.append(term_with_class)
        elif classification['tier'] == 2:
            tier2_terms.append(term_with_class)
        elif classification['tier'] == 3:
            tier3_terms.append(term_with_class)
        elif classification['tier'] == 'converting':
            converting_terms.append(term_with_class)

# Calculate totals
total_tier1_spend = sum(float(t['spend_gbp'].replace('£', '')) for t in tier1_terms)
total_tier2_spend = sum(float(t['spend_gbp'].replace('£', '')) for t in tier2_terms)

print(f"Processing complete:")
print(f"- Tier 1 (High Confidence): {len(tier1_terms)} terms, £{total_tier1_spend:.2f} waste")
print(f"- Tier 2 (Medium Confidence): {len(tier2_terms)} terms, £{total_tier2_spend:.2f} spend")
print(f"- Tier 3 (Insufficient Data): {len(tier3_terms)} terms")
print(f"- Converting: {len(converting_terms)} terms")

# Save tier data to JSON files for report generation
output_dir = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/clear-prospects/reports')
output_dir.mkdir(exist_ok=True)

with open(output_dir / 'tier1-terms-2025-12-17.json', 'w') as f:
    json.dump(tier1_terms, f, indent=2)

with open(output_dir / 'tier2-terms-2025-12-17.json', 'w') as f:
    json.dump(tier2_terms, f, indent=2)

with open(output_dir / 'converting-terms-2025-12-17.json', 'w') as f:
    json.dump(converting_terms, f, indent=2)

# Save CSV files
today = datetime.date.today().strftime('%Y-%m-%d')

# Tier 1 CSV
with open(output_dir / f'clear-prospects-tier1-{today}.csv', 'w', newline='') as f:
    if tier1_terms:
        writer = csv.DictWriter(f, fieldnames=['search_term', 'campaign', 'clicks', 'spend_gbp', 'conversions', 'daily_click_rate', 'recommendation'])
        writer.writeheader()
        for term in tier1_terms:
            writer.writerow({
                'search_term': term['search_term'],
                'campaign': term['campaign'],
                'clicks': term['clicks'],
                'spend_gbp': term['spend_gbp'],
                'conversions': term['conversions'],
                'daily_click_rate': f"{term['daily_click_rate']:.2f}",
                'recommendation': term['recommendation']
            })

# Tier 2 CSV
with open(output_dir / f'clear-prospects-tier2-{today}.csv', 'w', newline='') as f:
    if tier2_terms:
        writer = csv.DictWriter(f, fieldnames=['search_term', 'campaign', 'clicks', 'spend_gbp', 'conversions', 'daily_click_rate', 'next_review_date'])
        writer.writeheader()
        for term in tier2_terms:
            writer.writerow({
                'search_term': term['search_term'],
                'campaign': term['campaign'],
                'clicks': term['clicks'],
                'spend_gbp': term['spend_gbp'],
                'conversions': term['conversions'],
                'daily_click_rate': f"{term['daily_click_rate']:.2f}",
                'next_review_date': term.get('next_review_date', '')
            })

print(f"\nCSV files generated:")
print(f"- {output_dir}/clear-prospects-tier1-{today}.csv")
print(f"- {output_dir}/clear-prospects-tier2-{today}.csv")
