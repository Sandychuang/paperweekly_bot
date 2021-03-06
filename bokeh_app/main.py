from __future__ import unicode_literals
from os.path import dirname, join
import pandas as pd
import sqlite3
import sys
#from pprint import pprint

from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, Button, DataTable, TableColumn, NumberFormatter,TextInput
from bokeh.io import curdoc

#https://pythonspot.com/sqlite-database-with-pandas/
conn = sqlite3.connect(join(dirname(__file__), '../group_chat_message.db'))
query = "SELECT * FROM message ORDER BY createdAt" #排序 时间
df = pd.read_sql_query(query,conn)
#print(df[:10]) #ok
#sys.exit(0)

source = ColumnDataSource(data=dict())

def update():
    current = df[df.content.str.contains(search_text.value.strip())==True] #df[""]
    source.data = {
        'group_name' :current.group_name,
        'group_user_name': current.group_user_name,
        'content' : current.content,
        'user_img' : current.user_img,
        'createdAt' : current.createdAt,
    }

search_text = TextInput(title="search")
#search_text_val = search_text.value.strip()
#slider = Slider(title="开始时间", start=10000, end=250000, value=150000, step=1000)
#slider.on_change('value', lambda attr, old, new: update())
search_text.on_change('value', lambda attr, old, new: update())



'''
button = Button(label=u"搜索", button_type="success")
button.callback = CustomJS(args=dict(source=source),
                           code=open(join(dirname(__file__), "download.js")).read())

'''


columns = [
    TableColumn(field="group_name", title="Group Name"),
    TableColumn(field="group_user_name", title="Group User Name"),
    TableColumn(field="content", title="Content"),
    TableColumn(field="user_img", title="User Img"),
    TableColumn(field="createdAt", title="createdAt"),
    #TableColumn(field="salary", title="Income", formatter=NumberFormatter(format="$0,0.00")),
]

data_table = DataTable(source=source, columns=columns, width=800)

controls = widgetbox(search_text) #, button)
table = widgetbox(data_table)

curdoc().add_root(row(controls, table))
curdoc().title = "Explore message"

update()
