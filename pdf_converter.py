# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 02:58:38 2020

@author: Owner
"""
from __future__ import division
import pandas as pd
import numpy as np
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
# TO PLOT
import plotly
import bubbly
from plotly.offline import init_notebook_mode, iplot,plot
# init_notebook_mode()
from bubbly.bubbly import bubbleplot


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    #codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

#%%
#Read pdf
text = convert_pdf_to_txt(path='CONS_1993.pdf')
#%%
# Limpieza 
text = text.lower()
text = text.replace(',','').replace('.', '')
text_split = text.split()

df_text = pd.DataFrame({'word':text_split})
acum_text = df_text.groupby(['word'])['word'].agg('count')
acum_text = acum_text.to_frame()
acum_text.rename(columns={'word':'count'},inplace=True)
acum_text.sort_values('count',ascending=False,inplace=True)
acum_text.reset_index(inplace=True)
#%%
#Remove StopWords


#%%
#filter the dataframe according to u_input

traces = plotly.graph_objs.Scatter(x=acum_text[:10]['word'],
                                    y=acum_text[:10]['count'],
                                    mode='lines') 

layout = plotly.graph_objs.Layout(xaxis=dict(tickvals=acum_text[:10]['word'].unique()))
fig = plotly.graph_objs.Figure(data=traces, layout=layout)

plotly.offline.plot(fig)

#%%


figure = bubbleplot(dataset=acum_text, x_column='count', y_column='count',bubble_column='count', size_column='count', color_column='word', 
    x_title="Palabras", y_title="Repeticiones", title='Palabras en la constitucion',
    x_logscale=True, scale_bubble=3, height=650)

plot(figure, filename="holi.html")
