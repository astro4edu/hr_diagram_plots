from astropy.table import Table,vstack, unique
import matplotlib as mpl
import numpy as np
import pandas as pd
import json
from pathlib import Path
from glob import glob
from slugify import slugify
import argparse
import arabic_reshaper
from bidi.algorithm import get_display

def split_text_in_middle(tmp_str):
    midpoint=len(tmp_str)/2
    word_list=tmp_str.split(' ')
    length_vec=[len(x) for x in word_list]
    split_point_diff=[np.abs(sum(length_vec[0:x])-midpoint) for x in range(0,len(length_vec))]
    split_point=split_point_diff.index(min(split_point_diff))
    for index,word in enumerate(word_list):
        if index==0:
           output_str=word
        elif index!=split_point:
            output_str=output_str+' '+word
        else:
            output_str=output_str+'\n'+word
    return output_str

def split_text_at_character(tmp_str,split_char=' ',reverse=False):
    if reverse:
        split_pos=tmp_str.find(split_char)
    else:
        split_pos=tmp_str.rfind(split_char)
    if split_pos<0:
        return tmp_str
    else:
        if tmp_str[split_pos-1]==' ':
            return tmp_str[0:split_pos-1]+'\n'+tmp_str[split_pos:]
        elif split_char==' ':
            return tmp_str[0:split_pos]+'\n'+tmp_str[split_pos+1:]
        else:    
            return tmp_str[0:split_pos]+'\n'+tmp_str[split_pos:]

def rgb_from_spt_teff(teff,data_table):
    tmp_ind=np.argmin(abs(data_table['T_eff']-teff))
    rgb=[data_table['R'][tmp_ind],data_table['G'][tmp_ind],data_table['B'][tmp_ind]]
    return rgb
def rgb_from_bb_teff(teff,data_table):
    tmp_ind=np.argmin(abs(data_table['T_eff']-teff))
    rgb=[data_table['R'][tmp_ind],data_table['G'][tmp_ind],data_table['B'][tmp_ind]]
    return rgb
def rgb_from_teff_logg(teff,logg,data_table,teff_values,logg_values):
    tmp_ind1=np.argmin(abs(teff_values-teff))
    tmp_ind2=np.argmin(abs(logg_values-logg))
    mask = (data_table['T_eff']==teff_values[tmp_ind1]) & (data_table['logg']==logg_values[tmp_ind2])
    
    tmp_table=data_table[mask]
    if len(tmp_table)>0:
        
        rgb=[tmp_table['R'][0],tmp_table['G'][0],tmp_table['B'][0]]
    else:
        rgb=[1,1,1]
    return rgb

def font_loader(possible_fonts):
    usable_fonts=[]
    #find any fonts in the font folder of package and load them
    packaged_fonts_path = Path(__file__).parent / 'fonts/*ttf'
    packaged_font_files=glob(str(packaged_fonts_path))
    for font_file in packaged_font_files:
        font_manager.fontManager.addfont(font_file)
    loaded_font_list=[f.name for f in font_manager.fontManager.ttflist]
    #loop over fonts for the required script and add any that are available to the list of fonts to pass to matplotlib
    for font in possible_fonts:
        if font in loaded_font_list:
            usable_fonts.append(font)
    if "Noto Sans" in loaded_font_list:
        usable_fonts.append("Noto Sans") #add Noto Sans font as backup
    if "Arial Unicode" in loaded_font_list:
        usable_fonts.append("Arial Unicode") #add Arial Unicode font as backup
    if "DejaVu Sans" in loaded_font_list:
        usable_fonts.append("DejaVu Sans") #add default matplotlib font as backupNotoSans
    plt.rcParams['font.family']=usable_fonts #pass fonts to matplotlib


#Begin argument parsing
parser = argparse.ArgumentParser(description='Make spectrum plots of stars')

parser.add_argument('--lang', help='add language code')
parser.add_argument('--text-direction', help='add the text direction, ltr=left to right or rtl=right to left, default is ltr')
parser.add_argument('--plot_dir', help='add directory for output plots. Default is plots directory in this package.')
parser.add_argument('--translations_file', help='add the JSON file containing translations. Default is translations.json in this package.')
parser.add_argument('--output_format', help='add the output format for the plots. options: eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff. Default is png.',default='png')
parser.add_argument('--translate_filenames', help='If True output filenames will be in requested language. If False output filenames will be in English. Default is False',default=False)
parser.add_argument('--unicode_font', help='add a font that covers the full unicode multilingual plane (only needed for mplcairo)')

args = parser.parse_args()

if not args.translations_file:
    translations_path = Path(__file__).parent / "./translations/translations.json"
else:
    translations_path = Path(args.translations_file)
translations_file = open(translations_path)
translations_dicts = json.load(translations_file)
translations_file.close()

if not args.lang:
    need_language=True
else:
    if args.lang in translations_dicts.keys():
        language_code=args.lang
        need_language=False
    else:
        need_language=True
prompt_string="Available languages:"
for i0,key_tmp in enumerate(translations_dicts.keys()):
    if i0>0:
        prompt_string=prompt_string+', '
    prompt_string=prompt_string+key_tmp
prompt_string=prompt_string+'\nPlease enter a language code:'
while need_language:
    language_code=input(prompt_string)
    if language_code in  translations_dicts.keys():
        need_language=False

if not args.plot_dir:
    outfile_base = Path(__file__).parent / "./plots/"
else:
    outfile_base = Path(args.plot_dir)

#end argument parsing
#load translation file
text_list=translations_dicts[language_code]
possible_fonts=text_list['possible_fonts']

#important that arabic reshaper comes before bidi get_display
if language_code.startswith('ar'):
    text_list = {key:(arabic_reshaper.reshape(value) if type(value)==str else value) for key, value in text_list.items()}


text_list = {key:(get_display(value) if type(value)==str else value) for key, value in text_list.items()}

#check is cairo is required and load matplotlib
if text_list["matplotlib_cairo"]:
    import mplcairo
import matplotlib as mpl
if text_list["matplotlib_cairo"]:
    mpl.use("module://mplcairo.qt")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib import font_manager
from matplotlib import cm
from matplotlib.lines import Line2D
from matplotlib.patches import CirclePolygon,Circle
from matplotlib.collections import PolyCollection,RegularPolyCollection

text_list_en=translations_dicts['en']



#load in input data from the various input files
pickles_data = Table.read(Path(__file__).parent / "./data/pickles1998.vot")
filtered_data1=pickles_data['teff_gspphot','luminosity','radius_gspphot','logg_gspphot']
filtered_data1['teff_gspphot'].name = 'teff'
filtered_data1['radius_gspphot'].name = 'radius'
filtered_data1['logg_gspphot'].name = 'logg'
bright_nearby_data = Table.read(Path(__file__).parent / "./data/bright_nearby_stars_sample.vot")
filtered_data2=bright_nearby_data['teff_gspphot','luminosity','radius_gspphot','logg_gspphot']
filtered_data2['teff_gspphot'].name = 'teff'
filtered_data2['radius_gspphot'].name = 'radius'
filtered_data2['logg_gspphot'].name = 'logg'

nearby_data = Table.read(Path(__file__).parent / "./data/nearby_stars_sample.vot")
filtered_data3=nearby_data['teff_gspphot','luminosity','radius_gspphot','logg_gspphot']
filtered_data3['teff_gspphot'].name = 'teff'
filtered_data3['radius_gspphot'].name = 'radius'
filtered_data3['logg_gspphot'].name = 'logg'

wd_data = Table.read(Path(__file__).parent / "./data/vincent2024_nearby_white_dwarfs.vot")
wd_data['radius']=10.0**wd_data['logR']
wd_data['luminosity']=10.0**wd_data['logL']
filtered_data4=wd_data['teff','luminosity','radius','logg']
filtered_data=vstack([filtered_data1,filtered_data2,filtered_data3,filtered_data4],metadata_conflicts='silent')

#load named star data
named_stars_data=Table.read(Path(__file__).parent / "./data/named_stars.vot")

#read in colour data from Harre & Heller tables
harre_heller_2021_t1_data = Table.read(Path(__file__).parent / "./data/harre_heller_2021_t1.csv")
harre_heller_2021_t2_data = Table.read(Path(__file__).parent / "./data/harre_heller_2021_t2.csv")
harre_heller_2021_t5_data = Table.read(Path(__file__).parent / "./data/harre_heller_2021_t5.csv")
teff_values=sorted(list(set(harre_heller_2021_t2_data['T_eff'])))
logg_values=sorted(list(set(harre_heller_2021_t2_data['logg'])))
colours_tmp=[]

#loop over nearby star data + white dwarfs and add RGB colours to each star
for row in filtered_data:
    if row['logg']>5.5 or not row['logg']:
        #if it's a white dwarf use blackbody relation
        colour_tmp=rgb_from_bb_teff(row['teff'],harre_heller_2021_t1_data)
    elif row['teff']>10000:
        #if its a hot star use just Teff to colour
        colour_tmp=rgb_from_spt_teff(row['teff'],harre_heller_2021_t5_data)
    else:
        colour_tmp=rgb_from_teff_logg(row['teff'],row['logg'],harre_heller_2021_t2_data,teff_values,logg_values)
    colours_tmp.append([colour_tmp])
filtered_data.add_column(colours_tmp, name='colour')

plt.figure()
plt.axis([50000,2000,0.00001,1000000.0])
plt.scatter(filtered_data['teff'],filtered_data['luminosity'],s=10.0*np.sqrt(filtered_data['radius']),marker='o',c=filtered_data['colour'],edgecolor='k',linewidths=0.1)

#loop over named star data and add RGB colours to each star or white dwarf
for  row in named_stars_data:
    if row['literature_logg']>5.5:
        #if it's a white dwarf use blackbody relation
        colour_tmp=rgb_from_bb_teff(row['literature_effective_temperature'],harre_heller_2021_t1_data)
    elif row['literature_effective_temperature']>10000 or not row['literature_logg']:
        #if its a hot star or has no gravity estimate use just Teff to colour
        colour_tmp=rgb_from_spt_teff(row['literature_effective_temperature'],harre_heller_2021_t5_data)
    else:
        colour_tmp=rgb_from_teff_logg(row['literature_effective_temperature'],row['literature_logg'],harre_heller_2021_t2_data,teff_values,logg_values)
    scatter_tmp=plt.scatter(row['literature_effective_temperature'],row['literature_luminosity'],s=10.0*np.sqrt(row['radius_used']),marker='o',c=[colour_tmp],edgecolor='k',linewidths=0.1)
    if row['text_offset_x']>1.0:
        ha_tmp='right'
    else:
        ha_tmp='left'
    """
    if row['text_offset_y']>1.0:
        va_tmp='bottom'
    else:
        va_tmp='top'
    """
    text_tmp=text_list[slugify(row['english_name']+'-name')]
    if len(text_tmp)>12:
        index_tmp=row['english_name'].rfind(' ')
        text_tmp=text_tmp[:index_tmp]+'\n'+text_tmp[index_tmp+1:]
    plt.text(row['text_offset_x']*row['literature_effective_temperature'],row['literature_luminosity'],text_tmp,ha=ha_tmp,va='center',fontsize=6)
    
plt.xlabel(text_list['xaxis_text'])
plt.ylabel(text_list['yaxis_text'])
plt.xscale('log')
plt.yscale('log')
plt.title(text_list['title_text'])
plt.xticks([50000.0,30000.0,10000.0,5000.0,3000.0,2000.0],[50000,30000,10000,5000,3000,2000])

#add the labels for luminosity classes
plt.text(10000.0,0.0003,text_list['wd_text'],rotation=-20,ha='center',va='center')
plt.text(7000.0,0.8,text_list['ms_text'],rotation=-35,ha='center',va='center')
plt.text(5000.0,3,text_list['sbg_text'],rotation=-35,ha='center',va='center')
plt.text(5300.0,80,text_list['g_text'],rotation=-15,ha='right',va='center')
plt.text(5300.0,5500,split_text_in_middle(text_list['bg_text']),rotation=0,ha='left',va='center')
plt.text(6000.0,100000,text_list['spg_text'],rotation=0,ha='center',va='center')
plt.text(2010.0,0.000035,split_text_in_middle(text_list['bd_text']),rotation=0,ha='right',va='center')
handles=[]
legends=[]
for i0 in range(0,6):
    radius_tmp=pow(10.0,3-i0)
    handles.append(Line2D([], [], color='white', marker='o',markersize=np.sqrt(10.0*np.sqrt(radius_tmp)), markerfacecolor=None,markeredgecolor='k',markeredgewidth=0.1))
    if radius_tmp>1:
        legends.append(str(int(radius_tmp)))
    else:
        legends.append(str(radius_tmp))
#add the legend
if '(' in text_list['rad_text']:
    rad_legend=split_text_at_character(text_list['rad_text'],split_char='(')
else:
    rad_legend=split_text_in_middle(text_list['rad_text'])
leg=plt.legend(handles,legends,loc="lower left", title=rad_legend,fontsize=6,title_fontsize=8,labelspacing=1.5)
plt.setp(leg.get_title(), multialignment='center')
filename_tmp=text_list['filename']
print('Saving to: '+str(outfile_base.joinpath(filename_tmp+'.'+str.lower(args.output_format))))
plt.savefig(str(outfile_base.joinpath(filename_tmp+'.'+str.lower(args.output_format))))
