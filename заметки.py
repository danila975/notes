import wx
import sqlite3
# подключаем библиотеки
app = wx.App() # создаём экземпляр класса wx
conn = sqlite3.connect('orders.db') # создаём и подключаем базу данных
cur = conn.cursor() # создаём объект для взаимодействия с ней
cur.execute("""CREATE TABLE IF NOT EXISTS notes(
   note_id INT PRIMARY KEY,
   content TEXT);""")
conn.commit() # создаём таблицу
window = wx.Frame(None, title = 'заметки', size = (1920,1080)) # создаём начальное окно преложения
panel = wx.Panel(window, pos= (0,0), size =(1920,1080), name= 'заметки')
create = wx.Button(panel, label = 'создать новую', pos= (100,200), size = (30,60)) # создаём кнопку для создания новой заметки
def oncreate(event): # функция, выполняемая при нажатии на кнопку создать новую
    window = wx.Frame(None, title = 'пишите здесь', size = (1920,1080)) # окно для текстового редактора
    text = wx.TextCtrl(window, style = wx.TE_MULTILINE) # сам редактор
    menu = wx.Menu() # создаём миню
    saveItem = menu.Append(wx.ID_SAVE,"сохранить")
    exitItem = menu.Append(wx.ID_EXIT,"назад")
    bar = wx.MenuBar()
    bar.Append(menu,"File")
    window.SetMenuBar(bar) # показываем миню в редакторе
    def OnExit(e): # функция для обработки событий для пункта назад
        window.Close() # закрываем окно
    def Onsave(e): # функция для сохранить
        cur.execute('select note_id from notes order by note_id desc;') # запрашиваем последний по номеру ключ note_id
        e = cur.fetchone() # помещаем результат в e
        if e == None:
            e = 1
        else:
            e = e[0]
            e = int(e) +1 # создаём ключ больше, самого большого имеющегося в базе
        c = [] # создаём список для добавления в базу
        c.append(e) # добавляем в него ключ
        c.append(text.GetValue()) # добавляем то, что в редакторе
        cur.execute('INSERT INTO notes VALUES(?, ?);', c)
        conn.commit() # добавляем то, что записали в редакторе в базу
    window.Bind(wx.EVT_MENU, Onsave, saveItem) # обработчик событий для сохранить
    window.Bind(wx.EVT_MENU, OnExit, exitItem) # обработчик событий для назад
    window.Show(True)   # показываем на экране окно с редактором
    app.MainLoop() # запускаем цикл событий
create.Bind(wx.EVT_BUTTON, oncreate,) # обработчик событий для кнопки создать новую
change = wx.Button(panel, label = 'редактировать', pos = (200,200), size = (30,60)) # создаём кнопку для редактирования заметки
def onchange(e):
    window = wx.Frame(None, title = 'пишите здесь', size = (1920,1080)) # окно для редактирования
    text1 = wx.TextCtrl(window, style = wx.TE_MULTILINE) # сам редактор
    cur.execute('select content from notes order by note_id desc;') # запрашиваем последнюю заметку
    f = cur.fetchone() # помещаем результат в f
    if f == None:
        text1.SetValue('вы ещё не создавали заметок')
    else:
        cur.execute("DELETE FROM notes WHERE content = ?;", f)
        conn.commit()
        f = f[0] # вытаскиваем результат из картежа
        text1.SetValue(f)
    menu = wx.Menu() # создаём миню
    saveItem = menu.Append(wx.ID_SAVE,"сохранить")
    exitItem = menu.Append(wx.ID_EXIT,"назад")
    bar = wx.MenuBar()
    bar.Append(menu,"File")
    window.SetMenuBar(bar) # показываем миню в редакторе
    def OnExit(e): # функция для обработки событий для пункта назад
        window.Close() # закрываем окно
    def Onsave(e): # функция для сохранить
        cur.execute('select note_id from notes order by note_id desc;') # запрашиваем последний по номеру ключ note_id
        e = cur.fetchone() # помещаем результат в e
        if e == None:
            e = 1
        else:
            e = e[0]
            e = int(e) +1 # создаём ключ больше, самого большого имеющегося в базе
        c = [] # создаём список для добавления в базу
        c.append(e) # добавляем в него ключ
        c.append(text1.GetValue()) # добавляем то, что в редакторе
        cur.execute('INSERT INTO notes VALUES(?, ?);', c)
        conn.commit() # добавляем то, что записали в редакторе в базу
    window.Bind(wx.EVT_MENU, Onsave, saveItem) # обработчик событий для сохранить
    window.Bind(wx.EVT_MENU, OnExit, exitItem) # обработчик событий для назад
    window.Show(True)   # показываем окно редактирования
    app.MainLoop() # запускаем цикл событий здесь
change.Bind(wx.EVT_BUTTON, onchange,) # обработчик событий для кнопки редактировать
window.Show(True)   # показываем основное окно
app.MainLoop() # запускаем цикл событий здесь